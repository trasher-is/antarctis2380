import pygame

import json
import os
import sys


# Gamestate selector for different game states to split main game from character selection and end game
# intro(): fake intro screen
# character_selection(): choose a character picture from list, use arrow keys and enter or mouse
# main_game(): core game loop, handles all elements
# end_game(): fake end game window, can restart to character selection
# state_manager(): manages state switching

class GameState:
    def __init__(self):
        self.state = 'intro'

    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state = 'character_selection'

        game_name_font = pygame.font.Font(os.path.join('assets', 'font', 'Preahvihear.ttf'), 80)
        game_name_text = 'ANTARCTIS 2380'

        start_font = pygame.font.Font(os.path.join('assets', 'font', 'Preahvihear.ttf'), 30)
        start_text = 'Press "ENTER" to start game'

        screen.blit(intro_background, (0, 0))
        game_name_text_surface = game_name_font.render(game_name_text, True, (255, 255, 255))
        screen.blit(game_name_text_surface, (550, 10))
        start_text_surface = start_font.render(start_text, True, (255, 255, 255))
        screen.blit(start_text_surface, (800, 660))

        pygame.display.flip()

    def character_selection(self):
        global current_character, selected_character
        left_button = pygame.Rect(0, 300, 50, 200)
        right_button = pygame.Rect(1230, 300, 50, 200)
        select_button = pygame.Rect(800, 600, 200, 50)
        char_info_field = pygame.Rect(600, 150, 500, 400)

        left_image = pygame.image.load(os.path.join('assets', 'img', 'left.png')).convert_alpha()
        right_image = pygame.image.load(os.path.join('assets', 'img', 'right.png')).convert_alpha()
        select_image = pygame.image.load(os.path.join('assets', 'img', 'select.png')).convert_alpha()
        char_info_image = pygame.image.load(os.path.join('assets', 'img', 'char_info.png')).convert_alpha()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if left_button.collidepoint(event.pos):
                    current_character = (current_character - 1) % len(character_images)
                elif right_button.collidepoint(event.pos):
                    current_character = (current_character + 1) % len(character_images)
                elif select_button.collidepoint(event.pos):
                    selected_character = current_character
                    self.state = 'main_game'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_character = (current_character - 1) % len(character_images)
                elif event.key == pygame.K_RIGHT:
                    current_character = (current_character + 1) % len(character_images)
                elif event.key == pygame.K_RETURN:
                    selected_character = current_character
                    self.state = 'main_game'

        screen.blit(char_select_background, (0, 0))
        screen.blit(character_images[current_character % len(character_images)], (100, 60))
        screen.blit(left_image, left_button)
        screen.blit(right_image, right_button)
        screen.blit(select_image, select_button)
        screen.blit(char_info_image, char_info_field)

        pygame.display.flip()

    def main_game(self):
        location_view = LocationView()
        action_box = ActionBox()
        player = Player(location_view, action_box)
        player_icon = PlayerIcon()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player.move('up')
                    elif event.key == pygame.K_DOWN:
                        player.move('down')
                    elif event.key == pygame.K_LEFT:
                        player.move('left')
                    elif event.key == pygame.K_RIGHT:
                        player.move('right')
                    elif event.key == pygame.K_x:
                        self.state = 'end_game'

            if self.state == 'end_game':
                break

            screen.blit(main_background, (0, 0))

            player.draw(screen)
            player_icon.draw(screen)
            action_box.draw(screen)
            location_view.draw(screen)

            pygame.display.flip()

    def end_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    self.state = 'character_selection'

        end_game_font = pygame.font.Font(os.path.join('assets', 'font', 'Preahvihear.ttf'), 80)
        end_game_text = 'FINAL DESTINATION'
        end_game_new_font = pygame.font.Font(os.path.join('assets', 'font', 'Preahvihear.ttf'), 40)
        end_game_new_text = 'Press ESC to exit or R to restart'

        screen.blit(end_game_background, (0, 0))
        end_game_text_surface = end_game_font.render(end_game_text, True, (255, 255, 255))
        screen.blit(end_game_text_surface, end_game_text_surface.get_rect(center=(640, 360)))
        end_game_new_text_surface = end_game_new_font.render(end_game_new_text, True, (255, 255, 255))
        screen.blit(end_game_new_text_surface, end_game_text_surface.get_rect(center=(700, 600)))

        pygame.display.flip()

    def state_manager(self):
        if self.state == 'intro':
            self.intro()
        if self.state == 'character_selection':
            self.character_selection()
        if self.state == 'main_game':
            self.main_game()
        if self.state == 'end_game':
            self.end_game()


# initialize pygame engine and load backgrounds and character images, read json file

pygame.init()
clock = pygame.time.Clock()
game_state = GameState()
pygame.display.set_caption('Antarctis 2380')

screen = pygame.display.set_mode((1280, 720))

intro_background = pygame.image.load(os.path.join('assets', 'img', 'intro_bg8.png')).convert()
char_select_background = pygame.image.load(os.path.join('assets', 'img', 'intro_bg8b.png')).convert()
main_background = pygame.image.load(os.path.join('assets', 'img', 'bg.png')).convert()
end_game_background = pygame.image.load(os.path.join('assets', 'img', 'intro_bg8b.png')).convert()

character_images = [
    pygame.image.load(os.path.join('assets', 'img', 'char_f_1.png')).convert_alpha(),
    pygame.image.load(os.path.join('assets', 'img', 'char_f_2.png')).convert_alpha(),
    pygame.image.load(os.path.join('assets', 'img', 'char_f_3.png')).convert_alpha(),
    pygame.image.load(os.path.join('assets', 'img', 'char_f_4.png')).convert_alpha(),
    pygame.image.load(os.path.join('assets', 'img', 'char_m_1.png')).convert_alpha(),
    pygame.image.load(os.path.join('assets', 'img', 'char_m_2.png')).convert_alpha(),
    pygame.image.load(os.path.join('assets', 'img', 'char_m_3.png')).convert_alpha(),
    pygame.image.load(os.path.join('assets', 'img', 'char_m_4.png')).convert_alpha()
]
current_character = 0
selected_character = 0

with open('assets/locations.json', 'r') as f:
    locations = json.load(f)


# create game objects with pygame.Sprite classes inheritance
# Player class is main game class which handles movement and updates other classes based on location

class Player(pygame.sprite.Sprite):
    def __init__(self, location_view, action_box):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.map_image = pygame.image.load(os.path.join('assets', 'img', 'map.png')).convert()
        self.rect = self.map_image.get_rect()
        self.velocity = 100
        self.pos_x = 100
        self.pos_y = 100
        self.tile_x = 0
        self.tile_y = 0
        self.update_image()
        self.location_view = location_view
        self.action_box = action_box

    def draw(self, surface):
        surface.blit(self.image, (10, 10))

    def move(self, direction):
        new_tile_x = self.tile_x
        new_tile_y = self.tile_y
        new_pos_x = self.pos_x
        new_pos_y = self.pos_y
        if direction == 'up' and self.tile_y > 0:
            new_pos_y += self.velocity
            new_tile_y -= 1
        elif direction == 'down' and self.tile_y < 8:
            new_pos_y -= self.velocity
            new_tile_y += 1
        elif direction == 'left' and self.tile_x > 0:
            new_pos_x += self.velocity
            new_tile_x -= 1
        elif direction == 'right' and self.tile_x < 8:
            new_pos_x -= self.velocity
            new_tile_x += 1

        if 0 <= new_tile_x <= 8 and 0 <= new_tile_y <= 8:
            for location in locations:
                if location['x'] == new_tile_x and location['y'] == new_tile_y:
                    if location['status'] == 0:
                        return
                    elif location['status'] == 1:
                        self.tile_x = new_tile_x
                        self.tile_y = new_tile_y
                        self.pos_x = new_pos_x
                        self.pos_y = new_pos_y
                    elif location['status'] == 2:
                        if direction in location['door']:
                            self.tile_x = new_tile_x
                            self.tile_y = new_tile_y
                            self.pos_x = new_pos_x
                            self.pos_y = new_pos_y
                        else:
                            return

        self.update_image()
        self.update_location_view()
        self.update_actionbox()

    def update_image(self):
        new_image = self.map_image
        circle_mask = pygame.Surface((300, 300), pygame.SRCALPHA)
        pygame.draw.ellipse(circle_mask, (255, 255, 255, 255), (0, 0, 300, 300))
        circle_mask.blit(new_image, (self.pos_x, self.pos_y), special_flags=pygame.BLEND_RGBA_MIN)

        marker = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.line(marker, (250, 250, 250), (15, 0), (15, 30), 2)
        pygame.draw.line(marker, (200, 250, 250), (0, 15), (30, 15), 2)
        marker_rect = marker.get_rect(center=circle_mask.get_rect().center)
        circle_mask.blit(marker, marker_rect)
        self.image = circle_mask

    def update_location_view(self):
        for location in locations:
            if location['x'] == self.tile_x and location['y'] == self.tile_y:
                self.location_view.update(location)

    def update_actionbox(self):
        for location in locations:
            if location['x'] == self.tile_x and location['y'] == self.tile_y:
                self.action_box.update(location)


class LocationView(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('assets', 'img', 'hall_1.png')).convert()
        self.rect = self.image.get_rect(center=(640, 256))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, location):
        self.image = pygame.image.load(location["image_url"]).convert()


class PlayerIcon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None

    def draw(self, surface):
        self.image = character_images[selected_character]
        self.rect = self.image.get_rect(center=(180, 640))
        surface.blit(self.image, self.rect)


class ActionBox(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((620, 190), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(640, 610))
        self.font = pygame.font.Font(None, 30)
        self.text1 = locations[0]['description'][0]
        self.text2 = locations[0]['description'][1]

    def draw(self, surface):
        text_surface1 = self.font.render(self.text1, True, (255, 255, 255))
        text_surface2 = self.font.render(self.text2, True, (255, 255, 255))
        self.image.blit(text_surface1, (10, 10))
        self.image.blit(text_surface2, (10, 40))
        surface.blit(self.image, self.rect)

    def update(self, location):
        new_text1 = location['description'][0]
        new_text2 = location['description'][1]
        self.text1 = new_text1
        self.text2 = new_text2
        self.image.fill((0, 0, 0, 0))
        text_surface1 = self.font.render(new_text1, True, (255, 255, 255))
        text_surface2 = self.font.render(new_text2, True, (255, 255, 255))
        self.image.blit(text_surface1, (10, 10))
        self.image.blit(text_surface2, (10, 40))
        self.draw(self.image)


while True:
    game_state.state_manager()
    clock.tick(30)
