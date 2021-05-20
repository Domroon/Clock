import pygame
from pygame import image
import pygame.freetype

class Number(pygame.sprite.Sprite):
    def __init__(self, digit, size, color, pos_x, pos_y):
        super().__init__()
        self.size = size
        font = pygame.freetype.Font(None, size)
        self.image = digit
        font.render_to(self.image, (0, 0), digit, color)
        self.font = pygame.freetype.Font(None)
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, digit):
        if len(digit) > 1:
            self._image = pygame.Surface((self.size + 5, self.size - 20))
        else:
            self._image = pygame.Surface((self.size/2, self.size - 20))


class Circle(pygame.sprite.Sprite):
    def __init__(self, radius, color, pos):
        super().__init__()
        self.image = pygame.Surface((radius*2, radius*2))
        pygame.draw.circle(self.image, color, (radius,radius), radius, width=10)
        self.rect = self.image.get_rect()
        self.rect.center = (pos['x'], pos['y'])


def add_circle(center, radius, window):
    circle_group = pygame.sprite.Group()
    circle_white = Circle(radius, (255, 255, 255), center)
    circle_group.add(circle_white)
    circle_group.draw(window)


def add_numbers(center_vector, radius_vector, size, window):
    angle = 360/12
    number_vectors = []
    
    radius_vectors = [radius_vector for vector in range(0, 12)]
    for vector in radius_vectors:
        vector = vector.rotate(int(angle))
        number_vectors.append(center_vector + vector)
        angle += 360/12

    numbers = []
    for i in range(len(number_vectors)):
        numbers.append(Number(str(i+1), size, (255, 255, 255), number_vectors[i].x, number_vectors[i].y))

    numbers_group = pygame.sprite.Group()
    numbers_group.add(numbers)
    numbers_group.draw(window)


def add_second_lines(center_vector, radius, window):
    second_line_begin_vector = pygame.math.Vector2(0, -230)
    second_line_end_vector = pygame.math.Vector2(0, -radius+5)
    angle_offset = 360/60

    for angle in range(0, 60):
        second_line_begin_vector2 = second_line_begin_vector.rotate(angle*angle_offset)
        second_line_end_vector2 = second_line_end_vector.rotate(angle*angle_offset)
        pygame.draw.line(window, (255, 255, 255), center_vector + second_line_begin_vector2, center_vector + second_line_end_vector2, width=5)


def main():
    pygame.init()
    pygame.freetype.init()

    screen_width = 720
    screen_height = 720

    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Clock")

    # constants
    center = {'x' : screen_width/2, 'y': screen_height/2}
    radius = screen_width/2 - 100
    size = 80
    center_vector = pygame.math.Vector2(center['x'], center['y'])
    radius_vector = pygame.math.Vector2(0, -radius - size/1.5)

    clock = pygame.time.Clock()

    run = True
    game_speed = 120
    while run:
        window.fill((0, 0, 0))
        clock.tick(game_speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        add_circle(center, radius, window)
        add_numbers(center_vector, radius_vector, size, window)
        add_second_lines(center_vector, radius, window)

        pygame.display.update()


if __name__ == '__main__':
    main()