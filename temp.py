import pygame, os

pygame.init()
window = pygame.display.set_mode((300, 300))

background = pygame.image.load(os.path.join('assets', 'img', 'map.png')).convert()

size = window.get_size()
cropped_background = pygame.Surface(size, pygame.SRCALPHA)

pygame.draw.ellipse(cropped_background, (255, 255, 255, 255), (0, 0, *size))
cropped_background.blit(background, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill(0)
    window.blit(cropped_background, (0, 0))
    pygame.display.flip()