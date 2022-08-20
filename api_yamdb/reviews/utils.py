import datetime


def year_validator(year):
    if year > datetime.datetime.now().year:
        raise ValueError(f'{year} is not correct')
