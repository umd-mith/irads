import pytest

from extract import extract_metadata

def test_metadata1():
    m = extract_metadata('test-data/ocr1.txt')
    assert m['id'] == 2727
    assert m['text'] == 'Real Mexican-American pride. Respect!\nFYI: The three largest Hispanic groups in the United States are the Mexican-\nAmericans, Puerto Ricans and Cubans.\n\n'
    assert m['url'] == 'https://www.facebook.com/brownunitedfront/'
    assert m['impressions'] == 82748
    assert m['clicks'] == 11051
    assert m['spend'] == {'amount': '440.00', 'currency': 'RUB'}
    assert m['created'] == '2017-02-16T00:42:01-08:00'
    assert m['ended'] == '2017-02-18T00:42:01-08:00'

def test_age():
    m = extract_metadata('test-data/ocr2.txt')
    assert m['targeting']['age'] == '18 - 65+'

def test_placements():
    m = extract_metadata('test-data/ocr1.txt')
    assert m['targeting']['placements'] == [
        'News Feed on desktop computers',
        'News Feed on mobile devices'
    ]

def test_living_in():
    m = extract_metadata('test-data/ocr1.txt')
    assert m['targeting']['living_in'] == 'United States'

def test_languages():
    m = extract_metadata('test-data/ocr2.txt')
    assert m['targeting']['languages'] == ['English (US)']
    m = extract_metadata('test-data/ocr3.txt')
    assert m['targeting']['languages'] == ['English (UK)', 'English (US)']

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
    assert m['targeting']['match'] == [
        'Interests: Hispanic and latino american culture',
        'Interests: Mexico',
        'Interests: Mexican american culture',
        'Interests: Hispanic culture',
        'Interests: Latino culture',
        'Interests: Latin hip hop',
        'Interests: Chicano',
        'Interests: Chicano Movement',
        'Interests: Hispanidad',
        'Interests: Mexican Pride',
        'Interests: Lowrider',
        'Interests: Chicano rap',
        'Interests: La Raza'
    ]

        


