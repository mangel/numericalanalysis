import numpy as np
import numpy.linalg as la
from pprint import pprint
import matplotlib.pyplot as plt

def explicit(I, dt, a, h, A, n, u_0):
    return np.dot(la.matrix_power(I + (dt*a/h**2)*A, n), u_0)

def exact_solution(t, x):
	return np.e**((-np.pi**(2)*t)/4)*np.sin((np.pi*x)/2)

# Diffusion coefficient
a=np.pi**-2
# Simulation parameters
dt=1/64
h=1/4

den = 4
iteration = 1

for iteration in range(9, 10):
	den = 2**(iteration+1)
	h = 1/den
	dt = ((h**2)/(2*a))*0.001
	print("---------------------Iteration ", iteration, ": dt=", dt,"h=1/",den)
	exact = np.asarray([exact_solution(den*dt, h*i) for i in range(1,den)])
	I = np.diag([1]*(den-1))
	# Diagonal matrix with -2 in its diagonal.	
	A = np.diag([-2]*(den-1)) + np.diag([1]*(den-2),-1) + np.diag([1]*(den-2),1)
	#Initial solution
	u_0 = np.asarray([np.sin((np.pi*h*i)/2) if i < (den-2) else np.e**((-np.pi**2)*dt*den/4) for i in range(1,den)])
	estimated_solution = explicit(I, dt, a, h, A, 2, u_0)

	pprint(estimated_solution)
	pprint(exact)
		
	x = np.asarray([h*i for i in range(1,den)])
	plt.plot(x, estimated_solution, '--')

	plt.plot(x, exact)

plt.show()
