from typing import Tuple
import pygame
import math
import copy

RED = (250, 0, 0)
GREEN = (0, 250, 0)

WIDTH = 50
HEIGHT = 100
GRAVITY = 0.05
DAMPING = 0.03

LANDER_BASE = 0
LANDER_BOOST_MAIN = 1
LANDER_BOOST_LEFT = 2
LANDER_BOOST_RIGHT = 3

class Lander(pygame.sprite.Sprite) :
    def __init__(self, x: float = 0, y: float = 0, width = WIDTH, height = HEIGHT) -> None:
        super(Lander, self).__init__()
        
        self.images = []
        self.images.append(pygame.image.load("game/sprites/lander/lander.png"))
        self.images.append(pygame.image.load("game/sprites/lander/lander-boost_main.png"))
        self.images.append(pygame.image.load("game/sprites/lander/lander-boost_left.png"))
        self.images.append(pygame.image.load("game/sprites/lander/lander-boost_right.png"))
        
        self.image = self.images[LANDER_BASE]
        
        self.width = width
        self.height = height
        self.color = RED
    
        # Angular
        self.rotation = 0
        self.angular_velocity = 0
        self.angular_acceleration = 0
        
        # Linear
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0)
        self.acceleration = pygame.Vector2(0)
        
        # self.surface = pygame.Surface((width, height))
        # self.surface.set_colorkey((0, 0, 0))
        # self.surface.fill(self.color)
        self.rect = self.image.get_rect()
        
        self.has_gravity = True
        self.boosting = False
        self.rotating = 0
        
        
    def draw(self, screen: pygame.Surface) -> None:
        # pygame.draw.rect(screen, self.color, self.rect)
        
        # self.surface.fill(self.color)
        # self.rect = self.surface.get_rect()
        # self.rect.center = (int(self.position.x), int(self.position.y))
        
        # self.surface.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.position.x), int(self.position.y))
        
        old_center = self.rect.center
        new = pygame.transform.rotate(self.image, -self.rotation)
        self.rect = new.get_rect()
        self.rect.center = old_center

        screen.blit(new, self.rect)
        
    def update(self, dt: float) -> None:
        self.velocity += self.acceleration
        self.position += self.velocity
        
        self.angular_velocity += self.angular_acceleration
        self.rotation += self.angular_velocity
        
        self.rect.x = int(self.position.x)
        self.rect.y = int(self.position.y)
    
    def gravity(self, amount: float = GRAVITY) -> None:
        if self.has_gravity:
            self.acceleration.y = amount
            
    def damping(self):
        if math.isclose(self.angular_velocity, 0, abs_tol=0.001):
            self.angular_velocity = 0
        
        if self.angular_velocity > 0 :
            self.angular_acceleration = -DAMPING
        elif self.angular_velocity < 0:
            self.angular_acceleration = DAMPING
        else :
            self.angular_acceleration = 0
    
    def boost(self, amount: float):
        self.velocity += pygame.Vector2(math.sin(math.radians(self.rotation)), -math.cos(math.radians(self.rotation))) * amount
        self.boosting = True
        self.image = self.images[LANDER_BOOST_MAIN]
        
    def rotate_right(self, angle: float) -> None:
        self.angular_velocity += angle % 360
        self.rotating = 1
        self.image = self.images[LANDER_BOOST_LEFT]
    
    def rotate_left(self, angle: float) -> None:
        self.angular_velocity -= angle % 360
        self.rotating = -1
        self.image = self.images[LANDER_BOOST_RIGHT]
        
    def reset(self):
        self.boosting = False
        self.rotating = 0
        self.image = self.images[LANDER_BASE]