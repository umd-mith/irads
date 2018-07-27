#!/usr/bin/env python3

import os
import PyPDF2
import logging
import pytesseract

from glob import glob
from PIL import Image

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

if __name__ == "__main__":
    main()
