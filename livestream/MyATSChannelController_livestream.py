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
            start_slow = -0.210
            start_fast= -0.235
            step_slow = 30e-3
            step_fast = 30e-3
            
            #sync_output_slow = 2
            #sync_output_fast = 1
            
            #qdac_OX.ch07.sync(sync_output_slow)
            #qdac_OX.ch14.sync(sync_output_fast)

            self.qdac.ramp_voltages_2d(slow_chans=[7], slow_vstart=[start_slow], slow_vend=[start_slow + step_slow],
                                  fast_chans=[14], fast_vstart=[start_fast], fast_vend=[start_fast + step_fast],
                                  slow_steps = 30, fast_steps = 30,
                                  step_length=0.001)

