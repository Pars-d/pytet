import pygame

def main():
    pygame.init()

    FPS = 60
    FramePerSec = pygame.time.Clock()

    pygame.display.set_caption("minimal program")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((800,600))
     
    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        FramePerSec.tick(FPS)


if __name__ == "__main__":
    main()