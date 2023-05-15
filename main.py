from xml.dom import minidom
import random
from sympy import *

def vytvor_typy_pr(priklady):

    typy_prikladu = {}

    for priklad in priklady:
        if priklad.getAttribute("id") not in typy_prikladu.keys():
            typy_prikladu[priklad.getAttribute("id")] = [priklad]
        else:
            typy_prikladu[priklad.getAttribute("id")].append(priklad)

    return typy_prikladu


def vytvor_seznam_pr(typy_pr, pozadovane_typy):     #TODO spatny format?

    seznam = []

    for typ in pozadovane_typy.keys():
        for _ in range (pozadovane_typy[typ]):
            seznam.append(random.choice(typy_pr[typ]))

    return seznam


def vytvor_komplet_priklad(priklad):        #TODO zlomky, floaty, -,  kontrola min max, jednicka, same priklad

    zadani = priklad.getElementsByTagName('zadani')[0].firstChild.data.strip()
    promenne = priklad.getElementsByTagName('promenna')

    for promenna in promenne:
        znacka = promenna.getElementsByTagName('znacka')[0].firstChild.data
        min = int(promenna.getElementsByTagName('min')[0].firstChild.data)
        max = int(promenna.getElementsByTagName('max')[0].firstChild.data)
        hodnota = random.randint(min, max)
        zadani = zadani.replace('{'+ znacka + '}', str(hodnota))
    
    return Priklad(zadani)


def vyres_priklad(priklad):     #TODO Nerovnosti a výrazy
    
    if ('=' in priklad) and ('<' not in priklad and '>' not in priklad):

        rovnitko = priklad.find('=')
        left_side = priklad[:rovnitko]
        left_side = left_side.replace('x', '*x')
        left_side = sympify(left_side)

        right_side = priklad[rovnitko + 1:]
        right_side = right_side.replace('x', '*x')
        right_side = sympify(right_side)

        reseni = solve(Eq(left_side, right_side))

        return reseni

    elif '<' in priklad or '>' in priklad:
        ...
    else:
        ...


class Database:         #TODO Špatná cesta, změna cesty?
    def __init__(self, path):

        self._document = minidom.parse(path)
        self._typy_prikladu = vytvor_typy_pr(self._document.getElementsByTagName('priklad'))

    @property
    def document(self):
        return self._document
    @document.setter
    def document(self, value):
        raise AttributeError("Nemůžete změnit hodnotu atributu.")
    
    @property
    def typy_prikladu(self):
        return self._typy_prikladu
    @typy_prikladu.setter
    def typy_prikladu(self, value):
        raise AttributeError("Nemůžete změnit hodnotu atributu.")
    

class Priklad:

    def __init__(self, priklad):
        self._priklad = priklad
        self._reseni = vyres_priklad(priklad)
        self._uspesnost = []
    
    @property
    def priklad(self):
        return self._priklad
    @priklad.setter
    def priklad(self, value):
        raise AttributeError("Nemůžete změnit hodnotu atributu.")
    
    @property
    def reseni(self):
        return self._reseni
    @reseni.setter
    def reseni(self, value):
        raise AttributeError("Nemůžete změnit hodnotu atributu.")
    
    @property
    def uspesnost(self):
        return sum(self._uspesnost)/len(self._uspesnost)
    @uspesnost.setter
    def uspesnost(self, value):
        self._uspesnost.append(value)

    
class Student:

    def __init__():
        ...


def main():         #TODO ofc dodelat a prehlednejsi?

    path = input('Adresa xml souboru: ')
    typy = input('Typy prikladů ve tvaru: typ - počet, typ - počet ')
    typy = dict((x.strip(), int(y.strip()))
             for x, y in (element.split('-')
             for element in typy.split(', ')))

    soubor = Database(path)

    seznam_pr = []
    for priklad in vytvor_seznam_pr(soubor.typy_prikladu, typy):

        seznam_pr.append(vytvor_komplet_priklad(priklad))

    for zadani in seznam_pr:

        print(zadani.priklad)
        odpoved = sympify(input('Výsledek?'))
        
        if odpoved == zadani.reseni[0]:
            print(f'GJ vysledek je {zadani.reseni[0]}')
            zadani.uspesnost = 1
        else:
            print(f'bad, reseni je {zadani.reseni[0]}')
            zadani.uspesnost = 0

    for zadani in seznam_pr:
        print(zadani.uspesnost)
    
    input('konec?')

if __name__ == "__main__":
    main()