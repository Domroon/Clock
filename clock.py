import pygame
import pygame.freetype
import time

class Number(pygame.sprite.Sprite):
    def __init__(self, digit, size, color, pos):
        super().__init__()
        self.font = pygame.freetype.Font(None, size)
        self.pos = pos
        self.digit = digit
        self.color = color
        self.image, self.rect = self.font.render(digit, self.color)
        self.rect.center = pos

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self.image, self.rect = self.font.render(self.digit, self._color)
        self.rect.center = self.pos


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


def add_numbers(radius, size, window):
    radius_vector = pygame.Vector2(0, -radius)
    numbers_list = []

    for hour in range(1, 13):
        pos = window.get_rect().center + radius_vector.rotate(int(360 / 12 * hour))
        numbers_list.append(Number(str(hour), size, (255, 255, 255), pos))

    return numbers_list


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
    try:
        screen_width = 720
        screen_height = 720

        window = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Clock")

        radius = min(window.get_rect().center) - 100
        assert radius > 0
        number_size = 80

        numbers_group = pygame.sprite.Group()
        numbers_list = add_numbers(radius, number_size, window)
        numbers_list[4].color = (255, 0, 0)
        numbers_group.add(numbers_list)
        numbers_group.sprites()[5].color = (0, 255, 255) #change add_number function so that is return a number_group!

        clock = pygame.time.Clock()
        fps = 120
        while True:
            window.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            numbers_group.draw(window)

            pygame.display.update()
            clock.tick(fps)
    finally:
        pygame.quit()

if __name__ == '__main__':
    main()