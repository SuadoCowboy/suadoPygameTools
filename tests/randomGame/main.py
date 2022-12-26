import pygame
import suadoPygameTools as pgTools

pygame.init()

WIDTH, HEIGHT = 800, 600
display = pygame.display.set_mode((WIDTH,HEIGHT))

clock = pygame.time.Clock()
target_fps = 100

keyInputHandler = pgTools.KeyInputHandler()

player = pygame.Rect(0,0,10,15)
playerColor = (0,0,0)
playerVelocity = 10

rectSize = (20,20)
def createRects():
    rects = [
        pygame.Rect(-1,0, 1,HEIGHT),
        pygame.Rect(WIDTH,0, 1,HEIGHT),
        pygame.Rect(0,-1, WIDTH,1),
        pygame.Rect(0,HEIGHT, WIDTH,1) # the map barriers
    ]
    for y in range(0, HEIGHT, rectSize[1]):
        for x in range(0, WIDTH, rectSize[0]):

            if not pgTools.randomChance(1, 100000):
                rects.append(pygame.Rect(x, y, *rectSize))
                if rects[-1].colliderect(player):
                    rects.pop(-1)
    
    rectsColors = {}
    for rect in rects:
        rectsColors[repr(rect)] = [pgTools.getRandomRGB(), 2]

    return rects, rectsColors

rects, rectsColors = createRects()

points = 0

running = True
while running:
    dt = clock.tick(target_fps) / 10
    display.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mousePos = pygame.mouse.get_pos()
    keyInputHandler.update()

    if keyInputHandler.mouseKeyPressed(0):
        rectsColliding = pgTools.getCollidingRectangles([*mousePos, 1, 1], rects)
        if len(rectsColliding) != 0:
            for rect in rectsColliding:
                rects.remove(rect)
                points += 1
    
    if keyInputHandler.keyPressedOnce(pygame.K_f):
        print(f'You have {points} points.')
    
    if keyInputHandler.keyPressedOnce(pygame.K_r):
        rects, rectsColors = createRects()
    
    if keyInputHandler.keyPressed(pygame.K_w):
        pgTools.moveY(player, -playerVelocity * dt, rects)
    if keyInputHandler.keyPressed(pygame.K_s):
        pgTools.moveY(player, playerVelocity * dt, rects)
    
    if keyInputHandler.keyPressed(pygame.K_a):
        pgTools.moveX(player, -playerVelocity * dt, rects)
    if keyInputHandler.keyPressed(pygame.K_d):
        pgTools.moveX(player, playerVelocity * dt, rects)
    
    playerColor = pgTools.rainbowEffectUpdate(playerColor, 1)
    
    pygame.draw.rect(display, playerColor, player)

    for rect in rects:
        rectRepresentation = repr(rect)
        rectsColors[rectRepresentation] = [*pgTools.rainbowEffectUpdate(rectsColors[rectRepresentation][:-1], rectsColors[rectRepresentation][-1]), rectsColors[rectRepresentation][-1]]
        
        pygame.draw.rect(display, rectsColors[rectRepresentation][:-1], rect)

    pygame.display.flip()

pygame.quit()