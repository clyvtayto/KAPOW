import asyncio
import pygame


# constants
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
IMAGE_SIZE = 80
VELOCITY = 8

WALK_TIMER = 8 # this runs 8/60 seconds

async def main():
    # INITialize pygame systems, it's like turning on the engine #choochoo
    pygame.init()
    # create canvas 
    screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
    # timer object, replaces time.sleep() to allow the human eye to perceive changes
    clock = pygame.time.Clock()

    # images of the user character
    user = set_up_user()

    # await allows 
    await game_loop(screen, user, clock)

async def game_loop(screen, user, clock):
    while True:
        
        # this resets user character to standing image 
        user['current_frame'] = user['standing']

        # every frame pygame collects a list of things of what happened — mouse clicks,
        # key presses, windows closing etc. We loop through it to check what happened
        # this is the equivalent of canvas.get_last_click in CIP but with more types of events
        for event in pygame.event.get():

            # this is the event where the user clicks on the X button to close the window
            if event.type == pygame.QUIT:
                pygame.quit()

            # this resets the direction every frame
            direction = None

            direction = detect_mobile_input(event)

            # KEYDOWN fires when a key is pressed, KEYUP fires when a key is released
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    direction = 'right'
            
                elif event.key == pygame.K_LEFT:
                    direction = 'left'

            if event.type == pygame.MOUSEBUTTONDOWN:
                direction = detect_mobile_input(event)

            if direction == 'right':
                    user['x'] += VELOCITY
                    animate(user, 'walking')

            elif direction == 'left':
                    user['x'] -= VELOCITY
                    animate(user, 'walking')

        # this handles the animation of the walking image, running it for WALK_TIMER frames
        if user['walk_timer'] > 0:
                        user['current_frame'] = user['walking']
                        user['walk_timer'] -= 1

        draw(screen, user)

        # this limits the game to 60 frames per second, so that the human eye can perceive changes
        clock.tick(60)

        # this provides breathing room for the browser, providing a pause point
        await asyncio.sleep(0)

# this hides the standing image for a moment, show action image, then show standing image again
def animate(user, action):
    user['current_frame'] = user[f'{action}']

    if action == 'walking':
        user['walk_timer'] = WALK_TIMER
    
        
def set_up_user():
    left_x = CANVAS_WIDTH/2 - IMAGE_SIZE/2
    top_y = CANVAS_HEIGHT/2 - IMAGE_SIZE/2

    standing = pygame.image.load('flushedstanding.png')
    standing = pygame.transform.scale(standing, (IMAGE_SIZE, IMAGE_SIZE))

    walking = pygame.image.load('flushedwalking.png')
    walking = pygame.transform.scale(walking, (IMAGE_SIZE, IMAGE_SIZE))

    return {
        'x': left_x,
        'y': top_y,
        'standing': standing,
        'walking': walking,
        'walk_timer': 0,
        'current_frame': standing,
    }
# this function fills the canvas with white, draws current frame, and updates display every frame
def draw(screen, user):

    # this fills the canvas with white ever single frame, replacing the previous frame RGB (_,_,_)
    # everything has to happen after this because this is the base layer
    screen.fill((255, 255, 255))

    # this draws the user character ever frame, it will be reset to standing function
    screen.blit(user['current_frame'], (user['x'], user['y']))

    create_mobile_controls(screen)

    # this updates the display, kinda like publishing the whole image as a whole
    pygame.display.flip()

def create_mobile_controls(screen):

    # similar concept to CIP's canvas.create_polygon, covering canvas, colour and coordinates
    left_arrow = pygame.draw.polygon(screen, 
                                    (0,0,0),
                                    [(20, 350), (70, 320), (70, 380)],
                                    2)

    right_arrow = pygame.draw.polygon(screen, 
                                    (0,0,0),
                                    [(140, 350), (90, 320), (90, 380)],
                                    2)

    up_arrow = pygame.draw.polygon(screen,
                                    (0,0,0),
                                    [(290, 320), (260, 380), (320, 380)],
                                    2)

    down_arrow = pygame.draw.polygon(screen,
                                    (0,0,0),
                                    [(350, 380), (320, 320), (380, 320)],
                                    2)

def detect_mobile_input(event):

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event is not None:
            # this returns the coordinate of mouse/ on screen click, it returns event position as a tuple (x, y)
            x, y = event.pos

            if 20 <= x <= 70 and 320 <= y <= 380:
                return 'left'
            elif 90 <= x <= 140 and 320 <= y <= 380:
                return 'right'
            elif 260 <= x <= 320 and 320 <= y <= 380:
                return 'up'
            elif 320 <= x <= 380 and 320 <= y <= 380:
                return 'down'
         

asyncio.run(main())