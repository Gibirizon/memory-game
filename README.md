[![en](https://img.shields.io/badge/lang-en-red.svg)](./README.md)
[![pl](https://img.shields.io/badge/lang-pl-white.svg)](./README-PL.md)

# Memory Game

## Table of Contents

- [Game Description](#game-description)
- [Screenshots](#screenshots)
- [Installation](#installation)
  - [Windows](#windows)
  - [Linux](#linux)
- [Player Instructions](#player-instructions)
- [Main Features](#main-features)
- [Configuration](#configuration)

## Game Description

Memory Game is a classic memory game implemented as a console application for two players. Players take turns revealing two cards, trying to find pairs of identical symbols. A player who finds a pair can take another turn. The person who collects the most pairs wins.

The game was created using modern Python libraries, providing a pleasant user interface despite its console-based nature.

## Screenshots

### Windows terminal

![windows terminal gameplay](./docs/screenshots/windows_terminal_gameplay.png)
![windows terminal game over](./docs/screenshots/windows_terminal_game_over.png)

### Linux terminals

- _Gnome terminal_

![gnome terminal gameplay](./docs/screenshots/gnome_terminal.png)

- _Kitty terminal_

![kitty board](./docs/screenshots/kitty_terminal_board.png)
![kitty gameplay](./docs/screenshots/kitty_terminal_gameplay.png)

## Installation

### System Requirements

- Python 3.8 or newer
- Pip (Python package manager)

### Windows

1. Install Python:
   - Download and install Python 3.8 or newer from [python.org](https://python.org)
   - During installation, check "Add Python to environment variables"
2. Open Command Prompt (cmd) as administrator
3. Clone the repository and navigate to the project directory:

```cmd
git clone <repository-url>
cd memory-game
```

4. Create and activate virtual environment:

```cmd
python -m venv venv
venv\Scripts\activate
```

5. Install the game:

```cmd
pip install -e .
```

### Linux

1. Install Python (if not installed):

- _Debian based distributions_ (use appropriate package manager and packages for other distributions)

```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv git
```

2. Clone the repository and navigate to the project directory:

```bash
git clone <repository-url>
cd memory-game
```

3. Create and activate virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install the game:

```bash
pip install -e .
```

## Player Instructions

### Running the Game

After installation, you can run the game in one of the following ways:

1. If you installed using requirements.txt:

```bash
python main.py -c config/default.ini
# or
python -m src.memory_game.app -c config/default.ini
# or
memory-game -c config/default.ini
```

- To see available launch parameters:

```bash
python main.py --help
# or
memory-game --help
```

### Gameplay

1. The game begins with choosing the board size (max. 6x6)
2. After selecting dimensions, a board with hidden cards appears
3. Players take turns selecting two cards
4. If the cards form a pair:
   - Player gets a point
   - Cards remain revealed
   - Player can make another move
5. If the cards are different:
   - Cards are hidden again
   - Turn passes to the other player
6. Game ends when all pairs are found

### Additional Information

- To exit the game, use the keyboard shortcut `ctrl+q`
- To save game state, press `s`
- Loading game state is done through the configuration file described below
- `ctrl+p` displays possible actions
- Use `Tab` to navigate through the board and buttons
- In case of any errors, please check the `memory_game.log` file in the directory from which the game is launched

## Main Features

- Configurable board size
- Game state save and load system
- Encryption of saved game states
- Intuitive console user interface
- Colored markers and card symbols
- Score counter for both players
- Configuration through INI file

## Configuration

The game can be configured through an INI file containing the following sections:

### [BOARD]

- `width` - board width (number of cards)
- `height` - board height (number of cards)

### [SAVE_GAME]

- `game_save_file` - path to the file where game state will be saved when pressing "s"
- `key_save_file` - path to the file where encryption key will be saved

> [!NOTE]
> The content of `game_save_file` will be completely replaced when saving game state.

> [!TIP]
> By default, game state will be saved in the directory from which the game is launched in files game_save.dat and save.key.

### [LOAD_GAME]

- `game_load_file` - path to the file with saved game state
- `key_load_file` - path to the file with encryption key for reading game state
- `load` - flag determining whether to load saved game (true/false)

> [!NOTE]
> Paths in the configuration file can be relative (starting directory will be the launch location - _current working directory_) or absolute.

> [!TIP]
> If load is set to true, game state will be loaded by default from game_save.dat and save.key files in the game launch directory. Loading game state is performed automatically at startup.

Example `default.ini` file:

```ini
[BOARD]
width = 2
height = 3

[SAVE_GAME]
game_save_file = /home/user/Documents/game_save.dat
key_save_file = /home/user/Documents/save.key

[LOAD_GAME]
game_load_file = /home/user/Documents/game_save.dat
key_load_file = /home/user/Documents/save.key
load = true
```
