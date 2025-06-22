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

# Funkcje dla urzędów
def dodaj_urzad():
    nazwa = entry_nazwa_urzad.get()
    adres = entry_adres_urzad.get()
    miejscowosc = entry_miejscowosc_urzad.get()
    if nazwa and adres and miejscowosc:
        urzedy.append(Urzad(nazwa=nazwa, adres=adres, miejscowosc=miejscowosc))
        pokaz_urzedy()
        entry_nazwa_urzad.delete(0, END)
        entry_adres_urzad.delete(0, END)
        entry_miejscowosc_urzad.delete(0, END)
        entry_nazwa_urzad.focus()
    else:
        label_status.config(text="Wypełnij wszystkie pola!")

def pokaz_urzedy():
    listbox_lista_obiektow.delete(0, END)
    for idx, urzad in enumerate(urzedy):
        listbox_lista_obiektow.insert(idx, f"{idx+1} {urzad.nazwa} {urzad.adres} {urzad.miejscowosc}")

def usun_urzad():
    i = listbox_lista_obiektow.index(ACTIVE)
    urzedy[i].marker.delete()
    urzedy.pop(i)
    pokaz_urzedy()
    label_status.config(text="Urząd usunięty!")

def edytuj_urzad():
    i = listbox_lista_obiektow.index(ACTIVE)
    entry_nazwa_urzad.insert(0, urzedy[i].nazwa)
    entry_adres_urzad.insert(0, urzedy[i].adres)
    entry_miejscowosc_urzad.insert(0, urzedy[i].miejscowosc)
    button_dodaj_urzad.config(text='Zapisz', command=lambda: zapisz_urzad(i))

def zapisz_urzad(i):
    nazwa = entry_nazwa_urzad.get()
    adres = entry_adres_urzad.get()
    miejscowosc = entry_miejscowosc_urzad.get()
    if nazwa and adres and miejscowosc:
        urzedy[i].nazwa = nazwa
        urzedy[i].adres = adres
        urzedy[i].miejscowosc = miejscowosc
        urzedy[i].coordinates = urzedy[i].get_coordinates()
        urzedy[i].marker.delete()
        urzedy[i].marker = map_widget.set_marker(urzedy[i].coordinates[0], urzedy[i].coordinates[1], text=nazwa)
        pokaz_urzedy()
        button_dodaj_urzad.config(text='Dodaj', command=dodaj_urzad)
        entry_nazwa_urzad.delete(0, END)
        entry_adres_urzad.delete(0, END)
        entry_miejscowosc_urzad.delete(0, END)
        entry_nazwa_urzad.focus()
        label_status.config(text="Urząd zaktualizowany!")
    else:
        label_status.config(text="Wypełnij wszystkie pola!")

def pokaz_szczegoly_urzad():
    i = listbox_lista_obiektow.index(ACTIVE)
    label_nazwisko_szczegoly_wartosc.config(text=urzedy[i].nazwa)
    label_imie_szczegoly_wartosc.config(text=urzedy[i].adres)
    label_miejscowosc_szczegoly_wartosc.config(text=urzedy[i].miejscowosc)
    map_widget.set_zoom(12)
    map_widget.set_position(urzedy[i].coordinates[0], urzedy[i].coordinates[1])

# Funkcje dla pracowników
def dodaj_pracownika():
    imie = entry_imie_pracownik.get()
    nazwisko = entry_nazwisko_pracownik.get()
    urzad_nazwa = entry_urzad_pracownik.get()
    miejscowosc = entry_miejscowosc_pracownik.get()
    if imie and nazwisko and urzad_nazwa and miejscowosc and urzad_nazwa in [u.nazwa for u in urzedy]:
        pracownicy.append(Pracownik(imie=imie, nazwisko=nazwisko, urzad_nazwa=urzad_nazwa, miejscowosc=miejscowosc))
        pokaz_pracownikow()
        entry_imie_pracownik.delete(0, END)
        entry_nazwisko_pracownik.delete(0, END)
        entry_urzad_pracownik.delete(0, END)
        entry_miejscowosc_pracownik.delete(0, END)
        entry_imie_pracownik.focus()
    else:
        label_status.config(text="Wypełnij wszystkie pola i wybierz istniejący urząd!")

def pokaz_pracownikow():
    listbox_lista_obiektow.delete(0, END)
    for idx, pracownik in enumerate(pracownicy):
        listbox_lista_obiektow.insert(idx, f"{idx+1} {pracownik.imie} {pracownik.nazwisko} {pracownik.urzad_nazwa} {pracownik.miejscowosc}")

def usun_pracownika():
    i = listbox_lista_obiektow.index(ACTIVE)
    pracownicy[i].marker.delete()
    pracownicy.pop(i)
    pokaz_pracownikow()
    label_status.config(text="Pracownik usunięty!")

def edytuj_pracownika():
    i = listbox_lista_obiektow.index(ACTIVE)
    entry_imie_pracownik.insert(0, pracownicy[i].imie)
    entry_nazwisko_pracownik.insert(0, pracownicy[i].nazwisko)
    entry_urzad_pracownik.insert(0, pracownicy[i].urzad_nazwa)
    entry_miejscowosc_pracownik.insert(0, pracownicy[i].miejscowosc)
    button_dodaj_pracownik.config(text='Zapisz', command=lambda: zapisz_pracownika(i))

def zapisz_pracownika(i):
    imie = entry_imie_pracownik.get()
    nazwisko = entry_nazwisko_pracownik.get()
    urzad_nazwa = entry_urzad_pracownik.get()
    miejscowosc = entry_miejscowosc_pracownik.get()
    if imie and nazwisko and urzad_nazwa and miejscowosc and urzad_nazwa in [u.nazwa for u in urzedy]:
        pracownicy[i].imie = imie
        pracownicy[i].nazwisko = nazwisko
        pracownicy[i].urzad_nazwa = urzad_nazwa
        pracownicy[i].miejscowosc = miejscowosc
        pracownicy[i].coordinates = pracownicy[i].get_coordinates()
        pracownicy[i].marker.delete()
        pracownicy[i].marker = map_widget.set_marker(pracownicy[i].coordinates[0], pracownicy[i].coordinates[1], text=f"{imie} {nazwisko}")
        pokaz_pracownikow()
        button_dodaj_pracownik.config(text='Dodaj', command=dodaj_pracownika)
        entry_imie_pracownik.delete(0, END)
        entry_nazwisko_pracownik.delete(0, END)
        entry_urzad_pracownik.delete(0, END)
        entry_miejscowosc_pracownik.delete(0, END)
        entry_imie_pracownik.focus()
        label_status.config(text="Pracownik zaktualizowany!")
    else:
        label_status.config(text="Wypełnij wszystkie pola i wybierz istniejący urząd!")

def pokaz_szczegoly_pracownika():
    i = listbox_lista_obiektow.index(ACTIVE)
    label_imie_szczegoly_wartosc.config(text=pracownicy[i].imie)
    label_nazwisko_szczegoly_wartosc.config(text=pracownicy[i].nazwisko)
    label_urzad_szczegoly_wartosc.config(text=pracownicy[i].urzad_nazwa)
    label_miejscowosc_szczegoly_wartosc.config(text=pracownicy[i].miejscowosc)
    map_widget.set_zoom(12)
    map_widget.set_position(pracownicy[i].coordinates[0], pracownicy[i].coordinates[1])

# Funkcje dla klientów
def dodaj_klienta():
    imie = entry_imie_klient.get()
    nazwisko = entry_nazwisko_klient.get()
    urzad_nazwa = entry_urzad_klient.get()
    miejscowosc = entry_miejscowosc_klient.get()
    data_wizyty = entry_data_klient.get()
    if imie and nazwisko and urzad_nazwa and miejscowosc and data_wizyty and urzad_nazwa in [u.nazwa for u in urzedy]:
        try:
            from datetime import datetime
            datetime.strptime(data_wizyty, "%Y-%m-%d")
            klienci.append(Klient(imie=imie, nazwisko=nazwisko, urzad_nazwa=urzad_nazwa, miejscowosc=miejscowosc, data_wizyty=data_wizyty))
            pokaz_klientow()
            entry_imie_klient.delete(0, END)
            entry_nazwisko_klient.delete(0, END)
            entry_urzad_klient.delete(0, END)
            entry_miejscowosc_klient.delete(0, END)
            entry_data_klient.delete(0, END)
            entry_imie_klient.focus()
        except ValueError:
            label_status.config(text="Niepoprawny format daty! Użyj RRRR-MM-DD")
    else:
        label_status.config(text="Wypełnij wszystkie pola i wybierz istniejący urząd!")

def pokaz_klientow():
    listbox_lista_obiektow.delete(0, END)
    for idx, klient in enumerate(klienci):
        listbox_lista_obiektow.insert(idx, f"{idx+1} {klient.imie} {klient.nazwisko} {klient.urzad_nazwa} {klient.miejscowosc} {klient.data_wizyty}")

def usun_klienta():
    i = listbox_lista_obiektow.index(ACTIVE)
    klienci[i].marker.delete()
    klienci.pop(i)
    pokaz_klientow()
    label_status.config(text="Klient usunięty!")

def edytuj_klienta():
    i = listbox_lista_obiektow.index(ACTIVE)
    entry_imie_klient.insert(0, klienci[i].imie)
    entry_nazwisko_klient.insert(0, klienci[i].nazwisko)
    entry_urzad_klient.insert(0, klienci[i].urzad_nazwa)
    entry_miejscowosc_klient.insert(0, klienci[i].miejscowosc)
    entry_data_klient.insert(0, klienci[i].data_wizyty)
    button_dodaj_klient.config(text='Zapisz', command=lambda: zapisz_klienta(i))

def zapisz_klienta(i):
    imie = entry_imie_klient.get()
    nazwisko = entry_nazwisko_klient.get()
    urzad_nazwa = entry_urzad_klient.get()
    miejscowosc = entry_miejscowosc_klient.get()
    data_wizyty = entry_data_klient.get()
    if imie and nazwisko and urzad_nazwa and miejscowosc and data_wizyty and urzad_nazwa in [u.nazwa for u in urzedy]:
        try:
            from datetime import datetime
            datetime.strptime(data_wizyty, "%Y-%m-%d")
            klienci[i].imie = imie
            klienci[i].nazwisko = nazwisko
            klienci[i].urzad_nazwa = urzad_nazwa
            klienci[i].miejscowosc = miejscowosc
            klienci[i].data_wizyty = data_wizyty
            klienci[i].coordinates = klienci[i].get_coordinates()
            klienci[i].marker.delete()
            klienci[i].marker = map_widget.set_marker(klienci[i].coordinates[0], klienci[i].coordinates[1], text=f"{imie} {nazwisko}")
            pokaz_klientow()
            button_dodaj_klient.config(text='Dodaj', command=dodaj_klienta)
            entry_imie_klient.delete(0, END)
            entry_nazwisko_klient.delete(0, END)
            entry_urzad_klient.delete(0, END)
            entry_miejscowosc_klient.delete(0, END)
            entry_data_klient.delete(0, END)
            entry_imie_klient.focus()
            label_status.config(text="Klient zaktualizowany!")
        except ValueError:
            label_status.config(text="Niepoprawny format daty! Użyj RRRR-MM-DD")
    else:
        label_status.config(text="Wypełnij wszystkie pola i wybierz istniejący urząd!")

def pokaz_szczegoly_klienta():
    i = listbox_lista_obiektow.index(ACTIVE)
    label_imie_szczegoly_wartosc.config(text=klienci[i].imie)
    label_nazwisko_szczegoly_wartosc.config(text=klienci[i].nazwisko)
    label_urzad_szczegoly_wartosc.config(text=klienci[i].urzad_nazwa)
    label_miejscowosc_szczegoly_wartosc.config(text=klienci[i].miejscowosc)
    label_data_szegoly_wartosc.config(text=klienci[i].data_wizyty)
    map_widget.set_zoom(12)
    map_widget.set_position(klienci[i].coordinates[0], klienci[i].coordinates[1])

# Funkcje dla map
def pokaz_mape_urzedow():
    for u in urzedy:
        u.marker = map_widget.set_marker(u.coordinates[0], u.coordinates[1], text=u.nazwa)
    for p in pracownicy:
        p.marker.delete()
    for k in klienci:
        k.marker.delete()
    if urzedy:
        map_widget.set_position(urzedy[0].coordinates[0], urzedy[0].coordinates[1])
        map_widget.set_zoom(6)
    label_status.config(text="Wyświetlono mapę urzędów")

def pokaz_mape_pracownikow():
    for u in urzedy:
        u.marker.delete()
    for p in pracownicy:
        p.marker = map_widget.set_marker(p.coordinates[0], p.coordinates[1], text=f"{p.imie} {p.nazwisko}")
    for k in klienci:
        k.marker.delete()
    if pracownicy:
        map_widget.set_position(pracownicy[0].coordinates[0], pracownicy[0].coordinates[1])
        map_widget.set_zoom(6)
    label_status.config(text="Wyświetlono mapę pracowników")

def pokaz_mape_klientow_urzedu():
    urzad_nazwa = entry_urzad_mapa.get()
    if urzad_nazwa not in [u.nazwa for u in urzedy]:
        label_status.config(text="Wybierz istniejący urząd!")
        return
    for u in urzedy:
        u.marker.delete()
    for p in pracownicy:
        p.marker.delete()
    for k in klienci:
        if k.urzad_nazwa == urzad_nazwa:
            k.marker = map_widget.set_marker(k.coordinates[0], k.coordinates[1], text=f"{k.imie} {k.nazwisko}")
        else:
            k.marker.delete()
    for u in urzedy:
        if u.nazwa == urzad_nazwa:
            map_widget.set_position(u.coordinates[0], u.coordinates[1])
            map_widget.set_zoom(12)
            break
    label_status.config(text=f"Wyświetlono mapę klientów urzędu {urzad_nazwa}")

def pokaz_mape_pracownikow_urzedu():
    urzad_nazwa = entry_urzad_mapa.get()
    if urzad_nazwa not in [u.nazwa for u in urzedy]:
        label_status.config(text="Wybierz istniejący urząd!")
        return
    for u in urzedy:
        u.marker.delete()
    for k in klienci:
        k.marker.delete()
    for p in pracownicy:
        if p.urzad_nazwa == urzad_nazwa:
            p.marker = map_widget.set_marker(p.coordinates[0], p.coordinates[1], text=f"{p.imie} {p.nazwisko}")
        else:
            p.marker.delete()
    for u in urzedy:
        if u.nazwa == urzad_nazwa:
            map_widget.set_position(u.coordinates[0], u.coordinates[1])
            map_widget.set_zoom(12)
            break
    label_status.config(text=f"Wyświetlono mapę pracowników urzędu {urzad_nazwa}")

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

# Formularz pracowników
label_imie_pracownik = Label(ramka_formularz, text='Imię pracownika')
label_imie_pracownik.grid(row=5, column=0, sticky=W)
entry_imie_pracownik = Entry(ramka_formularz)
entry_imie_pracownik.grid(row=5, column=1)

label_nazwisko_pracownik = Label(ramka_formularz, text='Nazwisko')
label_nazwisko_pracownik.grid(row=6, column=0, sticky=W)
entry_nazwisko_pracownik = Entry(ramka_formularz)
entry_nazwisko_pracownik.grid(row=6, column=1)

label_urzad_pracownik = Label(ramka_formularz, text='Urząd')
label_urzad_pracownik.grid(row=7, column=0, sticky=W)
entry_urzad_pracownik = Entry(ramka_formularz)
entry_urzad_pracownik.grid(row=7, column=1)

label_miejscowosc_pracownik = Label(ramka_formularz, text='Miejscowość')
label_miejscowosc_pracownik.grid(row=8, column=0, sticky=W)
entry_miejscowosc_pracownik = Entry(ramka_formularz)
entry_miejscowosc_pracownik.grid(row=8, column=1)

button_dodaj_pracownik = Button(ramka_formularz, text='Dodaj', command=dodaj_pracownika)
button_dodaj_pracownik.grid(row=9, column=0, columnspan=2)

# Formularz klientów
label_imie_klient = Label(ramka_formularz, text='Imię klienta')
label_imie_klient.grid(row=10, column=0, sticky=W)
entry_imie_klient = Entry(ramka_formularz)
entry_imie_klient.grid(row=10, column=1)

label_nazwisko_klient = Label(ramka_formularz, text='Nazwisko')
label_nazwisko_klient.grid(row=11, column=0, sticky=W)
entry_nazwisko_klient = Entry(ramka_formularz)
entry_nazwisko_klient.grid(row=11, column=1)

label_urzad_klient = Label(ramka_formularz, text='Urząd')
label_urzad_klient.grid(row=12, column=0, sticky=W)
entry_urzad_klient = Entry(ramka_formularz)
entry_urzad_klient.grid(row=12, column=1)

label_miejscowosc_klient = Label(ramka_formularz, text='Miejscowość')
label_miejscowosc_klient.grid(row=13, column=0, sticky=W)
entry_miejscowosc_klient = Entry(ramka_formularz)
entry_miejscowosc_klient.grid(row=13, column=1)

label_data_klient = Label(ramka_formularz, text='Data wizyty (RRRR-MM-DD)')
label_data_klient.grid(row=14, column=0, sticky=W)
entry_data_klient = Entry(ramka_formularz)
entry_data_klient.grid(row=14, column=1)

button_dodaj_klient = Button(ramka_formularz, text='Dodaj', command=dodaj_klienta)
button_dodaj_klient.grid(row=15, column=0, columnspan=2)

# Formularz mapy
label_urzad_mapa = Label(ramka_formularz, text='Urząd dla mapy')
label_urzad_mapa.grid(row=16, column=0, sticky=W)
entry_urzad_mapa = Entry(ramka_formularz)
entry_urzad_mapa.grid(row=16, column=1)

button_mapa_urzedow = Button(ramka_formularz, text='Mapa urzędów', command=pokaz_mape_urzedow)
button_mapa_urzedow.grid(row=17, column=0)

button_mapa_pracownikow = Button(ramka_formularz, text='Mapa pracowników', command=pokaz_mape_pracownikow)
button_mapa_pracownikow.grid(row=17, column=1)

button_mapa_klientow_urzedu = Button(ramka_formularz, text='Mapa klientów urzędu', command=pokaz_mape_klientow_urzedu)
button_mapa_klientow_urzedu.grid(row=18, column=0)

button_mapa_pracownikow_urzedu = Button(ramka_formularz, text='Mapa pracowników urzędu', command=pokaz_mape_pracownikow_urzedu)
button_mapa_pracownikow_urzedu.grid(row=18, column=1)

# Ramka szczegóły obiektu
label_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text='Szczegóły obiektu:')
label_szczegoly_obiektu.grid(row=0, column=0)

label_imie_szczegoly = Label(ramka_szczegoly_obiektow, text='Nazwa/Imię:')
label_imie_szczegoly.grid(row=1, column=0)
label_imie_szczegoly_wartosc = Label(ramka_szczegoly_obiektow, text='.....')
label_imie_szczegoly_wartosc.grid(row=1, column=1)

label_nazwisko_szczegoly = Label(ramka_szczegoly_obiektow, text='Adres/Nazwisko:')
label_nazwisko_szczegoly.grid(row=1, column=2)
label_nazwisko_szczegoly_wartosc = Label(ramka_szczegoly_obiektow, text='.....')
label_nazwisko_szczegoly_wartosc.grid(row=1, column=3)

label_urzad_szczegoly = Label(ramka_szczegoly_obiektow, text='Urząd:')
label_urzad_szczegoly.grid(row=1, column=4)
label_urzad_szczegoly_wartosc = Label(ramka_szczegoly_obiektow, text='.....')
label_urzad_szczegoly_wartosc.grid(row=1, column=5)

label_miejscowosc_szczegoly = Label(ramka_szczegoly_obiektow, text='Miejscowość:')
label_miejscowosc_szczegoly.grid(row=1, column=6)
label_miejscowosc_szczegoly_wartosc = Label(ramka_szczegoly_obiektow, text='.....')
label_miejscowosc_szczegoly_wartosc.grid(row=1, column=7)

label_data_szczegoly = Label(ramka_szczegoly_obiektow, text='Data wizyty:')
label_data_szczegoly.grid(row=1, column=8)
label_data_szegoly_wartosc = Label(ramka_szczegoly_obiektow, text='.....')
label_data_szegoly_wartosc.grid(row=1, column=9)

label_status = Label(ramka_szczegoly_obiektow, text='')
label_status.grid(row=2, column=0, columnspan=10)

# Ramka mapa
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=800, height=600)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.set_position(52.23, 21.00)
map_widget.set_zoom(6)

# Dynamiczne przypisanie akcji w zależności od trybu
def ustaw_tryb(tryb):
    global pokaz_szczegoly, usun_obiekt, edytuj_obiekt
    listbox_lista_obiektow.delete(0, END)
    if tryb == 'urzedy':
        pokaz_urzedy()
        pokaz_szczegoly = pokaz_szczegoly_urzad
        usun_obiekt = usun_urzad
        edytuj_obiekt = edytuj_urzad
    elif tryb == 'pracownicy':
        pokaz_pracownikow()
        pokaz_szczegoly = pokaz_szczegoly_pracownika
        usun_obiekt = usun_pracownika
        edytuj_obiekt = edytuj_pracownika
    elif tryb == 'klienci':
        pokaz_klientow()
        pokaz_szczegoly = pokaz_szczegoly_klienta
        usun_obiekt = usun_klienta
        edytuj_obiekt = edytuj_klienta
    button_pokaz_szczegoly.config(command=pokaz_szczegoly)
    button_usun_obiekt.config(command=usun_obiekt)
    button_edytuj_obiekt.config(command=edytuj_obiekt)

# Przyciski wyboru trybu
button_tryb_urzedy = Button(ramka_lista_obiektow, text='Urzędy', command=lambda: ustaw_tryb('urzedy'))
button_tryb_urzedy.grid(row=3, column=0)

button_tryb_pracownicy = Button(ramka_lista_obiektow, text='Pracownicy', command=lambda: ustaw_tryb('pracownicy'))
button_tryb_pracownicy.grid(row=3, column=1)

button_tryb_klienci = Button(ramka_lista_obiektow, text='Klienci', command=lambda: ustaw_tryb('klienci'))
button_tryb_klienci.grid(row=3, column=2)

# Ustaw domyślny tryb
ustaw_tryb('urzedy')

root.mainloop()