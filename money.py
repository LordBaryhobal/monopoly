import pygame

from colors import Colors
from font_manager import FontManager

class Money:
    BILLS = [
        [1, Colors.BILL_0],
        [5, Colors.BILL_1],
        [10, Colors.BILL_2],
        [20, Colors.BILL_3],
        [50, Colors.BILL_4],
        [100, Colors.BILL_5],
        [500, Colors.BILL_6]
    ]
    
    _resized = {}
    
    def resize(width):
        Money._resized = {}
        for val, img in Money.BILLS:
            img = pygame.transform.scale(img, [width, width*img.get_height()/img.get_width()])
            Money._resized[val] = img
    
    def get(val):
        return Money._resized[val]

    def init():
        font = FontManager.get("Times New Roman", 75, bold=True)
        for i, [value, color] in enumerate(Money.BILLS):
            surf = pygame.Surface([500, 250], pygame.SRCALPHA)
            surf.fill((255,255,255, 50))
            pygame.draw.rect(surf, (0,0,0,50), [20, 20, 460, 210])
            pygame.draw.rect(surf, (0,0,0,0), [40, 40, 420, 170])
            pygame.draw.rect(surf, (0,0,0,150), [20, 20, 460, 210], 2)
            pygame.draw.rect(surf, (0,0,0,150), [40, 40, 420, 170], 2)
            pygame.draw.ellipse(surf, (255,255,255,100), [160,50,180,150])
            pygame.draw.ellipse(surf, (0,0,0,100), [170,60,160,130], 5)
            txt = font.render(str(value), True, (0,0,0))
            txt.set_alpha(200)
            surf.blit(txt, [250-txt.get_width()/2, 125-txt.get_height()/2])
            
            bill = pygame.Surface([500, 250])
            bill.fill(color)
            bill.blit(surf, [0, 0])
            Money.BILLS[i][1] = bill