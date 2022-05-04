# Создаем класс Relative
# Парсим данные из файла js

import os
import datetime
from datetime import date
import requests


communications = { 'MM': { '11': 'Brothers' ,'01': 'Father and Son' ,'02':'Grandfather and Grandson' ,'22': 'Cousins','33': 'Troyrod brothers', '10': 'Son and Father' ,'20':'Grandson and Grandfather' ,'23': 'Uncle and Cousin nephew','32': 'Cousin nephew and Uncle','60':'Relatives','54': 'Cousins 4th','55':'Relatives', '-2-3': 'Relatives'} ,'MF':{'11':'Brother and Sister' ,'01': 'Father and Dauther','21': '21','22': 'Cousins','31': '31','41': '41','54': 'Cousins 4th','10': 'Son and Mother','14': '14','13': '13','24': '24','60':'Relatives','55':'Relatives'}, 'FM':{'11': 'Sister and Brother' ,'12': 'Aunt and Nephew','14': '14','13': '13','24': '24','21': '21','30': '30','40': '40','54': 'Cousins 4th', '10': 'Dauther and Father','22': 'Cousins','03': '03','04': '04','60':'Relatives','55':'Relatives'} ,'FF':{'11':'Sisters' ,'01': 'Mother adn Dauther','14': '14','13': '13','54': 'Cousins 4th','20':'Grandmother and Granddauther' ,'24': '24','30': 'Granddauther and Grand-grandMother', '40': 'Relatives', '10': 'Dauther and Mother' ,'33': 'Troyrod sisters','02': 'Granddauther and Grandmother','03': 'Grand-grandMother and Granddauther','04': 'Relatives','60':'Relatives','55':'Relatives'}}


class Relative:
    def __init__(self, name, lastname, gender, date_birth, date_dead, codeDad, codeMam):
        self.name = name
        self.lastname = lastname
        self.gender = gender
        self.date_birth = date_birth
        self.date_dead = date_dead
        self.codeDad = codeDad
        self.codeMam = codeMam
        # self.avatar = avatar
        # self.codeSpo = codeSpo
        # self.codeSpo2 = codeSpo2
        # self.codeSpo3 = codeSpo3
        # self.codeSpo4 = codeSpo4
        # self.codeSpo5 = codeSpo5
        # self.info = info
        # self.war = war
        # self.p_i = p_i_
        # self.fb = fb
        # self.email_name = email_name
        # self.p2ga = p2ga
    

    def __str__(self):
        return f'Name: {self.name} {self.lastname} \nDate of birth: {self.date_birth} \nDate of Dead {self.date_dead} \ncodeDad: {self.codeDad} \ncodeMam: {self.codeMam}'
    
    def print_full_info(self):
        return f'Name: {self.name}  {self.lastname} \nDate of birth: {self.date_birth} \nDate of Dead {self.date_dead} \nemail: {self.email_name} \nfb: {self.fb} \nP2GA: {self.p2ga}\n'

def find_name(name):  
    n = 0
    for key, value in dict_relatives.items():
        # print(f'{value.lastname}, {value.lastname == name}')
        if value.name == name or value.lastname == name:
            n += 1
            print(f'{n}\nID: {key},  \n{value}')
    else:
        if n == 0:
            print('Don\'t find')
    return

# составление матрицы связей
def create_ties(id: str):
    # Формат словаря связей ключ- это  глубина родства(current_level), значение  codedad codeMam
    ties_relatives = {0: [id]}
    current_level = 1
    _up = True
    while _up:
        level_relatives_list = []
        for id_relatives in ties_relatives[current_level-1]:
            # print(dict_relatives['16'])
            if dict_relatives[id_relatives].codeDad != '':
                level_relatives_list.append(dict_relatives[id_relatives].codeDad)
            if dict_relatives[id_relatives].codeMam != '':
                level_relatives_list.append(dict_relatives[id_relatives].codeMam)
        if level_relatives_list == []:
            _up = False
        else:
            ties_relatives[current_level] = level_relatives_list
            current_level += 1
        # print(current_level)
    _down = True
    current_level = -1
    while _down:        
        level_relatives_list = []
        for code_relatives in ties_relatives[current_level+1]:
            # print(code_relatives)
            for id_relatives in dict_relatives.keys():
                if dict_relatives[id_relatives].codeDad == code_relatives or dict_relatives[id_relatives].codeMam == code_relatives:
                    level_relatives_list.append(id_relatives)
                    # print(level_relatives_list)
        if level_relatives_list == []:
            _down = False
        else:
            ties_relatives[current_level] = level_relatives_list
            # print(level_relatives_list)
            current_level -= 1
    return ties_relatives

def clean_values(value,clear_string: str):
    new_value = value.lstrip(clear_string)
    # print(new_value)
    if new_value == "":
        new_value = None
    new_value = new_value.strip('"')
    return new_value
    
def make_date(year, month, day):
    if year == month == day == None:
        date_value == None
    if year.isdigit():
        if month.isdigit():
            if day.isdigit():  
                date_value = datetime.date(int(year), int(month), int(day))
            date_value = datetime.date(int(year), int(month), 1)
        date_value = datetime.date(int(year), 1, 1)  
    date_value = year + '/' + month + '/' + day
   
    return date_value
        
def read_person():
# Запись из файла
    dict_relatives = {}
    response = requests.get('http://myfamilytree.live/dataOfPersons.js')
    reader_list = response.text.split('\r\n')
    reader_list.pop() #убирает последнюю строчку в файле
    # print(reader_list)
    for i in range(13, len(reader_list), 26):
        id_person = clean_values(reader_list[i],'var a=')
        # data_person = id_person
        # print(data_person)
        name_person = clean_values(reader_list[i+2],'pers[a].first = ')
        lastname_person = clean_values(reader_list[i+3],'pers[a].last = ')
        gender_person = clean_values(reader_list[i+4],'pers[a].F_M = ')
        # дата рождения и смерти
        dob_person = clean_values(reader_list[i+5],'pers[a].dob = ')
        dobMM_person = clean_values(reader_list[i+6],'pers[a].dobMM = ')
        dobDD_person = clean_values(reader_list[i+7],'pers[a].dobDD = ')
        
        dod_person = clean_values(reader_list[i+8],'pers[a].dod = ')
        dodMM_person = clean_values(reader_list[i+9],'pers[a].dodMM = ')
        dodDD_person = clean_values(reader_list[i+10],'pers[a].dodDD = ')
        
        date_birth = make_date(dob_person,dobMM_person,dobDD_person)
        date_dead = make_date(dod_person,dodMM_person,dodDD_person)

        # связи родственников
        codeDad_person = clean_values(reader_list[i+11],'pers[a].codeDad = ')
        codeMam_person = clean_values(reader_list[i+12],'pers[a].codeMam = ')

        data_person = Relative(name_person, lastname_person, gender_person, date_birth, date_dead, codeDad_person, codeMam_person)
        

        # дополнительная информация
        data_person.avatar = clean_values(reader_list[i+13],'pers[a].Avatar = ')
        data_person.codeSpo = clean_values(reader_list[i+14],'pers[a].codeSpo = ')
        data_person.codeSpo2 = clean_values(reader_list[i+15],'pers[a].codeSpo2 = ')
        data_person.codeSpo3 = clean_values(reader_list[i+16],'pers[a].codeSpo3 = ')
        data_person.codeSpo4 = clean_values(reader_list[i+17],'pers[a].codeSpo4 = ')
        data_person.codeSpo5 = clean_values(reader_list[i+18],'pers[a].codeSpo5 = ')
        data_person.info = clean_values(reader_list[i+19],'pers[a].info = ')
        data_person.war = clean_values(reader_list[i+20],'pers[a].War = ')
        data_person.p_i = clean_values(reader_list[i+21],'pers[a].pi = ')
        data_person.fb = clean_values(reader_list[i+22],'pers[a].fb = ')
        data_person.email_name = clean_values(reader_list[i+23],'pers[a].email = ')
        data_person.p2ga = clean_values(reader_list[i+24],'pers[a].P2GA = ')
        dict_relatives[id_person] = data_person
        # print(id_person)
        # print(data_person)   
        # print(data_person.__dir__())
        # print(date_birth)
    return dict_relatives

def compare_persons(person_1: str, person_2: str):
    for key_1, value_1 in create_ties(person_1).items():
        for key_2, value_2 in create_ties(person_2).items(): 
            for value in value_2:
                if value in value_1:
                    tie = [key_1, key_2, value, dict_relatives[person_1].gender + dict_relatives[person_2].gender]
                    print(dict_relatives[person_1])
                    print(dict_relatives[person_2])
                    print(tie)
                    return f'Common asncestor  \n{dict_relatives[value]} \n Related communication is founded' 
                    # {communications[tie[3]][str(key_1) + str(key_2)]}               
    return print('Don\'t have ties')


if __name__  == '__main__':

    dict_relatives = read_person()
    w ='yes'
    while w != 'n':

        # print(dict_relatives)
        # print(create_ties('55'))
    
        # print(dict_relatives['7'])
        # print(dict_relatives['16'].print_full_info())
        # find_name('Gordon')
        # print(compare_persons('108','42'))
        person_1 = input('Person №1:')
        person_2 = input('Person №2:')
        print(compare_persons(person_1, person_2))
        w = input('Again?:')
