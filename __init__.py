import pygame
import random

# Made by Suado Cowboy
# Feel free to "steal" this code and change it the way you prefer

def hasMethod(classObj: object, method: str):
    if method in classObj.__dir__() and str(type(classObj.__getattribute__(method))) == '<class \'method\'>':
        return True
    return False

def getCollidingObjects(rect: pygame.Rect, objects: list, ignoreRects: list=None):
    """
    returns a list of objects that are colliding with the rect;

    ignoreObjects appends rect parameter to it automatically.
    """
    if type(rect) != pygame.Rect: # tries to make a rectangle if it's only the rect arguments
        rect = pygame.Rect(*rect)
    
    if ignoreRects == None:
        ignoreRects = []
    
    ignoreRects.append(rect)
    
    collideList = []
    for object in objects:
        collideList.append(object)
    
    indexes = rect.collidelistall(collideList)
    
    output = []
    for index in indexes:
        if objects[index] in ignoreRects:
            continue
        
        output.append(objects[index])
    
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
    if it collides with an object, it stops on the past pixel

    Returns False if collided with an object
    """

    xPlus = 1 if xVelocity > 0 else -1

    # collision checking (if statements can be slow, maybe try a better system on future)
    for x in range(int(rectangle.x), int(rectangle.x+xVelocity), xPlus):
        rectanglesColliding = getCollidingObjects([x+xPlus, rectangle.y, rectangle.width, rectangle.height], rectangles, ignoreRectangles)
        if len(rectanglesColliding) != 0:
            rectangle.x = x
            return False
    
    rectangle.x += xVelocity
    return True

def moveY(rectangle: pygame.Rect, yVelocity: int | float, rectangles: list[pygame.Rect], ignoreRectangles: list[pygame.Rect]=None):
    """
    Function to move without considerating gravity.

    this function iterates through each pixel until it reaches the final y position.
    if it collides with an object, it stops on the past pixel

    Returns False if collided with an object
    """
    
    yPlus = 1 if yVelocity > 0 else -1

    # collision checking (if statements can be slow, maybe try a better system on future)
    for y in range(int(rectangle.y), int(rectangle.y+yVelocity), yPlus):
        rectanglesColliding = getCollidingObjects([rectangle.x, y+yPlus, rectangle.width,rectangle.height], rectangles, ignoreRectangles)
        if len(rectanglesColliding) != 0:
            rectangle.y = y
            return False

    rectangle.y += yVelocity
    return True

def moveTo(rectangle: pygame.Rect, pos: tuple[int, int], rectangles: list[pygame.Rect], ignoreRectangles: list[pygame.Rect]=None):
    """
    Function to move without considerating gravity.

    this function iterates through each pixel until it reaches the final position.
    if it collides with an object, it stops on the past pixel

    Returns False if collided with an object
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
# pygame.rect.inflate is the correcct function for zooming
class Camera:
    def __init__(self, x: int, y: int, width: int, height: int, viewportX: int, viewportY: int, viewportBackgroundColor: tuple=(0,0,0)):
        """
        x, y, width, height - area where the camera will search for objects to draw
        viewportX, viewportY - position of viewport surface(viewport uses camera width height)
        viewportBackgroundColor - self explanatory
        """
        self.x = x
        self.y = y

        self.width = width
        self.height = height
        
        self.objects = []
        self.objectsBeingDrawn = [] # entities are also in it

        self.entities = []
        
        self.following = False
        self.followObject = None
        
        self.viewportX = viewportX
        self.viewportY = viewportY
        self.viewportBackgroundColor = viewportBackgroundColor
        self.viewportSurface = pygame.Surface((self.width, self.height))

        self.disabled = False
    
    def addObject(self, object, drawFunction):
        self.objects.append((object, drawFunction))

    def draw(self, surface):
        surface.blit(self.viewportSurface, (self.viewportX, self.viewportY))
        self.viewportSurface.fill(self.viewportBackgroundColor)
        objects = [*[entity[:2] for entity in self.entities], *self.objects]

        self.objectsBeingDrawn = self.getObjectsAtCameraArea(objects.__reversed__())
        for obj, drawFunc in self.objectsBeingDrawn:

            originalPosition = (obj.x, obj.y)
            
            obj.x = obj.x-self.x
            obj.y = obj.y-self.y
            
            drawFunc(self.viewportSurface)
            
            obj.x, obj.y = originalPosition
    
    def toggleFollow(self, toggle=None):
        if toggle == None:
            toggle = not self.following
        
        self.following = toggle
    
    def follow(self, obj=None):
        """
        obj on center only!
        
        use this function a single time and
        then put camera update function on main loop
        """
        self.following = True
        if obj:
            self.followObject = obj
    
    def unfollow(self):
        self.following = False
        self.followObject = None

    def update(self):
        if self.following and self.followObject != None:
            # object.center-width.center = object at center of screen
            self.x = self.followObject.x+self.followObject.width/2-self.width/2
            self.y = self.followObject.y+self.followObject.height/2-self.height/2

    def getObjectsAtCameraArea(self, objects: list | list[tuple]):
        output = []
        for objectOrObjectTuple in objects:
            object = objectOrObjectTuple
            if type(objectOrObjectTuple) in [list,tuple]:
                object = objectOrObjectTuple[0]
            
            if (object.x+object.width > self.x and object.x < self.x+self.width) and (object.y+object.height > self.y and object.y < self.y+self.height):
                output.append(objectOrObjectTuple)

        return output