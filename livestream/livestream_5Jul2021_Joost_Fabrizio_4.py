# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 16:11:08 2021

@author: T7-2
"""
from pulsequantum.livestream.qdac_alazar_interface.QDacATSChannelController import MyATSChannelController_livestream
from pulsequantum.livestream.qdac_alazar_interface.QDevil_QDAC_livestream import QDac_livestream
#run QDacATSChannelController.py

# run qdac drivers from QDevil_QDAC_livestream.py

qdac_CPH = QDac_livestream('qdac', 'ASRL5::INSTR', update_currents=False)
#STATION.add_instrument('qdac_CPH')
alazar = STATION.load_instrument('Alazar')
# %%
alazar.get_idn()
# %%
with alazar.syncing():    
    alazar.clock_source('INTERNAL_CLOCK')
    alazar.sample_rate(10_000)
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
    alazar.buffer_timeout(1000)
# %%
myctrl.close()
myctrl = MyATSChannelController_livestream(name='my_controller', alazar_name='Alazar',qdac = qdac_CPH)

# %%
chan1 = AlazarChannel(myctrl, 'myrecvssamples', demod=False, average_records=False, integrate_samples=False)
myctrl.channels.append(chan1)
# %%
myctrl.n_avg = 30 #number of averages
myctrl.start_slow = -0.275
myctrl.start_fast = -0.245
myctrl.step_lentgh = 0.001
alazar.trigger_delay(104)
alazar.sample_rate(2e5) 
alazar.sync_settings_to_card()

myctrl.int_time(27e-3)
myctrl.int_delay()

chan1.num_averages(myctrl.n_avg)
chan1.records_per_buffer(myctrl.slow_steps)
chan1.alazar_channel('B')
chan1.prepare_channel()
# Measure this 
data1 = do0d(chan1.data)
qdac_CPH.ch06.v(-0.667)
qdac_CPH.ch12.v(-0.230)
qdac_CPH.ch10.v(-0.260)
# %%