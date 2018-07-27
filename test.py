import pytest

from extract import extract_metadata

def test_metadata1():
    m = extract_metadata('test-data/ocr1.txt')
    assert m['id'] == 2727
    assert m['text'] == 'Real Mexican-American pride. Respect!\nFYI: The three largest Hispanic groups in the United States are the Mexican-\nAmericans, Puerto Ricans and Cubans.\n\n'
    assert m['url'] == 'https://www.facebook.com/brownunitedfront/'
    assert m['impressions'] == 82748
    assert m['clicks'] == 11051
    assert m['spend'] == {'amount': '440.00', 'denomination': 'RUB'}
    assert m['created'] == '2017-02-16T00:42:01-08:00'
    assert m['ended'] == '2017-02-18T00:42:01-08:00'

def test_age():
    m = extract_metadata('test-data/ocr2.txt')
    assert m['targeting']['age'] == '18 - 65+'

def test_placements():
    m = extract_metadata('test-data/ocr1.txt')
    assert m['targeting']['placements'] == 'News Feed on desktop computers or News Feed on mobile devices'


def test_living_in():
    m = extract_metadata('test-data/ocr1.txt')
    assert m['targeting']['living_in'] == 'United States'

def test_language():
    m = extract_metadata('test-data/ocr2.txt')
    assert m['targeting']['language'] == 'English (US)'

def test_location():
    m = extract_metadata('test-data/ocr2.txt')
    assert m['targeting']['locations'] == [
      'United States: Alabama',
      'United States: Arkansas',
      'United States: Florida',
      'United States: Georgia',
      'United States: Louisiana',
      'United States: Mississippi',
      'United States: North Carolina',
      'United States: South Carolina',
      'United States: Tennessee',
      'United States: Texas',
      'United States: Virginia',
    ]

def test_interests():
    m = extract_metadata('test-data/ocr1.txt')
    assert m['targeting']['interests'] == [
        'Hispanic and latino american culture',
        'Mexico',
        'Mexican american culture',
        'Hispanic culture',
        'Latino culture',
        'Latin hip hop',
        'Chicano',
        'Chicano Movement',
        'Hispanidad',
        'Mexican Pride',
        'Lowrider',
        'Chicano rap',
        'La Raza'
    ]
        


