import pygame
from support import *


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 640
TILE_SIZE = 64



MAP_LAYOUTS = {
    'map_1': {
        'floor': import_csv_layout('./Assets/map_files/map_1/flyby_1_floor.csv'),
        'player': import_csv_layout('./Assets/map_files/map_1/flyby_1_player.csv'),
        'driver': import_csv_layout('./Assets/map_files/map_1/flyby_1_driver.csv'),
        'cannons': import_csv_layout('./Assets/map_files/map_1/flyby_1_cannon.csv'),
        'enemy1': import_csv_layout('./Assets/map_files/map_1/flyby_1_enemy1.csv'),
        'enemy4': import_csv_layout('./Assets/map_files/map_1/flyby_1_enemy4.csv'),
        'to_next': import_csv_layout('./Assets/map_files/map_1/flyby_1_to_next.csv')},
    'map_2': {
        'floor': import_csv_layout('./Assets/map_files/map_2/flyby_2_floor.csv'),
        'cannons': import_csv_layout('./Assets/map_files/map_2/flyby_2_cannon.csv'),
        'player': import_csv_layout('./Assets/map_files/map_2/flyby_2_player.csv'),
        'driver': import_csv_layout('./Assets/map_files/map_2/flyby_2_driver.csv'),
        'enemy1': import_csv_layout('./Assets/map_files/map_2/flyby_2_enemy1.csv'),
        'enemy2': import_csv_layout('./Assets/map_files/map_2/flyby_2_enemy2.csv'),
        'enemy3': import_csv_layout('./Assets/map_files/map_2/flyby_2_enemy3.csv'),
        'to_next': import_csv_layout('./Assets/map_files/map_2/flyby_2_to_next.csv')},
    'map_3': {
        'player': import_csv_layout('./Assets/map_files/map_3/flyby_3_player.csv'),
        'enemy1': import_csv_layout('./Assets/map_files/map_3/flyby_3_enemy1.csv'),
        'enemy2': import_csv_layout('./Assets/map_files/map_3/flyby_3_enemy2.csv'),
        'enemy3': import_csv_layout('./Assets/map_files/map_3/flyby_3_enemy3.csv'),
        'enemy4': import_csv_layout('./Assets/map_files/map_3/flyby_3_enemy4.csv'),
        'driver': import_csv_layout('./Assets/map_files/map_3/flyby_3_driver.csv'),
        'boss_threshold': import_csv_layout('./Assets/map_files/map_3/flyby_3_boss_threshold.csv'),
        'boss': import_csv_layout('./Assets/map_files/map_3/flyby_3_boss.csv'),
        'arm': import_csv_layout('./Assets/map_files/map_3/flyby_3_boxx_arms.csv')},
    'map_4': {
        'player': import_csv_layout('./Assets/map_files/map_4/flyby_4_player.csv'),
        'boss': import_csv_layout('./Assets/map_files/map_4/flyby_4_boss.csv'),
        'driver': import_csv_layout('./Assets/map_files/map_4/flyby_4_driver.csv'),
        'arm': import_csv_layout('./Assets/map_files/map_4/flyby_4_boss_arm.csv'),
        'threshold': import_csv_layout('./Assets/map_files/map_4/flyby_4_boss_threshold.csv')
    }}

MAP_URL = {
    'map_1': {'url': './Assets/map_files/map_1/flyby_1.png'},
    'map_2': {'url': './Assets/map_files/map_2/flyby_2.png'},
    'map_3': {'url': './Assets/map_files/map_3/flyby_3.png'},
    'map_4': {'url': './Assets/map_files/map_4/flyby_4.png'}
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
AMMO_COLOR = (191, 87, 0)

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'Arial'
UI_FONT_SIZE = 18



START_TEXT = (
    "The year was 2030, after we destroyed the world with the \"Armaggedon War\".\n"
    "That's when they attacked. Some think our bombs are what made them come.\n"
    "They eliminated a quarter of the population in a week, they had no reason to fear us...\n"
    "That was until the remaining superpowers launched an attack with everything they had left.\n"
    "These ships were more human in their structure; we understood how they worked once we captured one.\n"
    "We developed a gravity cannon that is powered by the ship's core.\n"
    "We pushed even as they kept bombing our cities...\n"
    "We pushed...\n"
    "The year is 2077... My name is David, I am the last millennial.\n"
    "We are ready...\n"
    "Now it's in your hands... fly Pilot.\n"
    "Press Enter"
)

# lower fire_rate int = faster shots.
WEAPONS = {
    'toxic': {'damage': 0.5, 'speed': 20, 'type': 'Shot1', 'fire_rate': 0.2, 'capacity': 7},
    'stun': {'damage': 0.5, 'speed': 20, 'type': 'Shot2', 'fire_rate': 0.15, 'capacity': 5},
    'flux': {'damage': 3, 'speed': 18, 'type': 'Shot3', 'fire_rate': 1.3, 'capacity': 3},
    'matter': {'damage': 2, 'speed': 10, 'type': 'Shot4', 'fire_rate': 0.7, 'capacity': 4},
    'mass': {'damage': 3, 'speed': 13, 'type': 'Shot5', 'fire_rate': 0.5, 'capacity': 2},
    'speed': {'damage': 1, 'speed': 15, 'type': 'Shot6', 'fire_rate': 0.1, 'capacity': 5},
    'gravity': {'damage': 1, 'speed': 15, 'type': 'Shot7', 'fire_rate': 0.4, 'capacity': 3}
}