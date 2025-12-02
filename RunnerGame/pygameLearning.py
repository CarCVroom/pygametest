import pygame
from sys import exit

pygame.init() # Starts pygame
screen = pygame.display.set_mode((800,400)) # Sets window size NOTE 0,0 is at the top left
pygame.display.set_caption("Runner") # Sets window name
clock = pygame.time.Clock() 
testFont = pygame.font.Font("RunnerGame/font/Pixeltype.ttf", 50) #Change/remove "Python/" depending on laptop or PC

skySurface = pygame.image.load("RunnerGame/graphics/Sky.png").convert()
groundSurface = pygame.image.load("RunnerGame/graphics/ground.png").convert()
# Lookes for files in ProgrammeringVS, so use path from there 
textSurface = testFont.render("My game for now", False, "Black")


snail_surf = pygame.image.load("RunnerGame/graphics/snail/snail1.png").convert_alpha ()
snail_rect = snail_surf.get_rect(midbottom = (600,300)) # Makes a rectangle

player_surf = pygame.image.load("RunnerGame/graphics/player/player_walk_1.png").convert_alpha() 
player_rect = player_surf.get_rect(midbottom = (80,300))

while True:
    # Everything happens in here
    for event in pygame.event.get(): # Listens for player input
        if event.type == pygame.QUIT:
            pygame.quit() # Ends pygame
            exit() # Ends while True statment with sys

    screen.blit(skySurface, (0,0)) 
    screen.blit(groundSurface, (0,300))
    screen.blit(textSurface, (300,50))

    snail_rect.x -= 4
    if snail_rect.right <= 0:
        snail_rect.left = 800
    screen.blit(snail_surf, snail_rect) # Sets rectangle as pos
    screen.blit(player_surf, player_rect)

    if player_rect.colliderect(snail_rect):  # No collision = 0, collision = 1 Or True or False
        print("collision")
        
    pygame.display.update() # Keeps the window open
    clock.tick(60) # Sets framecap
