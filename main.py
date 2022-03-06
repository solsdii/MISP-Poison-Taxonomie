# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from pprint import pprint

import wikipedia
import wikipediaapi
import requests
from bs4 import BeautifulSoup
import json


class Predicate:
    def __init__(self, value, expanded):
        self.value = value
        self.expanded = expanded

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=10)


class Values:
    def __init__(self, value, expanded):
        self.value = value
        self.expanded = expanded

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=20)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    response = requests.get(
        url="https://en.wikipedia.org/wiki/List_of_poisonous_plants"
    )
    soup = BeautifulSoup(response.content, 'html.parser')
    responsefungus = requests.get(
        url="https://en.wikipedia.org/wiki/List_of_poisonous_fungus_species"
    )
    soupfungus = BeautifulSoup(responsefungus.content, 'html.parser')

    stop = False
    table = soup.find('table')
    TabValues = []
    TabValuesFungus = []
    td = table.find('td')
    nb = 0
    PoisonousPlant: Predicate = Predicate("Poisonous plant", "")
    PoisonousFungus: Predicate = Predicate("Poisonous fungus", "")
    TabPredicate = [PoisonousPlant, PoisonousFungus]
    while not stop:
        a = td.find('a')
        if a is None:
            stop = True
        else:
            href = a.find('href')
            # print(a.attrs.get('href'))
             #td = td.find_next('td')
            nomScientifique = a.contents
            td = td.find_next('td')
            nomCommun = td.find('a')
            #print(aa.pop()+a.contents.pop())
            if nomCommun is None:
                nomCommun2 = td.find('b')
                if nomCommun2 is not None:
                    content = Values(nomScientifique.pop() + "/" + nomCommun2.contents.pop(), "")
                else:
                    content = Values(nomScientifique.pop(), "")
            else:
                content = Values(nomScientifique.pop() + "/" + nomCommun.contents.pop(), "")
            TabValues.append(content)
            for i in [1, 2, 3]:
                td = td.find_next('td')
            nb = nb + 1
    stop = False
    table = soupfungus.find('table')
    # print(table)
    print("---------------------------------------------------------------------------")
    td = table.find('td')
    nb = 0
    while not stop:
        a = td.find('a')
        if a is None:
            stop = True
        else:
            href = a.find('href')
            if a.contents == ['Turbinellus kauffmanii']:
                stop = True
            nomScientifique = a.contents
            td = td.find_next('td')
            nomCommum = td.contents
            if nomCommum == ['\n'] or nomCommum is None:
                content = Values(nomScientifique.pop(), "")
            else:
                test = nomCommum.pop(0)
                content = Values(nomScientifique.pop() + "/" + test.__str__().replace("\n",""), "")
            # Values: content = a.contents
            TabValuesFungus.append(content)
            for i in [1, 2, 3, 4, 5]:
                td = td.find_next('td')
            nb = nb + 1

    stop = False

    while not stop:
        a = td.find('a')
        if a is None:
            stop = True
        else:
            href = a.find('href')
            nomScientifique = a.contents
            td = td.find_next('td')
            nomCommum = td.contents
            if nomCommum == ['\n'] or nomCommum is None:
                content = Values(nomScientifique.pop(), "")
            else:
                test = nomCommum.pop(0)
                content = Values(nomScientifique.pop() + "/" + test.__str__().replace("\n", ""), "")
            # Values: content = a.contents
            TabValuesFungus.append(content)
            for i in [1, 2, 3]:
                td = td.find_next('td')
            nb = nb + 1
            if td is None:
                stop = True

    # print(TabValues[0].value)
    finalJSON = "{\n" \
                '   "namespace":"poison Taxonomy",\n' \
                '   "description":"Some descriptive words",\n' \
                '   "version": 1,\n' \
                '   "predicates": [\n'
    # finalJSON = finalJSON + "       " + PoisonousPlant.toJSON()
    finalJSON = finalJSON + TabPredicate[0].toJSON() + "," + TabPredicate[1].toJSON()
    finalJSON = finalJSON + "],"
    finalJSON = finalJSON + '"values" : [' \
                            '{\n' \
                            '"predicate":' + ' "' + TabPredicate[0].value + '",\n'
    finalJSON = finalJSON + '"entry": ['
    for i in TabValues[:-1]:
        finalJSON = finalJSON + i.toJSON() + ","
    finalJSON = finalJSON + TabValues[-1].toJSON()
    finalJSON = finalJSON + "],"
    finalJSON = finalJSON + '"predicate1":' + ' "' + TabPredicate[1].value + '",\n'
    finalJSON = finalJSON + '"entry1": ['
    for i in TabValuesFungus[:-1]:
        finalJSON = finalJSON + i.toJSON() + ","
    finalJSON = finalJSON + TabValuesFungus[-1].toJSON()
    finalJSON = finalJSON + "]}]}"

    t = (json.loads(finalJSON))

    tt = json.dumps(t, sort_keys=False, indent=4)
    with open("Misp.json", "w") as file:
        file.write(tt)

    # print(json.dumps(TabValues))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
