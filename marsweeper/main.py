import pygame
from pygame.locals import *

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
        self.square = 40
        self.margin = 5
        self.grid_colour = (255, 255, 255)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, RESIZABLE)
        self._running = True

    def render_grid(self):
        for row in range(10):
            for column in range(10):
                # print("PRINT")
                pygame.draw.rect(
                          self._display_surf,
                          self.grid_colour,
                          [(self.margin + self.square) * column + self.margin,
                          (self.margin + self.square) * row + self.margin,
                          self.square,
                          self.square]
                )
        pygame.display.update()
        
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()


    def on_execute(self):
        if self.on_init() == False:
            self._running == False

        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
