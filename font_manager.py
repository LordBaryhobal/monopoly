import pygame

from path import Path

class FontManager:
    _cache = {}
    
    def get(family, size, bold=False, italic=False):
        id_ = (family, size, bold, italic)
        if not id_ in FontManager._cache:
            if family.startswith("file:"):
                path = Path("assets", "fonts", family.split(":", 1)[1])
                FontManager._cache[id_] = pygame.font.Font(path, size)
            
            else:
                FontManager._cache[id_] = pygame.font.SysFont(family, size, bold=bold, italic=italic)
        
        return FontManager._cache[id_]