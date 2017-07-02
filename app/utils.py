# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
import datetime

from dateutil.parser import parse


def parse_date(string):
    string = string.replace('年', '-')
    string = string.replace('月', '-')
    string = string.replace('日', '-')
    try:
        result = parse(string)
        return datetime.date(result.year, result.month, result.day)
    except ValueError:
        return None


def is_wiki_about_person(text):
    pattern = re.compile(r'{{infobox person.*?}}', re.I | re.DOTALL)
    return True if pattern.search(text) else False


def get_birth_death_date(text):
    def filter_date(string):
        """
        # {{birth based on age as of date|mos=1|25|2009|02|03}}
        # from: https://zh.wikipedia.org/wiki/%E5%86%B0%E8%9B%99
        >>> filter_date("|mos=1|25|2009|02|03")
        ['25', '2009', '02', '03']
        """
        result = []
        for i in string.strip('|').split('|'):
            i = i.strip()
            if not i:
                continue
            if '=' in i:
                continue
            result.append(i)
        return result
    # def get_date_from_text(pattern, text, callback):
    #     match = re.search(pattern, text, flags=re.I)
    #     if not match:
    #         return None
        # return callback()

    birth_date, death_date = None, None

    # birth date and age
    match = re.search(r'{{\s*birth\s*date and age\s*\|[^\d]*(\d+\|\d+\|\d+)', text, flags=re.I)
    if match:
        # living
        return parse_date(match.group(1).replace('|', '-')), None

    # birth date
    match = re.search(r'{{\s*birth\s*date\s*\|[^\d]*(\d+\|\d+\|\d+)', text, flags=re.I)
    if match:
        birth_date = parse_date(match.group(1).replace('|', '-'))

    # birth year and age
    # see: https://zh.wikipedia.org/wiki/Template:Birth_year_and_age
    if not birth_date:
        match = re.search(r'{{\s*birth\s*year and age\s*\|[^\d]*(\d+)', text, flags=re.I)
        if match:
            birth_date = datetime.date(int(match.group(1)), 1, 1)

    # birth based on age as of date
    # see: https://zh.wikipedia.org/wiki/Template:Birth_based_on_age_as_of_date
    if not birth_date:
        match = re.search(r'{{\s*birth based on age as of date\s*\|(.*?)}}', text, flags=re.I)
        if match:
            splitted = filter_date(match.group(1))
            if splitted:
                birth_date = datetime.date(int(splitted[1]) - int(splitted[0]), 1, 1)

    # birth_date  = 1957年6月27日
    # example: https://zh.wikipedia.org/wiki/%E7%9B%96%E5%B0%94%C2%B7%E4%BC%8A%E7%93%A6%E5%B0%94%E7%BB%A5
    if not birth_date:
        match = re.search(r'birth_date\s*=\s*(\d+)年(\d+)月(\d+)日', text, flags=re.I)
        if match:
            birth_date = datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))

    # death date and age
    match = re.search(r'{{\s*death\s*date and age\s*\|[^\d]*(\d+\|\d+\|\d+).*?}}', text, flags=re.I)
    if match:
        death_date = parse_date(match.group(1).replace('|', '-'))

    # death date
    # see: https://en.wikipedia.org/wiki/Template:Death_date
    if not death_date:
        match = re.search(r'{{\s*death date\s*\|[^\d]*(\d+)\|(\d+)\|(\d+)', text, flags=re.I)
        if match:
            death_date = datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    if not death_date:
        match = re.search(r'{{\s*death date\s*\|[^\d]*(\d+)\|(\d+)', text, flags=re.I)
        if match:
            death_date = datetime.date(int(match.group(1)), int(match.group(2)), 1)
    if not death_date:
        match = re.search(r'{{\s*death date\s*\|[^\d]*(\d+)', text, flags=re.I)
        if match:
            death_date = datetime.date(int(match.group(1)), 1, 1)

    # death year and age
    # see: https://zh.wikipedia.org/wiki/Template:Death_year_and_age
    if not death_date:
        match = re.search(r'{{\s*death\s*year and age\s*\|[^\d]*(\d+)\|\d+\|(\d+)', text, flags=re.I)
        if match:
            death_date = datetime.date(int(match.group(1)), int(match.group(2)), 1)
        else:
            match = re.search(r'{{\s*death\s*year and age\s*\|[^\d]*(\d+)', text, flags=re.I)
            if match:
                death_date = datetime.date(int(match.group(1)), 1, 1)

    if not death_date:
        match = re.search(r'death_date\s*=\s*(\d+)年(\d+)月(\d+)日', text, flags=re.I)
        if match:
            death_date = datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))

    return birth_date, death_date


def get_wiki_abstract(text):
    pass
