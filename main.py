## Читаем адресную книгу в формате CSV в список contacts_list:
import csv
import re

with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

## 1. Выполните пункты 1-3 задания.
## Ваш код

def formated_contacts_list(contacts_list):
    '''
    функция на вход принимает список контактов
    выполняет форматирование списка - удаляет лишний пробелы для следующих случаев:
    1 - Если длина строки более 7 элементов (всего семь полей в структуре таблицы)
    2 - Если ФИО клиента записано в одном поле без разбивки
    '''

    # выравниваем количество элементов в строке (их должно быть не более 7)
    for row in contacts_list:
        if len(row) == 8:
            del row[-1]

    # Удаляем пустые строки для имени или отчества
    for i in range(len(contacts_list)):
        if contacts_list[i][0].count(' ') == 1 and contacts_list[i][1] != '' and contacts_list[i][2] == '':
            del contacts_list[i][2]
        if contacts_list[i][0].count(' ') == 2 and contacts_list[i][1] == '' and contacts_list[i][2] == '':
            del contacts_list[i][1:3]
        if contacts_list[i][1].count(' ') == 1 and contacts_list[i][1] != '' and contacts_list[i][2] == '':
            del contacts_list[i][2]
        if contacts_list[i][0].count(' ') == 1 and contacts_list[i][1] == '' and contacts_list[i][2] == '':
            del contacts_list[i][2]

    return contacts_list

def normalize_contacts(contacts_list):
    '''
    Функция принимает на вход список контактов и форматирует ФИО, раскладывая фамилию, имя и отчество
    по соответствующим полям.
    Также функция приводит номер телефона в заданный формат +7(999)999-99-99 доб.9999.
    '''
    contacts_list = formated_contacts_list(contacts_list)

    pattern_name = r'(^\w+)[,|\s](\w+)[,|\s](\w+)?'
    new_pattern_name = r'\1,\2,\3'
    pattern_tel =r'(\+7|7|8)\s*\(?(\d{3})\)?[\s*|-]?(\d{3})[\s*|-]?(\d{2})[\s*|-]?(\d{2,3})\s*\(?(доб.)?\s*(\d{4})?\)?'
    new_pattern_tel =r'+7(\2)\3-\4-\5 \6\7'

    fixed_phonebook = []

    for elem in contacts_list:
        row = ','.join(elem)
        fixed_name = re.sub(pattern_name, new_pattern_name, row)
        fixed_phone = re.sub(pattern_tel, new_pattern_tel, fixed_name)
        fixed_phonebook.append(fixed_phone.split(','))

    return fixed_phonebook

def dedublicated_contacts():
    '''
    функция объединяющая все дублирующиеся записи о человеке в одну строку
    '''
    fixed_phonebook = normalize_contacts(contacts_list)

    #создаем словарь для поиска дубликатов где ключ это фамилия и имя клиента, а значение список всех полей
    doubles_counter = {}

    for row in fixed_phonebook:
        fio = ' '.join(row[0:2])
        if fio in doubles_counter.keys():
            for i in range(len(row)):
                if doubles_counter[fio][i] == '':
                    doubles_counter[fio][i] = row[i]
        else:
            doubles_counter[fio] = row
            
    # создаем список для сохранения дедублицированных клиентов
    result = []
    for res in doubles_counter.values():
        result.append(res)

    return result

if __name__ == '__main__':
    new_contacts_list = dedublicated_contacts()

    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(new_contacts_list)