import pygame
import sys, math, time
from utils import scale_image, blit_rotate_center
from Button import Button

# Global variables
width, height = 1280, 720
FPS = 60
pygame.init()


##### Map images
LEVEL_BACKGROUND = pygame.image.load('img/background_with_border.png')
LEVEL_BACKGROUND = scale_image(LEVEL_BACKGROUND, 10)

ROCKS = pygame.image.load('img/rocks_mask.png')
ROCKS = scale_image(ROCKS, 10)

BORDER = pygame.image.load('img/border_mask.png')
BORDER = scale_image(BORDER, 10)

##### Masks
ROCKS_MASK = pygame.mask.from_surface(ROCKS)
BORDER_MASK = pygame.mask.from_surface(BORDER)


##### Loading images
BACKGROUND = pygame.image.load('img/bg.png')
EXIT_BUTTON = pygame.image.load('img/btn_exit.png')
PLAY_BUTTON = pygame.image.load('img/btn_play.png')
OPTIONS_BUTTON = pygame.image.load('img/btn_options.png')
SLED = pygame.image.load('img/sled.png')
SLED = scale_image(SLED, 2)

# Button pos variables
PLAY_BTN = Button(width // 2 - 137.5, height // 4, PLAY_BUTTON, 0.5)
OPTION_BTN = Button(width // 2 - 137.5, height // 2.5, OPTIONS_BUTTON, 0.5)
EXIT_BTN = Button(width // 2 - 137.5, height // 1.8, EXIT_BUTTON, 0.5)

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
    ##### ----- __init__ -----
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager

    ##### Variables 
    images = [(LEVEL_BACKGROUND, (0,0)), (ROCKS, (0, 0)), (BORDER, (0, 0))]

    # ---------------------------------------------------------------- Abstract sled & Player sled class ----------------------------------------------------------------

    class AbstractSled:

        ##### ----- __init__ -----
        def __init__(self, max_vel, rotation_vel):
            self.img = self.IMG
            self.max_vel = max_vel
            self.vel = 0
            self.rotation_vel = rotation_vel
            self.angle = 0
            self.x, self.y = self.START_POS
            self.acceleration = 0.1

        ##### Rotate
        def rotate(self, left=False, right=False):
            if left:
                self.angle += self.rotation_vel
            elif right:
                self.angle -= self.rotation_vel

        ##### Draw
        def draw(self, screen):
            blit_rotate_center(screen, self.img, (self.x, self.y), self.angle)
        
        ##### Move forward
        def move_forward(self):
            self.vel = min(self.vel + self.acceleration, self.max_vel)
            self.move()
        
        ##### Move backwards
        def move_backward(self):
            self.vel = max(self.vel - self.acceleration,  - self.max_vel / 2)
            self.move()
        
        ##### Move sled
        def move(self):
            radians = math.radians(self.angle)
            vertical = math.cos(radians) * self.vel
            horizontal = math.sin(radians) * self.vel

            self.y -= vertical
            self.x -= horizontal
        
        ##### Collisions
        def collide(self, mask, x=0, y=0):
            sled_mask = pygame.mask.from_surface(self.img)
            offset = (int(self.x - x), int(self.y - y))
            poi = mask.overlap(sled_mask, offset)
            return poi



# ---------------------------------------------------------------- Player car class ----------------------------------------------------------------
    class PlayerSled(AbstractSled):

        # Some fookin variables i dont give a single fuck xd
        IMG = SLED
        health = 20
        START_POS = (width // 2, height // 2)
        
        ##### Reduce speed 
        def reduce_speed(self):
            self.vel = max(self.vel - self.acceleration / 2, 0)
            self.move()
        
        # Stop when collision :((
        def stop_collision(self):
            self.vel = -self.vel * 2
            self.health = self.health - 1 
    
    ##### Draw game easy
    def draw_game(self, screen, images, player_sled):
        for img, pos in images:
            screen.blit(img, pos)

        player_sled.draw(screen)


    # ---------------------------------------------------------------- Move Player ----------------------------------------------------------------

    def move_player(self, player_sled):
        
        ##### Get keys to variable
        keys = pygame.key.get_pressed()
        
        ##### check if moving
        moved = False

        ##### Get input and react to it appropriately
        if keys[pygame.K_w]:
            moved = True
            self.player_sled.move_forward()
        if keys[pygame.K_s]:
            moved = True
            self.player_sled.move_backward()
        if keys[pygame.K_a] and abs(player_sled.vel) > 0.2:
            self.player_sled.rotate(left=True)
        if keys[pygame.K_d] and abs(player_sled.vel) > 0.2:
            self.player_sled.rotate(right=True)

        ##### If not moved for accelerating and decelerating
        if not moved:
            self.player_sled.reduce_speed()

    ###### Settings cls PlayerSled to variable for drawing it.
    player_sled = PlayerSled(4,4)
    font = pygame.font.Font(None, 36)
    black = (0,0,0)

    ##### ----- Main game loop-----

    def run(self):

        ##### Drawing images with for loop
        self.draw_game(self.screen, self.images, self.player_sled)

        ##### Calling function move_player
        self.move_player(self.player_sled)
        # SHIATT
        text = self.font.render(f"{}", True, self.black)
        self.screen.blit(text, (100, 100))

        ##### collision detection
        if self.player_sled.collide(BORDER_MASK) != None:
            self.player_sled.stop_collision()


# ---------------------------------------------------------------- Menu Class ----------------------------------------------------------------
class Start:
    ##### List for images to draw with def draw_game
    images = [(BACKGROUND, (0,0))]

    ##### ----- __INIT__ -----
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager

    ##### Easy image drawing
    def draw_game(self, screen, images):
        for img, pos in images:
            screen.blit(img, pos)

    ##### Main menu buttons
    def Create_Buttons(self):
        if PLAY_BTN.draw(self.screen):
            self.gameStateManager.set_state('level')
        if OPTION_BTN.draw(self.screen):
            pass
        if EXIT_BTN.draw(self.screen):
            pygame.quit()
            sys.exit()

    #####  Main menu loop
    def run(self):
        
        ##### Easier image drawing
        self.draw_game(self.screen, self.images)

        ##### Creating Buttons trough def Create_Buttons
        self.Create_Buttons()



# ---------------------------------------------------------------- GameStateManager ----------------------------------------------------------------
class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
        
    def get_state(self):
        return self.currentState
    
    def set_state(self, state):
        self.currentState = state



# ---------------------------------------------------------------- Settings scenes ----------------------------------------------------------------
if __name__ == "__main__":
    game = Game()
    game.run()