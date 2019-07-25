"""
Created 7/25/19

Hopefully this turns out to be a half decent minecraft clone
"""

import pygame
import pygame.locals as lcl

import OpenGL.GL as GL
import OpenGL.GLU as GLU

import h5py as hdf

import multiprocessing
import threading

fileLocation="\\\\wales.es.anl.gov\\DataArchive\\Software\\SegView\\sample_data\dataset_01.hdf5"
points=[]
dataSet=None

move_map = {pygame.K_w: ( 0, 0, .1),
            pygame.K_s: ( 0, 0,-.1),
            pygame.K_a: ( .1, 0, 0),
            pygame.K_d: (-.1, 0, 0),
            pygame.K_q: (1000, 0, 0),
            pygame.K_e: (0, 1000, 0)}

def checkKeys():
    move=[]
    pressed = pygame.key.get_pressed()
    for key in move_map:
        if pressed[key]:
            move.append(move_map[key])
    for direction in move:
        if direction[0]==1000:
            GL.glRotatef(1, 0, 0, 1)
        elif direction[1]==1000:
            GL.glRotatef(1, 0, 1, 0)
        else:
            GL.glTranslatef(direction[0], direction[1], direction[2])
    
#
#def calculatePoints():
#    for 
    
def points():
    GL.glBegin(GL.GL_POINTS)
    GL.glVertex3fv()
    GL.glEnd()

def main():
    global count, dataSet
    pygame.init()
    display = (1000,750)
    pygame.display.set_mode(display, lcl.DOUBLEBUF|lcl.OPENGL)
    
    GLU.gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    
    GL.glTranslatef(0.0,0.0, -5)
    GL.glPointSize(10)
    file=hdf.File(fileLocation, 'r')
    dataSet=file.get(list(file.items())[0][0])
    chunkify(4)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
#        GL.glTranslatef(0.0,0.0, -.1)
        checkKeys()
#        GL.glRotatef(1, 3, 1, 1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)
        points()
        pygame.display.flip()
        pygame.time.wait(10)

def chunkify(numChunks):
    dataLength=len(dataSet)
    chunkSize=int(dataLength/numChunks)
    chunks=[]
    chunks.append((0,chunkSize-1))
    for i in range(2, numChunks-1):
        chunks.append((chunkSize*(i-1)), chunkSize*i)
    chunks.append((chunkSize*(numChunks-1), dataLength))
    print(chunks)

main()