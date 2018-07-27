#!/usr/bin/env python3

import os
import re
import PyPDF2
import logging
import pytesseract

from glob import glob
from PIL import Image
from dateutil.tz import gettz
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
    targeting = match('(?s)Ad Targeting (.+Ad Impressions)', txt, strip=False)
    m = {
        'id': match_int('Ad ID (\d+)', txt),
        'text': match('(?s)Ad Text (.+)Ad Landing Page', txt, strip=False),
        'url': match('Ad Landing Page (.+)', txt),
        'impressions': match_int('Ad Impressions (.+)', txt),
        'clicks': match_int('Ad Clicks (.+)', txt),
        'spend': {
            'amount': match('Ad Spend ([0-9\.]+)', txt),
            'currency': match('Ad Spend [0-9\.]+ (.+)', txt)
        },
        'created': match_datetime('Ad Creation Date (.+)', txt),
        'ended': match_datetime('Ad End Date (.+)', txt),
        'targeting': {
            'age': match('^Age: (.+)', targeting),
            'languages': unpack(match('Language: (.+)', targeting)),
            'placements': unpack(match('(?s)Placements: (.+)^People', targeting)),
            'living_in': match('(?s)^Location - Living In: (.+)Age:', targeting),
            'locations': unpack(match('(?s)^Location: (.+)Age:', targeting), sep=';'),
            'match': unpack(match('(?s)People Who Match: (.+)((And Must Also Match:)|(Ad Impressions))', targeting))
        }
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

def match_datetime(pattern, string):
    s = match(pattern, string)
    if s:
        dt = parse_date(s, tzinfos={
            'PDT': -25200,
            'PST': -28800
        })
        return dt.isoformat()

def commas(s):
    if not s:
        return []
    parts = [p.strip() for p in s.split(',')]
    if ' or ' in parts[-1]:
        p = parts.pop().split(' or ')
        parts.extend(p)
    return parts

def unpack(s, sep=','):
    if not s:
        return []
    prefix = ''
    if ':' in s:
        prefix, s = s.split(':', 1)
        prefix = prefix + ': '
    parts = s.split(sep)
    if ' or ' in parts[-1]:
        parts.extend(parts.pop().split(' or '))
    return [prefix + p.strip() for p in parts]

if __name__ == "__main__":
    main()
