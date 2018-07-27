# irads

*irads* parses the metadata and images out of the 3,517 Facebook ads that were
reported to have been bought by the [Internet Research Agency]. These ads were
released by the House Intelligence Committee as a set of redacted PDF files.

### The data:

https://democrats-intelligence.house.gov/social-media-content/social-media-advertisements.htm

### The context:

https://democrats-intelligence.house.gov/social-media-content/

### The metadata:

The results of running the metadata extraction are available as:

* [ads.json](https://raw.githubusercontent.com/edsu/irads/master/ads.json)

If you would like to run the extraction yourself continue reading.

## Install Tesseract

You will need to install the [Tesseract] OCR engine, which should be as easy as:

    brew install tesseract

For Linux, Windows, and more please check out the [install instructions].

## Get the Data

    % git clone https://github.com/edsu/irads.git
    % cd irads/data
    % wget -i urls.txt
    % for f in `ls *.zip`; do unzip $f; done

## Extract the Images and OCR

The PDFs contain multiple pages each with an embedded image. The first page is
typically a page of metadata, and the second is a screencap of a Facebook post
of some kind. `extract.py` walks across all the PDFs, extracts images, and also
text for each and writes them out right next to the PDF files.

    % cd .. 
    % pip install -r requirements.txt
    % ./extract.py

This can take a while, so examine `extract.log` to see what's going on.

[Internet Research Agency]: https://en.wikipedia.org/wiki/Internet_Research_Agency
[install instructions]: https://github.com/tesseract-ocr/tesseract/wiki
[Tesseract]: https://github.com/tesseract-ocr/tesseract
