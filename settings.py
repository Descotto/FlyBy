import pygame
from support import *


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
TILE_SIZE = 64



MAP_LAYOUTS = {
    'map_1': {
        'floor': import_csv_layout('./Assets/map_files/map_1/map_1_floor.csv'),
        'player': import_csv_layout('./Assets/map_files/map_1/map_1_player.csv'),
        'cannons': import_csv_layout('./Assets/map_files/map_1/map_1_turrent.csv')}
}