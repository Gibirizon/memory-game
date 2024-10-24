# Memory Game

## Spis treści

- [Opis gry](#opis-gry)
- [Zrzuty ekranu](#zrzuty-ekranu)
- [Instalacja](#instalacja)
  - [Windows](#windows)
  - [Linux](#linux)
- [Instrukcja dla gracza](#instrukcja-dla-gracza)
- [Główne funkcjonalności](#główne-funkcjonalności)
- [Konfiguracja](#konfiguracja)

## Opis gry

Memory Game to klasyczna gra pamięciowa zaimplementowana jako aplikacja konsolowa dla dwóch graczy. Gracze na zmianę odkrywają po dwie karty, starając się odnaleźć pary identycznych symboli. Gracz, który znajdzie parę, może wykonać kolejny ruch. Wygrywa osoba, która zbierze najwięcej par.

Gra została stworzona z wykorzystaniem nowoczesnych bibliotek Pythona, zapewniających przyjemny interfejs użytkownika mimo konsolowego charakteru aplikacji.

## Zrzuty ekranu

[Tutaj zostaną dodane zrzuty ekranu z gry]

## Instalacja

### Wymagania systemowe

- Python 3.8 lub nowszy
- Pip (menedżer pakietów Pythona)

### Windows

1. Pobierz i zainstaluj Pythona ze strony [python.org](https://python.org)
2. Otwórz wiersz poleceń (cmd) jako administrator
3. Przejdź do katalogu z grą:

```cmd
cd ścieżka\do\katalogu\z\grą
```

4. Stwórz i aktywuj wirtualne środowisko:

```cmd
python -m venv venv
venv\Scripts\activate
```

5. Zainstaluj wymagane pakiety:

```cmd
pip install -r requirements.txt
```

### Linux

1. Zainstaluj Pythona (jeśli nie jest zainstalowany):

```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
```

2. Przejdź do katalogu z grą:

```bash
cd ścieżka/do/katalogu/z/grą
```

3. Stwórz i aktywuj wirtualne środowisko:

```bash
python3 -m venv venv
source venv/bin/activate
```

4. Zainstaluj wymagane pakiety:

```bash
pip install -r requirements.txt
```

## Instrukcja dla gracza

### Uruchomienie gry

1. Z domyślnymi ustawieniami:

```bash
python main.py
```

2. Z własnym plikiem konfiguracyjnym:

```bash
python main.py -c ścieżka/do/config.ini
```

### Rozgrywka

1. Gra rozpoczyna się od planszy z zakrytymi kartami
2. Gracze na zmianę wybierają po dwie karty
3. Jeśli karty tworzą parę:
   - Gracz zdobywa punkt
   - Karty pozostają odkryte
   - Gracz może wykonać kolejny ruch
4. Jeśli karty są różne:
   - Karty zostają zakryte
   - Kolejka przechodzi na drugiego gracza
5. Gra kończy się, gdy wszystkie pary zostaną odnalezione

## Główne funkcjonalności

- Konfigurowalna wielkość planszy
- System zapisu i wczytywania stanu gry
- Szyfrowanie zapisanych stanów gry
- Intuicyjny interfejs użytkownika w konsoli
- Kolorowe oznaczenia i symbole kart
- Licznik punktów dla obu graczy
- Możliwość konfiguracji poprzez plik INI

## Konfiguracja

Gra może być konfigurowana poprzez plik INI zawierający następujące sekcje:

### [BOARD]

- `width` - szerokość planszy (liczba kart)
- `height` - wysokość planszy (liczba kart)

### [SAVE_GAME]

- `game_save_file` - ścieżka do pliku zapisu stanu gry
- `key_save_file` - ścieżka do pliku klucza szyfrowania

### [LOAD_GAME]

- `game_load_file` - ścieżka do pliku z zapisanym stanem gry
- `key_load_file` - ścieżka do pliku klucza szyfrowania
- `load` - flaga określająca czy wczytać zapisaną grę (true/false)

Przykładowy plik config.ini:

```ini
[BOARD]
width = 2
height = 3

[SAVE_GAME]
game_save_file = /home/wojtek/Dokumenty/game_save.dat
key_save_file = /home/wojtek/Dokumenty/save.key

[LOAD_GAME]
game_load_file = /home/wojtek/Dokumenty/game_save.dat
key_load_file = /home/wojtek/Dokumenty/save.key
load = true
```

**Uwaga:** Wszystkie ścieżki w pliku konfiguracyjnym powinny być bezwzględne (pełne ścieżki do plików).
