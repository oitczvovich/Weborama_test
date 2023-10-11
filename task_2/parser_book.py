import os
import warnings
import argparse
from ebooklib import epub
import xml.etree.ElementTree as ET


def _parse_epub(file_path):
    """Парсер данных из книг формата epub.

    Args:
        file_path (_type_): путь до файла книги формата epub.

    Returname_space:
        title: название книги.
        author: автор книги.
        publisher: издатель книги.
        year: год издания книги.
    """
    try:
        # Чтение файла epub
        book = epub.read_epub(file_path)
        # Получение метаданных книги
        title = book.get_metadata('DC', 'title')[0][0]
        author = book.get_metadata('DC', 'creator')[0][0]
        publisher = book.get_metadata('DC', 'publisher')[0][0]
        year = book.get_metadata('DC', 'date')[0][0].split('-')[0]
    except (KeyError, IndexError, AttributeError):
        # Обработка исключений, если метаданные отсутствуют или имеют неправильный формат
        title = None
        author = None
        publisher = None
        year = None
    return title, author, publisher, year


def _parse_fb2(file_path):
    """Парсер данных из книг формата epub.

    Args:
        file_path (_type_): путь до файла книги формата epub.

    Returname_space:
        title: название книги.
        author: автор книги.
        publisher: издатель книги.
        year: год издания книги.
    """
    # Пространство имен для парсинга XML
    name_space = '{http://www.gribuser.ru/xml/fictionbook/2.0}'
    # Загрузка корневого элемента из файла fb2
    book = ET.parse(file_path).getroot()
    try:
        # извлекаем информацию о книге из раздела title-info
        description = book.find(f'{name_space}description/{name_space}title-info')
        # извлекаем даннын имени автора
        first_name = description.find(f'{name_space}author/{name_space}first-name').text
        middle_name = description.find(f'{name_space}author/{name_space}middle-name').text
        last_name = description.find(f'{name_space}author/{name_space}last-name').text
        author = ' '.join((first_name, middle_name, last_name))
        # извлекаем название книги
        title = description.find(f'{name_space}book-title').text
        # извлекаем название издательства
        publisher = book.find(
            f'{name_space}description/{name_space}publish-info/{name_space}publisher'
        ).text
        # извлекаем год издания
        year = description.find(f'{name_space}date').text
    except (KeyError, IndexError, AttributeError):
        # Обработка исключений, если информация отсутствует или имеет неправильный формат
        title = None
        author = None
        publisher = None
        year = None
    return title, author, publisher, year


def _parse_file(file_path):
    # Определяет формат файла.
    if file_path.endswith('.epub'):
        return _parse_epub(file_path)
    elif file_path.endswith('.fb2'):
        return _parse_fb2(file_path)
    else:
        raise ValueError('Uname_spaceupported file format')


if __name__ == '__main__':
    # убрать предупреждения от epub
    warnings.simplefilter(action='ignore', category=UserWarning)
    parser = argparse.ArgumentParser(
        description=(
            'Скрипт для парсинга данных о книге. Формат fb2 или epub. '
            '\nВозвращает данные: Название, Автор, Издатель, Год издания'
        )
    )
    parser.add_argument(
        'file_path',
        help=(
            'Путь до книги. Полные или если книга '
            'в текущей папке указать название книги.'
        )
    )
    args = parser.parse_args()
    if os.path.exists(args.file_path):
        res = _parse_file(file_path=args.file_path)
        print(res)
    else:
        print("Файл не существует или указан не правильный путь к файлу.")
