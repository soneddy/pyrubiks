#!/usr/bin/env python

"""
N x N x N Rubik's Cube
"""

__author__  = "Edwin J. Son <edwin.son@ligo.org>"
__version__ = "0.0.1a"
__date__    = "May 27 2017"

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class cube:
    colors = ('white', 'yellow', 'orange', 'red', 'skyblue', 'blue')
    faces = ('front', 'back', 'left', 'right', 'top', 'bottom')
    def __init__(self, n_shuffle=50, size=3):
        self.size = size
        self.face_dic = {self.faces[i]:i for i in range(len(self.faces))}
        self.data = np.ones((len(self.faces), size, size),dtype='int') * np.arange(len(self.faces)).reshape((len(self.faces), 1, 1))
        self.shuffle(n_shuffle)
        return
    def shuffle(self, n_shuffle=20):
        if n_shuffle < 1:
            n_shuffle = 20
        for i in range(n_shuffle):
            ridx = np.random.randint(2)
            fidx = np.random.randint(len(self.faces))
            lidx = np.random.randint((self.size + 1) // 2)
            if ridx == 0:
                self.clockwise(self.faces[fidx], lidx)
            else:
                self.cntclkwise(self.faces[fidx], lidx)
        return
    def clockwise(self, face='front', level=0):
        if face not in self.faces:
            raise RuntimeError('"{}" is not in self.faces'.format(face))
        if level < 0:
            l = 0
        elif level < self.size:
            l = level
        else:
            l = self.size - 1
        il = self.size - 1 - l
        if (self.face_dic[face] % 2) == 0:
            fidx = (self.face_dic[face] + np.arange(len(self.faces))) % len(self.faces)
        else:
            fidx = (self.face_dic[face] + np.arange(len(self.faces),0,-1)) % len(self.faces)
        if l == 0:
            self.data[fidx[0],:,:] = self.data[fidx[0],::-1,:].T
        elif l == self.size - 1:
            self.data[fidx[1],:,:] = self.data[fidx[1],:,::-1].T
        bak = self.data[fidx[2], :, il].copy()
        self.data[fidx[2], :, il] = self.data[fidx[5], ::-1, l]
        self.data[fidx[5], :, l] = self.data[fidx[3], il, :]
        self.data[fidx[3], il, :] = self.data[fidx[4], l, ::-1]
        self.data[fidx[4], l, :] = bak[:]
        return
    def cntclkwise(self, face='front', level=0):
        if face not in self.faces:
            raise RuntimeError('"{}" is not in self.faces'.format(face))
        if level < 0:
            l = 0
        elif level < self.size:
            l = level
        else:
            l = self.size - 1
        il = self.size - 1 - l
        if (self.face_dic[face] % 2) == 0:
            fidx = (self.face_dic[face] + np.arange(len(self.faces))) % len(self.faces)
        else:
            fidx = (self.face_dic[face] + np.arange(len(self.faces),0,-1)) % len(self.faces)
        if l == 0:
            self.data[fidx[0],:,:] = self.data[fidx[0],:,::-1].T
        elif l == self.size - 1:
            self.data[fidx[1],:,:] = self.data[fidx[1],::-1,:].T
        bak = self.data[fidx[2], ::-1, il].copy()
        self.data[fidx[2], :, il] = self.data[fidx[4], l, :]
        self.data[fidx[4], l, :] = self.data[fidx[3], il, ::-1]
        self.data[fidx[3], il, :] = self.data[fidx[5], :, l]
        self.data[fidx[5], :, l] = bak[:]
        return
    def display(self, face=None, lw=2, figsize=(6, 4), dpi=75):
        fig = plt.figure(figsize=figsize, dpi=dpi)
        X = np.linspace(0,1,10)
        Y, Z = np.meshgrid(X, X)
        X = np.zeros_like(Y)
        ax = [fig.add_subplot(2,3,i+1, projection='3d') for i in range(6)]
        ax[0].set_title('top')
        ax[1].set_title('top')
        ax[2].set_title('top')
        ax[3].set_title('left')
        ax[4].set_title('front')
        ax[5].set_title('right')
        for i in range(6):
            ax[i].set_xticks([])
            ax[i].set_yticks([])
            ax[i].set_zticks([])
        for i in range(self.size):
            ii = self.size - 1 - i
            for j in range(self.size):
                ij = self.size - 1 - j
                #c = self.colors[1+i+2*j]
                # front
                c = self.colors[self.data[self.face_dic['front'], i, j]]
                ax[0].plot_surface(X+self.size, Y+i, Z+j, color=c, lw=lw)
                ax[3].plot_surface(X+self.size, Y+j, Z+ii, color=c, lw=lw)
                ax[1].plot_surface(Y+i, X, Z+j, color=c, lw=lw)
                ax[4].plot_surface(Y+i, Z+j, X+self.size, color=c, lw=lw)
                # back
                c = self.colors[self.data[self.face_dic['back'], i, j]]
                ax[2].plot_surface(X+self.size, Y+ij, Z+i, color=c, lw=lw)
                ax[5].plot_surface(X+self.size, Y+i, Z+j, color=c, lw=lw)
                # left
                c = self.colors[self.data[self.face_dic['left'], i, j]]
                ax[0].plot_surface(Y+j, X, Z+ii, color=c, lw=lw)
                ax[3].plot_surface(Y+j, Z+ii, X+self.size, color=c, lw=lw)
                # right
                c = self.colors[self.data[self.face_dic['right'], i, j]]
                ax[1].plot_surface(X+self.size, Y+ii, Z+ij, color=c, lw=lw)
                ax[4].plot_surface(X+self.size, Y+ij, Z+i, color=c, lw=lw)
                ax[2].plot_surface(Y+ii, X, Z+ij, color=c, lw=lw)
                ax[5].plot_surface(Y+ii, Z+ij, X+self.size, color=c, lw=lw)
                # top
                c = self.colors[self.data[self.face_dic['top'], i, j]]
                ax[0].plot_surface(Y+ii, Z+ij, X+self.size, color=c, lw=lw)
                ax[1].plot_surface(Y+ij, Z+i, X+self.size, color=c, lw=lw)
                ax[2].plot_surface(Y+i, Z+j, X+self.size, color=c, lw=lw)
                # bottom
                c = self.colors[self.data[self.face_dic['bottom'], i, j]]
                ax[3].plot_surface(Y+ij, X, Z+i, color=c, lw=lw)
                ax[4].plot_surface(Y+ii, X, Z+ij, color=c, lw=lw)
                ax[5].plot_surface(Y+j, X, Z+ii, color=c, lw=lw)
        return
