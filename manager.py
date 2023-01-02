import pygame

from game import Game
from gui import GUI
from money import Money
from render_manager import RenderManager
from state import State

class Manager:
    WIDTH = 800
    HEIGHT = 600
    FPS = 30
    
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode([self.WIDTH, self.HEIGHT], pygame.RESIZABLE)
        
        self.state = State.MAIN_MENU
        self.gui = GUI(self)
        self.game = Game(self)
        self.render_mgr = RenderManager(self)
        
        self.clock = pygame.time.Clock()
        
        Money.init()
    
    def mainloop(self):
        while self.state != State.STOP:
            pygame.display.set_caption(f"Monopoly - {self.clock.get_fps():.2f}fps")
            self.handle_events(pygame.event.get())
            self.render()
            self.clock.tick(self.FPS)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.quit()
            
            elif event.type == pygame.VIDEORESIZE:
                self.WIDTH, self.HEIGHT = event.w, event.h
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.gui.on_mouse_down(event)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self.gui.on_mouse_up(event)
            
            elif event.type == pygame.USEREVENT+1:
                name = event.name
                
                if name == "main.quit":
                    self.quit()
                
                elif name == "main.play":
                    self.play()
                
                elif name == "pause.return":
                    self.resume()
                
                elif name == "pause.main":
                    self.gui.set_menu("main")
                    self.state = State.MAIN_MENU
            
            elif event.type == pygame.KEYDOWN:
                if self.state == State.IN_GAME:
                    if event.key == pygame.K_ESCAPE:
                        self.pause()
                    """if event.key == pygame.K_SPACE:
                        self.game.player.pos += 1
                        self.game.player.pos %= 40
                    
                    elif event.key == pygame.K_RETURN:
                        self.game.player.id += 1
                        self.game.player.id %= 8"""
                
                elif self.state == State.PAUSE:
                    if event.key == pygame.K_ESCAPE:
                        self.resume()
    
    def on_resized(self):
        Money.resize(self.render_mgr.hmargin/2)
    
    def render(self):
        self.render_mgr.render()
    
    def quit(self):
        self.state = State.STOP
    
    def play(self):
        self.gui.hide()
        self.state = State.IN_GAME
    
    def pause(self):
        self.gui.set_menu("pause")
        self.gui.show()
        self.state = State.PAUSE
    
    def resume(self):
        self.gui.hide()
        self.state = State.IN_GAME