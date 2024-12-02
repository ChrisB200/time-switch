import pygame
import logging
import sys

from scripts.entity import Entity, Player, Controls
from scripts.animation import load_animations
from scripts.renderer import Window
from scripts.input import Keyboard
from scripts.map import Tile, TileMap

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

        self.window = Window((1920, 1080), 3)
        self.assets = load_animations(ASSET_PATH)
        self.clock = pygame.time.Clock()
        self.key_controls = Controls(pygame.K_a, pygame.K_d, pygame.K_SPACE)
        self.keyboard = Keyboard(self.key_controls)
        self.dt = 1

        self.entities = pygame.sprite.Group()
        self.tile_map = TileMap()

        self.player = Player(self.assets, "player", (50, 50), (9, 18), self.keyboard)
        self.player.set_offset((-2, 0), False)
        self.player.set_offset((-2, 0), True)

        tile = Tile((100, 0, 0), (0, 200), (600, 20))
        self.tile_map.add(tile)

    def draw(self):
        self.window.screen.fill((200, 200, 200))

        for e in self.entities:
            e.draw(self.window)
        self.player.draw(self.window)
        self.tile_map.draw(self.window)
        self.window.draw()
        pygame.display.flip()

    def event_handler(self):
        for event in pygame.event.get():
            for e in self.entities:
                e.event_handler(event)
            self.player.event_handler(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        self.dt = self.clock.tick(60) / 1000
        for e in self.entities:
            e.update(self.dt)
        self.player.update(self.dt, self.tile_map)
        self.window.set_target(self.player)
        self.window.update()

    def run(self):
        while True:
            self.draw()
            self.update()
            self.event_handler()


if __name__ == "__main__":
    game = Game()
    game.run()
