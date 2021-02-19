# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 14:35:25 2019

@author: Triton4acq_2
"""



from qcodes.dataset.measurements import Measurement
import time
#HP2.ch1.function_type('RAMP')
#HP2.ch1.ramp_symmetry(100)
#HP2.ch1.amplitude_unit('VPP')
#HP2.ch1.amplitude(0.02)
#HP2.ch1.offset(0)
#HP2.ch1.frequency(0.09756)
#
#HP2.sync.output('OFF')
#HP2.ch1.output('OFF')


agi3.trigger.source('EXT')
agi3.trigger.count(1)
agi3.trigger.delay(0.041)
agi3.sample.count(250)
agi3.sample.source('TIM')
agi3.sample.timer(0.041)

agi3.init_measurement()

HP2.sync.output('ON')
HP2.ch1.output('ON')

agi3.fetch()



def do_buffered_2d_measurement(param, start, stop, n_steps, delay, dmm):
    meas = Measurement()
    set_vals = np.linspace(start, stop, n_steps)
    inner_setpoints = np.linspace(-0.01, 0.01, 250)
    meas.register_parameter(param)
    meas.register_custom_parameter('buffer_setpoints', 'Buffer Setpoints','V', paramtype='array')
    meas.register_custom_parameter('buffer', 'Buffer', 'V', setpoints=[param,'buffer_setpoints'], paramtype='array')
    with meas.run() as datasaver:
        for val in set_vals:
            param.set(val)
            time.sleep(delay)
            dmm.init_measurement()
            time.sleep(2.5)
            data = dmm.fetch()

            datasaver.add_result((param.full_name, val),
                                 ('buffer_setpoints', inner_setpoints),
                                 ('buffer', data),
                                 )
    return datasaver.run_id



agi3.reset()





import time
start_time = time.time()

do1d(qdac.BNC16,0.594,0.606,200,0.001,agi3.volt)

print("--- %s seconds ---" % (time.time() - start_time))




def do1dtriggereddmm(param, start, stop, n_steps, delay, dmm):
    meas = Measurement()
    set_vals = np.linspace(start, stop, n_steps)
    inner_setpoints = np.linspace(0, 1, 1)
    meas.register_parameter(param)
    meas.register_custom_parameter('buffer_setpoints', 'Buffer Setpoints','V', paramtype='numeric')
    meas.register_custom_parameter('buffer', 'Buffer', 'V', setpoints=[param,'buffer_setpoints'], paramtype='numeric')
    
    
    old_timeout = dmm.visa_handle.timeout  # it is in milliseconds
    new_timeout = 60000
    
    
    dmm.trigger.source('EXT')
    dmm.trigger.count(1)
    dmm.trigger.delay(0.0)
    dmm.sample.count(1)
    #dmm.sample.pretrigger_count(0)
    dmm.init_measurement()
    dmm.visa_handle.timeout = new_timeout
    
        
    with meas.run() as datasaver:
        for val in set_vals:
            param.set(val)
            time.sleep(delay)
            
    try:
        data = dmm.fetch()
        print(data)
        datasaver.add_result((param.full_name, val),
                                 ('buffer_setpoints', inner_setpoints),
                                 ('buffer', data),
                                 )
            
    finally:
        dmm.visa_handle.timeout = old_timeout
    return datasaver.run_id