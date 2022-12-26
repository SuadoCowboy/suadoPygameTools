import pygame
import random

def hasMethod(classObject: object, method: str):
    if method in classObject.__dir__() and str(type(classObject.__getattribute__(method))) == '<class \'method\'>':
        return True
    return False

def getCollidingRectangles(rect: pygame.Rect, rectangles: list, ignoreRects: list=None):
    """
    returns a list of rectangles that are colliding with the rect;

    ignoreRectangles appends rect parameter to it automatically.
    """
    if type(rect) != pygame.Rect: # tries to make a rectangle if it's only the rect arguments
        rect = pygame.Rect(*rect)
    
    if ignoreRects == None:
        ignoreRects = []
    
    ignoreRects.append(rect)
    
    collideList = []
    for rectangle in rectangles:
        collideList.append(rectangle)
    
    indexes = rect.collidelistall(collideList)
    
    output = []
    for index in indexes:
        if rectangles[index] in ignoreRects:
            continue
        
        output.append(rectangles[index])
    
    return output

def loadImage(imagePath: str, size=None):
    image = pygame.image.load(imagePath)

    if size != None:
        image = pygame.transform.scale(image, size)
    
    return image

def moveX(rectangle: pygame.Rect, xVelocity: int | float, rectangles: list[pygame.Rect], ignoreRectangles: list[pygame.Rect]=None):
    """
    Function to move without considerating gravity.

    this function iterates through each pixel until it reaches the final x position.
    if it collides with an rectangle, it stops on the past pixel

    Returns False if collided with an rectangle
    """

    xPlus = 1 if xVelocity > 0 else -1

    # collision checking (if statements can be slow, maybe try a better system on future)
    for x in range(int(rectangle.x), int(rectangle.x+xVelocity), xPlus):
        rectanglesColliding = getCollidingRectangles([x+xPlus, rectangle.y, rectangle.width, rectangle.height], rectangles, ignoreRectangles)
        if len(rectanglesColliding) != 0:
            rectangle.x = x
            return False
    
    rectangle.x += xVelocity
    return True

def moveY(rectangle: pygame.Rect, yVelocity: int | float, rectangles: list[pygame.Rect], ignoreRectangles: list[pygame.Rect]=None):
    """
    Function to move without considerating gravity.

    this function iterates through each pixel until it reaches the final y position.
    if it collides with an rectangle, it stops on the past pixel

    Returns False if collided with an rectangle
    """
    
    yPlus = 1 if yVelocity > 0 else -1

    # collision checking (if statements can be slow, maybe try a better system on future)
    for y in range(int(rectangle.y), int(rectangle.y+yVelocity), yPlus):
        rectanglesColliding = getCollidingRectangles([rectangle.x, y+yPlus, rectangle.width,rectangle.height], rectangles, ignoreRectangles)
        if len(rectanglesColliding) != 0:
            rectangle.y = y
            return False

    rectangle.y += yVelocity
    return True

def moveTo(rectangle: pygame.Rect, pos: tuple[int, int], rectangles: list[pygame.Rect], ignoreRectangles: list[pygame.Rect]=None):
    """
    Function to move without considerating gravity.

    this function iterates through each pixel until it reaches the final position.
    if it collides with an rectangle, it stops on the past pixel

    Returns False if collided with an rectangle
    """
    
    if ignoreRectangles == None:
        ignoreRectangles = []
    ignoreRectangles.append(rectangle)
    
    xPlus = 1 if pos[0]-rectangle.x > 0 else -1
    yPlus = 1 if pos[1]-rectangle.y > 0 else -1

    pos = (int(pos[0]), int(pos[1]))

    futureXCollided = False
    futureYCollided = False
    while rectangle.x != pos[0] or rectangle.y != pos[1]:
        if rectangle.x == pos[0]:
            xPlus = 0
        if rectangle.y == pos[1]:
            yPlus = 0
        
        futureXRect = pygame.Rect(rectangle.x+xPlus, rectangle.y, *rectangle.size)
        futureYRect = pygame.Rect(rectangle.x, rectangle.y+yPlus, *rectangle.size)
        futureRect = pygame.Rect(rectangle.x+xPlus, rectangle.y+yPlus, *rectangle.size)
        for rect in rectangles:
            if rect in ignoreRectangles:
                continue
            
            if rect.colliderect(futureRect):
                futureXCollided = rect.colliderect(futureXRect)
                futureYCollided = rect.colliderect(futureYRect)
                if futureXCollided:
                    xPlus = 0
                    pos = (rectangle.x, pos[1])
                if futureYCollided:
                    yPlus = 0
                    pos = (pos[0], rectangle.y)
                if futureXCollided and futureYCollided:
                    return False
        
        rectangle.x += xPlus
        rectangle.y += yPlus

    return True

def getRandomRGB():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

def getRandomRGBA():
    return (*getRandomRGB(), random.randint(0,255))

def rainbowEffectUpdate(colorRGB: tuple[float, float, float, float], plusAmount: float=1):
    color = pygame.Color(*colorRGB)
    
    if color.hsla[0]+plusAmount > 359:
        color.hsla = (0, 100, 50, 100)
    
    color.hsla = (color.hsla[0] + plusAmount, 100, 50, 100)

    return (color.r, color.g, color.b)

def randomChance(winPercentage: int, percentage: int=100):
    if random.randint(0,percentage) <= winPercentage:
        return True
    return False

class KeyInputHandler:
    def __init__(self):
        self.keysPressed = ()
        self.keysPressedBefore = ()
        self.keysReleased = ()
        
        self.mouseKeysPressed = ()
        self.mouseKeysPressedBefore = ()
        self.mouseKeysReleased = ()
    
    def update(self):
        """
        should be called after pygame.event.get function, or else mouse keys could not work as expected
        """
        self.keysPressedBefore = self.keysPressed
        self.mouseKeysPressedBefore = self.mouseKeysPressed

        self.keysPressed = pygame.key.get_pressed()
        self.mouseKeysPressed = pygame.mouse.get_pressed(num_buttons=5)

        self.keysReleased = self.getKeysReleased(self.keysPressed, self.keysPressedBefore)
        self.mouseKeysReleased = self.getKeysReleased(self.mouseKeysPressed, self.mouseKeysPressedBefore)

    def getKeysReleased(self, keysPressed: list, keysPressedBefore: list):
        keysReleased = list(keysPressed)
        
        for key in range(len(keysPressedBefore)):
            if keysPressedBefore[key] and not keysPressed[key]:
                keysReleased[key] = True
            else:
                keysReleased[key] = False
        
        return keysReleased

    def keyPressed(self, key: int):
        return self.keysPressed[key]
    
    def keyPressedOnce(self, key: int):
        return self.keyPressed(key) and not self.keysPressedBefore[key]

    def keyReleased(self, key: int):
        return self.keysReleased[key]

    def mouseKeyPressed(self, key: int):
        return self.mouseKeysPressed[key]
    
    def mouseKeyPressedOnce(self, key: int):
        return self.mouseKeyPressed(key) and not self.mouseKeysPressedBefore[key]

    def mouseKeyReleased(self, key: int):
        return self.mouseKeysReleased[key]

# to make a zoom system I guess it needs to change rect size and image size too...
# pygame.rect.inflate is a good function to see if we can make a zoom system
class Camera:
    def __init__(self, x: int, y: int, width: int, height: int, viewportX: int, viewportY: int, viewportBackgroundColor: tuple=(0,0,0)):
        """
        x, y, width, height - area where the camera will search for rectangles to draw
        viewportX, viewportY - position of viewport surface(viewport uses camera width height)
        viewportBackgroundColor - self explanatory

        viewport is the area where the screen will be drawn for the player to see
        """
        self.x = x
        self.y = y

        self.width = width
        self.height = height
        
        self.rectangles = []
        self.rectanglesDrawFunctions = {}
        self.rectanglesAtCameraArea = []
        
        self.following = False
        self.followRect = None
        
        self.viewportX = viewportX
        self.viewportY = viewportY
        self.viewportBackgroundColor = viewportBackgroundColor
        self.viewportSurface = pygame.Surface((self.width, self.height))
    
    def addRectangle(self, rectangle: pygame.Rect, drawFunction):
        self.rectangles.append(rectangle)
        self.rectanglesDrawFunctions[str(rectangle)] = drawFunction

    def draw(self, surface: pygame.Surface):
        surface.blit(self.viewportSurface, (self.viewportX, self.viewportY))
        self.viewportSurface.fill(self.viewportBackgroundColor)

        self.rectanglesAtCameraArea = self.getRectanglesAtCameraArea(self.rectangles)
        for rectangle in self.rectanglesAtCameraArea:
            drawFunction = self.rectanglesDrawFunctions[str(rectangle)]

            originalPosition = (rectangle.x, rectangle.y)
            
            rectangle.x = rectangle.x-self.x
            rectangle.y = rectangle.y-self.y
            
            drawFunction(self.viewportSurface)
            
            rectangle.x, rectangle.y = originalPosition
    
    def toggleFollow(self, toggle: bool=None):
        if toggle == None:
            toggle = not self.following
        
        self.following = toggle
    
    def follow(self, rectangle: pygame.Rect=None):
        """
        use this function a single time and
        then put camera update function on main loop
        """
        self.following = True
        if rectangle:
            self.followRectangle = rectangle
    
    def unfollow(self):
        self.following = False
        self.followRectangle = None

    def update(self):
        if self.following and self.followRectangle != None:
            # rectangle.center-camera.center/2 = rectangle at center of screen
            self.x = self.followRectangle.centerx-self.width/2
            self.y = self.followRectangle.centery-self.height/2

    def isRectangleBeingDrawn(self, rectangle: pygame.Rect):
        if (rectangle.x+rectangle.width > self.x and rectangle.x < self.x+self.width) and (rectangle.y+rectangle.height > self.y and rectangle.y < self.y+self.height):
            return True
        return False

    def getRectanglesAtCameraArea(self, rectangles: list[pygame.Rect]):
        rectanglesAtCameraArea = []
        for rectangle in rectangles:
            if self.isRectangleBeingDrawn(rectangle):
                rectanglesAtCameraArea.append(rectangle)

        return rectanglesAtCameraArea