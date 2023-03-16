from typing import Tuple
import pygame
import math
import copy

RED = (250, 0, 0)
GREEN = (0, 250, 0)

WIDTH = 50
HEIGHT = 100
GRAVITY = 0.05
DAMPING = 0.05

class Ship :
    width: int
    height: int
    color: Tuple[int, int, int]
    rotation: float
    
    has_gravity: bool
    rect: pygame.Rect
    position: pygame.Vector2
    velocity: pygame.Vector2
    acceleration: pygame.Vector2
    
    def __init__(self, x: float = 0, y: float = 0, width = WIDTH, height = HEIGHT) -> None:
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
        
        self.surface = pygame.Surface((width, height))
        self.surface.set_colorkey((0, 0, 0))
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()
        
        self.fire = pygame.Surface((width, height + 10))
        self.fire.set_colorkey((0, 0, 0))
        self.fire.fill((250, 250, 0))
        
        self.has_gravity = True
        self.boosting = False
        
        
    def draw(self, screen: pygame.Surface) -> None:
        # pygame.draw.rect(screen, self.color, self.rect)
        
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()
        self.rect.center = (int(self.position.x), int(self.position.y))
        
        old_center = self.rect.center
        new = pygame.transform.rotate(self.surface, -self.rotation)
        self.rect = new.get_rect()
        self.rect.center = old_center
        
        old_center_fire = copy.deepcopy(old_center)
        new_fire = pygame.transform.rotate(self.fire, -self.rotation)
        fire_rect = copy.deepcopy(self.rect)
        fire_rect.center = old_center_fire
        
        if self.boosting:
            screen.blit(new_fire, fire_rect)
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
        
    def rotate_right(self, angle: float) -> None:
        self.angular_velocity += angle % 360
    
    def rotate_left(self, angle: float) -> None:
        self.angular_velocity -= angle % 360
        
    def reset(self):
        self.boosting = False