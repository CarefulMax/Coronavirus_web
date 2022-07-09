import requests
import logging
from re import sub
from django.db import IntegrityError
from bs4 import BeautifulSoup
from bs4.element import Tag
from json import loads
from stats.models import RegionalStats, Regions, LastParsed, \
    Restrictions, RegionalRestrictions
from datetime import datetime

stop_coronavirus_url = 'https://xn--80aesfpebagmfblc0a.xn--p1ai/information/'
unicode_symbols = {
    '\\u0410': 'А',
    '\\u0411': 'Б',
    '\\u0412': 'В',
    '\\u0413': 'Г',
    '\\u0414': 'Д',
    '\\u0415': 'Е',
    '\\u0416': 'Ж',
    '\\u0417': 'З',
    '\\u0418': 'И',
    '\\u0419': 'Й',
    '\\u041a': 'К',
    '\\u041b': 'Л',
    '\\u041c': 'М',
    '\\u041d': 'Н',
    '\\u041e': 'О',
    '\\u041f': 'П',
    '\\u0420': 'Р',
    '\\u0421': 'С',
    '\\u0422': 'Т',
    '\\u0423': 'У',
    '\\u0424': 'Ф',
    '\\u0425': 'Х',
    '\\u0426': 'Ц',
    '\\u0427': 'Ч',
    '\\u0428': 'Ш',
    '\\u0429': 'Щ',
    '\\u042a': 'Ъ',
    '\\u042b': 'Ы',
    '\\u042c': 'Ь',
    '\\u042d': 'Э',
    '\\u042e': 'Ю',
    '\\u042f': 'Я',
    '\\u0430': 'а',
    '\\u0431': 'б',
    '\\u0432': 'в',
    '\\u0433': 'г',
    '\\u0434': 'д',
    '\\u0435': 'е',
    '\\u0436': 'ж',
    '\\u0437': 'з',
    '\\u0438': 'и',
    '\\u0439': 'й',
    '\\u043a': 'к',
    '\\u043b': 'л',
    '\\u043c': 'м',
    '\\u043d': 'н',
    '\\u043e': 'о',
    '\\u043f': 'п',
    '\\u0440': 'р',
    '\\u0441': 'с',
    '\\u0442': 'т',
    '\\u0443': 'у',
    '\\u0444': 'ф',
    '\\u0445': 'х',
    '\\u0446': 'ц',
    '\\u0447': 'ч',
    '\\u0448': 'ш',
    '\\u0449': 'щ',
    '\\u044a': 'ъ',
    '\\u044b': 'ы',
    '\\u044c': 'ь',
    '\\u044d': 'э',
    '\\u044e': 'ю',
    '\\u044f': 'я'
}
symbols_to_replace = {
    '\/': '/',
    '\\r': '',
    '\\n': '',
    '<li>': ' ',
    '</li>': '',
    '<ul>': '',
    '</ul>': ''
}
months = {'января': '01',
          'февраля': '02',
          'марта': '03',
          'апреля': '04',
          'мая': '05',
          'июня': '06',
          'июля': '07',
          'августа': '08',
          'сентября': '09',
          'октября': '10',
          'ноября': '11',
          'декабря': '12'}
country_keys_change = {'sickChange': 'sick_incr',
                       'hospitalized': 'hospitalized',
                       'healedChange': 'healed_incr',
                       'diedChange': 'died',
                       'vaccineFirst': 'first',
                       'vaccineSecond': 'second'}
restriction_changes = {
    'и загрузить результат на портал госуслуг. До получения результатов теста необходимо соблюдать режим самоизоляции.': 'и загрузить результат на портал госуслуг; До получения результатов теста необходимо соблюдать режим самоизоляции.',
    'т.ч.': 'тч',
    ' им. ': ' им ',
    '.00': ':00',
    ' кв.м.': ' кв м',
    ' др.': ' др',
    ' г.': 'г',
    ' соц.': 'соц'
}


def __get_stopcoronavirus_rf_page__():
    """
    Отправка реквеста на стопкоронавирус.рф/information/
    :return: Текст страницы, либо None при возникновении ошибки
    :raises Exception: e - ошибка для дальнейшней обработки
    """
    try:
        return requests.get(stop_coronavirus_url).text
    except requests.ConnectionError as e:
        print('При отправке запроса произошла ошибка соединения')
        raise e
    except requests.RequestException as e:
        print('При отправке запроса произошло исключение')
        raise e
    except Exception as e:
        print('При отправке запроса произошла неизвестная ошибка')
        raise e


def parseregions(page_text):
    return __parse_regions_stopcoronavirus_rf_page__(page_text)


def __parse_regions_stopcoronavirus_rf_page__(page_text: str) -> Tag:
    """Выделяет из текста страницы тег регионов

    :param page_text: Текст страницы стопкоронавирус.рф/information/
    :param type: regions для получения данных по регионам, country - для России
    :return: Тэг cv-spread-overview, содержащий актуальную информацию либо None в случае ошибки
    :raises Exception: e - ошибка для дальнейшней обработки
    """
    if page_text is None:
        raise ValueError('Текст страницы is none')
    try:
        soup = BeautifulSoup(page_text, 'html.parser')
        tag = soup.find_all('cv-spread-overview')[0]
        tag.findChild(recursive=False).decompose()
        return tag
    except Exception as e:
        print('При парсинге регионов из текста страницы произошла ошибка:' + str(e))
        raise e


def __get_strings_from_tag__(tag: Tag):
    """
    Получение необработанных списков данных из тэга
    :param tag: Тэг cv-spread-overview, содержащий актуальную информацию
    :return: tuple списков с информацией (в строковом формате без обработки) либо None в случае ошибки
    :raises Exception: e - ошибка для дальнейшней обработки
    """
    if tag is None:
        raise ValueError('Тег данных is none')
    try:
        spread_data = tag.get(':spread-data')

        # Данные о степенях изоляции, возможно понадобятся
        # todo Добавить либо удалить
        # isolation_data = div.get(':isolation-data')
        # covid_free_states = div.get(':covid-free-states')

        global_stat_date = tag.get('global-stat-date')
        return spread_data, global_stat_date
    except Exception as e:
        print("При формировании листов произошла ошибка")
        raise e


def __clean_string__(string: str) -> str:
    """
    Очистка строки от символов HTML, лишних пробелов, а также замена символов в кодировке Юникод
    :param string: строка для замены
    :return: res_string: очищенная строка либо None в случае ошибки
    :raises Exception: e - ошибка для дальнейшней обработки
    """
    try:
        res_string = string
        for unicode_char, char in unicode_symbols.items():
            res_string = res_string.replace(unicode_char, char)
        for to_replace, replace_by in symbols_to_replace.items():
            res_string = res_string.replace(to_replace, replace_by)
        res_string = " ".join(res_string.split())
        return res_string
    except Exception as e:
        print(f'Произошла ошибка при парсинге строки: {string}')
        raise e


def __eval_string__(string: str):
    """
    Перевод данных из строкового формата в массив
    :param string: Строка с данными
    :return: Результат перевода либо None в случае ошибки
    :raises Exception: e - ошибка для дальнейшней обработки
    """
    try:
        result = loads(string)
        return result
    except Exception as e:
        print('При переводе информации из строкового типа произошла ошибка')
        raise e


def __parse_date__(date_str: str) -> str:
    """Переводит дату в необходимый формат

    Из '11 марта 14:20' в '11.03.*актуальный год*'

    :param date_str: дата в формате парсинга
    :return: дата в новом формате
    """
    try:
        split = date_str.split(' ')
        return f'{datetime.today().year}-{months[split[1]]}-{split[0]}'
    except Exception as e:
        print('При переводе даты в другой формат произошла ошибка')
        raise e


def __parse_country_stopcoronavirus_rf_page__(page_text: str) -> dict:
    """Выделяет из текста страницы информацию по стране

    Проводит весь цикл работы от текста до словаря, так как данные по стране парсятся иначе чем региональные

    :param page_text: Текст страницы стопкоронавирус.рф/information/
    :return: Словарь с данными о России
    """
    if page_text is None:
        raise ValueError('Текст страницы is none')
    try:
        country_stats = {'title': 'Россия'}
        soup = BeautifulSoup(page_text, 'html.parser')
        # print(soup)
        spread_tag = soup.find_all('cv-stats-virus')[0]
        stats_data = spread_tag.get(':stats-data')
        stats_data = __eval_string__(stats_data)
        for k, v in stats_data.items():
            stats_data[k] = int(v.replace(' ', ''))
        for k, v in country_keys_change.items():
            country_stats[v] = stats_data[k]
        collective_immunity = soup.find_all('h3')[2]
        collective_immunity = collective_immunity.text
        collective_immunity = float(collective_immunity.rstrip('%').replace(',', '.'))
        country_stats['immune_percent'] = collective_immunity
        country_stats['died_incr'] = country_stats['died']
        print(country_stats)
        return country_stats
    except Exception as e:
        print('При парсинге страны из текста страницы произошла ошибка:')
        raise e


def __create_regional_stats_list__(dicts: list, date: str) -> list:
    """Формирует список статистики типа данных модели

    :param dicts: массив словарей со статистикой (формат парсинга)
    :param date: дата данных
    :return: список статистики типа данных RegionalStats
    """
    try:
        regional_stats = []
        # print('Создание списка')
        for region_dict in dicts:
            # print(region_dict)
            # print(region_dict['isolation'])
            region_title = region_dict['title'].strip(' ')
            region = Regions.objects.get(region=region_title)
            new_cases = region_dict['sick_incr']
            hospitalised = region_dict['hospitalized']
            recovered = region_dict['healed_incr']
            died = region_dict['died_incr']
            vaccinated_first_component_cumulative = region_dict['first']
            vaccinated_fully_cumulative = region_dict['second']
            collective_immunity = region_dict['immune_percent']
            stats = RegionalStats(date=date, region=region, new_cases=new_cases, hospitalised=hospitalised,
                                  recovered=recovered, died=died,
                                  vaccinated_first_component_cumulative=vaccinated_first_component_cumulative,
                                  vaccinated_fully_cumulative=vaccinated_fully_cumulative,
                                  collective_immunity=collective_immunity)
            regional_stats.append(stats)
        if len(regional_stats) != 86:
            raise ValueError('Не все регионы прошли парсинг')
        return regional_stats
    except Exception as e:
        print('При создании списка статистики произошла ошибка')
        raise e


def __create_regional_restrictions_list__(dicts: list, date: str) -> list:
    try:
        regional_stats = []
        for region_dict in dicts:
            print(region_dict)
            region_title = region_dict['title'].strip(' ')
            region = Regions.objects.get(region=region_title)
            print(region_title)
            print(region)
            # print(region_dict)
            # print(region_dict['isolation'])
            # print()
            restrictions = region_dict['isolation']['descr']
            if restrictions is None:
                continue
            print(restrictions)
            print()
            restrictions = sub("<a.*/a>", "", restrictions)
            restrictions = sub("<.*>", "", restrictions)
            for k, v in restriction_changes.items():
                restrictions = restrictions.replace(k, v)
            for item in restrictions.split('.'):
                restriction = item.strip(' ')
                if restriction == '':
                    continue
                try:
                    Restrictions(description=restriction).save()
                except IntegrityError as e:
                    pass
                finally:
                    restriction = Restrictions.objects.get(description=restriction)
                    regional_stats.append(RegionalRestrictions(region=region, date=date, restriction=restriction))
        # print(len(regional_stats))
        # print(regional_stats)
        return regional_stats
    except Exception as e:
        print('При создании списка ограничений произошла ошибка')
        raise e


def __save_new_stats__(stats: list, restrictions: list, date: str):
    try:
        for region_restrictions in restrictions:
            try:
                region_restrictions.save()
            except IntegrityError as e:
                pass
        for region_stats in stats:
            try:
                region_stats.save()
            except IntegrityError as e:
                pass
        parse_info = LastParsed.objects.get()
        parse_info.parse_success = True
        parse_info.parsed_info_datetime = stats[0].date
        # print(parse_info)
        parse_info.save()
    except Exception as e:
        print('При сохранении ограничений произошла ошибка')
        raise e


def update() -> bool:
    """
    Проводит весь процесс взятия данных со стопкоронавирус.рф, их обработки и занесения в базу данных.
    :return bool: Успешность выполнения парсинга
    """
    print("Начат процесс сверки данных с стопокоронавирус.рф")
    try:
        page_text = __get_stopcoronavirus_rf_page__()
        regions_tag = __parse_regions_stopcoronavirus_rf_page__(page_text)
        spread_data, global_stat_date = __get_strings_from_tag__(regions_tag)
        global_stat_date = __parse_date__(global_stat_date)
        spread_data = __clean_string__(spread_data)
        spread_data = __eval_string__(spread_data)
        restrictions_list = __create_regional_restrictions_list__(spread_data, global_stat_date)
        spread_data.append(__parse_country_stopcoronavirus_rf_page__(page_text).copy())
        stats_list = __create_regional_stats_list__(spread_data, global_stat_date)
        __save_new_stats__(stats_list, restrictions_list, global_stat_date)
        print("Сверка данных успешно завершена")
        return True
    except Exception as e:
        print('Ошибка в функции db_updater.updater.update(): ' + str(e))
        parse_info = LastParsed.objects.get()
        parse_info.parse_datetime = datetime.now()
        parse_info.parse_success = False
        parse_info.save()
        return False


if __name__ == '__main__':
    update()
