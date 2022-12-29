import pygame

from state import State

class RenderManager:
    def __init__(self, manager):
        self.mgr = manager
        self.game = self.mgr.game
        self.win = self.mgr.win
    
    def render(self):
        self.win.fill(0)
        state = self.mgr.state
        
        if state == State.MAIN_MENU:
            self.mgr.gui.render(self.win)
        
        pygame.display.flip()