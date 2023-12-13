import pygame, os

# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# clock = pygame.time.Clock()
# running = True


class MapTiles(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((96, 96))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=(x, y))


class MapBg(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((320, 320))
        self.image.fill('black')
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect(center=(160, 160))
        pygame.draw.circle(self.image, 'white', self.rect.center, 150)

        self.tiles = pygame.sprite.Group()
        for i in range(3):
            for j in range(3):
                tile = MapTiles(i * 100 + 12, j * 100 + 12)
                self.tiles.add(tile)

    def update(self):
        self.tiles.update()

    def draw(self, surface):
        self.tiles.draw(self.image, special_flags=pygame.BLEND_RGBA_MULT)
        surface.blit(self.image, self.rect)


class PlayerIcon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None

    def draw(self, surface):
        global selected_character
        self.image = character_images[selected_character]
        self.rect = self.image.get_rect(center=(160, 720))
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

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class PlayerInventory(pygame.sprite.Sprite):
    # laukas HP/XP/energy ir itemmu atvaizdavimui
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((320, 320))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=(1120, 560))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class LocationView(pygame.sprite.Sprite):
    # laukas lokacijos paveikslui ir NPC/itemam jei ju yra ten
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((620, 500))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=(640, 260))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# hud_background = MapBg()
# player_icon_bg = PlayerIconBg()
# npc_icon_bg = NpcIconBg()
# action_box = ActionBox()
# location_view = LocationView()
# player_inventory = PlayerInventory()
#
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     screen.fill("teal")
#
#     hud_background.draw(screen)
#     player_icon_bg.draw(screen)
#     npc_icon_bg.draw(screen)
#     action_box.draw(screen)
#     location_view.draw(screen)
#     player_inventory.draw(screen)
#
#     pygame.display.flip()
#     clock.tick(30)
#
# pygame.quit()
