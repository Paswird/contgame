import random

# Створення карти за заданими розмірами
def create_board(rows, cols):
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(' ')
        board.append(row)
    return board

# Розмір карти за складністю
level_s = {'нуб': 5, 'середнячок': 10, 'крейзі': 20}

# Запит ім'я користувача
while True:
    name = input("як тебе зовуть, друже мій: ")
    if name.strip() != "":
        break

# Запит складності
while True:
    level = input("наскільки ти про (нуб, середнячок, крейзі): ")
    if level in level_s:
        rows = cols = level_s[level]
        break

# Генерація координат скарбу
treasure_row = random.randint(0, rows-1)
treasure_col = random.randint(0, cols-1)

# Початок гри
board = create_board(rows, cols)
board[treasure_row][treasure_col] = ''

print("Карта згенерована! Скарб знаходиться в клітинці з координатами.".format(treasure_row, treasure_col))
for i in range(rows):
    print(" " + "___" * cols)
    row_str = "|"
    for j in range(cols):
        row_str += " {} |".format(board[i][j])
    print(row_str)
print(" " + "___" * cols)

print("Гра почалася, {}! Ваше завдання - знайти скарб, розташований на карті. Успіхів юний пірате!".format(name))


import random
import sqlite3

# Define game constants
LEVELS = {
    'easy': {'size': 5, 'water': 2},
    'medium': {'size': 10, 'water': 2, 'animal': 1, 'shovel': 1},
    'hard': {'size': 20, 'water': 2, 'animal': 2, 'shovel': 1, 'key': 1}
}
ACTIONS = ['go', 'dig', 'search']
DIRECTIONS = ['left', 'right', 'up', 'down']

# Define SQLite database functions
def create_table():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scores
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 player_name TEXT,
                 level TEXT,
                 moves INTEGER,
                 won INTEGER)''')
    conn.commit()
    conn.close()

def add_score(player_name, level, moves, won):
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('INSERT INTO scores (player_name, level, moves, won) VALUES (?, ?, ?, ?)',
              (player_name, level, moves, won))
    conn.commit()
    conn.close()

def get_scores():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('SELECT player_name, level, moves FROM scores WHERE won = 1')
    scores = c.fetchall()
    conn.close()
    return scores

# Define game functions
def get_level_choice():
    while True:
        level = input('Choose a level (easy, medium, hard): ')
        if level.lower() in LEVELS:
            return level.lower()
        print('Invalid level choice. Try again.')

def get_player_name():
    while True:
        player_name = input('Enter your player name: ')
        conn = sqlite3.connect('game.db')
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM scores WHERE player_name = ?', (player_name,))
        count = c.fetchone()[0]
        conn.close()
        if count == 0:
            return player_name
        print('Player name is already taken. Try another one.')

def generate_map(size, water, animal, shovel, key):
    map = [[' ' for _ in range(size)] for _ in range(size)]
    map[random.randint(0, size-1)][random.randint(0, size-1)] = 'treasure'
    for _ in range(water):
        x = random.randint(0, size-1)
        y = random.randint(0, size-1)
        while map[x][y] != ' ':
            x = random.randint(0, size-1)
            y = random.randint(0, size-1)
        map[x][y] = 'water'
    if animal:
        x = random.randint(0, size-1)
        y = random.randint(0, size-1)
        while map[x][y] != ' ':
            x = random.randint(0, size-1)
            y = random.randint(0, size-1)
        map[x][y] = 'animal'
    if shovel:
        x = random.randint(0, size-1)