import pygame

from game import Game
from gui import GUI
from render_manager import RenderManager
from state import State

class Manager:
    WIDTH = 600
    HEIGHT = 600
    FPS = 30
    
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode([self.WIDTH, self.HEIGHT], pygame.RESIZABLE)
        pygame.display.set_caption("Monopoly")
        
        self.state = State.MAIN_MENU
        self.gui = GUI(self)
        self.game = Game(self)
        self.render_mgr = RenderManager(self)
        
        self.clock = pygame.time.Clock()
    
    def mainloop(self):
        while self.state != State.STOP:
            self.handle_events(pygame.event.get())
            self.render()
            self.clock.tick(self.FPS)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.quit()
    
    def render(self):
        self.render_mgr.render()
    
    def quit(self):
        self.state = State.STOP