import pygame
import sys
import random

def color_picker(string: str):
    match string:
        case "0000":
            return (0, 0, 0)
        case "0001":
            return (157, 157, 157)
        case "0010":
            return (255, 255, 255)
        case "0011":
            return (190, 38, 51)
        case "0100":
            return (224, 111, 139)
        case "0101":
            return (73, 60, 43)
        case "0110":
            return (164, 100, 34)
        case "0111":
            return (235, 137, 49)
        case "1000":
            return (247, 226, 107)
        case "1001":
            return (47, 72, 78)
        case "1010":
            return (68, 137, 26)
        case "1011":
            return (163, 206, 39)
        case "1100":
            return (27, 38, 50)
        case "1101":
            return (0, 87, 132)
        case "1110":
            return (49, 162, 242)
        case "1111":
            return (178, 220, 239)
        case _:
            print("Color out of bounds (color_picker)")
            return (255, 0, 255)

class pixelDisplay:
    def __init__(self, ram):
        self.ram = ram
        self.colors = ["#000000" for i in range(4096)]
    
    def translateRamToColors(self):
        color_bytes = self.ram.registers[63488:65536] # letzten 2 kb 
        
        for i, color_byte in enumerate(color_bytes):
            self.colors[i*2] = color_picker(color_byte.getByte()[:4])
            self.colors[i*2+1] = color_picker(color_byte.getByte()[4:])


    def run(self):
        pygame.init()
        logical_size = (64, 64)
        display_size = (500, 500)
        
        draw_surface = pygame.Surface(logical_size)
        screen = pygame.display.set_mode(display_size)
        clock = pygame.time.Clock()
        pygame.display.set_caption('Pixelbased Display')
        pygame.display.set_icon(pygame.image.load("anderes/images/icon.png"))
        
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