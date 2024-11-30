import pygame
import logging
import sys

from scripts.entities import Entity
from scripts.animation import load_animations
from scripts.renderer import Window

ASSET_PATH = "data/images/"

logging.basicConfig(
    level=logging.INFO,  # set the log level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.FileHandler("game.log"),  # Log to a file
        logging.StreamHandler()          # Also log to console
    ]
)

logger = logging.getLogger(__name__)

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        pygame.joystick.init()

        self.window = Window((1920, 1080), 4)
        self.assets = load_animations(ASSET_PATH)
        self.clock = pygame.time.Clock()
        self.e = Entity(self.assets, (50, 50), (24, 24), "newPlayer")

    @property
    def dt(self):
        return self.clock.tick() / 1000

    def draw(self):
        self.window.draw()
        self.window.screen.fill((100, 100, 100))
        self.e.draw(self.window)
        pygame.display.flip()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        self.e.update_animation(self.dt)

    def run(self):
        while True:
            self.draw()
            self.update()
            self.event_handler()


if __name__ == "__main__":
    game = Game()
    game.run()
