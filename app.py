import pygame
import sys, math, Button, time
from utils import scale_image, blit_rotate_center

# Global variables
width, height = 1280, 720
FPS = 60

# Loading images
BACKGROUND = pygame.image.load('img/bg.png')
EXIT_BUTTON = pygame.image.load('img/btn_exit.png')
PLAY_BUTTON = pygame.image.load('img/btn_play.png')
OPTIONS_BUTTON = pygame.image.load('img/btn_options.png')
SLED = pygame.image.load('img/sled.png')
SLED = scale_image(SLED, 2)

# ---------------------------------------------------------------- Game ----------------------------------------------------------------
class Game:

    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.GameStateManager = GameStateManager('start')
        self.start = Start(self.screen, self.GameStateManager)
        self.level = Level(self.screen, self.GameStateManager)

        self.states = {'start':self.start, 'level':self.level}

    # GAME
    def run(self):
        while True:
            # quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.states[self.GameStateManager.get_state()].run()
            
            pygame.display.update()
            self.clock.tick(FPS)

# ---------------------------------------------------------------- Level ----------------------------------------------------------------


class Level:
    # ---------------------------------------------------------------- Abstract sled & Player sled class ----------------------------------------------------------------

    class AbstractSled:

        def __init__(self, max_vel, rotation_vel):
            self.img = self.IMG
            self.max_vel = max_vel
            self.vel = 0
            self.rotation_vel = rotation_vel
            self.angle = 0
            self.x, self.y = self.START_POS
            self.acceleration = 0.1

        def rotate(self, left=False, right=False):
            if left:
                self.angle += self.rotation_vel
            elif right:
                self.angle -= self.rotation_vel

        def draw(self, screen):
            blit_rotate_center(screen, self.img, (self.x, self.y), self.angle)
        
        def move_forward(self):
            self.vel = min(self.vel + self.acceleration, self.max_vel)
            self.move()
        
        def move_backward(self):
            self.vel = max(self.vel - self.acceleration,  - self.max_vel / 2)
            self.move()
        
        def move(self):
            radians = math.radians(self.angle)
            vertical = math.cos(radians) * self.vel
            horizontal = math.sin(radians) * self.vel

            self.y -= vertical
            self.x -= horizontal
            


# ---------------------------------------------------------------- Player car class ----------------------------------------------------------------
    class PlayerSled(AbstractSled):
        IMG = SLED
        START_POS = (width // 2, height // 2)

        def reduce_speed(self):
            self.vel = max(self.vel - self.acceleration / 2, 0)
            self.move()
    
    def draw_game(self, screen, images, player_sled):
        for img, pos in images:
            screen.blit(img, pos)

        player_sled.draw(screen)


    # ---------------------------------------------------------------- Move Player ----------------------------------------------------------------

    def move_player(self, player_sled):
        # Get keys to variable
        keys = pygame.key.get_pressed()
        # check if moving
        moved = False

        # Get input and react to it appropriately
        if keys[pygame.K_w]:
            moved = True
            self.player_sled.move_forward()
        if keys[pygame.K_s]:
            moved = True
            self.player_sled.move_backward()
        if keys[pygame.K_a] and abs(player_sled.vel) > 0.5:#(keys[pygame.K_w] or keys[pygame.K_s]):
            self.player_sled.rotate(left=True)
        if keys[pygame.K_d] and abs(player_sled.vel) > 0.5:#(keys[pygame.K_w] or keys[pygame.K_s]):
            self.player_sled.rotate(right=True)

        if not moved:
            
            self.player_sled.reduce_speed()

    # Variables 
    player_sled = PlayerSled(4,4)
    images = [(BACKGROUND, (0,0))]

    # ----- __init__ -----
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager
    


    # ----- Main game loop-----

    def run(self):
        self.draw_game(self.screen, self.images, self.player_sled)


        # Calling function move_player
        self.move_player(self.player_sled)











# ---------------------------------------------------------------- Menu ----------------------------------------------------------------


class Start:
    
    # ----- __INIT__ -----
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager

    #  Main menu loop
    def run(self):

        # Background
        self.screen.blit(BACKGROUND, (0,0))

        # Create buttons
        play_btn = Button.Button(width // 2 - 137.5, height // 4, PLAY_BUTTON, 0.5)
        options_btn = Button.Button(width // 2 - 137.5, height // 2.5, OPTIONS_BUTTON, 0.5)
        exit_btn = Button.Button(width // 2 - 137.5, height // 1.8, EXIT_BUTTON, 0.5)

        # Main menu buttons
        if play_btn.draw(self.screen):
            self.gameStateManager.set_state('level')
        if options_btn.draw(self.screen):
            pass
        if exit_btn.draw(self.screen):
            pygame.quit()
            sys.exit()




# ---------------------------------------------------------------- GameStateManager ----------------------------------------------------------------

class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
        
    def get_state(self):
        return self.currentState
    
    def set_state(self, state):
        self.currentState = state

if __name__ == "__main__":
    game = Game()
    game.run()