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

### Windows terminal

![windows terminal gameplay](./screenshots/windows_terminal_gameplay.png)
![windows terminal game over](./screenshots/windows_terminal_game_over.png)

### Linux

- _Gnome terminal_

![gnome terminal gameplay](./screenshots/gnome_terminal.png)

- _Kitty terminal_

![kitty board](./screenshots/kitty_terminal_board.png)
![kitty gameplay](./screenshots/kitty_terminal_gameplay.png)

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

- _Debian based distributions_ (na innych dystrybucjach należy użyć innego systemu zarządzania pakietami i odpowiadających pakietów)

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

2. Z własnym plikiem konfiguracyjnym (opisanym poniżej):

```bash
python main.py -c ścieżka/do/config.ini
```

- Aby zobaczyć możliwe parametry przy uruchamianiu pliku:

```bash
python main.py --help
```

### Rozgrywka

1. Gra rozpoczyna się od wyboru rozmiaru planszy (max. 6x6)
2. Po wyborze wymiarów pojawi się plansza z zakrytymi kartami
3. Gracze na zmianę wybierają po dwie karty
4. Jeśli karty tworzą parę:
   - Gracz zdobywa punkt
   - Karty pozostają odkryte
   - Gracz może wykonać kolejny ruch
5. Jeśli karty są różne:
   - Karty zostają zakryte
   - Kolejka przechodzi na drugiego gracza
6. Gra kończy się, gdy wszystkie pary zostaną odnalezione

### Dodatkowe informacje

- Aby wyjść z gry należy użyć skrótu klawiszowego `ctrl+q`.
- Aby zapisać stan gry należy użyć klawisza `s`.
- Wczytywanie stanu gry jest wykonywane za pomocą pliku konfiguracyjnego opisanego w dalszej części.
- `Ctrl+p` wyświetli możliwe do wykonania akcje.
- Za pomocą klawisza `Tab` można poruszać się po planszy i przyciskach.
- W przypadku jakichkolwiek błędów proszę przejrzeć plik: `memory_game.log` znajdujący się w katalogu gry.

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

- `game_save_file` - ścieżka do pliku, do którego zostanie zapisany stan gry po wciśnięciu klawisza "s"
- `key_save_file` - ścieżka do pliku, w któym zostanie zapisany klucz szyfrowania

> **Uwaga:** Zawartość pliku `game_save_file` zostanie całkowicie zastąpiona przy zapisywaniu stanu gry.

> **INFO:** Domyślnie stan gry zostanie zapisany w katalogu, gdzie znajduje się gra w plikach game_save.dat i save.key.

### [LOAD_GAME]

- `game_load_file` - ścieżka do pliku z zapisanym stanem gry
- `key_load_file` - ścieżka do pliku z kluczem szyfrowania pozwalającym na odczytanie stanu gry
- `load` - flaga określająca czy wczytać zapisaną grę (true/false)

> **Uwaga:** Ścieżki w pliku konfiguracyjnym mogą być względne (początkowym katalogiem będzie miejsce katalogu z grą - _current working directory_) lub absolutne.

> **INFO:** Jeżeli load jest ustawione na true, stan gry zostanie wczytany domyślnie z plików game_save.dat i save.key w katalogu gry. Wczytanie stanu gry jest wykonywane automatycznie przy uruchamianiu.

Przykładowy plik `config.ini`:

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
