# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 14:27:21 2021

@author: Triton4acq_2
"""

agi3.reset()
agi3.device_clear()
agi3.range(1) #since our signal is in the 100 mV range
agi3.NPLC(0.2)
n_samples = 100
agi3.trigger.source('IMM')
agi3.trigger.count(1)
agi3.trigger.delay(0.0)
agi3.sample.count(n_samples)
agi3.sample.pretrigger_count(0)
agi3.sample.source('TIM')
agi3.sample.timer('MIN')
agi3.display.text('hello world') #to speed up acquisition
agi3.init_measurement()
time_per_sample = agi3.sample.timer()

old_timeout = agi3.visa_handle.timeout
vtime = np.arange(n_samples) * time_per_sample
new_timeout = old_timeout + vtime[-1]
# where, n_samples == agi3.sample.count(),
# and time_per_sample == agi3.sample.timer()
with agi3.timeout.set_to(new_timeout):
    data = agi3.fetch()

plt.plot(vtime,data)
