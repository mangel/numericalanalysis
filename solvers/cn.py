#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 19:24:09 2019

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
u_1 = np.dot(la.inv(I - (dt*a/h**2)*A), u_0)
u_2 = np.dot(la.inv(I - (dt*a/h**2)*A), u_1)

def implicit(I, dt, a, h, A, n, u_0):
    return np.dot(la.matrix_power(la.inv(I - (dt*a/h**2)*A), n), u_0)

def explicit(I, dt, a, h, A, n, u_0):
    return np.dot(la.matrix_power(I + (dt*a/h**2)*A, n), u_0)

def crank_nicolson(I, dt, a, h, A, n, u_0):
    return np.dot(la.matrix_power(np.matmul(I + (dt*a/h**2)*A ,la.inv(I - A*(a*dt/h**2))), n), u_0)


implicit = implicit(I, dt, a, h, A, 2, u_0)
explicit = explicit(I, dt, a, h, A, 2, u_0)
crank_nicolson = crank_nicolson(I, dt, a, h, A, 2, u_0)

pprint(implicit)
pprint(explicit)
pprint(crank_nicolson)
