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


class PointSightingLine(pygame.sprite.Sprite):
    def __init__(self, pos, width, length, color, radius=0, offset=0, rotate_itself=True):
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((width, length), pygame.SRCALPHA)
        self.image = self.image.convert_alpha() # work faster with this image
        self.image.fill(color)
        self.image_copy = self.image
        self.move_vector = Vector2(0, -radius - offset)
        self.rect = self.image.get_rect(center=self.pos+self.move_vector)
        self.radius = radius
        self.rotate_itself = rotate_itself

    def rotate(self, angle):
        move_vector = self.move_vector
        move_vector = move_vector.rotate(angle)
        if self.rotate_itself:
                self.image = pygame.transform.rotozoom(self.image_copy, -angle, 1)
        self.rect = self.image.get_rect(center = self.pos + move_vector)


class Hand(PointSightingLine):
    def __init__(self, hand_type, pos, width, length, color, radius=0, offset=0):
        super().__init__(pos, width, length, color, radius, offset)
        self.hand_type = hand_type
        self.angle_per_second = 360/60
        self.angle_per_minute = self.angle_per_second
        self.angle_per_hour = 360/12

    def update(self, now):
        if self.hand_type == "second":
            self.rotate(self.angle_per_second * now.second)
        elif self.hand_type == "minute":
            self.rotate(self.angle_per_minute * now.minute)
        elif self.hand_type == "hour":
            self.rotate(self.angle_per_hour * now.hour + 30 * (now.minute/60))


class Number(PointSightingLine):
    def __init__(self, number, size, pos, color, radius, offset=0, width=0, length=0, rotate_itself=False):
        super().__init__(pos, width, length, color, radius, offset, rotate_itself)
        self.pos = pos
        self.number = number
        self.settings = {}
        self.font = pygame.freetype.Font(None, size)
        self.color = color
        self.image, self.rect = self.font.render(self.number, self.color)
        self.image_copy = self.image
        self.rect = self.image.get_rect(center=pos + self.move_vector)
        self.r = 255
        self.g = 255
        self.b = 255

    def update(self, frame):
        pass
        #self.increase_decrease_brightness(frame)
        #self.increase_decrease_brightness(frame, increase=False)
        #self.blink_all(frame)
    
    def change_color(self, color):
        self.font.render_to(self.image, (0, 0), self.number, color)
        self.font.bgcolor = (0, 0, 0)

    def increase_decrease_brightness(self, frame, increase=True):
        if self.r <= 255 and self.r > 50:
            if increase:
                self.r += 2
                self.g += 2
                self.b += 2
            else:
                self.r -= 2
                self.g -= 2
                self.b -= 2
        self.font.render_to(self.image, (0, 0), self.number, (self.r, self.g, self.b))
        self.font.bgcolor = (0, 0, 0)

    def blink_all(self, frame, duration=60):
        if frame == 1:
            self.font.render_to(self.image, (0, 0), self.number, (255, 0, 0))
        if frame == duration:
            self.font.bgcolor = (0, 0, 0)
            self.font.render_to(self.image, (0, 0), self.number, (0, 0, 0))


class Animation:
    def __init__(self, segments):
        self.segments = segments
        self.total_necessary_frames = self._calculate_total_necessary_frames()
        self.frames_list = self._save_segment_frames()
        self.current_segment = 1
        self.past_frames = self.frames_list[0]
        self.segments_frames = 0

    def _calculate_total_necessary_frames(self):
        total_necessary_frames = 0
        for segment in self.segments:
            total_necessary_frames += segment.necessary_frames

        return total_necessary_frames

    # save the frames from all segments in a list
    def _save_segment_frames(self):
        frames_list = []
        for segment in self.segments:
            frames_list.append(segment.necessary_frames)

        return frames_list

    def start_next_segment(self):
        pass

    def update(self, current_frame):
        self.segments_frames += int(current_frame/current_frame)
        #print(self.past_frames)
        self.segments[self.current_segment-1].update()
        if self.segments_frames == self.total_necessary_frames:
            #print(f"Reached Total necessary frame: {self.segments_frames}")
            self.segments_frames = 0
            self.current_segment = 1
            self.past_frames = self.frames_list[0]

        if self.segments_frames == self.past_frames:
            self.past_frames += self.frames_list[self.current_segment]
            self.current_segment +=1


class Segment:
    def __init__(self, animation_elements, color, element_numbers, time_in_ms, pattern, fps=120):
        self.animation_elements = animation_elements
        self.color = color
        self.element_numbers = element_numbers
        self.basic_status_color = (50, 50, 50)
        self.necessary_frames = int(fps * (time_in_ms/1000))
        self.pattern = pattern
        self.test = 0
        self.frame = 1

    #def set_color_pattern(self, color, number):
        #for number in self.numbers:
            #if number.number == number:
                #number.color = color

    def set_color(self):
        for number in self.element_numbers:
            self.animation_elements[number].change_color(self.color)
            if self.frame == self.necessary_frames:
                self.animation_elements[number].change_color(self.basic_status_color)

    def do_nothing(self):
        pass

    def fade_out_pattern(self, number, time_in_ms):
        pass

    def test_pattern_1(self):
        self.test += 1
        print(f"test_pattern_1: {self.frame}")

    def test_pattern_2(self):
        self.test += 1
        print(f"test_pattern_2: {self.frame}")

    def test_pattern_3(self):
        self.test += 1
        print(f"test_pattern_3: {self.frame}")

    def update(self):
        #print(self.frame)
        if self.pattern == "test_pattern_1":
            self.test_pattern_1()
        elif self.pattern == "test_pattern_2":
            self.test_pattern_2()
        elif self.pattern == "test_pattern_3":
            self.test_pattern_3()
        elif self.pattern == "set_color":
            self.set_color()
        elif self.pattern == "do_nothing":
            self.do_nothing() 

        self.frame += 1
        if self.frame == self.necessary_frames + 1:
            self.frame = 1


def draw_circle(radius, screen_width, surface):
    pygame.draw.circle(surface, (0, 100, 200), surface.get_rect().center, radius, int(screen_width/100))


def generate_numbers(radius, numbers_group, size, surface):
    angel_per_number = 360/12
    basic_status_color = (50, 50, 50)
    for i in range(1, 13):
        number = Number(str(i), size, surface.get_rect().center, basic_status_color, radius=radius, offset=50)
        number.rotate(i * angel_per_number)
        numbers_group.add(number)


def generate_tick_marks(radius, screen_width, tick_mark_group, surface):
    angle_per_minute = 360/60
    
    for second in range(0, 60):
        tick_length = screen_width/36
        tick_width = screen_width/400
        offset = -screen_width/48
        if second % 15 == 0:
            tick_length = screen_width/18
            tick_width = screen_width/80
            offset = -screen_width/28
        if second % 5 == 0 and not second % 15 == 0:
            tick_length = screen_width/18  
            tick_width = screen_width/160
            offset = -screen_width/28
        tick = PointSightingLine(surface.get_rect().center, tick_width, tick_length, (0, 100, 200), radius=radius, offset=offset)
        tick.rotate(second*angle_per_minute)
        tick_mark_group.add(tick)


def generate_hands(radius, hands_group, screen_width, surface):
    offset = -screen_width/4
    second_hand = Hand("second", (surface.get_rect().center), screen_width/400, screen_width/3, (0, 200, 200), radius=radius, offset=offset)
    minute_hand = Hand("minute", (surface.get_rect().center), screen_width/80, screen_width/3, (0, 150, 150), radius=radius, offset=offset)
    hour_hand = Hand("hour", (surface.get_rect().center), screen_width/80, screen_width/5, (0, 100, 150), radius=radius, offset=offset-screen_width/15)
    hands_group.add(minute_hand, hour_hand, second_hand)


def main():
    pygame.init()
    try:
        screen_width = 720

        window = pygame.display.set_mode((screen_width, screen_width))
        pygame.display.set_caption("Clock")

        background = pygame.Surface(window.get_size())
        
        # circle
        radius = min(window.get_rect().center) - screen_width/8
        assert radius > 0
        draw_circle(radius, screen_width, background)

        # hands
        hands_group = pygame.sprite.Group()
        generate_hands(radius, hands_group, screen_width, window)

        # numbers
        number_size = screen_width/12                                                                
        numbers_group = pygame.sprite.Group()
        generate_numbers(radius, numbers_group, number_size, window)

        # tick marks
        tick_mark_group = pygame.sprite.Group()
        generate_tick_marks(radius, screen_width, tick_mark_group, background)

        #testing segments and animations
        animation_elements = numbers_group.sprites()

        #segment_1 = Segment([1, 2, 3], 500, "test_pattern_1")
        #segment_2 = Segment([4, 5, 6], 250, "test_pattern_2")
        #segment_3 = Segment([4, 5, 6], 250, "test_pattern_3")
        segment_1 = Segment(animation_elements, (255, 0, 0), [0, 2], 200, "set_color")
        segment_2 = Segment(animation_elements, (0, 0, 255), [1, 3], 200, "set_color")
        segment_3 = Segment(animation_elements, (0, 255, 0), [2, 4], 200, "set_color")
        segment_4 = Segment(animation_elements, (255, 0, 255), [3, 5], 200, "set_color")
        segment_5 = Segment(animation_elements, (255, 255, 0), [4, 6], 200, "set_color")
        segment_6 = Segment(animation_elements, (0, 255, 255), [5, 7], 200, "set_color")
        segment_7 = Segment(animation_elements, (255, 255, 255), [6, 8], 200, "set_color")
        segment_8 = Segment(animation_elements, (255, 0, 0), [7, 9], 200, "set_color")
        segment_9 = Segment(animation_elements, (0, 0, 255), [8, 10], 200, "set_color")
        segment_10 = Segment(animation_elements, (0, 255, 0), [9, 11], 200, "set_color")
        #segment_11 = Segment(animation_elements, (255, 0, 255), [10, 12], 200, "set_color")

        segment_list = [segment_1, segment_2, segment_3, segment_4, segment_5, segment_6, segment_7, segment_8, segment_9, segment_10]

        animation = Animation(segment_list)
        print(segment_1.necessary_frames)
        #print(segment_2.necessary_frames)
        #print(segment_3.necessary_frames)
        print(f"total: {animation.total_necessary_frames}")
        print(animation.frames_list)

        clock = pygame.time.Clock()
        fps = 120
        frame = 0
        while True:
            window.fill((0, 0, 0))
            frame += 1
            window.blit(background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            tick_mark_group.draw(window)        

            now = DateTime.now()
            hands_group.update(now)
            hands_group.draw(window)
            
            numbers_group.update(frame)
            numbers_group.draw(window)

            animation.update(frame)

            pygame.display.update()
            clock.tick(fps)
            if frame == fps:
                frame = 0
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()