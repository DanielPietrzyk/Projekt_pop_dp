from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

# Listy przechowujące dane
urzedy = []
pracownicy = []
klienci = []

# Klasy dla danych
class Urzad:
    def __init__(self, nazwa: str, adres: str, miejscowosc: str):
        self.nazwa = nazwa
        self.adres = adres
        self.miejscowosc = miejscowosc
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=nazwa)

    def get_coordinates(self) -> list:
        try:
            url = f'https://pl.wikipedia.org/wiki/{self.miejscowosc}'
            response = requests.get(url).text
            response_html = BeautifulSoup(response, 'html.parser')
            longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
            latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
            return [latitude, longitude]
        except:
            return [52.23, 21.00]  # Domyślne współrzędne (Warszawa) w razie błędu

class Pracownik:
    def __init__(self, imie: str, nazwisko: str, urzad_nazwa: str, miejscowosc: str):
        self.imie = imie
        self.nazwisko = nazwisko
        self.urzad_nazwa = urzad_nazwa
        self.miejscowosc = miejscowosc
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"{imie} {nazwisko}")

    def get_coordinates(self) -> list:
        try:
            url = f'https://pl.wikipedia.org/wiki/{self.miejscowosc}'
            response = requests.get(url).text
            response_html = BeautifulSoup(response, 'html.parser')
            longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
            latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
            return [latitude, longitude]
        except:
            return [52.23, 21.00]

class Klient:
    def __init__(self, imie: str, nazwisko: str, urzad_nazwa: str, miejscowosc: str, data_wizyty: str):
        self.imie = imie
        self.nazwisko = nazwisko
        self.urzad_nazwa = urzad_nazwa
        self.miejscowosc = miejscowosc
        self.data_wizyty = data_wizyty
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"{imie} {nazwisko}")

    def get_coordinates(self) -> list:
        try:
            url = f'https://pl.wikipedia.org/wiki/{self.miejscowosc}'
            response = requests.get(url).text
            response_html = BeautifulSoup(response, 'html.parser')
            longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
            latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
            return [latitude, longitude]
        except:
            return [52.23, 21.00]

# GUI
root = Tk()
root.title('System Zarządzania Urzędami')
root.geometry('1000x800')

# Ramki
ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektow = Frame(root)
ramka_mapa = Frame(root)

ramka_lista_obiektow.grid(row=0, column=0, padx=50, sticky="n")
ramka_formularz.grid(row=0, column=1, sticky="n")
ramka_szczegoly_obiektow.grid(row=1, column=0, columnspan=2)
ramka_mapa.grid(row=2, column=0, columnspan=2)

# Ramka lista obiektów
label_lista_obiektow = Label(ramka_lista_obiektow, text='Lista obiektów')
label_lista_obiektow.grid(row=0, column=0, columnspan=3)

listbox_lista_obiektow = Listbox(ramka_lista_obiektow, width=50)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)

button_pokaz_szczegoly = Button(ramka_lista_obiektow, text='Pokaż szczegóły')
button_pokaz_szczegoly.grid(row=2, column=0)

button_usun_obiekt = Button(ramka_lista_obiektow, text='Usuń obiekt')
button_usun_obiekt.grid(row=2, column=1)

button_edytuj_obiekt = Button(ramka_lista_obiektow, text='Edytuj obiekt')
button_edytuj_obiekt.grid(row=2, column=2)

# Ramka formularz
label_formularz = Label(ramka_formularz, text='Formularz')
label_formularz.grid(row=0, column=0, columnspan=2)

# Formularz urzędów
label_nazwa_urzad = Label(ramka_formularz, text='Nazwa urzędu')
label_nazwa_urzad.grid(row=1, column=0, sticky=W)
entry_nazwa_urzad = Entry(ramka_formularz)
entry_nazwa_urzad.grid(row=1, column=1)

label_adres_urzad = Label(ramka_formularz, text='Adres')
label_adres_urzad.grid(row=2, column=0, sticky=W)
entry_adres_urzad = Entry(ramka_formularz)
entry_adres_urzad.grid(row=2, column=1)

label_miejscowosc_urzad = Label(ramka_formularz, text='Miejscowość')
label_miejscowosc_urzad.grid(row=3, column=0, sticky=W)
entry_miejscowosc_urzad = Entry(ramka_formularz)
entry_miejscowosc_urzad.grid(row=3, column=1)

button_dodaj_urzad = Button(ramka_formularz, text='Dodaj', command=dodaj_urzad)
button_dodaj_urzad.grid(row=4, column=0, columnspan=2)