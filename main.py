import asyncio
import pygame


# constants
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
IMAGE_SIZE = 80

async def main():
    # initialize pygame systems, it's like turning on the engine #choochoo
    pygame.init()

    # create canvas 
    screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))

    # timer object, replaces time.sleep() to allow the human eye to perceive changes
    clock = pygame.time.Clock()

    # images of the user character
    user = set_up_user()

    while True:

        # every frame pygame collects a list of things of what happened — mouse clicks,
        # key presses, windows closing etc. We loop through it to check what happened
        for event in pygame.event.get():

            # this is the event where the user clicks on the X button to close the window
            if event.type == pygame.QUIT:
                pygame.quit()

            # KEYDOWN fires when a key is pressed, KEYUP fires when a key is released
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    user['x'] += 5

                if event.key == pygame.K_LEFT:
                    user['x'] -= 5

        # this fills the backgrounfd with white every frame, RGB (_,_,_)
        screen.fill((255, 255, 255))

        # this draws the user character every frame, with the standing image as default
        screen.blit(user['standing'], (user['x'], user['y']))

        # this updates the display, kinda like publishing the whole image as a whole
        pygame.display.flip()

        clock.tick(60)

        await asyncio.sleep(0)

def set_up_user():
    x = CANVAS_WIDTH/2 - IMAGE_SIZE/2
    y = CANVAS_HEIGHT/2 - IMAGE_SIZE/2

    standing = pygame.image.load('flushedstanding.png')
    standing = pygame.transform.scale(standing, (IMAGE_SIZE, IMAGE_SIZE))

    walking = pygame.image.load('flushedwalking.png')
    walking = pygame.transform.scale(walking, (IMAGE_SIZE, IMAGE_SIZE))

    return {
        'x': x,
        'y': y,
        'standing': standing,
        'walking': walking
    }

asyncio.run(main())