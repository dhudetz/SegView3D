"""
Created 7/25/19

Hopefully this turns out to be a half decent minecraft clone
"""

import pygame
import pygame.locals as lcl

import OpenGL.GL as GL
import OpenGL.GLU as GLU

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )


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
    

def Cube():
    GL.glBegin(GL.GL_LINES)
    for edge in edges:
        for vertex in edge:
            GL.glVertex3fv(verticies[vertex])
    GL.glEnd()

def main():
    global count
    pygame.init()
    display = (1000,750)
    pygame.display.set_mode(display, lcl.DOUBLEBUF|lcl.OPENGL)
    
    GLU.gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    
    GL.glTranslatef(0.0,0.0, -5)
    GL.glPointSize(100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
#        GL.glTranslatef(0.0,0.0, -.1)
        checkKeys()
#        GL.glRotatef(1, 3, 1, 1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)

main()