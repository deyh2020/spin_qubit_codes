# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 14:44:34 2021

@author: Triton4acq_2
"""

from qcodes.dataset.measurements import Measurement
import numpy as np
import time

# Is there a way to put sampling/triggering parameters inside of do_buffered_measurement?
agi3.reset()
# %% 1D
def do1d_buffered(param, start, stop, n_steps,delay, dmm):
    meas = Measurement()
    set_vs = np.linspace(start, stop, n_steps)
    meas.register_parameter(param)
    meas.register_custom_parameter('buffer', 'Buffer', 'V', setpoints=(param,))
    with meas.run() as datasaver:
        for set_v in set_vs:
            param.set(set_v)
            dmm.trigger.force()
            time.sleep(0.003205)
            time.sleep(delay)
        data = dmm.fetch()
        datasaver.add_result((param, set_vs),
                             ('buffer', data))
        dataset = datasaver.dataset
# %%
agi3.device_clear()
n_trigger = 101
n_samples= 1
agi3.range(1) #since our signal is in the 100 mV range
agi3.NPLC(0.2)
agi3.trigger.source('BUS') #needs init_measurement afterwards
agi3.trigger.count(n_trigger)
agi3.trigger.delay(0.0)
agi3.sample.count(n_samples)
agi3.sample.source('IMM')
agi3.sample.timer('MIN')
# %%
agi3.timeout.set(1) #in seconds
agi3.init_measurement()
do1d_buffered(dummy_time, 0, 100, 101, 0, agi3)
# %% 2D
def do2d_buffered(param1, start1, stop1, n_steps1 ,delay1, param2, start2, stop2, n_steps2 ,delay2, dmm):
    meas = Measurement()
    v1s = np.linspace(start1, stop1, n_steps1)
    v2s = np.linspace(start2, stop2, n_steps2)
    meas.register_parameter(param1)
    meas.register_parameter(param2)
    meas.register_custom_parameter('buffer', 'Buffer', 'V', setpoints=(param1,param2,))
    with meas.run() as datasaver:    
        for v1 in v1s:
            param1.set(v1)
            for v2 in v2s:                
                param2.set(v2)
                dmm.trigger.force()
                time.sleep(0.010205)
                time.sleep(delay2)
        time.sleep(delay1)
                
        data = dmm.fetch()
        datasaver.add_result((param1, np.repeat(v1s,n_steps2)),
                             (param2, np.tile(v2s,n_steps1)),
                             ('buffer', data))    
        dataset2D = datasaver.dataset
# %%
agi3.device_clear()
agi3.timeout.set(1) #in seconds

n_steps1 = 10
n_steps2 = 10
n_trigger = n_steps1*n_steps2
agi3.trigger.count(n_trigger)
dummy_time2 = ManualParameter('dummy_time') #Run this in order to have access to dummy time FK

agi3.init_measurement()
do2d_buffered(dummy_time, 0, 100, n_steps1, 0, dummy_time2, 0, 100, n_steps2, 0, agi3)
