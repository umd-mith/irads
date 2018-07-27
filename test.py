import pytest

from extract import extract_metadata

def test_metadata():
    m = extract_metadata('test-data/ocr1.txt')
    assert m['id'] == 2727
    assert m['text'] == 'Real Mexican-American pride. Respect!\nFYI: The three largest Hispanic groups in the United States are the Mexican-\nAmericans, Puerto Ricans and Cubans.'
    assert m['url'] == 'https://www.facebook.com/brownunitedfront/'
    assert m['impressions'] == 82748
    assert m['clicks'] == 11051
    assert m['spend'] == {'amount': '440.00', 'denomination': 'RUB'}
    assert m['created'] == '2017-02-16T00:42:01-08:00'
    assert m['ended'] == '2017-02-18T00:42:01-08:00'
    assert m['targeting'] == {
        'age': '18 - 65+'
    }

