import asyncio
import pygame


# constants
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
IMAGE_SIZE = 80
VELOCITY = 8

WALK_TIMER = 8

async def main():
    # INITialize pygame systems, it's like turning on the engine #choochoo
    pygame.init()
    # create canvas 
    screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
    # timer object, replaces time.sleep() to allow the human eye to perceive changes
    clock = pygame.time.Clock()

    # images of the user character
    user = set_up_user()
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

            # KEYDOWN fires when a key is pressed, KEYUP fires when a key is released
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    user['x'] += VELOCITY
                    animate(user, 'walking')

                elif event.key == pygame.K_LEFT:
                    user['x'] -= VELOCITY
                    animate(user, 'walking')

        if user['walk_timer'] > 0:
                        user['current_frame'] = user['walking']
                        user['walk_timer'] -= 1

        draw(screen, user)

        # this limits the game to 60 frames per second, so that the human eye can perceive changes
        clock.tick(60)

        # this provides breathing room for the browser
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
        'current_frame': standing,
        'walk_timer': 0
    }
# this function fills the canvas with white, draws current frame, and updates display every frame
def draw(screen, user):
    # this fills the canvas with white ever single frame, replacing the previous frame RGB (_,_,_)
    screen.fill((255, 255, 255))

    # this draws the user character ever frame, it will be reset to standing function
    screen.blit(user['current_frame'], (user['x'], user['y']))

    # this updates the display, kinda like publishing the whole image as a whole
    pygame.display.flip()

asyncio.run(main())