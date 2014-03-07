import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

  
def load_obj(filename, swapyz=False):
    """Loads a Wavefront OBJ file. """
    vertices = []
    normals = []
    texcoords = []
    faces = []

    material = None
    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'v':
            v = map(float, values[1:4])
            if swapyz:
                v = v[0], v[2], v[1]
            vertices.append(v)
        elif values[0] == 'vn':
            v = map(float, values[1:4])
            if swapyz:
                v = v[0], v[2], v[1]
            normals.append(v)
        elif values[0] == 'vt':
            texcoords.append(map(float, values[1:3]))
        elif values[0] == 'f':
            face = []
            texcoords = []
            norms = []
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0:
                    texcoords.append(int(w[1]))
                else:
                    texcoords.append(0)
                if len(w) >= 3 and len(w[2]) > 0:
                    norms.append(int(w[2]))
                else:
                    norms.append(0)
            faces.append((face, norms, texcoords, material))

    gl_list = glGenLists(1)
    glNewList(gl_list, GL_COMPILE)
    glEnable(GL_TEXTURE_2D)
    glFrontFace(GL_CCW)
    for face in faces:
        lvertices, lnormals, ltexture_coords, lmaterial = face


        glBegin(GL_POLYGON)
        for i in range(len(lvertices)):
            if lnormals[i] > 0:
                glNormal3fv(normals[lnormals[i] - 1])
            glVertex3fv(vertices[lvertices[i] - 1])
        glEnd()
    glDisable(GL_TEXTURE_2D)
    glEndList()
    return gl_list


def project_obj(srf, cam, obj_file, image=None):
 
    viewport = srf.get_size()

    # LOAD OBJECT AFTER PYGAME INIT
    obj_gl_list = load_obj("resources/"+obj_file, swapyz=True)
          
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = srf.get_size()
    gluPerspective(90.0, width/float(height), 1, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
     
    rx, ry = (0,0)
    xpos, ypos, zpos = (0,0, 0)
    camx, camy, camz = cam
    up = (0, 0, 1)
    for i in range(2):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        gluLookAt (camx, camy, camz, 0, 0, 0, 0, 0, 1);
        # RENDER OBJECT
        glTranslate(xpos, ypos, zpos)
        glRotate(ry, 1, 0, 0)
        glRotate(rx, 0, 1, 0)
        glCallList(obj_gl_list)
        
        pygame.display.flip()
        
    if image:
        pygame.image.save(srf, "resources/"+image)
    return glReadPixels(0, 0, viewport[0], viewport[1], GL_RGB, GL_UNSIGNED_INT)
    
def project_sphere(srf, cam, pos, image=None):
    
    viewport = srf.get_size()
    radius = 5
     
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = viewport
    gluPerspective(90.0, width/float(height), 1, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
     
   
    camx, camy, camz = cam
    
    for _ in range(2):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt (camx, camy, camz, 0, 0, 0, 0, 0, 1);

        # RENDER OBJECT
        for (x,y,z) in pos:
            
            quadric = gluNewQuadric()
            glPushMatrix()
            glTranslate(x, y, z)
            gluSphere( quadric , radius , 36 , 18 )
            glPopMatrix()

        pygame.display.flip()
        
    if image:
        pygame.image.save(srf, "resources/"+image)
        
    return glReadPixels(0, 0, viewport[0], viewport[1], GL_RGB, GL_UNSIGNED_INT)
    
        