import pygame
import sys

def run_screen():
    pygame.init()
    logical_size = (64, 64)
    display_size = (500, 500)
    
    draw_surface = pygame.Surface(logical_size)
    screen = pygame.display.set_mode(display_size)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_surface.fill((0, 0, 0)) 

        draw_surface.set_at((10, 10), (255, 255, 255))  # pixel (10, 10) to white

        # Skalieren und auf Bildschirm zeichnen (keine Ahnung warum das jetzt funktioniert)
        scaled_surface = pygame.transform.scale(draw_surface, display_size)
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        clock.tick(30)  # 30 FPS limit

if __name__ == "__main__":
    run_screen()