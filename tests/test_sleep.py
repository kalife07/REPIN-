import pytest

from app.sleep import sleep


@pytest.mark.parametrize('bed_time, wake_up_time', [
    ('9 pm', '5:30 am'),
    ('10 pm', '6:30 am'),
    ('11 pm', '7:30 am'),
    ('12 am', '8:30 am'),
    ('1 am', '9:30 am'),
    ('2 am', '10:30 am'),
])
def test_bedtime_options_from_frontend(bed_time, wake_up_time):
    assert sleep(bed_time) == wake_up_time


def test_noon_bedtime():
    assert sleep('12 pm') == '8:30 pm'


def test_wake_up_time_crossing_noon():
    assert sleep('4 am') == '12:30 pm'


def test_uppercase_am_pm():
    assert sleep('10 PM') == '6:30 am'


@pytest.mark.parametrize('bed_time', ['', None])
def test_missing_bedtime(bed_time):
    assert sleep(bed_time) == 'N/A'


@pytest.mark.parametrize('bed_time', ['10', 'ten pm'])
def test_invalid_bedtime_raises(bed_time):
    with pytest.raises((IndexError, ValueError)):
        sleep(bed_time)
