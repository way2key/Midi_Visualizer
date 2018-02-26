from pyglet.gl import *
from math import *


class sector(object):
    def __init__(self, radius, inner_radius, angle, angle_in, points):
        self.radius = radius
        self.inner_radius = inner_radius
        self.angle = angle
        self.angle_in = angle_in
        self.points = points
        self.vertex = []
        self.color = []
        self.indices = []
        for i in range(points):
            angle = self.angle * (i / (points - 1)) + angle_in
            x = cos(angle) * radius
            y = sin(angle) * radius
            z = 0
            self.vertex.extend([x,y,z])
            self.color.extend([255, 8, 45])
        for i in range(points):
            angle = self.angle - self.angle * (i/(points-1)) + angle_in
            x = cos(angle) * inner_radius
            y = sin(angle) * inner_radius
            z = 0
            self.vertex.extend([x,y,z])
            self.color.extend([255,120,12])
        for i in range(points - 1):
            n = 2 * points - 1
            self.indices.extend([i, i + 1 , n - i])
            self.indices.extend([n - i, n - 1 - i, i + 1])
    def render(self):
        self.vertices = pyglet.graphics.draw_indexed(2 * self.points, GL_TRIANGLES, self.indices, ('v3f', self.vertex),('c3B',self.color))
    def played(self):
        self.color = []
        for i in range(2 * self.points):
            self.color.extend([0,0,255])
        self.vertices = pyglet.graphics.draw_indexed(2 * self.points, GL_TRIANGLES, self.indices, ('v3f', self.vertex),('c3B',self.color))

class ring(object):
    def __init__(self):
        self.notes = {
        'c' : None,
        'c#': None,
        'd' : None,
        'd#': None,
        'e' : None,
        'f' : None,
        'f#': None,
        'g' : None,
        'g#': None,
        'a' : None,
        'a#': None,
        'b' : None
        }
        i = 0
        for note in self.notes:
            self.notes[note] = sector(0.7, 0.6, pi / 6.4, 2 * i * pi / 12, 360)
            i += 1
    def render(self):
        for note in self.notes:
            self.notes[note].render()

class myWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(300, 300)
        glClearColor(0.2, 0.2, 0.21, 1)
        self.ring = ring()
        self.draw_list = []
        self.sectors = [sector(0.7, 0.6, pi / 6.4, 2 * n * pi / 12, 360) for n in range(12)]
    def on_draw(self):
        self.clear()
        self.ring.render()

        for sector in self.draw_list:
            sector.played()

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)

    def on_key_press(self, key, modifier):
        #default behavior
        if key == pyglet.window.key.ESCAPE:
            pyglet.app.exit()
        # Mapping key presses
        if key == pyglet.window.key.Q:
            self.draw_list.append(self.sectors[0])
        elif key == pyglet.window.key.W:
            self.draw_list.append(self.sectors[1])
        elif key == pyglet.window.key.E:
            self.draw_list.append(self.sectors[2])
        elif key == pyglet.window.key.R:
            self.draw_list.append(self.sectors[3])
        elif key == pyglet.window.key.T:
            self.draw_list.append(self.sectors[4])
        elif key == pyglet.window.key.Z:
            self.draw_list.append(self.sectors[5])
        elif key == pyglet.window.key.U:
            self.draw_list.append(self.sectors[6])
        elif key == pyglet.window.key.I:
            self.draw_list.append(self.sectors[7])
        elif key == pyglet.window.key.O:
            self.draw_list.append(self.sectors[8])

    def on_key_release(self, key, modifier):
        self.draw_list.clear()




if __name__ == "__main__":
    windows = myWindow(800, 800, "midi_visualizer", resizable=True)
    pyglet.app.run()
