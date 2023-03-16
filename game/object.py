import pygame

GRAVITY = 0.05

class GameObject:
    has_gravity: bool
    movex: float
    movey: float
    
    def __init__(self) -> None:
        self.has_gravity = True
        self.movex = 0
        self.movey = 0
    
    def draw(self, screen: pygame.Surface) -> None:
        raise NotImplementedError()
    
    def update(self, dt: float) -> None:
        raise NotImplementedError()
    
    def gravity(self) -> None:
        if self.has_gravity :
            self.movey += GRAVITY