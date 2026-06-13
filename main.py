import asyncio
import pygame


# constants

# image handling
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
IMAGE_SIZE = 80
OFFSET = 20 # this is to account for the space in the images
VELOCITY = 8

# frame animation
WALK_TIMER = 6 # this runs 6/60 seconds
# separate punch and block timer in case I wanna change either
PUNCH_TIMER = 8 
BLOCK_TIMER = 7

async def main():
    # INITialize pygame systems, it's like turning on the engine #choochoo
    pygame.init()
    # create canvas 
    screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
    # timer object, replaces time.sleep() to allow the human eye to perceive changes
    clock = pygame.time.Clock()

    # images of the user character, doesnt actually show the various images of the user, just establishing the size
    # this also returns a dict of all essential components that can be referenced and changed as we go!
    user = set_up_user()

    # images of the opponent character, same concept as the user above! 
    oppo = set_up_opponent()

    # await allows the browser to have some room to breathe?
    await game_loop(screen, user, oppo, clock)

# this is what makes the game run!
async def game_loop(screen, user, oppo, clock):
    
    while oppo['health'] > 0:
        
        # this resets user character to standing image so the animation will reset
        user['current_frame'] = user['standing']

        # every frame pygame collects a list of things of what happened — mouse clicks,
        # key presses, windows closing etc. We loop through it to check what happened
        # this is the equivalent of canvas.get_last_click in CIP but with more types of events
        for event in pygame.event.get():

            # this is the event where the user clicks on the X button to close the window
            if event.type == pygame.QUIT:
                pygame.quit()

            if user['animating'] == False:
                user_controls(event,user, oppo)

        # this sets the number of frames, and has to be OUTSIDE the loop because it resets based on the event NOT duration
        handle_timer(user)

        # this handles the loop of layering the canvas, and all the images in each iteration 
        draw(screen, user, oppo)

        # this limits the game to 60 frames per second, so that the human eye can perceive changes
        clock.tick(60)

        # this provides breathing room for the browser, providing a pause point
        await asyncio.sleep(0)

# this converts input into action and animates the respective actions 
def user_controls(event,user,oppo):
            
            # this resets the direction every frame
            direction = None

            # KEYDOWN fires when a key is pressed, KEYUP fires when a key is released
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    direction = 'left'
                
                elif event.key == pygame.K_RIGHT:
                    direction = 'right'

                elif event.key == pygame.K_UP:
                    direction = 'up'

                elif event.key == pygame.K_DOWN:
                    direction = 'down' 

            # this handles the clicks on the screen and allows for mobile fun!
            elif event.type == pygame.MOUSEBUTTONDOWN:
                direction = detect_mobile_input(event)

            # this prevents the user from gg out of frame on the left
            if direction == 'left' and user['x'] > -15:
                    user['x'] -= VELOCITY
                    animate(user, 'walking')

            # the second part of this prevents the user from overlapping the opponent, will stop at touching gloves
            elif direction == 'right' and user['x'] + IMAGE_SIZE < oppo['x'] + OFFSET:
                    user['x'] += VELOCITY
                    animate(user, 'walking')

            elif direction == 'up':
                    # using the same principle as the boundary detection on top, based on coordinates
                    # this checks if the two character gloves are touching
                    # if the opponent is NOT currently in the blocking animation, deal damage
                    if user['x'] + IMAGE_SIZE >= oppo['x'] + OFFSET and oppo['current_frame'] != oppo['blocking']:
                        oppo['health'] -= 1
                    animate(user, 'punching')

            elif direction == 'down':
                    animate(user, 'blocking')

            pygame.event.get() # added to get one more the programme to reset the event???

# this function counts down the different timer each action lasts, each have their respective timings
def handle_timer(user):

        # this handles the animation of the walking image, running it for WALK_TIMER frames
        if user['walk_timer'] > 0:
            user['animating'] = True
            user['current_frame'] = user['walking']
            user['walk_timer'] -= 1

        elif user['punch_timer'] > 0:
            user['animating'] = True
            user['current_frame'] = user['punching']
            user['punch_timer'] -= 1

        elif user['block_timer'] > 0:
            user['animating'] = True
            user['current_frame'] = user['blocking']
            user['block_timer'] -=1

        else: # this only runs if all timers are at 0
            user['animating'] = False

# this hides the standing image for a moment, show action image, then show standing image again
def animate(user, action):

    user['current_frame'] = user[f'{action}']

    if action == 'walking':
        user['walk_timer'] = WALK_TIMER

    if action == 'punching':
        # this sets
        user['punch_timer'] = PUNCH_TIMER

    if action == 'blocking':
        user['block_timer'] = BLOCK_TIMER

# this returns a bunch of images, x and y coordinates in a dict and will be referenced constantly
def set_up_user():
    # starting coordinates for the user
    left_x = CANVAS_WIDTH/2 - IMAGE_SIZE/2
    top_y = CANVAS_HEIGHT/2 - IMAGE_SIZE/2

    standing = pygame.image.load('flushedstanding.png')
    standing = pygame.transform.scale(standing, (IMAGE_SIZE, IMAGE_SIZE))

    walking = pygame.image.load('flushedwalking.png')
    walking = pygame.transform.scale(walking, (IMAGE_SIZE, IMAGE_SIZE))

    punching = pygame.image.load('flushedpunching.png')
    punching = pygame.transform.scale(punching, (IMAGE_SIZE, IMAGE_SIZE))

    blocking = pygame.image.load('flushedblocking.png')
    blocking = pygame.transform.scale(blocking, (IMAGE_SIZE, IMAGE_SIZE))

    return {
        'x': left_x,
        'y': top_y,
        'standing': standing,
        'walking': walking,
        'punching': punching,
        'blocking': blocking,
        'walk_timer': 0,
        'punch_timer': 0,
        'block_timer': 0,
        'current_frame': standing,
        'animating': False,
        'health': 3
    }

# this function fills the canvas with white, draws current frame, and updates display every frame
def draw(screen, user, oppo):

    # this fills the canvas with white ever single frame, replacing the previous frame RGB (_,_,_)
    # everything has to happen after this because this is the base layer
    screen.fill((255, 255, 255))

    # this draws the user character ever frame, it will be reset to standing function
    screen.blit(user['current_frame'], (user['x'], user['y']))

    screen.blit(oppo['current_frame'], (oppo['x'], oppo['y']))

    create_mobile_controls(screen)

    # this updates the display, kinda like publishing the whole image as a whole
    pygame.display.flip()

# this creates the triangles so that mobile users can enjoy!
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

# this returns the intended input into commands through checking which position is clicked
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

# this returns a bunch of images, x and y coordinates in a dict n will be referenced constantly later on
def set_up_opponent():
    left_x = CANVAS_WIDTH - IMAGE_SIZE + 15
    top_y = CANVAS_HEIGHT/2 - IMAGE_SIZE/2

    standing = pygame.image.load('oppostanding.png')
    standing = pygame.transform.scale(standing, (IMAGE_SIZE, IMAGE_SIZE))

    walking = pygame.image.load('oppowalking.png')
    walking = pygame.transform.scale(walking, (IMAGE_SIZE, IMAGE_SIZE))

    punching = pygame.image.load('oppopunching.png')
    punching = pygame.transform.scale(punching, (IMAGE_SIZE, IMAGE_SIZE))

    blocking = pygame.image.load('oppoblocking.png')
    blocking = pygame.transform.scale(blocking, (IMAGE_SIZE, IMAGE_SIZE))

    return {
         'x': left_x,
         'y': top_y,
        'standing': standing,
        'walking': walking,
        'punching': punching,
        'blocking': blocking,
        'walk_timer': 0,
        'punch_timer': 0,
        'block_timer': 0,
        'current_frame': standing,
        'health': 3
    }


# this is the if __name__ == __main__ kinda equivilant but asyncio version    
asyncio.run(main())