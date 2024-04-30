'''
Здесь находятся все классы.
'''

import random
from enum import Enum

COEFFS = Enum('COEFFS', {"Normal": 1.2, "SlightDamage": 0.95, "HalfDamage": 0.55, "AlmostAllDamage":0.25, 
                         "Trash": 0.1})

'''Игрок'''

class Player:
    def __init__(self, MAX_LOAD, MAX_SPEED):
        self.MAX_LOAD = int(MAX_LOAD.split()[0])
        self.MAX_SPEED = int(MAX_SPEED)
    speed = random.randint(3, 5) 
    balance = random.randint(100, 1000)
    products = []

'''Товары'''

class Item:
    def __init__(self, item):
        self.item = item
    price = None
    quality = COEFFS.Normal.value

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

class City:
    distance = random.randint(50, 150)