import requests
import logging
from bs4 import BeautifulSoup
from bs4.element import Tag
from json import loads

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


class DbUpdater:
    is_instanced = False
    is_working = True


def __get_stopcoronavirus_rf_page__():
    """
    Отправка реквеста на стопкоронавирус.рф/information/
    :return: Текст страницы, либо None при возникновении ошибки
    """
    try:
        return requests.get(stop_coronavirus_url).text
    except requests.ConnectionError:
        logging.exception('При отправке запроса произошла ошибка соединения')
    except requests.RequestException:
        logging.exception('При отправке запроса произошло исключение')
    except Exception:
        logging.exception('При отправке запроса произошла неизвестная ошибка')
    return None


def __parse_stopcoronavirus_rf_page__(page_text: str) -> Tag:
    """
    Выделяет из текста страницы
    :param page_text: Текст страницы стопкоронавирус.рф/information/
    :return: Тэг cv-spread-overview, содержащий актуальную информацию либо None в случае ошибки
    """
    try:
        soup = BeautifulSoup(page_text, 'html.parser')
        tag = soup.find_all('cv-spread-overview')[0]
        tag.findChild(recursive=False).decompose()
        return tag
    except Exception:
        logging.exception('При парсинге текста страницы произошла ошибка:')
    return None


def __get_strings_from_tag__(tag: Tag):
    """
    Получение необработанных списков данных из тэга
    :param tag: Тэг cv-spread-overview, содержащий актуальную информацию
    :return: tuple списков с информацией (в строковом формате без обработки) либо None в случае ошибки
    """
    try:
        spread_data = tag.get(':spread-data')

        # Данные о степенях изоляции, возможно понадобятся
        # todo Добавить либо удалить
        # isolation_data = div.get(':isolation-data')
        # covid_free_states = div.get(':covid-free-states')

        global_stat_date = tag.get('global-stat-date')
        return spread_data, global_stat_date
    except Exception:
        logging.exception("При формировании листов произошла ошибка")
    return None


def __clean_string__(string: str) -> str:
    """
    Очистка строки от символов HTML, лишних пробелов, а также замена символов в кодировке Юникод
    :param string: строка для замены
    :return: res_string: очищенная строка либо None в случае ошибки
    """
    try:
        res_string = string
        for unicode_char, char in unicode_symbols.items():
            res_string = res_string.replace(unicode_char, char)
        for to_replace, replace_by in symbols_to_replace.items():
            res_string = res_string.replace(to_replace, replace_by)
        res_string = " ".join(res_string.split())
        return res_string
    except Exception:
        logging.exception(f'Произошла ошибка при парсинге строки: {string}')
    return None


def __eval_string__(string: str):
    """
    Перевод данных из строкового формата в массив
    :param string: Строка с данными
    :return: Результат перевода либо None в случае ошибки
    """
    try:
        result = loads(string)
        return result
    except Exception:
        logging.exception('При переводе информации из строкового типа произошла ошибка')
    return None


def update():
    logging.debug("Начат процесс сверки данных с стопокоронавирус.рф")
    try:
        page_text = __get_stopcoronavirus_rf_page__()
        info_tag = __parse_stopcoronavirus_rf_page__(page_text)
        spread_data, global_stat_date = __get_strings_from_tag__(info_tag)
        spread_data = __clean_string__(spread_data)
        spread_data = __eval_string__(spread_data)
    except Exception:
        logging.exception('Ошибка в функции update()')
    logging.debug("Сверка данных завершена")
