import pandas as pd
import random

NAME_FILE = 'test_archive.csv'
COUNT_STRING = 1000


def create_test_archive(file_path):
    # Создание пустого DataFrame
    df = pd.DataFrame(columns=['id', 'cache'])
    # Генерация случайных значений для колонок
    ids = []
    cache_values = []
    for i in range(COUNT_STRING):
        # Генерация случайного значения для id
        id_value = random.randint(1, 1000)
        ids.extend([id_value])
    # Заполнение DataFrame сгенерированными значениями
    df['id'] = ids
    # Генерация случайных значений для cache
    for i in range(len(df)):
        cache_value = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
        cache_values.append(cache_value)
    # Заполнение DataFrame сгенерированными значениями
    df['cache'] = cache_values
    # Сохранение DataFrame в CSV
    df.to_csv(file_path, index=False)


def pandas_search_id(file_path):
    """Решение на базе библитеки pandas."""
    df = pd.read_csv(file_path)
    # Подсчет количества повторений идентификаторов
    id_counts = df['id'].value_counts()
    # Вывод идентификаторов, которые встречаются только 3 раза
    ids_with_3_occurrences = id_counts[id_counts == 3].index
    # Подсчет частоты повторений идентификаторов
    frequency_counts = id_counts.value_counts()
    return ids_with_3_occurrences, frequency_counts


def count_id_csv(file_path):
    """
    Функция предоставляетс следующую информацию:  
    1) id, которые встречаются в файле только 3 раза  
    2) Частоту повторений (сколько уникальных ид встречалось 1 раз, 2 раза и т.д.)
    """
    # frequency_counts словарь в которые сохраняетя
    # {int- количество вхождений id в файл: [int - количество id, str - id...] }
    frequency_counts = {}
    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            # Обращаемся к id в каждой строчке
            id_line = line.split(',')[0]
            # Первое вхождения в цикл. Если словарь пустой создаем знаяения
            if not frequency_counts:
                frequency_counts.setdefault(1, [1, {id_line}])
            # Переходим к основной логике поиска
            else:
                # Подсчитываем какой максимальное количество повторений
                count_step = len(frequency_counts.keys())
                step = 0
                flag = True
                while flag:
                    # Первое вхождение в цикл, если количество повторений = 1 и id нет списке с количеством повтороний 
                    # и цикл дошел до списка с первым вхождением. Тогда в него добавляется id.   
                    if count_step - step == 1 and id_line not in frequency_counts[count_step - step][1] and count_step == 1:
                        frequency_counts[count_step][1].add(id_line)
                        frequency_counts[count_step][0] += 1
                        flag = False
                    # Условие когда список повторений больше 1, но id появилось в первые, так же помещаем в список с первым вхождением
                    # и увеличиваем счетчик
                    elif count_step - step == 1 and id_line not in frequency_counts[count_step - step][1]:
                        frequency_counts[count_step - step][1].add(id_line)
                        frequency_counts[count_step - step][0] += 1
                        flag = False
                    # Ищем id в списках с повторениями. От самого максимального. 
                    # В случаи если нашли id в списке, удаляем его из текущего списка,
                    # сокращаем счетчик на 1 и переносим в следущий список повторений
                    # и так же увеличиваем счетчик в нем. 
                    elif id_line in frequency_counts[count_step - step][1]:
                        frequency_counts[count_step - step][1].discard(id_line)
                        frequency_counts[count_step - step][0] -= 1
                        count_step = (count_step - step) + 1
                        frequency_counts.setdefault(count_step, [0, {id_line}])
                        frequency_counts[count_step][1].add(id_line)
                        frequency_counts[count_step][0] += 1
                        flag = False
                    else:
                        step += 1
        return frequency_counts


def check_answer_ids_with_3(pandas, my_code):
    pandas_with_3 = set(pandas)
    my_list = set(map(int, my_code))
    if pandas_with_3 == my_list:
        return "\n__Значения в списках совпадают__\n"
    else:
        return "__Значения в списках разные__"


def test_my_code():
    print("ТЕСТ")
    assert count_id_csv('test_task_1.csv') == (
        {1: [1, {'12'}], 2: [1, {'16'}], 3: [1, {'11'}], 4: [1, {'15'}], 5: [1, {'10'}]}
    ), "Ошибка в подсчетах."

    print("Тест пройден")


def main():
    # созданеие фалай для тестов
    create_test_archive(NAME_FILE)
    # работа моего модуля
    my_frequency_counts = count_id_csv(NAME_FILE)
    values_equal_to_3 = my_frequency_counts.get(3)[1]
    print('Идентификаторы, которые встречаются только 3 раза:\n', ', '.join(values_equal_to_3), '\n')
    print('Частота повторений ID:')
    print('\n'.join([f'{key} {val[0]}' for key, val in my_frequency_counts.items()]))
    # работа модуля pandas
    pandas_ids_with_3, pandas_frequency_counts = pandas_search_id(NAME_FILE)
    print("Ответ pandas:\n", pandas_ids_with_3)
    print(pandas_frequency_counts)
    # проверки сравнение ответа pandas и моего модуля
    print(check_answer_ids_with_3(pandas_ids_with_3, values_equal_to_3))
    test_my_code()


if __name__ == '__main__':
    main()
