import pygame
from support import *


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
TILE_SIZE = 64



MAP_LAYOUTS = {
    'map_1': {
        'floor': import_csv_layout('./Assets/map_files/map_1/flyby_1_floor.csv'),
        'player': import_csv_layout('./Assets/map_files/map_1/flyby_1_player.csv'),
        'cannons': import_csv_layout('./Assets/map_files/map_1/flyby_1_turrent.csv'),
        'enemy1': import_csv_layout('./Assets/map_files/map_1/flyby_1_enemy1.csv'),
        'enemy2': import_csv_layout('./Assets/map_files/map_1/flyby_1_enemy2.csv'),
        'enemy3': import_csv_layout('./Assets/map_files/map_1/flyby_1_enemy3.csv'),
        'enemy4': import_csv_layout('./Assets/map_files/map_1/flyby_1_enemy4.csv'),
        'boss': import_csv_layout('./Assets/map_files/map_1/flyby_1_boss.csv'),
        'to_next': import_csv_layout('./Assets/map_files/map_1/flyby_1_to_next.csv')},
    'map_2': {
        'floor': import_csv_layout('./Assets/map_files/map_2/flyby_2_floor.csv'),
        'cannons': import_csv_layout('./Assets/map_files/map_2/flyby_2_turrent.csv'),
        'player': import_csv_layout('./Assets/map_files/map_2/flyby_2_player.csv'),
        'enemy1': import_csv_layout('./Assets/map_files/map_2/flyby_2_Ship1.csv'),
        'enemy2': import_csv_layout('./Assets/map_files/map_2/flyby_2_Ship2.csv'),
        'enemy3': import_csv_layout('./Assets/map_files/map_2/flyby_2_Ship3.csv'),
        'enemy4': import_csv_layout('./Assets/map_files/map_2/flyby_2_Ship4.csv'),
        'boss': import_csv_layout('./Assets/map_files/map_2/flyby_2_boss.csv')}
}

MAP_URL = {
    'map_1': {'url': './Assets/map_files/map_1/map_1.png'},
    'map_2': {'url': './Assets/map_files/map_2/flyby_2.png'}
}



# ======================= UI

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'Arial'
UI_FONT_SIZE = 18