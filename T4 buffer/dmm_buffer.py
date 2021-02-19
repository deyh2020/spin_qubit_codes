# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 15:11:27 2021

@author: Triton4acq_2
"""

HP.ch1.function_type('RAMP')
HP.ch1.ramp_symmetry(100)
HP.ch1.amplitude_unit('VPP')
HP.ch1.amplitude(0.1)
HP.ch1.offset(5e-2)
HP.ch1.frequency(10)
HP.sync.source(1)
# Start it
HP.sync.output('ON')
HP.ch1.output('ON')

# stop it
HP.sync.output('OFF')
HP.ch1.output('OFF')
# %%
