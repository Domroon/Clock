import pygame
import pygame.freetype

class Digit(pygame.sprite.Sprite):
    def __init__(self, digit, width, height, pos_x, pos_y, color):
        super().__init__()
        self.digit = digit
        font = pygame.freetype.Font(None, 100)
        self.image = pygame.Surface((width, height))
        font.render_to(self.image, (0, 0), str(self.digit), color)
        self.font = pygame.freetype.Font(None)
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)


def main():
    pygame.init()
    pygame.freetype.init()

    screen_width = 1280
    screen_height = 720

    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Clock")

    clock = pygame.time.Clock()

    run = True
    game_speed = 10
    while run:
        window.fill((0,0,0))
        clock.tick(game_speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        digit= Digit(1, 50, 100, 100, 100, (255, 255, 255))
        digit_group = pygame.sprite.Group()
        digit_group.add(digit)
        digit_group.draw(window)
        
        pygame.display.update()


if __name__ == '__main__':
    main()