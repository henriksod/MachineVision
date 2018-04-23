# -*- coding: utf-8 -*-
"""
Beep blop

"""

import sys
sys.path.append('..')
import ctypes

import os
import pyglet
from pyglet.gl import *
from pywavefront import Wavefront
from pywavefront import ObjParser

import math
import numpy as np
from numpy.linalg import inv

def meanVertex(verticesArr, isCol):
    mean_x = np.mean(verticesArr[0,:] if isCol else verticesArr[:,0])
    mean_y = np.mean(verticesArr[1,:] if isCol else verticesArr[:,1])
    mean_z = np.mean(verticesArr[2,:] if isCol else verticesArr[:,2])

    return np.array([mean_x, mean_y, mean_z])

def longestVectorIndex(verticesArr, isCol):
	mem_size = int(len(verticesArr[0,:] if isCol else verticesArr[:,0]))
	distances = np.empty([mem_size], dtype=float)
	
	for x in range(0,len(vertices_only[0,:] if isCol else verticesArr[:,0])):
		if isCol:
			distances[x] = np.sqrt(vertices_only[:,x].dot(vertices_only[:,x]))#vertices_only[0,x]**2 + vertices_only[1,x]**2 + vertices_only[2,x]**2
		else:
			distances[x] = np.sqrt(vertices_only[x,:].dot(vertices_only[x,:]))

	return np.argmax(distances)

def initVertices(mesh, _vertices):
    i = 0
    for x in range(5,len(mesh),8):
        _vertices[0, i] = mesh[x]
        _vertices[1, i] = mesh[x+1]
        _vertices[2, i] = mesh[x+2]
        i += 1

def drawLine(pt1, pt2, color, scale):
    pyglet.graphics.draw(2,
                         pyglet.gl.GL_LINES,
                         ('v3f', (pt1[0], pt1[1], pt1[2], pt2[0]*scale, pt2[1]*scale, pt2[2]*scale)),
                         ('c3B', (color[0], color[1], color[2], color[0], color[1], color[2])))

def rotationTo(vec1, vec2):
    v = np.cross(vec1, vec2)
    s = np.sqrt(v.dot(v))
    c = vec1.dot(vec2)

    skewSymmV = np.matrix([[0,-v[2],v[1]],
                           [v[2],0,-v[0]],
                           [-v[1],v[0],0]])

    return np.transpose(np.identity(3) + skewSymmV + (skewSymmV.dot(skewSymmV))/(1+c))

def rotate(v, R):
    for x in range(0,len(v[0, :])):
        v[:, x] = R.dot(v[:, x])
        
def translate(vs, v):
    vs[0, :] = vs[0, :] - v[0]
    vs[1, :] = vs[1, :] - v[1]
    vs[2, :] = vs[2, :] - v[2]
    
def rotateMesh(m, R):
    for x in range(5,len(m),8):
        v = np.transpose(R.dot(np.transpose(m[x:x+3])))
        m[x] = v[0]
        m[x+1] = v[1]
        m[x+2] = v[2]
        
def translateMesh(m, v):
    for x in range(5,len(m),8):
        m[x] = m[x] - v[0]
        m[x+1] = m[x+1] - v[1]
        m[x+2] = m[x+2] - v[2]
#####################################################
rotation = 0

curPath = os.path.dirname(os.path.abspath(__file__))+'/full-egg-filtered/egg_model.obj'

meshes = Wavefront(curPath)
vertices = meshes.materials['egg_model'].vertices

print('Loaded mesh')

mem_size = int(len(vertices)/8)
		  
vertices_only = np.empty([3, mem_size], dtype=float)

initVertices(vertices, vertices_only)

print('Length: ' + str(len(vertices_only[0,:])))

mean_arr = meanVertex(vertices_only, True)

print('MEAN (' + str(mean_arr[0]) + ', ' + str(mean_arr[1]) + ', ' + str(mean_arr[2]) + ')')

translate(vertices_only, mean_arr)

maxIndexTop = longestVectorIndex(vertices_only, True)

maxVectorTop = vertices_only[:,maxIndexTop]
	
translate(vertices_only, maxVectorTop)
translateMesh(vertices, mean_arr+maxVectorTop)

maxIndexBottom = longestVectorIndex(vertices_only, True)

maxVectorBottom = vertices_only[:,maxIndexBottom]

print('TOP INDEX = ' + str(maxIndexTop))
print('TOP (' + str(maxVectorTop[0]) + ', ' + str(maxVectorTop[1]) + ', ' + str(maxVectorTop[2]) + ')')

print('BOTTOM INDEX = ' + str(maxIndexBottom))
print('BOTTOM (' + str(maxVectorBottom[0]) + ', ' + str(maxVectorBottom[1]) + ', ' + str(maxVectorBottom[2]) + ')')

#https://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
dir0 = np.transpose([0,0,1])
dirEgg = maxVectorBottom/np.sqrt(maxVectorBottom.dot(maxVectorBottom))
	
R = rotationTo(dir0, dirEgg)

print('R='+str(R))

rotate(vertices_only, R)
rotateMesh(vertices, R)

#updateMesh(vertices, vertices_only)

#maxIndexBottom = longestVectorIndex(vertices_only, True)

#maxVectorBottom = vertices_only[:,maxIndexBottom]

#print('TOP INDEX = ' + str(maxIndexTop))
#print('TOP (' + str(maxVectorTop[0]) + ', ' + str(maxVectorTop[1]) + ', ' + str(maxVectorTop[2]) + ')')

#print('BOTTOM INDEX = ' + str(maxIndexBottom))
#print('BOTTOM (' + str(maxVectorBottom[0]) + ', ' + str(maxVectorBottom[1]) + ', ' + str(maxVectorBottom[2]) + ')')

#https://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
#dir0 = np.transpose([0,1,0])
#dirEgg = maxVectorBottom/np.sqrt(maxVectorBottom.dot(maxVectorBottom))
	
#R = rotationTo(dir0, dirEgg)

#print('newR='+str(R))
#print('newR\'='+str(np.transpose(R)))

#for x in range(0,len(vertices_only[0, :])):
#    vertices_only[:, x] = np.transpose(R).dot(vertices_only[:, x])

#updateMesh(vertices, vertices_only)

	
window = pyglet.window.Window(1024, 720, caption = 'Demo', resizable = True)

lightfv = ctypes.c_float * 4
label = pyglet.text.Label('Hello, world', font_name = 'Times New Roman', font_size = 12, x = 800, y = 700, anchor_x = 'center', anchor_y = 'center')
	

@window.event
def on_resize(width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40.0, float(width)/height, 1, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    return True

@window.event
def on_draw():
    window.clear()
    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightfv(0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightfv(0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_MODELVIEW)
    glTranslated(0, .8, -20)
    glRotatef(-66.5, 0, 0, 1)
    glRotatef(rotation, 1, 0, 0)
    glRotatef(90, 0, 0, 1)
    glRotatef(0, 0, 1, 0)
    pyglet.graphics.draw(2,pyglet.gl.GL_LINES,('v3f', (-maxVectorBottom[0]*5, -maxVectorBottom[1]*5, -maxVectorBottom[2]*5,maxVectorBottom[0]*5, maxVectorBottom[1]*5, maxVectorBottom[2]*5)))
    
    drawLine([0,0,0], [1,0,0], [255,0,0], 5)
    drawLine([0,0,0], [0,1,0], [0,255,0], 5)
    drawLine([0,0,0], [0,0,1], [0,0,255], 5)
    
    meshes.draw()

def update(dt):
    #return 0
    global rotation
    rotation += 45 * dt
    if rotation > 720: 
		rotation = 0

pyglet.clock.schedule(update)

pyglet.app.run()
