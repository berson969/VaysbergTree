
import os
import datetime
from datetime import date
import requests


class Relative:
    def __init__(self, name, lastname, gender, date_birth, date_dead, codeDad, codeMam):
        self.name = name
        self.lastname = lastname
        self.gender = gender
        self.date_birth = date_birth
        self.date_dead = date_dead
        self.codeDad = codeDad
        self.codeMam = codeMam
    

    def __str__(self):
        return f'Name: {self.name} {self.lastname} \nDate of birth: {self.date_birth} \nDate of Dead {self.date_dead} \ncodeDad: {self.codeDad} \ncodeMam: {self.codeMam}'
    
def create_ties(id: str):
    ties_relatives = {0: [id]}
    current_level = 1
    _up = True
    while _up:
        level_relatives_list = []
        for id_relatives in ties_relatives[current_level-1]:
            if dict_relatives[id_relatives].codeDad != '':
                level_relatives_list.append(dict_relatives[id_relatives].codeDad)
            if dict_relatives[id_relatives].codeMam != '':
                level_relatives_list.append(dict_relatives[id_relatives].codeMam)
        if level_relatives_list == []:
            _up = False
        else:
            ties_relatives[current_level] = level_relatives_list
            current_level += 1
    _down = True
    current_level = -1
    while _down:        
        level_relatives_list = []
        for code_relatives in ties_relatives[current_level+1]:
            for id_relatives in dict_relatives.keys():
                if dict_relatives[id_relatives].codeDad == code_relatives or dict_relatives[id_relatives].codeMam == code_relatives:
                    level_relatives_list.append(id_relatives)
        if level_relatives_list == []:
            _down = False
        else:
            ties_relatives[current_level] = level_relatives_list
            current_level -= 1
    return ties_relatives

def clean_values(value,clear_string: str):
    new_value = value.lstrip(clear_string)
    if new_value == "":
        new_value = None
    new_value = new_value.strip('"')
    return new_value
        
def read_person():
    dict_relatives = {}
    response = requests.get('http://myfamilytree.live/dataOfPersons.js')
    reader_list = response.text.split('\r\n')
    reader_list.pop() #убирает последнюю строчку в файле
    for i in range(13, len(reader_list), 26):
        id_person = clean_values(reader_list[i],'var a=')
        name_person = clean_values(reader_list[i+2],'pers[a].first = ')
        lastname_person = clean_values(reader_list[i+3],'pers[a].last = ')
        gender_person = clean_values(reader_list[i+4],'pers[a].F_M = ')
        dob_person = clean_values(reader_list[i+5],'pers[a].dob = ')
        dobMM_person = clean_values(reader_list[i+6],'pers[a].dobMM = ')
        dobDD_person = clean_values(reader_list[i+7],'pers[a].dobDD = ')    
        dod_person = clean_values(reader_list[i+8],'pers[a].dod = ')
        dodMM_person = clean_values(reader_list[i+9],'pers[a].dodMM = ')
        dodDD_person = clean_values(reader_list[i+10],'pers[a].dodDD = ')  
        date_birth = 'Db'
        date_dead = 'Dd'
        codeDad_person = clean_values(reader_list[i+11],'pers[a].codeDad = ')
        codeMam_person = clean_values(reader_list[i+12],'pers[a].codeMam = ')
        data_person = Relative(name_person, lastname_person, gender_person, date_birth, date_dead, codeDad_person, codeMam_person)
        dict_relatives[id_person] = data_person
    return dict_relatives

def compare_persons(person_1: str, person_2: str):
    for key_1, value_1 in create_ties(person_1).items():
        for key_2, value_2 in create_ties(person_2).items(): 
            for value in value_2:
                if value in value_1:
                    tie = [key_1, key_2, value, dict_relatives[person_1].gender + dict_relatives[person_2].gender]
                    return tie        
    return 'Don\'t have ties'


if __name__  == '__main__':

    dict_relatives = read_person()
    w ='yes'
    while w != 'n':
        person_1 = input('Person №1:')
        person_2 = input('Person №2:')
        answer = compare_persons(person_1, person_2)
        if answer == 'Don\'t have ties':
            print(answer)
        else:
            url = f'http://myfamilytree.live/?{answer[2]}Ber{person_1}To{person_2}'
            print(url)
        w = input('Again?:')
