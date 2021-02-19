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


# %%
def do_buffered_measurement(param, start, stop, n_steps,delay, dmm):
    meas = Measurement()
    set_vs = np.linspace(start, stop, n_steps)
    meas.register_parameter(param)
    meas.register_custom_parameter('buffer', 'Buffer', 'V', setpoints=(param,))
    with meas.run() as datasaver:
        for set_v in set_vs:
            param.set(set_v)
            dmm.trigger.force()
            time.sleep(delay)
        data = dmm.fetch()
        datasaver.add_result((param, set_vs),
                             ('buffer', data))
        dataset = datasaver.dataset
# %%
n_trigger = 101
n_samples= 1
agi3.device_clear()
agi3.range(1) #since our signal is in the 100 mV range
agi3.NPLC(0.2)
agi3.trigger.source('BUS') #needs init_measurement afterwards
agi3.trigger.count(n_trigger)
agi3.trigger.delay(0.0)
agi3.sample.count(n_samples)
agi3.sample.source('IMM')
agi3.sample.timer('MIN')

agi3.timeout.set(1) #in seconds
agi3.init_measurement()
# for set_v in range(n_trigger):
#     agi3.trigger.force()    
#     time.sleep(0.00325)
# data = agi3.fetch()
# print(data)
# plt.plot(data)
do_buffered_measurement(dummy_time, 0, 100, 101, 0.003205, agi3)
