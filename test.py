import pygame
from consts import *
screen = pygame.display.set_mode((600,600))
def generate_outline(pic_list,a,b):
    outline_list = []
    for pic in pic_list:
        surf = pygame.Surface((a,b))
        surf.set_colorkey((0,0,0))
        mask = pygame.mask.from_surface(pic)
        pic_mask = mask.to_surface()
        pic_mask.set_colorkey((0,0,0))
        surf.blit(pic_mask,(0,1))
        surf.blit(pic_mask,(0,-1))
        surf.blit(pic_mask,(1,0))
        surf.blit(pic_mask,(-1,0))
        surf.blit(pic,(0,0))
        outline_list.append(surf)
    return outline_list

outlines = generate_outline([RED_CAR,BLUE_CAR],50,50)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    #for pic in outlines:
     #   screen.blit(pic,(0,0))
    
    screen.blit(TRACK_BORDER_MASK.to_surface(),(0,0))
    pygame.display.flip()