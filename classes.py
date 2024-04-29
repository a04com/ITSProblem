'''
Здесь находятся все классы.
'''

import random
from enum import Enum

ITEM_LIST = ['мясо', 'сухофрукты', 'зерно', 'мука', 'ткани', 'краска']
COEFFS = Enum('COEFFS', {"Normal": 1.2, "SlightDamage": 0.95, "HalfDamage": 0.55, "AlmostAllDamage":0.25, 
                         "Trash": 0.1})

'''Игрок'''

class Player:
    def __init__(self, MAX_LOAD):
        self.MAX_LOAD = float(MAX_LOAD.split()[0])
    speed = random.randint(1, 5) 
    balance = random.randint(100, 1000)
    products = []

'''Товары'''

class Item:
    def __init__(self, price):
        self.price = price
    item = random.choice(ITEM_LIST)
    quality = COEFFS.Normal

'''События'''

class Events(Enum):
    REGULAR_DAY = 0
    RAIN = 1
    SMOOTH_ROAD = 2
    BROKEN_CART = 3
    RIVER = 4
    LOCAL = 5
    ROBBER = 6
    TAVERN = 7
    RANDOM_SPOIL = 8

'''Город'''

class City():
    distance = random.randint(50, 150)