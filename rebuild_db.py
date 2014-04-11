import json
import csv
from backend.views import db
from backend.models import MemberOfParliament


def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    """
    Handles special characters.
    Courtesy Alex Martelli (http://stackoverflow.com/questions/904041/reading-a-utf8-csv-file-with-python)
    """
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


def parse_scraper_data():
    """
    Read input data file, and save as a pickle.
    """

    mp_list = []
    with open('scraper/out.csv','Ur') as f:
        # reader = csv.reader(f, delimiter=',')
        reader = unicode_csv_reader(f)
        for row in reader:
            print row
            tmp = MemberOfParliament(*row)
            mp_list.append(tmp)
    return mp_list


if __name__ == "__main__":

    db.drop_all()
    db.create_all()

    mp_list = parse_scraper_data()
    for mp in mp_list:
        db.session.add(mp)

    db.session.commit()