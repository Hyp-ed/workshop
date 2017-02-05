#!/usr/bin/python

import smbus
import math
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from time import time
import mpu6050

SCREEN_SIZE = (1200, 900)
#SCALAR = .5
#SCALAR2 = 0.2
#AVERAGE = 0
GYRO_W = 0.0
ACCL_W = 1.0 - GYRO_W


def get_y_rotation(x, z):
    radians = math.atan2(-x, z)
    return math.degrees(radians)


def get_x_rotation(y, z):
    radians = math.atan2(y, z)
    return math.degrees(radians)


def get_offset():
    xsum = 0
    ysum = 0
    zsum = 0
    n = 1000.0
    print 'Calibrating gyro...'
    t = time()
    for i in xrange(0, int(n)):
        (x, y, z) = mpu6050.read_gyro_data()
        xsum += x
        ysum += y
        zsum += z
    t = time() - t
    print 'Calibrated on {} readings in {} seconds'.format(int(n), t)
    return (xsum/n, ysum/n, zsum/n)


def get_gyro_scaled():
    (x, y, z) = mpu6050.read_gyro_data()
    return ((x - X_OFF)/mpu6050.GYRO_SCALE, (y - Y_OFF)/mpu6050.GYRO_SCALE, (z - Z_OFF)/mpu6050.GYRO_SCALE)


def get_accl_scaled():
    (x, y, z) = mpu6050.read_accl_data()
    return (x/mpu6050.ACCL_SCALE, y/mpu6050.ACCL_SCALE, z/mpu6050.ACCL_SCALE)


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

(X_OFF, Y_OFF, Z_OFF) = get_offset()

def run():
    #global gyro_total_x, gyro_total_y, last_x, last_y
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | OPENGL | DOUBLEBUF)
    resizeScreen(*SCREEN_SIZE)
    init()
    #clock = pygame.time.Clock()
    cube = Cube((0.0, 0.0, 0.0), (.5, .5, .7))

    (x_angle, y_angle, z_angle) = (0, 0, 0)
    t0 = time()
    r0 = get_gyro_scaled()
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glColor((1.,1.,1.))
        glLineWidth(1)
        glBegin(GL_LINES)


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


        #(angle, (x, y, z)) = get_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
        (x, y, z) = mpu6050.read_accl_data()
        accl_dx = get_x_rotation(y, z) - x_angle
        accl_dy = get_y_rotation(x, z) - y_angle

        t = time()
        r = get_gyro_scaled()
        dt = t - t0
        gyro_dx = (r0[0] + r[0])/2 * dt
        gyro_dy = (r0[1] + r[1])/2 * dt
        gyro_dz = (r0[2] + r[2])/2 * dt
        t0 = t
        r0 = r

        #print 'gx={0:10.6f}|  ax={1:10.6f}|  gy={2:10.6f}|  ay={3:10.6f}'.format(gyro_x, accl_x, gyro_y, accl_y)

        x_angle += ACCL_W*accl_dx + GYRO_W*gyro_dx
        y_angle += ACCL_W*accl_dy + GYRO_W*gyro_dy
        z_angle += gyro_dz
	print '{:10.6f}  {:10.6f}  {:10.6f}'.format(x_angle, y_angle, z_angle)

        glEnd()
        glPushMatrix()
        glRotate(x_angle, 1, 0, 0)
        glRotate(y_angle, 0, 0, 1)
        glRotate(z_angle, 0, 1, 0)
        #glRotate(angle, x, z, y)
        cube.render()
        glPopMatrix()
        pygame.display.flip()

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

if __name__ == "__main__":
    run()
