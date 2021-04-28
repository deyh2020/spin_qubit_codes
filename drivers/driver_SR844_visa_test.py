# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 16:53:50 2021

@author: Triton4acq_2
"""
# %%
import pyvisa
rm = pyvisa.ResourceManager()
print(rm.list_resources())
# %%
import qcodes.instrument.sims as sims

# path to the .yaml file containing the simulated instrument
visalib = sims.__file__.replace('__init__.py', 'Weinschel_8320.yaml@sim')

wein_sim = Weinschel_8320('wein_sim',
                          address='GPIB::1::INSTR',  # This matches the address in the .yaml file
                          visalib=visalib
                          )

# %%
import qcodes.instrument.sims as sims

# path to the .yaml file containing the simulated instrument
visalib = sims.__file__.replace('__init__.py', 'SR_844.yaml@sim')

SR844_sim.close()
SR844_sim = SR844('SR844_sim',
                          address='GPIB::1::INSTR',  # This matches the address in the .yaml file
                          visalib=visalib
                          )
SR844 = SR844('SR844', address='GPIB0::7::INSTR')


