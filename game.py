import pygame, sys, os

# General setup
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Antarctis 2380')
base_font = pygame.font.Font(os.path.join('assets', 'font', 'NovaSquare.ttf'),80)
user_text = 'ANTARCTIS 2380'


# Display surface
screen = pygame.display.set_mode((1280, 720))
intro_background = pygame.image.load(os.path.join('assets', 'img', 'intro_bg8.png'))


while True:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("teal")
    screen.blit(intro_background,(0,0))
    text_surface = base_font.render(user_text,True,(255,255,255))
    screen.blit(text_surface,(610,10))



    pygame.display.flip()
    clock.tick(60)

pygame.quit()
