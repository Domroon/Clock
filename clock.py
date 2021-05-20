import pygame
from pygame import image
import pygame.freetype

class Digit(pygame.sprite.Sprite):
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

def add_numbers(center, radius, window):
    size = 80

    # 360/12 are the angles for the numbers
    angle = 360/12
    center_vector = pygame.math.Vector2(center['x'], center['y'])
    radius_vector = pygame.math.Vector2(0, -radius - size/1.5)
    number_vectors = []
    
    radius_vectors = [radius_vector for vector in range(1, 12)]
    for vector in radius_vectors:
        vector = vector.rotate(int(angle))
        number_vectors.append(center_vector + vector)
        angle += 360/12

    # write alle 12 vectors in a new list and write an every place center_vector + radius_vector! then you have all correct vectors!
    digit_1 = Digit("1", size, (255, 255, 255), number_vectors[0].x, number_vectors[0].y)
    digit_2 = Digit("2", size, (255, 255, 255), number_vectors[1].x, number_vectors[1].y)
    digit_3 = Digit("3", size, (255, 255, 255), number_vectors[2].x, number_vectors[2].y)
    digit_4 = Digit("4", size, (255, 255, 255), number_vectors[3].x, number_vectors[3].y)
    digit_5 = Digit("5", size, (255, 255, 255), number_vectors[4].x, number_vectors[4].y)
    digit_6 = Digit("6", size, (255, 255, 255), number_vectors[5].x, number_vectors[5].y)
    digit_7 = Digit("7", size, (255, 255, 255), number_vectors[6].x, number_vectors[6].y)
    digit_group = pygame.sprite.Group()
    digit_group.add(digit_1, digit_2, digit_3, digit_4, digit_5,digit_6,digit_7)
    digit_group.draw(window)


def main():
    pygame.init()
    pygame.freetype.init()

    screen_width = 720
    screen_height = 720

    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Clock")

    # variables
    center = {'x' : screen_width/2, 'y': screen_height/2}
    radius = screen_width/2 - 100

    clock = pygame.time.Clock()

    run = True
    game_speed = 120
    while run:
        window.fill((0,0,0))
        clock.tick(game_speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        add_circle(center, radius, window)
        add_numbers(center, radius, window)

        pygame.display.update()


if __name__ == '__main__':
    main()