import time

import sdl2
import sdl2.ext
from fseq import parse

sdl2.ext.init()

fseq = parse(open('./tests/test.fseq', 'rb'))


class FseqDemo:
    start_frame = 2130 # more interesting
    size = (500, 300)

    def __init__(self):
        self.window = sdl2.ext.Window("fseq demo", size=self.size, flags=sdl2.SDL_WINDOW_ALLOW_HIGHDPI)
        self.renderer = sdl2.ext.Renderer(self.window)
        self.fontmanager = sdl2.ext.FontManager('/Library/Fonts/Arial.ttf', size=23, bg_color=(255, 0, 0))

    def draw_light(self, index, color):
        padding_top = 30
        x, y = (index % 100, index // 100)
        rect = (x * 10, padding_top + y * 10, 10, 10)
        self.renderer.fill([rect], color)

    def draw_frame_label(self, frame_index):
        surface = self.fontmanager.render('Frame %d' % frame_index)
        texture = sdl2.SDL_CreateTextureFromSurface(self.renderer.sdlrenderer, surface)
        x, y, w, h = surface.clip_rect.x, surface.clip_rect.y, surface.clip_rect.w, surface.clip_rect.h
        self.renderer.copy(texture.contents, dstrect=(x, y, w, h))

    def run(self):
        self.window.show()

        frame_index = self.start_frame

        running = True
        while running:
            events = sdl2.ext.get_events()
            for event in events:
                if event.type in (sdl2.SDL_QUIT, sdl2.SDL_WINDOWEVENT_CLOSE):
                    running = False
                    break

            self.draw_frame_label(frame_index)

            frame = fseq.get_frame(frame_index)

            for i in range(fseq.channel_count_per_frame // 3):
                r, g, b = frame[i * 3], frame[i * 3 + 1], frame[i * 3 + 2]
                self.draw_light(i, (r, g, b))

            frame_index = (frame_index + 1) % fseq.number_of_frames

            self.renderer.present()
            self.window.refresh()

if __name__ == '__main__':
    FseqDemo().run()
