import pygame

from rope import *


# Sweetie 16 Palette
colors = {
    "black":       (26,  28,  44),
    "maroon":      (93,  39,  93),
    "red":         (177, 62,  83),
    "orange":      (239, 125, 87),
    "yellow":      (255, 205, 117),
    "light_green": (167, 240, 112),
    "green":       (56,  183, 100),
    "dark_green":  (37,  113, 121),
    "dark_blue":   (41,  54,  111),
    "blue":        (59,  93,  201),
    "light_blue":  (65,  166, 246),
    "baby_blue":   (115, 239, 247),
    "white":       (244, 244, 244),
    "light_gray":  (148, 176, 194),
    "gray":        (86,  108, 134),
    "dark_gray":   (51,  60,  87)
}

display_size = (1920, 1080)


pygame.init()

display = pygame.display.set_mode(display_size, pygame.DOUBLEBUF)
clock   = pygame.time.Clock()
font    = pygame.font.SysFont("Arial", 50)

bow_image   = pygame.transform.scale(pygame.image.load("resources/bow.png"), (320, 640))
arrow_image = pygame.transform.scale(pygame.image.load("resources/arrow.png"), (320, 100))

pygame.display.set_caption("Bow and Arrow")


rope = Rope(25, 50, Vector(350, 300), Vector(350, 850))
rope.segment_length = 20


class Arrow:
    def __init__(self, position: Vector, velocity: Vector) -> None:
        self.position = position
        self.velocity = velocity
    
    def draw(self, surface: pygame.Surface) -> None:
        draw_position = (self.position - Vector(0, 25)).to_tuple()
        surface.blit(arrow_image, draw_position)
        
    def update(self, gravity: Vector, delta_time: float) -> None:
        self.velocity += gravity * delta_time
        self.position += self.velocity * delta_time


arrow = Arrow(rope.nodes[12].position, Vector(0, 0))
shot = False

string_held = False

initial_position = rope.nodes[12].position


run = True
while run:
    delta_time = clock.tick(60) / 1000
    mouse_position = Vector(*pygame.mouse.get_pos())
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if pygame.mouse.get_pressed()[0]:
        if rope.nodes[12].position.distance(mouse_position) <= 100 or string_held:
            rope.nodes[12].position = mouse_position
            string_held = True
    else:
        if string_held:
            string_held = False
            shot = True
            arrow.velocity = (initial_position - rope.nodes[12].position) * 20
        
    rope.update(Vector(0, 2500), delta_time, 20)

    if string_held:
        arrow.position = rope.nodes[12].position
    elif shot == True:
        arrow.update(Vector(0, 2500), delta_time)

    display.fill(colors["black"])

    display.blit(bow_image, (250, 250))
    
    for i in range(len(rope.nodes) - 1):
        pygame.draw.line(display, colors["white"],
                         rope.nodes[i].position.to_tuple(), rope.nodes[i + 1].position.to_tuple(), 5)
    
    arrow.draw(display)
    
    pygame.display.flip()
