# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 11:49:40 2021

@author: T7-2
"""

sync_output_slow = 2
sync_output_fast = 1

qdac_OX.ch07.sync(sync_output_slow) # s
qdac_OX.ch14.sync(sync_output_fast) # sync output 1 will fire a ms 5 V pulse when ch14 ramps

qdac_OX.ch07.sync_duration(10e-3)  # The sync pulse duration (s). 
qdac_OX.ch14.sync_duration(10e-3)  # The sync pulse duration (s). 

qdac_OX.print_slopes()
qdac_OX.print_syncs()
# %%
start_slow = -0.210
start_fast= -0.235
step_slow = 30e-3
step_fast = 30e-3

# 
#%%
Alazar.trigger_delay(0)
Alazar.sample_rate(50000) 
Alazar.trigger_level1(140)
AlazarController.int_time(5e-3)
Alazar.sync_settings_to_card()
ChannelA.acquisition_kwargs['buffer_timeout'] = 10000
ChannelA.num_averages(1)
ChannelA.records_per_buffer(50)
#
ChannelA.prepare_channel()
# %%
qdac_OX.ch07.sync(sync_output_slow)
qdac_OX.ch14.sync(sync_output_fast) 

qdac_OX.ramp_voltages_2d( slow_chans=[7], slow_vstart=[start_slow], slow_vend=[start_slow + step_slow],
                                  fast_chans=[14], fast_vstart=[start_fast], fast_vend=[start_fast + step_fast],
                                  slow_steps = 30, fast_steps = 30,
                                  step_length=0.001)
do0d(ChannelA.data)
# %%
for i in range(1000):
    qdac_OX.ch07.v(start_slow)

