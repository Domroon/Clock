import pygame
import pygame.freetype
import time

PATTERNS = {
        'test_pattern' : {
                        '1' : 
                                { '1' : {'color' : (255, 0, 0), 'duration' : 1}},
                        '2' : 
                                { '1' : {'color' : (255, 0, 0), 'duration' : 1}},
                        '3' : 
                                { '1': {'color' : (255, 0, 0), 'duration' : 1}},
                        '4' : 
                                { '1': {'color' : (255, 0, 0), 'duration' : 1}},
                        '5' : 
                                { '2': {'color' : (255, 0, 0), 'duration' : 1}},
                        '6' : 
                                { '2': {'color' : (255, 0, 0), 'duration' : 1}},
                        '7' : 
                                { '2': {'color' : (255, 0, 0), 'duration' : 1}},
                        '8' : 
                                { '2': {'color' : (255, 0, 0), 'duration' : 1}},
                        '9' : 
                                { '3': {'color' : (255, 0, 0), 'duration' : 1}},
                        '10' : 
                                { '3': {'color' : (255, 0, 0), 'duration' : 1}},
                        '11' : 
                                { '3': {'color' : (255, 0, 0), 'duration' : 1}},
                        '12' : 
                                { '3': {'color' : (255, 0, 0), 'duration' : 1}}},

        'test_pattern2' : {
                        '1' : 
                                { '1' : {'color' : (255, 0, 0), 'duration' : 1}},
                        '2' : 
                                { '2' : {'color' : (255, 0, 0), 'duration' : 1}},
                        '3' : 
                                { '3': {'color' : (255, 0, 0), 'duration' : 1}},
                        '4' : 
                                { '4': {'color' : (255, 0, 0), 'duration' : 1}},
                        '5' : 
                                { '5': {'color' : (255, 0, 0), 'duration' : 1}},
                        '6' : 
                                { '6': {'color' : (255, 0, 0), 'duration' : 1}},
                        '7' : 
                                { '7': {'color' : (255, 0, 0), 'duration' : 1}},
                        '8' : 
                                { '8': {'color' : (255, 0, 0), 'duration' : 1}},
                        '9' : 
                                { '9': {'color' : (255, 0, 0), 'duration' : 1}},
                        '10' : 
                                { '10': {'color' : (255, 0, 0), 'duration' : 1}},
                        '11' : 
                                { '11': {'color' : (255, 0, 0), 'duration' : 1}},
                        '12' : 
                                { '12': {'color' : (255, 0, 0), 'duration' : 1}}},

        'test_pattern3' : {
                        '1' : 
                                { '1' : {'color' : (255, 0, 0), 'duration' : 1}},
                        '2' : 
                                { '2' : {'color' : (255, 0, 0), 'duration' : 1}},
                        '3' : 
                                { '3': {'color' : (255, 0, 0), 'duration' : 1}},
                        '4' : 
                                { '4': {'color' : (255, 0, 0), 'duration' : 1}},
                        '5' : 
                                { '5': {'color' : (255, 0, 0), 'duration' : 1}},
                        '6' : 
                                { '6': {'color' : (255, 0, 0), 'duration' : 1}},
                        '7' : 
                                { '1': {'color' : (255, 0, 0), 'duration' : 1}},
                        '8' : 
                                { '2': {'color' : (255, 0, 0), 'duration' : 1}},
                        '9' : 
                                { '3': {'color' : (255, 0, 0), 'duration' : 1}},
                        '10' : 
                                { '4': {'color' : (255, 0, 0), 'duration' : 1}},
                        '11' : 
                                { '5': {'color' : (255, 0, 0), 'duration' : 1}},
                        '12' : 
                                { '6': {'color' : (255, 0, 0), 'duration' : 1}}}
        }

class Number(pygame.sprite.Sprite):
    def __init__(self, digit, size, color, pos):
        super().__init__()
        self.digit = digit
        self.settings = {}
        self.font = pygame.freetype.Font(None, size)
        self.pos = pos
        self.color = color
        self.image, self.rect = self.font.render(digit, self.color)
        self.rect.center = pos
    
    def update(self, timer):
        for time_point in self.settings:
            if int(time_point) == timer:
                self.color = self.settings[str(time_point)]['color']
            elif int(time_point) + self.settings[time_point]['duration'] == timer:
                self.color = (255, 255, 255) #white
            else:
                self.color = (255, 255, 255) #white
            
        self.image, self.rect = self.font.render(self.digit, self.color)
        self.rect.center = self.pos


class Circle(pygame.sprite.Sprite):
    def __init__(self, radius, color, pos):
        super().__init__()
        self.image = pygame.Surface((radius*2, radius*2))
        pygame.draw.circle(self.image, color, (radius,radius), radius, width=10)
        self.rect = self.image.get_rect()
        self.rect.center = (pos['x'], pos['y'])


def draw_circle(surface, radius):
    pygame.draw.circle(surface, (159, 226, 191), surface.get_rect().center, radius, 10)


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


def load_settings(numbers_group, pattern_dict):
    keys_list = []
    for key in pattern_dict:
        keys_list.append(key)

    for i in range(0, 12):
        #print(f"keys_list: {keys_list[i]} | (numbers_group.sprites()[i].digit: {numbers_group.sprites()[i].digit}")
        if int(keys_list[i]) == int(numbers_group.sprites()[i].digit):
                numbers_group.sprites()[i].settings = pattern_dict[str(i+1)]


class Timer():
    def __init__(self, max_sec):
        self.max_sec = max_sec
        self.counter = 0
        self.timer = round(time.perf_counter()) 
        self.rest_time = 0
    
    def reset(self):
        self.rest_time = self.timer * self.counter
        self.counter += 1

    def count(self):
            self.timer = round(time.perf_counter()) - self.rest_time
            if self.timer == self.max_sec:
                self.reset()


def main():
    pygame.init()
    try:
        screen_width = 720
        screen_height = 720

        window = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Clock")

        radius = min(window.get_rect().center) - 50
        assert radius > 0
        number_size = 80
                                                                                                    
        numbers_group = pygame.sprite.Group()
        numbers_list = add_numbers(radius, number_size, window)
        numbers_group.add(numbers_list)

        load_settings(numbers_group, PATTERNS['test_pattern2'])

        timer = Timer(13)

        clock = pygame.time.Clock()
        fps = 120
        while True:
            window.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            numbers_group.draw(window)
            draw_circle(window, radius - 50)
            timer.count()
            numbers_group.update(timer.timer)

            pygame.display.update()
            clock.tick(fps)
    finally:
        pygame.quit()

if __name__ == '__main__':
    main()