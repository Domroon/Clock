import pygame
import pygame.freetype
import time

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
    circle_white = Circle(radius, (159, 226, 191), center)
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
        numbers.append(Number(str(i+1), size, (255, 127, 80), number_vectors[i].x, number_vectors[i].y))

    numbers_group = pygame.sprite.Group()
    numbers_group.add(numbers)
    numbers_group.draw(window)


def add_second_lines(center_vector, radius, window):
    second_line_end_vector = pygame.math.Vector2(0, -radius+5)
    angle_offset = 360/60

    for angle in range(0, 60):
        if angle % 15 == 0:
            length = -210
            width = 10
        elif angle % 5 == 0:
            length = -210
        else:
            length = -230
            width = 5
            
        second_line_begin_vector = pygame.math.Vector2(0, length)

        second_line_begin_vector2 = second_line_begin_vector.rotate(angle*angle_offset)
        second_line_end_vector2 = second_line_end_vector.rotate(angle*angle_offset)
        pygame.draw.line(window, (159, 226, 191), center_vector + second_line_begin_vector2, center_vector + second_line_end_vector2, width=width)


def add_pointer(type, center_vector, radius, time, window, length=50, width=1, color=(255, 255, 255)):
    if type == "hour":
        angle_offset = 360/12
    elif type == "min":
        angle_offset = 360/60
    elif type == "sec":
        angle_offset = 360/60

    second_line_begin_vector = pygame.math.Vector2(0, 0)
    second_line_end_vector = pygame.math.Vector2(0, -radius + length)
    second_line_begin_vector = second_line_begin_vector.rotate(time*angle_offset)
    second_line_end_vector = second_line_end_vector.rotate(time*angle_offset)
    pygame.draw.line(window, color, center_vector + second_line_begin_vector, center_vector + second_line_end_vector, width=width)


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

        hour = time.gmtime().tm_hour + 2
        minute = time.gmtime().tm_min
        second = time.gmtime().tm_sec
        add_pointer("min", center_vector, radius, minute, window, color=(100, 149, 237), width=9)
        add_pointer("hour", center_vector, radius, hour, window, color=(64, 224, 208), length=130, width=3)
        add_pointer("sec", center_vector, radius, second, window, color=(0, 200, 100), width=2)

        pygame.display.update()


if __name__ == '__main__':
    main()