#!/usr/bin/python
import math
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

# ======= HERE THE INTERESTING PART STARTS ======================================

# Import the Gyro class representing the sensor. You can have a look at it in the
# file mpu6050.py
from mpu6050 import Gyro

# Create a Gyro object for reading the data from the sensor.
gyro = Gyro()

def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | OPENGL | DOUBLEBUF)
    resizeScreen(*SCREEN_SIZE)
    init()
    cube = Cube((0.0, 0.0, 0.0), (.5, .5, .7))

    while True:        
        for event in pygame.event.get():
            if event.type == QUIT:
                gyro.stop_integration()
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                gyro.stop_integration()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor((1.,1.,1.))
        glLineWidth(1)
        glBegin(GL_LINES)
        draw_grid()

        # Read the angles of rotation about each of the axes from the sensor.
        # See the end of the mpu6050.py file for details on how this is
        # calculated. You will also find the first EXERCISE there.
        (x_angle, y_angle, z_angle) = gyro.get_angular_position()

        glEnd()
        glPushMatrix()
        glRotate(x_angle, 0, 0, 1)
        glRotate(y_angle, 1, 0, 0)
        glRotate(z_angle, 0, 1, 0)
        cube.render()
        glPopMatrix()
        pygame.display.flip()

# ========== BONUS EXERCISE ====================================================
# Can you break it? (Not physically, please.) Run the program and play around
# with the sensor. How can you make the image on the screen disaggree with the
# reality? Can you do something about it?
# WARNING - when you start the program, gyro will be calibrating for several
#           seconds. DO NOT move the sensor until it says it is calibrated.

# =========== END OF THE INTERESTING PART ======================================
# You don't need to read any further. The code below is only responsible 

class Cube(object):

    def __init__(self, position, color):
        self.position = position
        self.color = color

    # Cube information
    num_faces = 6

    vertices = [ (-1.0, -0.05, 0.5),
                 (1.0, -0.05, 0.5),
                 (1.0, 0.05, 0.5),
                 (-1.0, 0.05, 0.5),
                 (-1.0, -0.05, -0.5),
                 (1.0, -0.05, -0.5),
                 (1.0, 0.05, -0.5),
                 (-1.0, 0.05, -0.5) ]

    normals = [ (0.0, 0.0, +1.0),  # front
                (0.0, 0.0, -1.0),  # back
                (+1.0, 0.0, 0.0),  # right
                (-1.0, 0.0, 0.0),  # left
                (0.0, +1.0, 0.0),  # top
                (0.0, -1.0, 0.0) ] # bottom

    vertex_indices = [ (0, 1, 2, 3),  # front
                       (4, 5, 6, 7),  # back
                       (1, 5, 6, 2),  # right
                       (0, 4, 7, 3),  # left
                       (3, 2, 6, 7),  # top
                       (0, 1, 5, 4) ] # bottom

    def render(self):
        #then = pygame.time.get_ticks()
        glColor(self.color)

        colors = [(1,0,0),self.color,(0,1,0),self.color,(0,0,1),self.color]

        vertices = self.vertices

        # Draw all 6 faces of the cube
        glBegin(GL_QUADS)

        for face_no in xrange(self.num_faces):
            glNormal3dv(self.normals[face_no])
            v1, v2, v3, v4 = self.vertex_indices[face_no]
            glColor(colors[face_no])
            glVertex(vertices[v1])
            glVertex(vertices[v2])
            glVertex(vertices[v3])
            glVertex(vertices[v4])
            
        glEnd()



SCREEN_SIZE = (1200, 900)


def resizeScreen(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / height, 0.001, 10.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 1.0, -5.0,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0)


def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_BLEND)
    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1.0));


def draw_grid():
    for x in range(-20, 22, 2):
        glVertex3f(x/10.,-1,-1)
        glVertex3f(x/10.,-1,1) 
    for x in range(-20, 22, 2):
        glVertex3f(x/10.,-1, 1)
        glVertex3f(x/10., 1, 1)
    for z in range(-10, 12, 2):
        glVertex3f(-2, -1, z/10.)
        glVertex3f( 2, -1, z/10.)
    for z in range(-10, 12, 2):
        glVertex3f(-2, -1, z/10.)
        glVertex3f(-2,  1, z/10.)
    for z in range(-10, 12, 2):
        glVertex3f( 2, -1, z/10.)
        glVertex3f( 2,  1, z/10.)
    for y in range(-10, 12, 2):
        glVertex3f(-2, y/10., 1)
        glVertex3f( 2, y/10., 1)
    for y in range(-10, 12, 2):
        glVertex3f(-2, y/10., 1)
        glVertex3f(-2, y/10., -1)
    for y in range(-10, 12, 2):
        glVertex3f(2, y/10., 1)
        glVertex3f(2, y/10., -1)



if __name__ == "__main__":
    run()
