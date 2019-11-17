#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 18:44:16 2019

@author: ingenierias
"""
import numpy as np
import numpy.linalg as la
from pprint import pprint
# Diffusion coefficient
a=np.pi**-2
# Simulation parameters
dt=1/64
h=1/16

# Diagonal matrix with -2 in its diagonal.
A = np.diag([-2]*15) + np.diag([1]*14,-1) + np.diag([1]*14,1)

u_0 = np.sin([np.pi*h*i for i in range(1,16)])
u_0 = u_0 + np.sin([2*np.pi*h*i for i in range(1,16)])

I = np.diag([1]*15)

#First iteration to get the vector u^1
u_1 = np.dot((I + (dt*a/h**2)*A), u_0)
u_2 = np.dot((I + (dt*a/h**2)*A), u_1)

# Generalization u^n+1 = ((I + (dt*a/h**2)*A)**(n+1))*u_0

u_n1 = la.matrix_power((I + (dt*a/h**2)*A), 2) #(I + dt*a/h^2*a)^(n+1)
u_n1 = np.dot(u_n1, u_0)

pprint(u_n1)

def explicit(I, dt, a, h, A, n, u_0):
    return np.dot(la.matrix_power(I + (dt*a/h**2)*A, n), u_0)

r = explicit(I, dt, a, h, A, 2, u_0)

pprint(r)
