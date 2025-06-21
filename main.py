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