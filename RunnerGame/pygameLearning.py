import pygame
from sys import exit

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000)- start_time
    score_surf = testFont.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)

def fps_counter():
    fps = clock.get_fps()
    fps_surf = FPS_Font.render(f'{fps:.0f}', False, (0,0,0))
    fps_rect = fps_surf.get_rect(topleft = (10,10))
    screen.blit(fps_surf, fps_rect)

pygame.init() # Starts pygame
screen = pygame.display.set_mode((800,400)) # Sets window size NOTE 0,0 is at the top left
pygame.display.set_caption("Runner") # Sets window name
clock = pygame.time.Clock() 
testFont = pygame.font.Font("RunnerGame/font/Pixeltype.ttf", 50) 
FPS_Font = pygame.font.Font("RunnerGame/font/Pixeltype.ttf", 25) 
game_active = False 
start_time = 0

skySurface = pygame.image.load("RunnerGame/graphics/Sky.png").convert()
groundSurface = pygame.image.load("RunnerGame/graphics/ground.png").convert()
# Lookes for files in Root directory, so use path from there 

# Text
# text_score = testFont.render("My game", False, (64,64,64))
# text_score_rect = text_score.get_rect(midtop = (400,20))

# Player and snail Models
snail_surf = pygame.image.load("RunnerGame/graphics/snail/snail1.png").convert_alpha ()
snail_rect = snail_surf.get_rect(midbottom = (600,300)) # Makes a rectangle

player_surf = pygame.image.load("RunnerGame/graphics/player/player_walk_1.png").convert_alpha() 
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

#Intro screen
player_stand = pygame.image.load("RunnerGame/graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

intro_text1_surf = testFont.render("Pixel Runner!", False, (111,196,169))
intro_text1_rect = intro_text1_surf.get_rect(center = (400, 70))

intro_text2_surf = testFont.render("Press space to start!", False, (0,0,0))
intro_text2_rect = intro_text2_surf.get_rect(center = (400, 330))

while True:
    # Everything happens in here
    for event in pygame.event.get(): # Listens for player input
        if event.type == pygame.QUIT:
            pygame.quit() # Ends pygame
            exit() # Ends while True statment with sys

        if game_active:    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity= -20


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                start_time = int(pygame.time.get_ticks() / 1000)
               

    if game_active:    
        screen.blit(skySurface, (0,0)) 
        screen.blit(groundSurface, (0,300))
        # pygame.draw.rect(screen, "#c0e8ec", text_score_rect,)
        # pygame.draw.rect(screen, "#c0e8ec", text_score_rect, 10)
        # screen.blit(text_score, text_score_rect)
        display_score()
        fps_counter()

        snail_rect.x -= 4
        if snail_rect.right <= 0:
            snail_rect.left = 800
        screen.blit(snail_surf, snail_rect) # Sets rectangle as pos

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)

        # collision
        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(intro_text1_surf,intro_text1_rect)
        screen.blit(intro_text2_surf,intro_text2_rect)


    pygame.display.update() # Keeps the window open
    clock.tick(60) # Sets framecap
