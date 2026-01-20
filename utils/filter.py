import re

# Lista słów, które oznaczają, że przedmiot jest "śmieciem" (akcesorium, uszkodzony itp.)
# Jeśli tytuł zawiera któreś z tych słów, oferta zostanie odrzucona automatycznie.
GLOBALNA_CZARNA_LISTA = [
    "etui", "case", "pokrowiec", "futerał", "obudowa", "plecki", "tył", "klapka", "husa", # Husa to etui po rumuńsku (częste na Vinted)
    "szkło", "folia", "szkiełko", "ochronne", "hydrożel", "hydrogel",
    "pudełko", "karton", "box", "opakowanie", "pusty", "puste",
    "uszkodzony", "uszkodzone", "niesprawny", "zepsuty", "złom", "części", "na części", "dawco",
    "zamiennik", "atrapa", "zdjęcie", "foto", 
    "pasek", "bransoleta", "ładowarka", "kabel", "zasilacz", "adapter", "przejściówka",
    # Gry i akcesoria, których nie chcemy widzieć szukając konsoli
    "gra", "gry", "game", "games", "giera",
    "pad", "kontroler", "controller", "dualsense", "dualshock", "joycon",
    "słuchawki", "headset",
    "kierownica", "wheel",
    "podstawka", "stojak", "stand", "dock",
    "skin", "naklejka", "okleina",
    "konto", "dostęp", # Konta z grami
    "bateria", "battery", "akumulator",
    "dysk", "ssd", "hdd", "napęd",
    "klawiatura", "keyboard", "mysz", "myszka", "mouse",
    "matryca", "ekran", "screen", "wyświetlacz",
    "ściereczka", "szmatka", "czyścik", "płyn",
    "osłona", "zaślepka"
]

def parsuj_fraze(fraza):
    """
    Rozdziela frazę wpisaną przez użytkownika na słowa kluczowe i wykluczenia (z minusem).
    Np. "iphone -etui -uszkodzony" -> ("iphone", ["etui", "uszkodzony"])
    """
    if not fraza:
        return "", []
        
    slowa = fraza.split()
    czyste_slowa = []
    wykluczenia = []
    
    for s in slowa:
        if s.startswith("-") and len(s) > 1:
            wykluczenia.append(s[1:].lower())
        else:
            czyste_slowa.append(s)
            
    czysta_fraza = " ".join(czyste_slowa)
    return czysta_fraza, wykluczenia

from thefuzz import fuzz

def czysc_tytul_z_parametrow(tytul):
    """
    Usuwa z tytułu parametry techniczne, które mogą mylić wyszukiwanie modelu.
    Np. "Sony Xperia 16 GB" -> "Sony Xperia" (żeby 16 GB nie pasowało do Iphone 16)
    """
    tytul_lower = tytul.lower()
    # Usuwamy frazy typu: 16gb, 16 gb, 128mah, 12v itp.
    # \d+ - cyfry, \s? - opcjonalna spacja, (gb|tb|...) - jednostki
    oczyszczony = re.sub(r'\b\d+\s?(gb|tb|mb|mah|v|ah|w)\b', '', tytul_lower)
    # Usuwamy wielokrotne spacje
    oczyszczony = re.sub(r'\s+', ' ', oczyszczony).strip()
    return oczyszczony

def czy_slowa_kluczowe_sa_w_tytule(tytul, fraza_szukania):
    """
    Ulepszona weryfikacja:
    1. Czyści tytuł z parametrów (gb, v, mah)
    2. Sprawdza obecność słów kluczowych
    3. (Opcjonalnie) Używa Fuzzy Matching dla literówek
    """
    if not fraza_szukania:
        return True
        
    tytul_czysty = czysc_tytul_z_parametrow(tytul)
    
    # Rozbijamy frazę na słowa, ignorując minusy (są obsłużone osobno)
    slowa = [s.lower() for s in fraza_szukania.split() if not s.startswith("-")]
    
    # KROK 1: Klasyczne sprawdzanie słów (ale na oczyszczonym tytule)
    wszystkie_znalezione = True
    for slowo in slowa:
        # Ignorujemy bardzo krótkie łączniki, chyba że to cyfra/model (np. "s8", "16")
        if len(slowo) < 2 and not any(c.isdigit() for c in slowo):
            continue
            
        # Regex boundary \b nie zawsze działa dobrze z fuzzy logic, ale dla ścisłości zostawiamy w pre-filterze
        # Używamy oczyszczonego tytułu!
        pattern = r'\b' + re.escape(slowo) + r'\b'
        if not re.search(pattern, tytul_czysty):
            wszystkie_znalezione = False
            break
            
    if wszystkie_znalezione:
        return True
        
    # KROK 2: Fuzzy Matching (Ratunek dla literówek)
    # WAŻNA POPRAWKA: Fuzzy Matching nie może "zgadywać" liczb.
    # Jeśli szukamy "iPhone 16", to musi być "16". Nie "6", nie "15".
    
    # Wyciągamy liczby z frazy wyszukiwania
    liczby_w_szukanym = re.findall(r'\d+', fraza_szukania)
    if liczby_w_szukanym:
        # Sprawdzamy czy każda liczba z zapytania występuje w oczyszczonym tytule
        # (jako osobne słowo lub część słowa, ale musi być)
        for liczba in liczby_w_szukanym:
            if liczba not in tytul_czysty:
                return False

    # Jeśli liczby się zgadzają (lub ich nie ma), sprawdzamy resztę tekstu metodą Fuzzy
    fraza_czysta = " ".join([s for s in slowa])
    ratio = fuzz.partial_ratio(fraza_czysta, tytul_czysty)
    
    # WAŻNE USPRAWNIENIE: Krótkie słowa kluczowe (jak "Air", "Pro", "Mini", "Max") muszą być dopasowane BARDZO ściśle.
    # Fuzzy match 85% dla słowa "Air" może łapać śmieci.
    
    # Sprawdzamy czy kluczowe krótkie słowa (z query) są w tytule
    slowa_kluczowe_krotkie = [s for s in slowa if len(s) < 4 and not s.isdigit()]
    for krotkie in slowa_kluczowe_krotkie:
        # Regex \bAir\b - musi być całe słowo
        pattern = r'\b' + re.escape(krotkie) + r'\b'
        if not re.search(pattern, tytul_czysty):
             # Ostatnia deska ratunku: Fuzzy, ale tylko 100% dla krótkich słów
             if fuzz.partial_ratio(krotkie, tytul_czysty) < 100:
                 return False

    if ratio >= 90: # Podnosimy próg z 85 na 90 dla pewności
        # Dodatkowe zabezpieczenie: Jeśli szukamy liczby (np. 16), Fuzzy ratio może być wysokie dla innych liczb
        # Jeśli fraza to krótka liczba, wymuszamy strict match
        if fraza_czysta.isdigit() and len(fraza_czysta) < 3:
            return False
        return True
        
    return False

def czy_oferta_jest_ok(tytul, wykluczenia_uzytkownika=None, fraza_szukania=None):
    """
    3-STOPNIOWA WERYFIKACJA:
    1. Czarna Lista (spam, etui, pudełka)
    2. Wykluczenia użytkownika (słowa z minusem)
    3. Zgodność tytułu (czy produkt zawiera szukane słowa)
    """
    tytul_lower = tytul.lower()
    
    # KROK 1: Globalna Czarna Lista
    # Inteligentne wykluczenie: Jeśli użytkownik SAM wpisał "etui" w wyszukiwaniu, to NIE usuwamy etui.
    szuka_akcesoriow = False
    if fraza_szukania:
        fraza_lower = fraza_szukania.lower()
        if any(smiec in fraza_lower for smiec in GLOBALNA_CZARNA_LISTA):
            szuka_akcesoriow = True
            
    if not szuka_akcesoriow:
        for smiec in GLOBALNA_CZARNA_LISTA:
            if smiec in tytul_lower:
                return False
            
    # KROK 2: Wykluczenia użytkownika
    if wykluczenia_uzytkownika:
        for wyklucz in wykluczenia_uzytkownika:
            if wyklucz in tytul_lower:
                return False

    # KROK 3: Zgodność tytułu (Strict Match)
    if fraza_szukania:
         if not czy_slowa_kluczowe_sa_w_tytule(tytul, fraza_szukania):
             return False
                 
    return True

    return dobre_oferty, odrzucone_licznik





def filtruj_oferty(wszystkie_oferty, wykluczenia_dla_frazy=None):
    """
    Przetwarza listę ofert i zwraca tylko te, które przeszły wstępny filtr.
    Polegamy na Smart Filtrze (słowa kluczowe + fuzzy logic).
    """
    dobre_oferty = []
    odrzucone_licznik = 0
    
    for oferta in wszystkie_oferty:
        tytul = oferta.get('title', '')
        fraza_szukania = oferta.get('search_query', '')
        
        wykluczenia = []
        if wykluczenia_dla_frazy and fraza_szukania in wykluczenia_dla_frazy:
            wykluczenia = wykluczenia_dla_frazy[fraza_szukania]
            
        # Weryfikacja (Smart Filter + Regex + Fuzzy)
        if czy_oferta_jest_ok(tytul, wykluczenia, fraza_szukania):
            dobre_oferty.append(oferta)
        else:
            odrzucone_licznik += 1
            
    return dobre_oferty, odrzucone_licznik
