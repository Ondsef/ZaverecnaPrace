from xml.dom import minidom
import random
from sympy import *
import pickle
import os


# z typů příkladů vyparsovaných ze xml souboru (typy_pr) vybere takové typy a takový počet, který zadá uživatel(požadovane_typy)
def vytvor_seznam_pr(typy_pr, pozadovane_typy):     #TODO spatny format?

    seznam = []

    for typ in pozadovane_typy.keys():
        for _ in range (pozadovane_typy[typ]):
            seznam.append(random.choice(typy_pr[typ]))

    return seznam


# v příkladu (priklad) nahradí proměnné náhodnými veličinami podle xml souboru, vratí vytvořený příklad (třídy Priklad)!!
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


# vrací známku podle úspěšnosti danného testu (uspesnost)
def vytvor_znamku(uspesnost):

    if uspesnost >= 0.8:
        return 1
    elif uspesnost >= 0.6:
        return 2
    elif uspesnost >= 0.4:
        return 3
    elif uspesnost >= 0.2:
        return 4
    else:
        return 5


# uloží známku (znamka), kterou dostal student (jmeno) do studentova souboru, pokud už má student záznam - "aktualizuje", jinak vytvoří nový soubor
def uloz_studenta(jmeno, znamka):

    znamka = int(znamka)
    soubor = f'studenti/{jmeno}.pkl'

    if os.path.exists(soubor):
        with open(soubor, 'rb') as file:
            student = pickle.load(file)

        student.pridat_znamku(znamka)
        student.ulozit()

        print(f"Známky pro uživatele {jmeno} byly aktualizovány.")

    else:
        student = Student(jmeno)
        student.pridat_znamku(znamka)
        student.ulozit()

        print(f"Uživatel {jmeno} byl vytvořen.")

    with open(soubor, 'rb') as file:
        student = pickle.load(file)
        print(student.znamky)


# třída Database, obsahuje vyparsované prvky z xml souboru
class Database:         #TODO Špatná cesta, změna cesty?
    def __init__(self, path):
        
        self._document = minidom.parse(path)

    @property
    def document(self):
        return self._document
    @document.setter
    def document(self, value):
        raise AttributeError("Nemůžete změnit hodnotu atributu.")
    
    # vrací slovník typů příkladů, které jsou v xml souboru
    def vytvor_typy_pr(self):

        typy_prikladu = {}

        for priklad in self._document.getElementsByTagName('priklad'):
            if priklad.getAttribute("id") not in typy_prikladu.keys():
                typy_prikladu[priklad.getAttribute("id")] = [priklad]
            else:
                typy_prikladu[priklad.getAttribute("id")].append(priklad)

        return typy_prikladu
    

# třída Priklad, obsahuje statistiku úspěšnosti jednotlivých příkladů v testu
class Priklad:

    def __init__(self, priklad):
        self._priklad = priklad
        self._uspesnost = []
    
    @property
    def priklad(self):
        return self._priklad
    @priklad.setter
    def priklad(self, value):
        raise AttributeError("Nemůžete změnit hodnotu atributu.")
    
    @property
    def uspesnost(self):
        return sum(self._uspesnost)/len(self._uspesnost)
    @uspesnost.setter
    def uspesnost(self, value):
        self._uspesnost.append(value)

    # vrací řešení příkladu
    def vyres_priklad(self):     #TODO Nerovnosti a výrazy

        if ('=' in self._priklad) and ('<' not in self._priklad and '>' not in self._priklad):

            rovnitko = self._priklad.find('=')
            left_side = self._priklad[:rovnitko]
            left_side = left_side.replace('x', '*x')
            left_side = sympify(left_side)

            right_side = self._priklad[rovnitko + 1:]
            right_side = right_side.replace('x', '*x')
            right_side = sympify(right_side)

            reseni = solve(Eq(left_side, right_side))

            return reseni

        elif '<' in self._priklad or '>' in self._priklad:
            ...
        else:
            ...


# třída Student, obsahuje jednotlivé známky, které daný žák získal
class Student:

    def __init__(self, jmeno):
        self._jmeno = jmeno
        self._znamky = []

    @property
    def jmeno(self):
        return self._jmeno
    @jmeno.setter
    def jmeno(self, value):
        raise AttributeError("Nemůžete změnit hodnotu atributu.")

    @property
    def znamky(self):
        return f'Tvoje znamky jsou: {self._znamky} a tvůj průměr je: {sum(self._znamky)/len(self._znamky)}.'
    @znamky.setter
    def trida(self, value):
        raise AttributeError("Nemůžete změnit hodnotu atributu.")
    
    def pridat_znamku(self, znamka):
        self._znamky.append(znamka)

    # ukládá studentovi známky do složky studenti
    def ulozit(self):
        soubor = f'studenti/{self._jmeno}.pkl'
        with open(soubor, 'wb') as file:
            pickle.dump(self, file)


def main():         #TODO ofc dodelat, ošetřit když bude blbý imput a prehlednejsi?

    # vstupy zadávající vyučující
    path = input('Adresa xml souboru: ')
    typy = input('Typy prikladů ve tvaru: typ - počet, typ - počet ')
    typy = dict((x.strip(), int(y.strip()))
             for x, y in (element.split('-')
             for element in typy.split(', ')))
    pocet_studentu = int(input('Kolik studentů bude psát test?'))

    soubor = Database(path)

    # vytvori seznam přepsaných příkladů podle požadovaného typu (třídy Priklad)
    seznam_pr = []
    for priklad in vytvor_seznam_pr(soubor.vytvor_typy_pr(), typy):

        seznam_pr.append(vytvor_komplet_priklad(priklad))


    # zadaní jednotlivých studentů
    for _ in range(pocet_studentu):

        jmeno = input('Zadej jmeno: ')
        znamka_poc = 0

        for zadani in seznam_pr:

            print(zadani.priklad)
            odpoved = sympify(input('Výsledek?'))
            
            if odpoved == zadani.vyres_priklad()[0]:
                print(f'GJ vysledek je {zadani.vyres_priklad()[0]}')
                zadani.uspesnost = 1
                znamka_poc += 1
            else:
                print(f'bad, reseni je {zadani.vyres_priklad()[0]}')
                zadani.uspesnost = 0

        znamka = vytvor_znamku(znamka_poc/len(seznam_pr))

        print(f'Tvoje známka je: {znamka}')

        uloz_studenta(jmeno, znamka)


    for zadani in seznam_pr:
        print(f'Zadani: {zadani.priklad} ma uspesnot: {zadani.uspesnost}')
    
    input('konec?')

if __name__ == "__main__":
    main()