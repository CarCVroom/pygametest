import pygame
from sys import exit

pygame.init() # Starts pygame
screen = pygame.display.set_mode((800,400)) # Sets window size NOTE 0,0 is at the top left
pygame.display.set_caption("Runner") # Sets window name
clock = pygame.time.Clock() 
testFont = pygame.font.Font("Python/RunnerGame/font/Pixeltype.ttf", 50)

skySurface = pygame.image.load("Python/RunnerGame/graphics/Sky.png").convert()
groundSurface = pygame.image.load("Python/RunnerGame/graphics/ground.png").convert()
# Lookes for files in ProgrammeringVS, so use path from there 
textSurface = testFont.render("My game for now", False, "Black")

snailSurface = pygame.image.load("Python/RunnerGame/graphics/snail/snail1.png").convert_alpha ()
snail_x_pos = 600 

while True:
    # Everything happens in here
    for event in pygame.event.get(): # Listens for player input
        if event.type == pygame.QUIT:
            pygame.quit() # Ends pygame
            exit() # Ends while True statment with sys

    screen.blit(skySurface, (0,0)) 
    screen.blit(groundSurface, (0,300))
    screen.blit(textSurface, (300,50))
    snail_x_pos -= 4
    if snail_x_pos < -100: # Use <, not ==
        snail_x_pos = 800     
    screen.blit(snailSurface,(snail_x_pos,250))

    pygame.display.update() # Keeps the window open
    clock.tick(60) # Sets framecap
