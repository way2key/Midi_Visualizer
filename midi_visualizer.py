from pyglet.gl import *
from math import *
import operator

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
        self.state = 0
        self.inner_point = angle/2+angle
        for i in range(self.points):
            angle = self.angle * (i / (self.points - 1)) + angle_in
            x = cos(angle) * radius
            y = sin(angle) * radius
            z = 0
            self.vertex.extend([x,y,z])
        for i in range(self.points):
            angle = self.angle - self.angle * (i/(self.points-1)) + angle_in
            x = cos(angle) * inner_radius
            y = sin(angle) * inner_radius
            z = 0
            self.vertex.extend([x,y,z])
        for i in range(self.points - 1):
            n = 2 * self.points - 1
            self.indices.extend([i, i + 1 , n - i])
            self.indices.extend([n - i, n - 1 - i, i + 1])
    def render(self):
        if self.state == 0:
            self.idle()
        elif self.state == 1:
            self.played()
    def played(self):
        self.state = 1
        self.color = []
        for i in range(2 * self.points):
            self.color.extend([0,255,0])
        self.vertices = pyglet.graphics.draw_indexed(2 * self.points, GL_TRIANGLES, self.indices, ('v3f', self.vertex),('c3B',self.color))
    def idle(self):
        self.state = 0
        self.color = []
        for i in range(self.points):
            self.color.extend([255,8,45])
        for i in range(self.points):
            self.color.extend([255,120,12])
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
            self.notes[note] = sector(0.8, 0.7, pi / 6.4, 2 * i * pi / 12, 360)
            i += 1
    def render(self):
        for note in self.notes:
            self.notes[note].render()

class line(object):
    def __init__(self,sectors):
        self.indices = []
        self.vertex = []
        self.color = []
        self.sectors = sectors
        self.active = {}


    def render(self):
        self.indices = []
        self.vertex = []
        self.color = []

        for note,sector in self.sectors.items():
            if sector.state == 1 :
                self.active[note] = note

            elif note in self.active.keys() :
                self.active.pop(note)

        print(self.active.keys(),note)

        for note in self.active:
            x = (cos((self.sectors[note].angle / 2) + self.sectors[note].angle_in)  * self.sectors[note].inner_radius)
            y = (sin((self.sectors[note].angle / 2) + self.sectors[note].angle_in)  * self.sectors[note].inner_radius)
            self.vertex.extend([x,y,0])
            self.color.extend([140,140,140])

        for i in range(len(self.active)-1):
            self.indices.extend([i, i + 1])

        if len(self.active) > 1:
            self.vertices = pyglet.graphics.draw_indexed(len(self.active), GL_LINES, self.indices, ('v3f', self.vertex),('c3B',self.color))


class myWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(300, 300)
        glClearColor(0.2, 0.2, 0.21, 1)
        self.ring = ring()
        self.line = line(self.ring.notes)


    def on_draw(self):
        self.clear()
        self.ring.render()
        self.line.render()


    def on_resize(self, width, height):
        glViewport(0, 0, width, height)

    def on_key_press(self, key, modifier):
        #default behavior
        if key == pyglet.window.key.ESCAPE:
            pyglet.app.exit()
        # Mapping key presses
        if key == pyglet.window.key.Q:
            self.ring.notes['c'].played()
        elif key == pyglet.window.key.W:
            self.ring.notes['c#'].played()
        elif key == pyglet.window.key.E:
            self.ring.notes['d'].played()
        elif key == pyglet.window.key.R:
            self.ring.notes['d#'].played()
        elif key == pyglet.window.key.T:
            self.ring.notes['e'].played()
        elif key == pyglet.window.key.Z:
            self.ring.notes['f'].played()
        elif key == pyglet.window.key.U:
            self.ring.notes['f#'].played()
        elif key == pyglet.window.key.I:
            self.ring.notes['g'].played()
        elif key == pyglet.window.key.O:
            self.ring.notes['g#'].played()
        elif key == pyglet.window.key.P:
            self.ring.notes['a'].played()
        elif key == pyglet.window.key.A:
            self.ring.notes['a#'].played()
        elif key == pyglet.window.key.S:
            self.ring.notes['b'].played()

    def on_key_release(self, key, modifier):
        #for note in self.ring.notes:
            #self.ring.notes[note].idle()
        if key == pyglet.window.key.Q:
            self.ring.notes['c'].idle()
        elif key == pyglet.window.key.W:
            self.ring.notes['c#'].idle()
        elif key == pyglet.window.key.E:
            self.ring.notes['d'].idle()
        elif key == pyglet.window.key.R:
            self.ring.notes['d#'].idle()
        elif key == pyglet.window.key.T:
            self.ring.notes['e'].idle()
        elif key == pyglet.window.key.Z:
            self.ring.notes['f'].idle()
        elif key == pyglet.window.key.U:
            self.ring.notes['f#'].idle()
        elif key == pyglet.window.key.I:
            self.ring.notes['g'].idle()
        elif key == pyglet.window.key.O:
            self.ring.notes['g#'].idle()
        elif key == pyglet.window.key.P:
            self.ring.notes['a'].idle()
        elif key == pyglet.window.key.A:
            self.ring.notes['a#'].idle()
        elif key == pyglet.window.key.S:
            self.ring.notes['b'].idle()


if __name__ == "__main__":
    windows = myWindow(800, 800, "midi_visualizer", resizable=True)
    pyglet.app.run()
