"""
Created 7/25/19

Hopefully this turns out to be a half decent minecraft clone
"""

import pygame
import pygame.locals as lcl

import OpenGL.GL as GL
import OpenGL.GLU as GLU

import h5py as hdf

import threading
from numpy import array
from scipy.ndimage import sobel

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
            GL.glRotatef(5, 1, 0, 0)
        elif direction[1]==1000:
            GL.glRotatef(5, 0, 0, 1)
        else:
            GL.glTranslatef(direction[0], direction[1], direction[2])
    
def calculatePoints(images):
    for i in range(images[0], images[1], 50):
        image=array(dataSet[i,:,:])
        for j in range(0, len(image), 10):
            highestPoint=-1
            lowestPoint=-1
            for k in range(0, len(image[j]), 10):
                if image[j][k]==1.0:
                    highestPoint=k
                    if lowestPoint==-1:
                        lowestPoint=k
            if highestPoint!=-1:
                if lowestPoint!=highestPoint:
                    points.append(((j-(len(image)/2))/100, (lowestPoint-(len(image)/2))/100, i/70))
                points.append(((j-(len(image)/2))/100, (highestPoint-(len(image)/2))/100, i/70))

def drawPoints():
    GL.glBegin(GL.GL_POINTS)
    for p in points:
        GL.glVertex3fv(p)
    GL.glEnd()

def chunkify(numChunks):
    dataLength=len(dataSet)
    chunkSize=int(dataLength/numChunks)
    chunks=[]
    chunks.append((0,chunkSize-1))
    for i in range(numChunks-1):
        chunks.append((chunkSize*(i-1), chunkSize*i))
    chunks.append((chunkSize*(numChunks-1), dataLength-1))
    processes=[]
    for i in range(numChunks):
        processes.append(threading.Thread(target=calculatePoints, args=(chunks[i],)))
    for p in processes:
        p.start()
    print(processes)

def main():
    global count, dataSet
    file=hdf.File(fileLocation, 'r')
    dataSet=file.get(list(file.items())[0][0])
    chunkify(40)
    pygame.init()
    display = (2000, 1000)
    pygame.display.set_mode(display, lcl.DOUBLEBUF|lcl.OPENGL)
    
    GLU.gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    
    GL.glTranslatef(0.0,0.0, -20)
    GL.glPointSize(1)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        checkKeys()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)
        drawPoints()
        pygame.display.flip()
        pygame.time.wait(10)



main()