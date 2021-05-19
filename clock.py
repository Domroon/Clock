import pygame

def main():
    pygame.init()

    screen_width = 1280
    screen_height = 720

    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Clock")

    clock = pygame.time.Clock()

    run = True
    game_speed = 10
    while run:
        clock.tick(game_speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


if __name__ == '__main__':
    main()