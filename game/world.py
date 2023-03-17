from typing import List
import pygame
from game.constants import BLACK, WHITE

from game.object import GameObject
from game.ship import Lander

DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720
BACKGROUND_COLOR = BLACK
FPS = 60
LANDER_SPEED = 0.1

class World :
    def __init__(self, width = DEFAULT_WIDTH, height = DEFAULT_HEIGHT) -> None:
        pygame.init()
        
        self.size = pygame.Vector2(width, height)
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.run = True
        self.dt = 0
        self.player = Lander(DEFAULT_WIDTH / 2, DEFAULT_HEIGHT / 2)
        self.font = pygame.font.Font(None, 32)
        
    def loop(self) ->None:
        while self.run:
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    self.run = False
                    
            self.screen.fill(BACKGROUND_COLOR)
            
            self.player.reset()
                    
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_SPACE]:
                self.player.boost(LANDER_SPEED)
            if keys[pygame.K_LEFT]:
                self.player.rotate_left(LANDER_SPEED)
            if keys[pygame.K_RIGHT]:
                self.player.rotate_right(LANDER_SPEED)
            
            self.player.gravity()
            self.player.damping()
            self.player.update(self.dt)
            self.player.draw(self.screen)
            
            
            self.display_stats()
            pygame.display.flip()
            
            self.dt = self.clock.tick(FPS) / 1000
            
    def display_stats(self) :
        velX = self.font.render(f"velocityX: {round(self.player.velocity.x, 1)}", True, WHITE, BACKGROUND_COLOR)
        velY = self.font.render(f"velocityY: {round(self.player.velocity.y, 1)}", True, WHITE, BACKGROUND_COLOR)

        velXRect = velX.get_rect()
        velXRect.top = 0
        velXRect.left = 0
        
        velYRect = velY.get_rect()
        velYRect.top = velYRect.height
        velYRect.left = 0
        
        self.screen.blit(velX, velXRect)
        self.screen.blit(velY, velYRect)
        
    def start(self) -> None:
        self.loop()