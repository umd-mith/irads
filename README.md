This is a scratch space for trying to parse the metadata and images out of the
3,517 Facebook ads that were reported to have been bought by the [Internet
Research Agency] and released by Facebook.

The data:

https://democrats-intelligence.house.gov/social-media-content/social-media-advertisements.htm

The context:

https://democrats-intelligence.house.gov/social-media-content/

## Get started

    % git clone https://github.com/edsu/irads.git
    % wget -i urls.txt
    % for f in `ls *.zip`; do unzip $f; done


[Internet Research Agency]: https://en.wikipedia.org/wiki/Internet_Research_Agency
