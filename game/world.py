from typing import List
import pygame

from game.object import GameObject
from game.ship import Lander

DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720
BACKGROUND_COLOR = "black"
FPS = 60

class World :
    run: bool
    dt: float
    player: Lander
    screen: pygame.Surface
    clock: pygame.time.Clock
    size: pygame.Vector2
    objects: List[GameObject]
    
    def __init__(self, width = DEFAULT_WIDTH, height = DEFAULT_HEIGHT) -> None:
        self.size = pygame.Vector2(width, height)
        self.objects = list()
        self.run = True
        self.dt = 0
        self.player = Lander(DEFAULT_WIDTH / 2, DEFAULT_HEIGHT / 2)
        
        
    def add(self, obj: GameObject) -> None:
        self.objects.append(obj)
        
    def loop(self) ->None:
        while self.run:
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    self.run = False
                    
            self.screen.fill(BACKGROUND_COLOR)
            
            self.player.reset()
                    
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_SPACE]:
                self.player.boost(0.1)
            if keys[pygame.K_LEFT]:
                self.player.rotate_left(0.1)
            if keys[pygame.K_RIGHT]:
                self.player.rotate_right(0.1)
            
            self.player.gravity()
            self.player.damping()
            self.player.update(self.dt)
            self.player.draw(self.screen)
            
            pygame.display.flip()
            
            self.dt = self.clock.tick(FPS) / 1000
        
    def start(self) -> None:
        pygame.init()
        
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        
        self.loop()