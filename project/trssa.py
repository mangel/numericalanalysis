import numpy as np
import random as rdm
import math
from pprint import pprint

def cj(t,m,k):
	return 1 / (1 + (t/K)**m)

def cj_bounds(t_1, t, m, k):
	result = [cj(t_1, m, k), cj(t, m, k)]
	return [min(result), max(result)]

#sigma constant
sigma = 0.7
K = 20
j=0
vj = 1

#initialize time t = 0 and state X = x (DONE)
t = 0
X = 0
# Define the bound [X_, X^] for state X (DONE?, on the birth model there is only possible state)
X_bounds = [0, 1]
# Discretize [0, tmax] to k intervals 0 < t1 < ... < tk = tmax (DONE)
ti = [x * 5 for x in range(0,5)]
t_bounds = [0, max(ti)]
tmax = t_bounds[1]
#set i = 1 (DONE)
i=1

# compute cj_ and cj^ over time interval [t_{i-1}, ti] for j = 1 ... m (DONE, Since there is only one possible reaction on the birth model there is only needed to compute j=1)
c_boundsj =  cj_bounds(ti[i-1], ti[i], 5, 20) # the birth problem states this parameter as 5
# compute hj_ and hj^ over abstract state [x_, x^] for j = 1 ... m (DONE, Since there is only one possible reaction on the birth model there is only needed to compute j=1, also there is only one species and one possible reaction hj is equal to 1 on it's bounds)
h_boundsj = [1, 1]
# derive propensity bounds aj_ and aj^ for j = 1 ... m (DONE, Since there is only one possible reaction on the birth model there is only needed to compute j=1
a_bounds = [c_boundsj[0]*h_boundsj[0], c_boundsj[1]*h_boundsj[1]]
#compute a0^ = sum from j=1 to m on aj^ (Done, there is only one possible reaction therefore no sum must be performed)
a0_upperbound = a_bounds[1]

while t<tmax:
	aj = cj(t, 5, 20)
	pprint(aj)
	# generate a random number r~U(0, 1)
	r1 = rdm.random()
	#compute tau = (-1/a0^)ln(r1)
	tau = (-1/a0_upperbound)*math.log(r1)
	#update time t = t + tau
	t = t + tau
	if t > ti[i]:
		# set t = t_i
		t = ti[i]
		# update i = i + 1
		i = i + 1
		# compute cj_ and cj^ over time interval [t_{i-1}, ti] for j = 1 ... m (DONE, Since there is only one possible reaction on the birth model there is only needed to compute j=1)
		c_boundsj =  cj_bounds(ti[i-1], ti[i], 5, 20) # the birth problem states this parameter as 5
		# Update propensity bounds aj_ and aj^ for j= 1 ... m (DONE, Since there is only one possible reaction on the birth model there is only needed to compute j=1
		a_bounds = [c_boundsj[0]*h_boundsj[0], c_boundsj[1]*h_boundsj[1]]
		continue
	#generate two random numbers r2,r3~U(0,1)
	r2 = rdm.random()
	r3 = rdm.random()
	# select minimum index j such that the sum from k=1 to j on ak^ is greater than r2*a0_ (DONE, since the number of reactions is equal to one, j would always be equal to 1).
	j = 1
	accepted = False
	if r3 <= a_bounds[0]/a_bounds[1]:
		accepted = True
	else:
		#evaluate aj with current state X (DONE, since hj is equal to 1, it is only necessary to compute cj)
		aj = cj(t, 5, 20)
		if r3 <= (aj/a_bounds[1]):
			accepted = True
	if accepted:
		#update state X = X + vj
		X = X + vj
		if X not in X_bounds:
			#define a new X_bounds around X (DONE, the coefficient is defined between 10% and 20%).
			X_bounds = [X*(1-0.15), X*(1.15)]
			# compute hj_ and hj^ for interval X_bounds for j = 1 ... m (DONE)
			h_boundsj = [1, 1]
			#update propensity bounds a_boundsj for j = 1 ... m (DONE, Since there is only one possible reaction on the birth model there is only needed to compute j=1
			a_bounds = [c_boundsj[0]*h_boundsj[0], c_boundsj[1]*h_boundsj[1]]

