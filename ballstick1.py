# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 12:50:20 2021

@author: sshi
"""

from neuron import h
from neuron.units import ms, mV

h.load_file('stdrun.hoc')

class BallAndStick:
    def __init__(self, gid):
        self._gid = gid
        self._setup_morphology()
        self._setup_biophysics()
    def _setup_morphology(self):
        self.soma = h.Section(name='soma', cell=self)
        self.dend = h.Section(name='dend', cell=self)
        self.all = [self.soma, self.dend]
        self.dend.connect(self.soma)
        self.soma.L = self.soma.diam = 12.6157
        self.dend.L = 200
        self.dend.diam = 1
    def _setup_biophysics(self):
        for sec in self.all:
            sec.Ra = 100    # Axial resistance in Ohm * cm
            sec.cm = 1      # Membrane capacitance in micro Farads / cm^2
            self.soma.insert('hh')                                                    # <-- NEW           
        for seg in self.soma:                                                     # <-- NEW
            seg.hh.gnabar = 0.12  # Sodium conductance in S/cm2                   # <-- NEW
            seg.hh.gkbar = 0.036  # Potassium conductance in S/cm2                # <-- NEW
            seg.hh.gl = 0.0003    # Leak conductance in S/cm2                     # <-- NEW
            seg.hh.el = -54.3     # Reversal potential in mV 
        self.dend.insert('pas')                                        # <-- NEW
        for seg in self.dend:                                          # <-- NEW
            seg.pas.g = 0.001  # Passive conductance in S/cm2          # <-- NEW
            seg.pas.e = -65    # Leak reversal potential mV
    def __repr__(self):
        return 'BallAndStick[{}]'.format(self._gid)

my_cell = BallAndStick(0)
my_cell = BallAndStick(0)

import matplotlib.pyplot as plt

h.PlotShape(False).plot(plt)

# enable NEURON's graphics
from neuron import gui

# here: True means show using NEURON's GUI; False means do not do so, at least not at first
ps = h.PlotShape(True)
ps.show(0)

for sec in h.allsec():
    print('%s: %s' % (sec, ', '.join(sec.psection()['density_mechs'].keys())))
stim = h.IClamp(my_cell.dend(1))
stim.get_segment()

print(', '.join(item for item in dir(stim) if not item.startswith('__')))

stim.delay = 5
stim.dur = 1
stim.amp = 0.1

soma_v = h.Vector().record(my_cell.soma(0.5)._ref_v)
t = h.Vector().record(h._ref_t)


h.finitialize(-65 * mV)


h.continuerun(25 * ms)


#%%

dend_v = h.Vector().record(my_cell.dend(0.5)._ref_v)
f = plt.figure()
plt.xlabel='t (ms)'
plt.ylabel='v (mV)'
amps = [0.075 * i for i in range(1, 5)]
colors = ['green', 'blue', 'red', 'black']
for amp, color in zip(amps, colors):
    
    stim.amp = amp
    h.finitialize(-65)
    h.continuerun(25)
    f.plot(t, list(soma_v), line_width=2, legend_label='amp=%g' % amp, color=color)
    f.plot(t, list(dend_v), line_width=2, line_dash='dashed', color=color)

plt.show(f)