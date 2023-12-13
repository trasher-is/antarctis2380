import pygame, sys, os, json


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
        screen.blit(right_image,right_button)
        screen.blit(select_image, select_button)
        screen.blit(char_info_image, char_info_field)

        pygame.display.flip()


    def main_game(self):
        running = True
        location_view = LocationView()
        actionbox = ActionBox()
        player = Player(location_view, actionbox)
        player_icon_bg = PlayerIconBg()
        player_icon = PlayerIcon()
        npc_icon_bg = NpcIconBg()
        player_inventory = PlayerInventory()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player.move('up')
                    elif event.key == pygame.K_DOWN:
                        player.move('down')
                    elif event.key == pygame.K_LEFT:
                        player.move('left')
                    elif event.key == pygame.K_RIGHT:
                        player.move('right')


            screen.fill("teal")

            player.draw(screen)
            player_icon_bg.draw(screen)
            player_icon.draw(screen)
            npc_icon_bg.draw(screen)
            actionbox.draw(screen)
            location_view.draw(screen)
            player_inventory.draw(screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def state_manager(self):
        if self.state == 'intro':
            self.intro()
        if self.state == 'character_selection':
            self.character_selection()
        if self.state == 'main_game':
            self.main_game()


pygame.init()
clock = pygame.time.Clock()
game_state = GameState()
pygame.display.set_caption('Antarctis 2380')

screen = pygame.display.set_mode((1280, 720))

intro_background = pygame.image.load(os.path.join('assets', 'img', 'intro_bg8.png')).convert()
char_select_background = pygame.image.load(os.path.join('assets', 'img', 'intro_bg8b.png')).convert()

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
selected_character = None

font = pygame.font.Font(os.path.join('assets', 'font', 'Preahvihear.ttf'), 30)

with open('assets/locations.json', 'r') as f:
    locations = json.load(f)


class Player(pygame.sprite.Sprite):
    def __init__(self, location_view, actionbox):
        pygame.sprite.Sprite.__init__(self)
        self.map_image = pygame.image.load(os.path.join('assets', 'img', 'map.png')).convert()
        self.rect = self.map_image.get_rect()
        self.velocity = 100
        self.pos_x = 100
        self.pos_y = 100
        self.tile_x = 0
        self.tile_y = 0
        self.update_image()
        self.location_view = location_view
        self.actionbox = actionbox

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
                    # elif location['status'] == 2 and direction == 'right': #ar man reikia sito is vis? as zaidejo krypties neseku gi,
                    # gal tik koridoriuje jei iejimas is kitos puses yra kad neieitu kiaurai siena
                    #     return

        self.tile_x = new_tile_x
        self.tile_y = new_tile_y
        self.pos_x = new_pos_x
        self.pos_y = new_pos_y
        self.update_image()
        self.update_location_view()
        self.update_actionbox()

    def update_image(self):
        self.get_location()
        self.image = self.map_image.copy()
        circle_mask = pygame.Surface((300, 300), pygame.SRCALPHA)
        pygame.draw.ellipse(circle_mask, (255, 255, 255, 255), (0, 0, 300, 300))
        circle_mask.blit(self.image, (self.pos_x, self.pos_y), special_flags=pygame.BLEND_RGBA_MIN)
        self.image = circle_mask

    def get_location(self):
        print(self.tile_x, self.tile_y)
        return self.tile_x, self.tile_y

    def update_location_view(self):
        for location in locations:
            if location['x'] == self.tile_x and location['y'] == self.tile_y:
                self.location_view.update(location)

    def update_actionbox(self):
        for location in locations:
            if location['x'] == self.tile_x and location['y'] == self.tile_y:
                self.actionbox.update(location)


class LocationView(pygame.sprite.Sprite):
    # laukas lokacijos paveikslui ir NPC/itemam jei ju yra ten
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
        global selected_character
        self.image = character_images[selected_character]
        self.rect = self.image.get_rect(center=(180, 640))
        surface.blit(self.image, self.rect)


class PlayerIconBg(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((320, 400))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=(160, 520))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class NpcIcon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('assets', 'img', 'char_m_21.png')).convert_alpha()
        self.rect = self.image.get_rect(center=(1120, 200))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class NpcIconBg(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((320, 400))
        self.image.fill('red')
        self.rect = self.image.get_rect(center=(1120, 210))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class ActionBox(pygame.sprite.Sprite):
    # laukas tekstui/pokalbiams ir veiksmams
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((620, 190))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=(640, 610))
        self.font = pygame.font.Font(None, 30)
        self.text = locations[0]['description']
        self.draw(self.image)

    def draw(self, surface):
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        self.image.fill('white')
        self.image.blit(text_surface, text_rect)
        surface.blit(self.image, self.rect)

    def update(self, location):
        self.text = location['description']


class PlayerInventory(pygame.sprite.Sprite):
    # laukas HP/XP/energy ir itemmu atvaizdavimui
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((320, 320))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=(1120, 560))

    def draw(self, surface):
        surface.blit(self.image, self.rect)



while True:
    game_state.state_manager()
    clock.tick(30)
