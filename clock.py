from datetime import datetime as DateTime
import pygame
from pygame import Vector2
import pygame.freetype
import time


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


class Animations:
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
    def __init__(self, animation_elements, pattern, color=(50, 50, 50), elements=[], time_in_ms=1000, fps=120):
        self.animation_elements = animation_elements
        self.color = color
        self.elements = elements
        self.basic_status_color = (50, 50, 50)
        self.necessary_frames = int(fps * (time_in_ms/1000))
        self.pattern = pattern
        self.test = 0
        self.frame = 1

    def set_color(self):
        for element in self.elements:
            self.animation_elements[element].change_color(self.color)
            if self.frame == self.necessary_frames:
                self.animation_elements[element].change_color(self.basic_status_color)

    def do_nothing(self):
        pass

    def fade_out_pattern(self, number, time_in_ms):
        pass

    def fade_in(self, from_color, to_color, time_in_ms):
        pass

    def permanent_color(self):
        for number in self.element_numbers:
            self.animation_elements[number].change_color(self.color)

    def update(self):
        if self.pattern == "set_color":
            self.set_color()
        elif self.pattern == "do_nothing":
            self.do_nothing() 
        elif self.pattern == "permanent_color":
            self.permanent_color()

        self.frame += 1
        if self.frame == self.necessary_frames + 1:
            self.frame = 1


class SegmentGenerator:
    def __init__(self):
        pass

    def set_color(self):
        pass


class AnimationGenerator:
    def __init__(self, animation_elements):
        self.animation_elements = animation_elements

    def raising_circling_num(self, rounds_per_ms_1, rounds_per_ms_2, number_of_steps, color=(255, 255, 255)):
        segments = []

        element_time = rounds_per_ms_1/12
        half_time = rounds_per_ms_2/2
        step_time = half_time/(number_of_steps-1)

        for j in range(0, number_of_steps):
            for i in range(0, 12):
                segments.append(Segment(self.animation_elements, "set_color", color=color, elements=[i], time_in_ms=element_time))
                print(segments[i])

            element_time += step_time/12

        return segments

    def circling_num(self, rounds, color=(255, 255, 255), clockwise=True, ms_per_num=100):
        segments = []
        for j in range(0, rounds):
            if clockwise:
                for i in range(0, 12):
                    segments.append(Segment(self.animation_elements, "set_color", color=color, elements=[i], time_in_ms=ms_per_num))
            else:
                for i in range(11, -1, -1):
                    segments.append(Segment(self.animation_elements, "set_color", color=color, elements=[i], time_in_ms=ms_per_num))

        return segments


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


def load_animations(numbers_group):

    animation_elements = numbers_group.sprites()

    animation_generator = AnimationGenerator(animation_elements)

    # segments
    segments = []
    # animations
    raising_circling_num = animation_generator.raising_circling_num(250, 2000, 10, color=(0, 255, 0))
    circling_num_counter_clockwise = animation_generator.circling_num(2, color=(0, 255, 0), clockwise=False)
    circling_num_clockwise = animation_generator.circling_num(2, color=(0, 255, 0))
    # animation groups
    animation_group = [circling_num_counter_clockwise, raising_circling_num, circling_num_clockwise]
    # add animations from animation_groups to animations_list
    animation_groups = [animation_group]

    animations_list = []
    for animation_group in animation_groups:
        for animation in animation_group:
            animations_list.append(animation)

    segment_list = []

    for animation in animations_list:
        for segment in animation:
            segment_list.append(segment)

    return segment_list


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
        
        animations = Animations(load_animations(numbers_group))

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

            animations.update(frame)

            pygame.display.update()
            clock.tick(fps)
            if frame == fps:
                frame = 0
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()