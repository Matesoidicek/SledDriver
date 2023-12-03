import pygame
import sys, Button

# Global variables
width, height = 1280, 720
FPS = 60


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
    # Load player (sled)
    sled = pygame.image.load("img/sled")

    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager
    
    def run(self):
        
        # Background
        self.screen.fill((0,183,255))






# ---------------------------------------------------------------- Menu ----------------------------------------------------------------


class Start:
    
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager
    
    def run(self):

        # Background
        bg_image = pygame.image.load("img/bg.png")
        self.screen.blit(bg_image, (0,0))

        # Load button images
        play_image = pygame.image.load("img/btn_play.png")
        options_image = pygame.image.load("img/btn_options.png")
        exit_image = pygame.image.load("img/btn_exit.png")

        # Create buttons
        play_btn = Button.Button(width // 2 - 137.5, height // 4, play_image, 0.5)
        options_btn = Button.Button(width // 2 - 137.5, height // 2.5, options_image, 0.5)
        exit_btn = Button.Button(width // 2 - 137.5, height // 1.8, exit_image, 0.5)

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