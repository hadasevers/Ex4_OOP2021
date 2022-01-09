import pygame
from pygame import font, color,Color, draw, rect, Rect
from pygame import gfxdraw



font.init()
Font = font.SysFont('Calibri', 15, bold=False)
clock = pygame.time.Clock()




class Button:

    def __init__(self, title: str, pos) -> None:
        self.title = title
        self.size = (70, 20)
        self.pos = pos
        self.color = Color(43, 43, 43)
        self.rect = Rect(self.pos, self.size)

    def draw(self, screen):
        title_srf = Font.render(self.title, True, Color(43, 43, 43))
        title_rect = title_srf.get_rect(center=self.rect.center)
        #pygame.draw.rect(screen, Color(43, 43, 43), self.rect, width=1)  # מצייר את המסגרת של הכפתור
        screen.blit(title_srf, title_rect)



