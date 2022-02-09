# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 11:20:28 2019

@author: Triton4acq_2
"""

from qdev_wrappers.alazar_controllers.ATSChannelController import ATSChannelController


class MyATSChannelController_livestream(ATSChannelController):
    
    """additional paramteres taht this subclass has:
        run_awg: if it is set to False, it just acquires continuosly.
                 if it is set to true, when running a dond on channel.data,
                 it will automatically starts the AWG, but not the single channels, and it will start acquiring 
                 sequentially from the first trigger.
        At the end of the acquisition it will always stop the AWG, independently from the awg_run status.
    """
    def __init__(self, name,
                 alazar_name: str,
                 qdac,
                 filter: str = 'win',
                 numtaps: int =101,
                 **kwargs):
        super().__init__(name,alazar_name,filter,numtaps,**kwargs)
        self.qdac = qdac
        self.run_qdac = True
        
    def pre_acquire(self):
        if self.run_qdac is True:
            start_slow = -0.275
            start_fast= -0.245
            step_slow = 30e-3
            step_fast = 30e-3
            
            #sync_output_slow = 2
            sync_output_fast = 1
            
            #qdac.ch10.sync(sync_output_slow)
            self.qdac.ch12.sync(sync_output_fast)
            self.qdac.ch12.sync_duration(1e-3)  # The sync pulse duration (s). 

            self.qdac.ramp_voltages_2d_avg(slow_chans=[10], slow_vstart=[start_slow], slow_vend=[start_slow + step_slow],
                                  fast_chans=[12], fast_vstart=[start_fast], fast_vend=[start_fast + step_fast],
                                  slow_steps = 30, fast_steps = 30,
                                  step_length=0.001, n_avg = 20)

