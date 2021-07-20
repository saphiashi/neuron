# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from neuron import h
from neuron.units import ms, mV

import matplotlib.pyplot as plt

soma = h.Section(name='soma')
print(h.topology())
print(soma.psection() )
print(soma.psection()['morphology']['L'] )
print(soma.L)
soma.L = 20
soma.diam = 20
print(dir(soma))

import textwrap
print(textwrap.fill(', '.join(dir(h))))

soma.insert('hh')
print("type(soma) = {}".format(type(soma)))
print("type(soma(0.5)) = {}".format(type(soma(0.5))))

mech = soma(0.5).hh
print(dir(mech))
print(mech.gkbar)
print(soma(0.5).hh.gkbar)

iclamp = h.IClamp(soma(0.5))
print([item for item in dir(iclamp) if not item.startswith('__')])
iclamp.delay = 2
iclamp.dur = 0.1
iclamp.amp = 0.9
print(soma.psection())

t = h.Vector().record(h._ref_t) 
v = h.Vector().record(soma(0.5)._ref_v)    

h.load_file('stdrun.hoc')
h.finitialize( -65 * mV)
h.continuerun(40* ms)

f1 = plt.figure()
plt.xlabel('t (ms)')
plt.ylabel('v (mV)')
plt.plot(t, v, linewidth=2)
plt.show(f1)

f1 = plt.figure()
plt.xlabel('t (ms)')
plt.ylabel('v (mV)')
plt.plot(t, v, linewidth=2)
plt.show(f1)


import csv

with open('data.csv', 'w') as f:
    csv.writer(f).writerows(zip(t, v))
    
with open('data.csv') as f:
    reader = csv.reader(f)
    tnew, vnew = zip(*[[float(val) for val in row] for row in reader if row])
    
plt.figure()
plt.plot(tnew, vnew)
plt.xlabel('t (ms)')
plt.ylabel('v (mV)')
plt.show()

    
    
    
    
    