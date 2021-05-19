import pygame
import pygame.freetype

class Digit(pygame.sprite.Sprite):
    def __init__(self, digit, size, color, pos_x, pos_y):
        super().__init__()
        self.digit = digit
        font = pygame.freetype.Font(None, size)
        self.image = pygame.Surface((size/2, size - 20))
        font.render_to(self.image, (0, 0), str(self.digit), color)
        self.font = pygame.freetype.Font(None)
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)

class Number:
    def __init__(self, number, size, color, pos_x, pos_y):
        self.digit_front = Digit(number[0], size, color, pos_x, pos_y)
        self.digit_back = Digit(number[1], size, color, pos_x + size/2, pos_y)

class Circle(pygame.sprite.Sprite):
    def __init__(self, radius, color, pos):
        super().__init__()
        self.image = pygame.Surface((radius*2, radius*2))
        pygame.draw.circle(self.image, color, (radius,radius), radius, width=10)
        self.rect = self.image.get_rect()
        self.rect.center = (pos['x'], pos['y'])


def main():
    pygame.init()
    pygame.freetype.init()

    screen_width = 720
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

        center = {'x' : screen_width/2, 'y': screen_height/2}
        radius = screen_width/2 - 100

        circle_group = pygame.sprite.Group()
        circle_white = Circle(radius, (255, 255, 255), center)
        circle_group.add(circle_white)
        circle_group.draw(window)

        size = 100

        digit_3 = Digit(3, size, (255, 255, 255), center['x'] + radius + size/3, center['y'])
        digit_6 = Digit(6, size, (255, 255, 255), center['x'], center['y'] + radius + size/2)
        digit_9 = Digit(9, size, (255, 255, 255), center['x'] - radius - size/3, center['y'])
        digit_group = pygame.sprite.Group()
        digit_group.add(digit_3, digit_6, digit_9)
        digit_group.draw(window)

        number_group = pygame.sprite.Group()
        number = Number("12", size, (255, 255, 255), center['x'] -size/4, center['y'] - radius - size/2.5)
        number_group.add(number.digit_front, number.digit_back)
        number_group.draw(window)
        
        
        pygame.display.update()


if __name__ == '__main__':
    main()