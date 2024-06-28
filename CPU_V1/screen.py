import pygame
import sys
import random

class pygameDisplay:
    def __init__(self, ram):
        self.ram = ram
        self.colors = ["#000000" for i in range(4096)]
    
    def translateRamToColors(self):
        color_bytes = self.ram.registers[63488:] # letzten 2 kb 
        
        for i, color_byte in enumerate(color_bytes):
            match color_byte.getByte()[:4]:
                case "0000":
                    first_color = (0, 0, 0)  
                case "1111":
                    first_color = (255, 255, 255)  
                case _:
                    first_color = (221, 0, 255)  

            match color_byte.getByte()[4:]:
                case "0000":
                    second_color = (0, 0, 0) 
                case "1111":
                    second_color = (255, 255, 255)
                case _:
                    second_color = (221, 0, 255) 

            self.colors[i*2] = first_color
            self.colors[i*2+1] = second_color


    def run(self):
        pygame.init()
        logical_size = (64, 64)
        display_size = (500, 500)
        
        draw_surface = pygame.Surface(logical_size)
        screen = pygame.display.set_mode(display_size)
        clock = pygame.time.Clock()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.translateRamToColors()

            draw_surface.fill((0, 0, 0))

            for i, color in enumerate(self.colors):
                x = i % 64
                y = i // 64
                draw_surface.set_at((x, y), color)

            # Skalieren und auf Bildschirm zeichnen (keine Ahnung warum das jetzt funktioniert)
            scaled_surface = pygame.transform.scale(draw_surface, display_size)
            screen.blit(scaled_surface, (0, 0))

            pygame.display.flip()
            clock.tick(30)  # 30 FPS limit
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    pass