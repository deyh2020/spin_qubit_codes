# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 16:13:05 2019

@author: Triton4acq_2
"""
from qcodes.dataset.measurements import Measurement
import numpy as np

# Is there a way to put sampling/triggering parameters inside of do_buffered_measurement?

agi2.trigger.source('BUS')
agi2.trigger.count(100)
agi2.trigger.delay(0.0)
agi2.sample.count(1)
agi2.sample.source('TIM')
agi2.sample.timer(2e-3)

agi2.init_measurement()

do1d(qdac.C10,0,0.1,100,0,agi2.trigger.force)


agi2.fetch()



def do_buffered_measurement(param, start, stop, n_steps, delay, dmm):
    meas = Measurement()
    set_vals = np.linspace(start, stop, n_steps)
    meas.register_parameter(param)
    meas.register_custom_parameter('buffer', 'Buffer', 'V', setpoints=[param])
    with meas.run() as datasaver:
        for val in set_vals:
            param.set(val)
            dmm.trigger.force()
        data = dmm.fetch()
        datasaver.add_result((param.full_name, set_vals),
                             ('buffer', data))
    return datasaver.run_id
            
    


























n_samples=100
time_per_sample=1e-3

old_timeout = agi4.visa_handle.timeout  # it is in milliseconds
new_timeout = old_timeout + n_samples * time_per_sample * 1000
agi4.visa_handle.timeout = new_timeout