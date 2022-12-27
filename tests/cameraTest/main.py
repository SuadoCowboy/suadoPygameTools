import pygame
import suadoPygameTools as pgTools

# KEYS:
# WASD - Movement
# R - change rectangles color
# F: prints out how many rectangles are being drawn on the screen

pygame.init()

WIDTH, HEIGHT = 800, 600
display = pygame.display.set_mode((WIDTH,HEIGHT))

clock = pygame.time.Clock()
target_fps = 60

keyInputHandler = pgTools.KeyInputHandler()

class SimpleRect(pygame.Rect):
    def __init__(self, x: float, y: float, width: float, height: float, color: tuple[int, int, int]):
        super().__init__(x, y, width, height)
        self.color = color
    
    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self)

class Player(pygame.Rect):
    def __init__(self, centerx: float, centery: float, width: int=16, height: int=24):
        super().__init__(centerx-width/2, centery-height/2, width, height)
        self.color = (255,255,255)
        self.velocity = 10
    
    def update(self, dt: float, keyInputHandler: pgTools.KeyInputHandler, rectangles: list[pygame.Rect]):
        if keyInputHandler.keyPressed(pygame.K_w):
            pgTools.moveY(self, -self.velocity * dt, rectangles)
        if keyInputHandler.keyPressed(pygame.K_s):
            pgTools.moveY(self, self.velocity * dt, rectangles)
        
        if keyInputHandler.keyPressed(pygame.K_a):
            pgTools.moveX(self, -self.velocity * dt, rectangles)
        if keyInputHandler.keyPressed(pygame.K_d):
            pgTools.moveX(self, self.velocity * dt, rectangles)

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self)

camera = pgTools.Camera(0,0,WIDTH,HEIGHT,0,0)
player = Player(0,0)

rectSize = (32,32)

rowSize = 128
columnSize = 128

print(f'{rowSize}x{columnSize} = {rowSize*columnSize} Possible amount of rectangles')

for y in range(-rectSize[1]*int(columnSize/2), rectSize[1]*int(columnSize/2), rectSize[1]):
    for x in range(-rectSize[0]*int(rowSize/2), rectSize[0]*int(rowSize/2), rectSize[0]):
        rect = SimpleRect(x, y, *rectSize, pgTools.getRandomRGB())
        camera.addRectangle(rect, rect.draw)

print(f'Amount of rectangles: {len(camera.rectangles)}')

camera.addRectangle(player, player.draw)
camera.follow(player)

running = True
while running:
    dt = clock.tick(target_fps) / 10
    display.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keyInputHandler.update()
    
    player.update(dt, keyInputHandler, [])

    if keyInputHandler.keyPressedOnce(pygame.K_f): # rectangles.length-1 -> -1 is because of the player rectangle
        print(f'Rectangles being drawn: {len(camera.rectanglesAtCameraArea)-1}')
    
    if keyInputHandler.keyPressedOnce(pygame.K_r):
        for rect in camera.rectangles:
            if rect == player:
                continue
            
            rect.color = pgTools.getRandomRGB()

    camera.update()
    camera.draw(display)

    pygame.display.flip()

pygame.quit()