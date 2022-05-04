import requests



response = requests.get('http://myfamilytree.live/dataOfPersons.js')
    # with open(FILE_PATH_PERSONS) as p:
        # reader_csv = csv.reader(p) 
reader_list = list(response.text)
# print(response.text)
reader_list = response.text.split('\n')
# print(response.text)
print(reader_list[13])