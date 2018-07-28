#!/usr/bin/env python3

import os
import re
import json
import PyPDF2
import logging
import pytesseract

from glob import glob
from PIL import Image, ImageChops
from dateutil.parser import parse as parse_date

def main():
    logging.basicConfig(
        filename='extract.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    for pdf in glob('data/*/*.pdf'):
        extract_images(pdf)

    for png in glob('data/*/*.png'):
        extract_ocr(png)

    write_site()

def extract_images(pdf):
    pdf_reader = PyPDF2.PdfFileReader(open(pdf, 'rb'))
    num_pages = pdf_reader.getNumPages()
    for page_num in range(0, num_pages):
        logging.info('extracting page %s from %s', page_num + 1, pdf)
        page = pdf_reader.getPage(page_num)
        try:
            objects = page['/Resources']['/XObject'].getObject()
            count = 0
            types = []
            for obj in objects:
                o = objects[obj]
                if o['/Subtype'] == '/Image':
                    count += 1
                    size = (o['/Width'], o['/Height'])
                    data = o.getData()
                    img_path = pdf.replace('.pdf', '-%02i.png' % page_num)
                    if os.path.isfile(img_path):
                        logging.info('%s already exists, skipping', img_path)
                    else:
                        img = Image.frombytes('RGB', size, data)
                        img.save(img_path)
                        logging.info('wrote %s', img_path)

        except Exception as e:
            logging.error('unable to extract images from %s: %s', pdf, e)

def extract_ocr(img_file):
    ocr_file = img_file.replace('.png', '.txt')
    if os.path.isfile(ocr_file):
        logging.info('ocr file %s already exists, skipping', ocr_file)
    else:
        try:
            img = Image.open(img_file)
            txt = pytesseract.image_to_string(img)
            with open(ocr_file, 'w') as fh:
                fh.write(txt)
            logging.info('wrote ocr to %s', ocr_file)
        except Exception as e:
            logging.error('unable to ocr %s: %s', img_file, e)

def extract_metadata(ocr_file):
    txt = open(ocr_file).read()

    # if 02.txt exists then the text from 00.txt ran over into 01.txt
    file3 = re.sub('00.txt$', '02.txt', ocr_file)
    if ocr_file != file3 and os.path.isfile(file3):
        txt += open(re.sub('00.txt$', '01.txt', ocr_file)).read()

    m = {
        'id': match_int('Ad ID (\d+)', txt),
        'file': ocr_file.replace('-00.txt', '.pdf'),
        'text': match('(?s)Ad Text (.+)Ad Landing Page', txt, strip=False),
        'url': match('Ad Landing Page (.+)', txt),
        'impressions': match_int('Ad Impressions (.+)', txt),
        'clicks': match_int('Ad Clicks (.+)', txt),
        'spend': {
            'amount': '{0:.2f}'.format(match_float('Ad Spend ([0-9,\.]+)', txt)),
            'currency': match('Ad Spend [0-9,\.]+ (.+)', txt)
        },
        'created': match_datetime('Ad Creation Date (.+)', txt),
        'ended': match_datetime('Ad End Date (.+)', txt),
        'targeting': targeting(txt)
    }

    return m

def match(pattern, string, strip=True):
    m = re.search(pattern, string, re.MULTILINE)
    if not m:
        return None
    s = m.group(1)
    if strip:
        s = s.replace('\n', ' ')
        s = re.sub(' +', ' ', s)
        s = s.strip()
    return s

def match_int(pattern, string):
    s = match(pattern, string)
    if s:
        return int(s.replace(',', ''))
    else:
        return 0

def match_float(pattern, string):
    s = match(pattern, string)
    f = 0.0
    if s:
        f = float(s.replace(',', ''))
    return f

def match_datetime(pattern, string):
    s = match(pattern, string)
    if s:
        # clean up some known ocr edge cases
        if s == '02/03/17 01 32:43 AM PST':
            s = '02/03/17 01:32:43 AM PST'
        if s == '05/17/1612121113 AM PDT':
            s = '05/17/16 12:21:13 AM PDT'
        s = re.sub(' :', ':', s)
        s = re.sub('O', '0', s)
        s = s.replace('z', ':')
        m = re.match('^(\d\d/\d\d/\d\d)(\d.+)$', s)
        if m:
            s = m.group(1) + ' ' + m.group(2)
        try:
            dt = parse_date(s, fuzzy=True, tzinfos={
                'PDT': -25200,
                'PST': -28800
            })
            return dt.isoformat()
        except Exception as e:
            logging.error('unable to convert time %s: %s', s, e)
            return None

def targeting(s):
    # this is gnarly but a state machine appears to be required to match
    # the structure in the Ad Targeting section
    t = match('(?s)Ad Targeting (.+)Ad Impressions', s, strip=False)
    meta = {}
    key = None
    if not t:
        return meta
    for line in t.split('\n'):
        m = re.match('^([A-Z].{1,20}?):(.+)', line)
        if m:
            key = m.group(1)
            line = m.group(2)
        if key:
            meta[key] = meta.get(key, '') + ' ' + line

    # lower case the keys and unpack the values if there are comma or 
    # semicolon delimited lists
    new_meta = {}
    for k, v in meta.items():
        k = k.lower()
        k = re.sub('[^a-z ]', '', k)
        k = re.sub(' +', '_', k)
        sep = ';' if  k == 'location' else ','
        new_meta[k] = unpack(v, sep)

    return new_meta

def unpack(s, sep=','):
    if not s:
        return []
    s = re.sub(' +', ' ', s).strip()

    prefix = ''
    m = re.match('^([A-Z].{1,20}?):(.+)', s)
    if m:
        prefix = m.group(1).lower().replace(' ', '_')
        s = m.group(2)

    parts = s.split(sep)

    if ' or ' in parts[-1]:
        parts.extend(parts.pop().split(' or '))

    parts = [p.strip() for p in parts]
    if prefix:
        data = {}
        data[prefix] = parts
    else:
        data = parts

    return data

def write_site():
    items = []
    for ocr in glob('data/*/*-00.txt'):
        m = extract_metadata(ocr)
        if m['id']:
            post_file = pick_post_image(m['file'])
            img_file = 'images/{:04d}.png'.format(m['id'])
            crop(post_file, 'site/' + img_file)
            m['image'] = img_file
            items.append(m)

    with open('site/index.json', 'w') as fh:
        json.dump(items, fh, indent=2)

def crop(path, new_path):
    im = Image.open(path)
    w, h = im.size

    # remove the bottom portion of he image that contains some text
    # that seems to confuse cropping
    im = im.crop((0, 0, w, h - 100))

    # get the bounding box of the central region of he image
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()

    # crop the image and save it
    if bbox:
        # add a margin
        m = 50 
        bbox = (bbox[0] - m, bbox[1] - m, bbox[2] + m, bbox[3] + m)

        # crop
        new_img = im.crop(bbox)

        # resize
        new_h = 400
        new_w = int(new_h * ((bbox[2] - bbox[0]) / (bbox[3] - bbox[1])))
        new_img = new_img.resize((new_w, new_h), Image.ANTIALIAS)

        # save
        new_img.save(new_path)

def pick_post_image(pdf_file):
    stem = pdf_file.replace('.pdf', '*.png')
    files = glob(stem)
    files.sort()
    return files[-1]

if __name__ == "__main__":
    main()
