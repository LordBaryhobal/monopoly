import pygame

from colors import Colors
from cells import PropertyCell, SpecialPropertyCell
from font_manager import FontManager
from i18n import I18n
from money import Money
from state import State

class RenderManager:
    CORNERS = [
        (0, 0),
        (1, 0),
        (1, 1),
        (0, 1)
    ]
    OFFSETS = [
        [(1, 0), (0, 1)],
        [(0, 1), (-1, 0)],
        [(-1, 0), (0, -1)],
        [(0, -1), (1, 0)]
    ]
    
    BORDER_WIDTH = 2
    
    def __init__(self, manager):
        self.mgr = manager
        self.game = self.mgr.game
        self.win = self.mgr.win
        self.unit = 0
    
    def render(self):
        self.overlay = pygame.Surface(self.win.get_size(), pygame.SRCALPHA)
        self.win.fill(Colors.BG)
        self.overlay.fill((0,0,0,0))
        state = self.mgr.state
        
        if state == State.IN_GAME or state == State.PAUSE:
            self.render_game()
            self.win.blit(self.overlay, [0, 0])
            
            if state == State.PAUSE:
                s = pygame.Surface(self.win.get_size(), pygame.SRCALPHA)
                s.fill(Colors.PAUSE_OVERLAY)
                self.win.blit(s, [0, 0])

        if state in [State.MAIN_MENU, State.PAUSE]:
            self.mgr.gui.render(self.win)

        pygame.display.flip()
    
    def render_game(self):
        W, H = self.mgr.WIDTH, self.mgr.HEIGHT
        self.board_size = min(H, W/2)
        self.board_size = self.board_size//37*37
        self.hmargin = (W-self.board_size)/2
        self.vmargin = (H-self.board_size)/2
        
        unit = self.board_size / 37
        self.s = unit*3
        self.S = unit*5
        
        if unit != self.unit:
            self.unit = unit
            self.mgr.on_resized()
        
        pygame.draw.rect(self.win, Colors.BOARD, [self.hmargin, self.vmargin, self.board_size, self.board_size])
    
        name_font = FontManager.get("ubuntu condensed", 12)
        mx, my = pygame.mouse.get_pos()
    
        hover = False
        for i in range(40):
            cell, x, y, rot = self.game.get_cell(i)
            X, Y = self.get_pos(x, y)
            if i%10 == 0:
                w, h = self.S, self.S
            
            elif i%20 < 10:
                w, h = self.s, self.S
            
            else:
                w, h = self.S, self.s
            
            cell.rect = [X, Y, w, h]
            
            if isinstance(cell, PropertyCell):
                if rot % 2 == 0:
                    w2, h2 = self.s, unit
                else:
                    w2, h2 = unit, self.s
                
                x, y = X, Y
                if rot == 1:
                    x = X+self.S-w2
                
                elif rot == 2:
                    y = Y+self.S-h2
                
                offset = 1/5 if isinstance(cell, SpecialPropertyCell) else 2/5
                self.render_text(cell.name, name_font, Colors.PROPERTY_NAME, rot, X, Y, w, h, 0.5, offset)
                
                if not isinstance(cell, SpecialPropertyCell):
                    color = cell.get_color()
                    pygame.draw.rect(self.win, color, [x, y, w2, h2])
                
                if cell.owner is not None:
                    player = self.game.players[cell.owner]
                    color = player.get_color()
                    
                    if rot % 2 == 0:
                        w3, h3 = unit*2, 10
                    else:
                        w3, h3 = 10, unit*2
                    
                    x, y = self.get_rel_pos(w, h, rot, 0.5, 1)
                    x += X
                    y += Y
                    
                    dx, dy = self.OFFSETS[rot][1]
                    dx, dy = dx*10, dy*10
                    x += dx
                    y += dy
                    
                    pygame.draw.rect(self.win, color, [x-w3/2, y-h3/2, w3, h3])
            
            """if X < mx < X+w and Y < my < Y+h:
                b = self.BORDER_WIDTH
                pygame.draw.rect(self.overlay, Colors.HOVER, [X+b, Y+b, w-b, h-b])
                hover = True"""
        
        """
        if hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)"""
        
        # Borders
        
        pygame.draw.lines(self.win, Colors.BORDER, True, [
            [self.hmargin, self.vmargin],
            [W-self.hmargin, self.vmargin],
            [W-self.hmargin, H-self.vmargin],
            [self.hmargin, H-self.vmargin]
        ], self.BORDER_WIDTH)
        
        pygame.draw.lines(self.win, Colors.BORDER, True, [
            [self.hmargin+self.S, self.vmargin+self.S],
            [W-self.hmargin-self.S, self.vmargin+self.S],
            [W-self.hmargin-self.S, H-self.vmargin-self.S],
            [self.hmargin+self.S, H-self.vmargin-self.S]
        ], self.BORDER_WIDTH)
        
        x1, x2 = self.hmargin, self.hmargin+self.S
        x3, x4 = W-self.hmargin, W-self.hmargin-self.S
        y1, y2 = self.vmargin, self.vmargin+self.S
        y3, y4 = H-self.vmargin, H-self.vmargin-self.S
        
        for i in range(1, 11):
            x, y = self.get_pos(i, i)
            pygame.draw.line(self.win, Colors.BORDER, [x, y1], [x, y2], self.BORDER_WIDTH)
            pygame.draw.line(self.win, Colors.BORDER, [x, y3], [x, y4], self.BORDER_WIDTH)
            pygame.draw.line(self.win, Colors.BORDER, [x1, y], [x2, y], self.BORDER_WIDTH)
            pygame.draw.line(self.win, Colors.BORDER, [x3, y], [x4, y], self.BORDER_WIDTH)

        
        # Players
        for player in self.game.players:
            cell, x, y, rot = self.game.get_cell(player.pos)
            px = (player.id%4)/5 + 0.2
            py = (player.id//4)*0.2 + 0.7
            
            if player.pos%10 == 0:
                w, h = self.S, self.S
            
            elif player.pos%20 < 10:
                w, h = self.s, self.S
            
            else:
                w, h = self.S, self.s
            
            X, Y = self.get_pos(x, y)
            x, y = self.get_rel_pos(w, h, rot, px, py)
            
            r = 0.1*self.s if player is self.game.player else 0.08*self.s
            pygame.draw.circle(self.win, player.get_color(), [X+x, Y+y], r)
        
        # Money
        y = 20
        font = FontManager.get("arial", 20)
        for val, count in self.game.player.money.items():
            if count == 0: continue
            img = Money.get(val)
            txt = f"{count}x "
            txt = font.render(txt, True, Colors.MONEY)
            h = max(txt.get_height(), img.get_height())
            self.win.blit(txt, [W-20-img.get_width()-txt.get_width(), y+h/2-txt.get_height()/2])
            self.win.blit(img, [W-20-img.get_width(), y+h/2-img.get_height()/2])
            y += h + 10
        
        # Actions
        font_title = FontManager.get("arial", 40)
        title = font_title.render(I18n.get("gui.actions"), True, Colors.ACTIONS_TITLE)
        self.win.blit(title, [self.hmargin/2-title.get_width()/2, 20])
        y = 40 + title.get_height()
        
        for action in self.game.actions:
            txt = font.render(I18n.get(action.I18N), True, Colors.ACTIONS)
            self.win.blit(txt, [self.hmargin/2-txt.get_width()/2, y])
            y += txt.get_height() + 20
    
    def get_pos(self, x, y):
        X = 0 if x == 0 else self.S + (x-1)*self.s
        Y = 0 if y == 0 else self.S + (y-1)*self.s
        X += self.hmargin
        Y += self.vmargin
        return (X, Y)

    def get_rel_pos(self, w, h, rot, rx, ry):
        corner = self.CORNERS[rot]
        offx, offy = self.OFFSETS[rot]
        
        ox, oy = corner[0]*w, corner[1]*h
        w, h = abs(offx[0]*w + offx[1]*h), abs(offy[0]*w + offy[1]*h)
        
        x = ox + offx[0]*rx*w + offy[0]*ry*h
        y = oy + offx[1]*rx*w + offy[1]*ry*h
        return (x, y)

    def render_text(self, text, font, color, rot, ox, oy, w, h, x, y):
        text = I18n.get(text)
        lines = text.split("\n")
        
        lines = list(map(lambda l: font.render(l, True, color), lines))
        widths = map(lambda l: l.get_width(), lines)
        heights = map(lambda l: l.get_height(), lines)
        tot_h = sum(heights)
        tot_w = max(widths)
        
        surf = pygame.Surface([tot_w, tot_h], pygame.SRCALPHA)
        surf.fill((0,0,0,0))
        
        Y = 0
        for line in lines:
            X = tot_w/2 - line.get_width()/2
            surf.blit(line, [X, Y])
            
            Y += line.get_height()
            #tx, ty = self.get_rel_pos(w, h, rot, x, y)
            #tx = ox+tx
            #ty = oy+ty
        
        surf = pygame.transform.rotate(surf, -90 * rot)
        X, Y = self.get_rel_pos(w, h, rot, x, y)
        X, Y = ox+X, oy+Y
        
        self.win.blit(surf, [X-surf.get_width()/2, Y-surf.get_height()/2])
        #self.win.blit(text, [tx-text.get_width()/2, ty-text.get_height()/2])