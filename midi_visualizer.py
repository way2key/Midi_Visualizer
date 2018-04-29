from pyglet.gl import *
from math import *
import time
import rtmidi
import sys

# Midi configuration

midi_in = rtmidi.MidiIn()
available_ports = midi_in.get_ports()
print(available_ports)
port = midi_in.open_port(1)

def printer(message, data):
    m = message[0][1]%12
    print(m)
    window.ring.notes[key_map[m]].played()




key_map = { 0:  "c",
            1:  "c#",
            2:  "d",
            3:  "d#",
            4:  "e",
            5:  "f",
            6:  "f#",
            7:  "g",
            8:  "g#",
            9:  "a",
            10: "a#",
            11: "b"
                    }

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
                tri = sorted(self.active.items(), key=lambda t: t[0])
                self.active = dict(tri)
            elif note in self.active.keys():
                self.active.pop(note)
        #print(self.active.keys())

        for note in self.active:
            x = (cos((self.sectors[note].angle / 2) + self.sectors[note].angle_in)  * self.sectors[note].inner_radius)
            y = (sin((self.sectors[note].angle / 2) + self.sectors[note].angle_in)  * self.sectors[note].inner_radius)
            self.vertex.extend([x,y,0])
            self.color.extend([140,140,240])

        for i in range(len(self.active) - 1):
            self.indices.extend([i, i + 1])
        self.indices.extend([len(self.active) - 1, 0])

        if len(self.active) > 2:
            self.vertices = pyglet.graphics.draw_indexed(len(self.active), GL_LINES, self.indices, ('v3f', self.vertex),('c3B',self.color))


class myWindow(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        icon = pyglet.image.load('icon.png')
        self.set_icon(icon)
        self.set_minimum_size(300, 300)
        glClearColor(0.2, 0.2, 0.21, 1)
        self.ring = ring()
        self.line = line(self.ring.notes)

    def on_draw(self):
        self.clear()
        self.ring.render()
        self.line.render()
        #self.ring.notes[key_map[0]].played()
        #self.ring.notes[key_map[0]].idle()

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)

    def on_key_press(self, key, modifier):
        if key == pyglet.window.key.ESCAPE:
            pyglet.app.exit()
            midi_in.close_port()
            print("Exit ;(")
            sys.exit()

    def on_key_release(self, key, modifier):
        if key == pyglet.window.key.Q:
            self.ring.notes[key_map[1]].played()



if __name__ == "__main__":
    window = myWindow(800, 800, "Midi_Visualizer", resizable=True)
    port.set_callback(printer)

    pyglet.app.run()
