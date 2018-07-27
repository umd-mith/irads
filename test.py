import pytest

from extract import extract_metadata, unpack

def test_unpack():
    assert unpack('Interests: Music, Mexico, M&Ms') == {
        'interests': ['Music', 'Mexico', 'M&Ms']
    }

def test_metadata():
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
    assert m['targeting']['age'] == ['18 - 65+']

def test_placements():
    m = extract_metadata('test-data/ocr1.txt')
    assert m['targeting']['placements'] == [
        'News Feed on desktop computers',
        'News Feed on mobile devices'
    ]

def test_location_living_in():
    m = extract_metadata('test-data/ocr1.txt')
    assert m['targeting']['location_living_in'] == ['United States']

def test_language():
    m = extract_metadata('test-data/ocr2.txt')
    assert m['targeting']['language'] == ['English (US)']
    m = extract_metadata('test-data/ocr3.txt')
    assert m['targeting']['language'] == ['English (UK)', 'English (US)']

def test_location():
    m = extract_metadata('test-data/ocr2.txt')
    assert m['targeting']['location']['united_states'] == [
      'Alabama',
      'Arkansas',
      'Florida',
      'Georgia',
      'Louisiana',
      'Mississippi',
      'North Carolina',
      'South Carolina',
      'Tennessee',
      'Texas',
      'Virginia',
    ]

def test_interests():
    m = extract_metadata('test-data/ocr1.txt')
    assert m['targeting']['people_who_match']['interests'] == [
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

def test_people_who_match():
    m = extract_metadata('test-data/ocr4.txt')
    assert m['targeting']['people_who_match'] == [
        'People who like LGBT United',
        'Friends of connections: Friends of people who are connected to LGBT United'
    ]

def test_targeting_edge_case():
    m = extract_metadata('test-data/ocr5.txt')
    assert m['targeting']['exclude']['behaviors'] == [
        'Hispanic (US - All)',
        'Hispanic (US - Spanish dominant)',
        'Hispanic (US - English dominant)',
        'Hispanic (US - Bilingual: English and Spanish)',
        'Asian American (US)'
    ]
