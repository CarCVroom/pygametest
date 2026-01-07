import pygame
from sys import exit
from random import randint, choice
import math

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("RunnerGame/graphics/player/player_walk_1.png").convert_alpha() 
        player_walk_2 = pygame.image.load("RunnerGame/graphics/player/player_walk_2.png").convert_alpha() 
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("RunnerGame/graphics/player/jump.png").convert_alpha()
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("RunnerGame/audio/jump.mp3")
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
        if keys[pygame.K_a]:
            if self.rect.bottom >= 300:
                self.rect.x -= 6
            else:
                self.rect.x -= 4
        if keys[pygame.K_d]:
            if self.rect.bottom >= 300:
                self.rect.x += 6
            else:
                self.rect.x += 4

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def wall_check(self):
        if self.rect.left <= -1:
            self.rect.left = 0
        elif self.rect.right >= screen_width:
            self.rect.right = screen_width

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        self.wall_check()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == "fly":
            fly_1 = pygame.image.load("RunnerGame/graphics/fly/fly1.png").convert_alpha()
            fly_2 = pygame.image.load("RunnerGame/graphics/fly/fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        elif type == "snail":
            snail_1 = pygame.image.load("RunnerGame/graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("RunnerGame/graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
       
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(1100,1300),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)] # Same as playr animation, but with obstacles

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000)- start_time
    score_surf = testFont.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = ((screen_width / 2),50))
    screen.blit(score_surf, score_rect)
    return current_time

def fps_counter():
    fps = clock.get_fps()
    fps_surf = FPS_Font.render(f'{fps:.0f}', False, (0,0,0))
    fps_rect = fps_surf.get_rect(topleft = (10,10))
    screen.blit(fps_surf, fps_rect)

# def obstacle_movment(obstacle_list):
#     if obstacle_list:
#         for obstacle_rect in obstacle_list: # Gives temporary name to variables in obstacle_list
#             obstacle_rect.x -= 5

#             if obstacle_rect.bottom == 300:
#                 screen.blit(snail_surf,obstacle_rect)
#             else:
#                 screen.blit(fly_surf,obstacle_rect)

#         obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100] # Delates obstacles

#         return obstacle_list
#     else: return []

# def collisions(player,obstacles):
#     if obstacles:
#         for obstacles_rect in obstacles:
#             if player.colliderect(obstacles_rect): return False
#     return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        global respawn_start_time
        respawn_start_time = pygame.time.get_ticks()  # start the pause
        return False
    else: return True

# def player_animation():
#     # Walking on floor 
#     # Jump while jumping
#     global player_surf, player_index

#     if player_rect.bottom < 300:
#         # jump cuz player is jumping idiot
#         player_surf = player_jump
#     else: 
#         # Walk cuz he is walking
#         player_index += 0.1
#         if player_index >= len(player_walk): player_index = 0
#         player_surf = player_walk[int(player_index)]

screen_width = 1000
screen_height = 400

pygame.init() # Starts pygame
screen = pygame.display.set_mode((screen_width,screen_height)) # Sets window size NOTE 0,0 is at the top left
pygame.display.set_caption("Runner") # Sets window name
clock = pygame.time.Clock() 
testFont = pygame.font.Font("RunnerGame/font/Pixeltype.ttf", 50) 
FPS_Font = pygame.font.Font("RunnerGame/font/Pixeltype.ttf", 25) 
game_active = False 
start_time = 0
score = 0
bg_music = pygame.mixer.Sound("RunnerGame/audio/music.wav")
bg_music.set_volume(0.5)
bg_music.play(loops = -1)

#Groups
player = pygame.sprite.GroupSingle() # Makes a Group using Player class
player.add(Player())

obstacle_group = pygame.sprite.Group()

skySurface = pygame.image.load("RunnerGame/graphics/Sky.png").convert()
sky_surface_width = skySurface.get_width()
groundSurface = pygame.image.load("RunnerGame/graphics/ground.png").convert()
ground_surface_width = groundSurface.get_width()

#game variables
scroll_ground = 0
tiles_ground = math.ceil(screen_width / ground_surface_width) + 1
scroll_sky = 0
tiles_sky = math.ceil(screen_width / sky_surface_width) + 1

respawn_start_time = 0
respawn_delay = 200  # milliseconds, half a second

# Lookes for files in Root directory, so use path from there 

# Text
# text_score = testFont.render("My game", False, (64,64,64))
# text_score_rect = text_score.get_rect(midtop = (400,20))

# Snail
# snail_frame_1 = pygame.image.load("RunnerGame/graphics/snail/snail1.png").convert_alpha ()
# snail_frame_2 = pygame.image.load("RunnerGame/graphics/snail/snail2.png").convert_alpha ()
# snail_frames = [snail_frame_1,snail_frame_2]
# snail_frame_index = 0
# snail_surf = snail_frames[snail_frame_index]

# # Fly
# fly_frame_1 = pygame.image.load("RunnerGame/graphics/fly/fly1.png").convert_alpha()
# fly_frame_2 = pygame.image.load("RunnerGame/graphics/fly/fly2.png").convert_alpha()
# fly_frames = [fly_frame_1,fly_frame_2]
# fly_frame_index = 0
# fly_surf = fly_frames[fly_frame_index]

# obstacle_rect_list = []

# Player models
# player_walk_1 = pygame.image.load("RunnerGame/graphics/player/player_walk_1.png").convert_alpha() 
# player_walk_2 = pygame.image.load("RunnerGame/graphics/player/player_walk_2.png").convert_alpha() 
# player_walk = [player_walk_1,player_walk_2]
# player_index = 0
# player_jump = pygame.image.load("RunnerGame/graphics/player/jump.png").convert_alpha()

# player_surf = player_walk[player_index] # Picks an image
# player_rect = player_surf.get_rect(midbottom = (80,300))
# player_gravity = 0

#Intro screen
player_stand = pygame.image.load("RunnerGame/graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = ((screen_width / 2),200))

intro_text1_surf = testFont.render("Pixel Runner!", False, (111,196,169))
intro_text1_rect = intro_text1_surf.get_rect(center = ((screen_width / 2), 70))

intro_text2_surf = testFont.render("Press space to start!", False, (111,196,169))
intro_text2_rect = intro_text2_surf.get_rect(center = ((screen_width / 2), 330))

# Timer
obstacle_timer = pygame.USEREVENT + 1 # Add +1 to not fuck up pygame
pygame.time.set_timer(obstacle_timer, 1400) # 1st argument: What happens, 2nd argument: when it happens

snail_animation_timer = pygame.USEREVENT + 2 
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3 
pygame.time.set_timer(fly_animation_timer,200)

while True:
    # Everything happens in here
    for event in pygame.event.get(): # Listens for player input
        if event.type == pygame.QUIT:
            pygame.quit() # Ends pygame
            exit() # Ends while True statment with sys

        if game_active:    
            # if event.type == pygame.MOUSEBUTTONDOWN: # CLICK JUMP
            #     if player_rect.collidepoint(event.pos):
            #         player_gravity= -20


            # if event.type == pygame.KEYDOWN: # SPACEBAR JUMP
            #     if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
            #         player_gravity = -20

            if event.type == obstacle_timer: # I did it bitch # Obstcle_rect shit 
                obstacle_type = choice(["fly", "fly", "snail", "snail", "snail", "snail", "null", "null", "null"])
                if obstacle_type != "null":   # only create an obstacle if not "null"
                    obstacle_group.add(Obstacles(obstacle_type))
                # if randint(0,2):
                #     obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900,1100),300)))
                # else: 
                #     obstacle_rect_list.append(fly_surf.get_rect(midbottom = (randint(900,1100),210)))

            # if event.type == snail_animation_timer:
            #     if snail_frame_index == 0: snail_frame_index = 1
            #     else: snail_frame_index = 0
            #     snail_surf = snail_frames[snail_frame_index]

            # if event.type == fly_animation_timer:
            #     if fly_frame_index == 0: fly_frame_index = 1
            #     else: fly_frame_index = 0
            #     fly_surf = fly_frames[fly_frame_index]
                    

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if pygame.time.get_ticks() - respawn_start_time > respawn_delay:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)

        # if event.type == obstacle_timer and game_active: # Better to place it in the if game_active statment, but im lazy
        #     print("test")
               

    if game_active:    
        for i in range(0, tiles_sky):
            screen.blit(skySurface, (i * sky_surface_width + scroll_sky, 0)) 
        for i in range(0, tiles_ground): 
            screen.blit(groundSurface, (i * ground_surface_width + scroll_ground, 300))

        scroll_ground -= 5
        scroll_sky -= 0.3

        #scroll reset
        if abs(scroll_ground) > ground_surface_width:
            scroll_ground = 0
        if abs(scroll_sky) > sky_surface_width:
            scroll_sky = 0
        
        # pygame.draw.rect(screen, "#c0e8ec", text_score_rect,)
        # pygame.draw.rect(screen, "#c0e8ec", text_score_rect, 10)
        # screen.blit(text_score, text_score_rect)
        score = display_score() # remember to learn how functions and return properly works
        fps_counter()

        # snail_rect.x -= 4
        # if snail_rect.right <= 0:
        #     snail_rect.left = 800
        # screen.blit(snail_surf, snail_rect) # Sets rectangle as pos
        
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 300:
        #     player_rect.bottom = 300
        # player_animation()
        # screen.blit(player_surf, player_rect)

        # Player and Obstacles

        player.draw(screen) # Adds player group to the game 
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # Obstacle movment
        # obstacle_rect_list = obstacle_movment(obstacle_rect_list)

        # collision
        game_active = collision_sprite()
        # if snail_rect.colliderect(player_rect):
            # game_active = False
        # game_active = collisions(player_rect,obstacle_rect_list)
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        # obstacle_rect_list.clear()
        # player_rect.midbottom = (80,300)
        # player_gravity = 0

        score_message = testFont.render(f"Your score: {score}", False, (111,196,169)) # remember to learn how f string properly works
        score_message_rect = score_message.get_rect(center = ((screen_width/2),330))
        screen.blit(intro_text1_surf,intro_text1_rect)

        if score == 0: # Adds score if there is one 
            screen.blit(intro_text2_surf,intro_text2_rect)
        else:
            screen.blit(score_message,score_message_rect)


    pygame.display.update() # Keeps the window open
    clock.tick(60) # Sets framecap
