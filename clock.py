from datetime import datetime as DateTime
import pygame
from pygame import Vector2
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
                                { '3': {'color' : (255, 0, 0), 'duration' : 1}},
                        'pattern_duration' : 4},

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
                                { '12': {'color' : (255, 0, 0), 'duration' : 1}},
                        'pattern_duration' : 13},

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
                                { '6': {'color' : (255, 0, 0), 'duration' : 1}},
                        'pattern_duration' : 7}
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

# implement update method? its not necessary because i update nothing, its static!
class PointSightingLine(pygame.sprite.Sprite):
    def __init__(self, pos, width, length, color, surface, radius=0, offset=0):
        super().__init__()
        self.width = width
        self.length = length
        self.surface = surface
        self.pos = pos
        self.image = pygame.Surface((width, length), pygame.SRCALPHA)
        self.image = self.image.convert_alpha() # work faster with this image
        self.image_copy = self.image
        self.rect = self.image.get_rect(center=self.pos)
        self.image.fill(color)
        self.move_vector = Vector2(0, -radius - offset)
        self.radius = radius

    def rotate(self, angle):
        move_vector = self.move_vector
        move_vector = move_vector.rotate(angle)

        self.image = pygame.transform.rotozoom(self.image_copy, -angle, 1)
        self.rect = self.image.get_rect(center = self.pos + move_vector)

class Hand(PointSightingLine):
    def __init__(self, pos, width, length, color, surface, radius=0, offset=0):
        super().__init__(pos, width, length, color, surface, radius, offset)


def draw_circle(surface, radius):
    pygame.draw.circle(surface, (0, 0, 255), surface.get_rect().center, radius, 10)


def generate_numbers(radius, size, window):
    radius_vector = pygame.Vector2(0, -radius)
    numbers_list = []

    for hour in range(1, 13):
        pos = window.get_rect().center + radius_vector.rotate(int(360 / 12 * hour))
        numbers_list.append(Number(str(hour), size, (255, 255, 255), pos))

    return numbers_list


def generate_tick_marks(radius, tick_mark_group, surface):
    angle_per_minute = 360/60
    
    for second in range(0, 60):
        tick_length = 20
        tick_width = 2
        offset = -70
        if second % 15 == 0:
            tick_length = 40
            tick_width = 10
            offset = -70
        if second % 5 == 0 and not second % 15 == 0:
            tick_length = 40  
            tick_width = 5
            offset = -80
        tick = PointSightingLine(surface.get_rect().center, tick_width, tick_length, (0, 0, 255), surface, radius=radius, offset=offset)
        tick.rotate(second*angle_per_minute)
        tick_mark_group.add(tick)


def generate_hands(radius, hands_group, surface):
    offset = -230
    second_hand = Hand((surface.get_rect().center), 2, 230, (0, 255, 255), surface, radius=radius, offset=offset)
    minute_hand = Hand((surface.get_rect().center), 10, 230, (0, 255, 0), surface, radius=radius, offset=offset)
    hour_hand = Hand((surface.get_rect().center), 10, 140, (0, 255, 0), surface, radius=radius, offset=offset-45)
    hands_group.add(minute_hand, hour_hand, second_hand)


def load_pattern(numbers_group, pattern_dict):
    keys_list = []
    for key in pattern_dict:
        keys_list.append(key)

    for i in range(0, 12):
        if int(keys_list[i]) == int(numbers_group.sprites()[i].digit):
                numbers_group.sprites()[i].settings = pattern_dict[str(i+1)]


def main():
    pygame.init()
    try:
        screen_width = 720
        screen_height = 720

        window = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Clock")

        background = pygame.Surface(window.get_size())

        radius = min(window.get_rect().center) - 50
        assert radius > 0
        number_size = 80

        # hands
        hands_group = pygame.sprite.Group()
        generate_hands(radius, hands_group, window)

        # numbers                                                                
        numbers_group = pygame.sprite.Group()
        numbers_list = generate_numbers(radius, number_size, window)
        numbers_group.add(numbers_list)

        # tick marks
        tick_mark_group = pygame.sprite.Group()
        generate_tick_marks(radius, tick_mark_group, background)

        # pattern
        pattern = PATTERNS['test_pattern3']
        load_pattern(numbers_group, pattern)
        timer = Timer(pattern['pattern_duration'])

        angle_per_second = 360/60
        angle_per_hour = 360/12

        clock = pygame.time.Clock()
        fps = 120
        while True:
            window.blit(background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            tick_mark_group.draw(window)        

            now = DateTime.now()
            hands_group.sprites()[2].rotate(angle_per_second * now.second) # give now-object to the update method and make this calulation in depence of the hand-type
            hands_group.sprites()[0].rotate(angle_per_second * now.minute) # give now-object to the update method and make this calulation in depence of the hand-type
            hands_group.sprites()[1].rotate(angle_per_hour * now.hour + 30 * (now.minute/60)) # give now-object to the update method and make this calulation in depence of the hand-type
            hands_group.draw(window)

            draw_circle(window, radius - 50)
            
            timer.count()
            numbers_group.update(timer.timer)
            numbers_group.draw(window)

            pygame.display.update()
            clock.tick(fps)
    finally:
        pygame.quit()

if __name__ == '__main__':
    main()