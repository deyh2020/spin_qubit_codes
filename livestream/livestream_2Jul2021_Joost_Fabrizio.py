# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 17:55:41 2021

@author: T7-2
"""

from qdev_wrappers.alazar_controllers.ATSChannelController import ATSChannelController

# %%
start_slow = -0.210
start_fast= -0.235
step_slow = 30e-3
step_fast = 30e-3
qdac_OX.ch07.sync(sync_output_slow)
qdac_OX.ch14.sync(sync_output_fast)
qdac_OX.ch07.sync_duration(1e-3)  # The sync pulse duration (s). 
qdac_OX.ch14.sync_duration(1e-3)  # The sync pulse duration (s). 

qdac_OX.print_slopes()
qdac_OX.print_syncs() 
# %%
qdac_OX.ramp_voltages_2d(slow_chans=[7], slow_vstart=[start_slow], slow_vend=[start_slow + step_slow],
                                  fast_chans=[14], fast_vstart=[start_fast], fast_vend=[start_fast + step_fast],
                                  slow_steps = 10, fast_steps = 10,
                                  step_length=0.001)

# %%
alazar = STATION.load_instrument('Alazar')
alazar.get_idn()
# %%
with alazar.syncing():    
    alazar.clock_source('INTERNAL_CLOCK')
    alazar.sample_rate(5_000)
    alazar.clock_edge('CLOCK_EDGE_RISING')
    alazar.decimation(1)
    alazar.coupling1('DC')
    alazar.coupling2('DC')
    alazar.channel_range1(.4)
    alazar.channel_range2(.4)
    alazar.impedance1(50)
    alazar.impedance2(50)
    alazar.trigger_operation('TRIG_ENGINE_OP_J')
    alazar.trigger_engine1('TRIG_ENGINE_J')
    alazar.trigger_source1('EXTERNAL')
    alazar.trigger_slope1('TRIG_SLOPE_POSITIVE')
    alazar.trigger_level1(140)
    alazar.trigger_engine2('TRIG_ENGINE_K')
    alazar.trigger_source2('DISABLE')
    alazar.trigger_slope2('TRIG_SLOPE_POSITIVE')
    alazar.trigger_level2(128)
    alazar.external_trigger_coupling('DC')
    alazar.external_trigger_range('ETR_2V5')
    alazar.trigger_delay(0)
    alazar.timeout_ticks(0)
    alazar.aux_io_mode('AUX_IN_AUXILIARY') # AUX_IN_TRIGGER_ENABLE for seq mode on
    alazar.aux_io_param('NONE') # TRIG_SLOPE_POSITIVE for seq mode on
    alazar.buffer_timeout(10000)
# %%
myctrl = ATSChannelController(name='my_controller', alazar_name='Alazar')
# %%
myctrl.int_delay(0.02)
myctrl.int_time(30e-3)
print(myctrl.samples_per_record())
# %%
myctrl.channels
# %%
chan1 = AlazarChannel(myctrl, 'mychan', demod=False, integrate_samples=False)
myctrl.channels.append(chan1)

# %%
chan1.num_averages(1)

chan1.alazar_channel('B')
chan1.prepare_channel()

# Measure this 
data1 = do0d(chan1.data)

# %%
chan1.num_averages(1)

chan1.alazar_channel('B')
chan1.prepare_channel()

# Measure this 

data1 = do0d(ramping_dac,chan1.data)