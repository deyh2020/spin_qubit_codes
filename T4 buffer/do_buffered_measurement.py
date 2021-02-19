# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 16:13:05 2019

@author: Triton4acq_2
"""
from qcodes.dataset.measurements import Measurement
import numpy as np
agi3.reset()
agi3.device_clear() #to reset device after failed fetching e.g. for dmm timeout

def do_buffered_measurement(param, start, stop, n_steps, delay, dmm):
    meas = Measurement()
    set_vals = np.linspace(start, stop, n_steps)
    meas.register_parameter(param)
    meas.register_custom_parameter('buffer', 'Buffer', 'V', setpoints=[param])
    with meas.run() as datasaver:
        dmm.init_measurement()
        for val in set_vals:
            param.set(val)
            dmm.trigger.force()
        data = dmm.fetch()
        datasaver.add_result((param.full_name, set_vals),
                             ('buffer', data))
    return datasaver.run_id
            
    
n_samples=101
time_per_sample=1e-3

agi3.trigger.source('BUS') #to call trigger from the software
agi3.trigger.count(101) #sets the number of triggers to be accepted before returning to the "idle" trigger state. The total number of measurements returned are the product of the sample count and trigger count.
agi3.trigger.delay(0.0) #delay between the trigger and the first sample
agi3.sample.count(1)  #number of samples per trigger.
agi3.sample.source('IMM') #not important since we have one sample for each trigger
agi3.sample.timer('MIN') #not important since we have one sample for each trigger
agi3.display.text('Hello world') #commands are executed faster when the display of the instrument is disabled or is displaying text.

old_timeout = agi3.visa_handle.timeout  # it is in milliseconds
new_timeout = old_timeout + n_samples * time_per_sample * 1000
agi3.visa_handle.timeout = new_timeout

do_buffered_measurement(dummy_time,0,100,n_samples,time_per_sample,agi3)
agi3.init_measurement()
agi3.trigger.force()

data = agi3.fetch()
# %%
agi3.device_clear() #to reset device after failed fetching e.g. for dmm timeout
agi3.reset()
agi3.trigger.source('IMM')
agi3.trigger.count(100)
agi3.trigger.delay(0.0)
agi3.sample.count(1)
agi3.sample.source('TIM')
agi3.sample.timer(2e-3)

agi3.init_measurement()
agi3.trigger.force()

data = agi3.fetch()
# %%
agi3.range(1) #since our signal is in the 100 mV range
agi3.NPLC(0.2)
agi3.aperture_mode('ON')
agi3.aperture_time(3e-3)
agi3.trigger.source('IMM')
agi3.trigger.count(1)
agi3.trigger.delay(0.0)
agi3.sample.count(100)
agi3.sample.pretrigger_count(0)
agi3.sample.source('TIM')
agi3.sample.timer('MIN')
agi3.display.text('hello world') #to speed up acquisition
agi3.init_measurement()
old_timeout = agi3.visa_handle.timeout
new_timeout = old_timeout + n_samples * time_per_sample
# where, n_samples == agi3.sample.count(),
# and time_per_sample == agi3.sample.timer()
with agi3.timeout.set_to(new_timeout):
    data = agi3.fetch()
plt.plot(data)