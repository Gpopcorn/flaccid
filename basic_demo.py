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

pygame.display.set_caption("Basic Demo")

paused_text = font.render("PAUSED", True, colors["white"])


rope = Rope(30, 50, Vector(500, 50), Vector(1500, 1050))
environment = [Circle(Vector(500, 500), 250), Rectangle(Vector(1200, 350), Vector(300, 400))]


run    = True
paused = True
while run:
    delta_time = clock.tick() / 1000
    mouse_position = Vector(*pygame.mouse.get_pos())
    
    right_click = False
    
    if not paused:
        rope.update(Vector(0, 5000), delta_time, 40, environment)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3: # right click
                right_click = True
                for node in rope.nodes:
                    if mouse_position.distance(node.position) <= 10:
                        node.fixed = not node.fixed
                        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
                        
    if pygame.mouse.get_pressed()[0]: # left held
        if not node_held:
            for node in rope.nodes:
                if mouse_position.distance(node.position) <= 10:
                    if right_click:
                        node.fixed = not node.fixed
                    node_held = node
    else: # left released
        node_held = None
        
    if node_held:
        node_held.position = mouse_position
            
    display.fill(colors["black"])
    
    for x in range(0, display_size[0], 100):
        pygame.draw.line(display, colors["dark_gray"], (x, 0), (x, display_size[1]))
    for y in range(0, display_size[1], 100):
        pygame.draw.line(display, colors["dark_gray"], (0, y), (display_size[0], y))
    
    # draw links
    for i in range(len(rope.nodes) - 1):
        pygame.draw.line(display, colors["white"],
                         rope.nodes[i].position.to_tuple(), rope.nodes[i + 1].position.to_tuple(), 5)
    
    # draw nodes
    for node in rope.nodes:
        color = "red" if node.fixed else "light_blue"
        pygame.draw.circle(display, colors[color], node.position.to_tuple(), 7)
    
    # draw environment
    for object in environment:
        if type(object) == Rectangle:
            position = object.center - object.size * (1 / 2)
            pygame.draw.rect(display, colors["green"], (position.to_tuple(), object.size.to_tuple()))
            pygame.draw.rect(display, colors["white"], (position.to_tuple(), object.size.to_tuple()), 5)
        elif type(object) == Circle:
            pygame.draw.circle(display, colors["green"], object.center.to_tuple(), object.radius)
            pygame.draw.circle(display, colors["white"], object.center.to_tuple(), object.radius, 5)
    
    if paused:
        display.blit(paused_text, (display_size[0] // 2 - paused_text.get_size()[0] // 2, 75))
    
    pygame.display.flip()
