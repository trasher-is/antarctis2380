import pygame
import sys, os, time, json

from model import GameState, MapBg, Item
from view import LocationView, PlayerIcon, ActionBox, PlayerInventory

pygame.init()
clock = pygame.time.Clock()

game_state = GameState()
intro_background = pygame.image.load(os.path.join('assets', 'img', 'intro_bg8.png')).convert()
char_select_background = pygame.image.load(os.path.join('assets', 'img', 'intro_bg8b.png')).convert()
character_images = [
    pygame.image.load(os.path.join('assets', 'img', 'char_f_1.png')).convert_alpha(),
    pygame.image.load(os.path.join('assets', 'img', 'char_f_2.png')).convert_alpha()
]
current_character = 0
selected_character = None
font = pygame.font.Font(os.path.join('assets', 'font', 'Preahvihear.ttf'), 30)
with open('assets/locations.json', 'r') as f:
    locations = json.load(f)

# Initialize view
pygame.display.set_caption('Antarctis 2380')
screen = pygame.display.set_mode((1280, 720))
location_view = LocationView()
actionbox = ActionBox()
hud_background = MapBg(location_view, actionbox)
player_icon_bg = PlayerIconBg()
player_icon = PlayerIcon()
npc_icon_bg = NpcIconBg()
player_inventory = PlayerInventory()

# Main game loop (controller)
while True:
    game_state.state_manager()
    clock.tick(30)
