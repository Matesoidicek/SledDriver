import pygame, sys
import ButtonMaker

pygame.init()
width, height = 1900, 1000
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


#       FONT
font = pygame.font.Font(None, 36)

# ---------------------------------------------------------------- GAME SCENE ----------------------------------------------------------------

def game():
    running_game = True
    
    # Loading sled image
    sled_old = pygame.image.load('img/snow_sled.png')
    sled_new = pygame.transform.scale(sled_old, (80,80))
    sled_rect = sled_new.get_rect()

    # Player variables

    player_x, player_y = width // 2, height // 2
    player_speed = 0
    max_speed = 5
    acceleration = 0.1
    deceleration = 0.2
    rotation_speed = 5


# ---------------------------------------------------------------- MAIN GAME LOOP ----------------------------------------------------------------

    while running_game:

        # Background

        screen.fill((0,205,255))
        
    # Player loading


        # Controlling the sled
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_y -= player_speed
        if keys[pygame.K_s]:
            player_y += player_speed
        if keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_d]:
            player_x += player_speed

        

        # Calculate fps
        fps = clock.get_fps()
        # Render FPS text
        fps_text = font.render(f"FPS: {int(fps)}", True, "Black")
        screen.blit(fps_text, (10,10))

        clock.tick(60)
        print(clock)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
                pygame.quit()
                sys.exit()
                
        pygame.display.update()

# ---------------------------------------------------------------- MAIN MENU SCENE ----------------------------------------------------------------


def main_menu():
    #       FONT

            # Buttons

    # Load button images
    play_img = pygame.image.load('img/btn_play.png').convert_alpha()
    options_img = pygame.image.load('img/btn_options.png').convert_alpha()
    exit_img = pygame.image.load('img/btn_exit.png').convert_alpha()

    # Create buttons

    play_btn = ButtonMaker.Button(675, 310, play_img, 1)
    options_btn = ButtonMaker.Button(675, 495, options_img, 1)
    exit_btn = ButtonMaker.Button(675, 680, exit_img, 1)


    running_menu = True
    background = pygame.image.load('img/bg.png')


# ---------------------------------------------------------------- MAIN MENU LOOP ----------------------------------------------------------------

    while running_menu:

        screen.blit(background, (0,0))
        pygame.display.set_caption('Main Menu')



        # Drawing buttons

        if play_btn.draw(screen):
            running_menu = False
            game()
        if options_btn.draw(screen):
            running_menu = False
            print("options")
        if exit_btn.draw(screen):
            running_menu = False
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_menu = False
                pygame.quit()
                sys.exit()

        # Calculate fps
        fps = clock.get_fps()
        # Render FPS text
        fps_text = font.render(f"FPS: {int(fps)}", True, "Black")
        screen.blit(fps_text, (10,10))




        pygame.display.update()
        
        print("MAIN MENU")
        # CLOCK
        clock.tick(25)

main_menu()

# GAME



