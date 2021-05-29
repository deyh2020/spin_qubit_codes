# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 17:47:54 2020

@author: T7
"""
# %% %matplotlib inline
import os
from time import sleep

import matplotlib.pyplot as plt
import numpy as np
import qcodes as qc
from qcodes import (
    Measurement,
    experiments,
    initialise_database,
    initialise_or_create_database_at,
    load_by_guid,
    load_by_run_spec,
    load_experiment,
    load_last_experiment,
    load_or_create_experiment,
    new_experiment,
)
from qcodes.dataset.plotting import plot_dataset, plot_by_id
# %%
import matplotlib.gridspec as gridspec
# %%
initialise_or_create_database_at("/Users/fabrizioberr/Dropbox/Triton 4/fabrizio qdev dropbox/swap/T4_UPGRADE.db"
# %%
fig = plt.figure()
gs1 = gridspec.GridSpec(10,10)

ax=fig.add_subplot(gs1[:,:])
ax.hlines(-23,-0.5,6e9,color='red', label = 'Expected DC att.')
axes1,colorbar1 = plot_by_id(28,axes=ax, label='Coax 1')
axes1,colorbar1 = plot_by_id(32,axes=ax, label='Coax 2')
axes1,colorbar1 = plot_by_id(18,axes=ax, label='Coax 3')
axes1,colorbar1 = plot_by_id(20,axes=ax, label='Coax 4')
axes1,colorbar1 = plot_by_id(22,axes=ax, label='Coax 5')
axes1,colorbar1 = plot_by_id(24,axes=ax, label='Coax 6')
ax.set_xlabel('Frequency (GHz)',size=30)
ax.set_ylabel('S21 (dB)',size=30)
ax.tick_params(labelsize=20) 
ax.set_title('RT transmission test - FB 25 May 2021 - database.db',size=30)
ax.grid()

ax.legend(fontsize=30)
# %%
fig = plt.figure()
gs1 = gridspec.GridSpec(10,10)

ax=fig.add_subplot(gs1[:,:])
axes1,colorbar1 = plot_by_id(29,axes=ax, label='Coax 1')
axes1,colorbar1 = plot_by_id(33,axes=ax, label='Coax 2')
axes1,colorbar1 = plot_by_id(19,axes=ax, label='Coax 3')
axes1,colorbar1 = plot_by_id(21,axes=ax, label='Coax 4')
axes1,colorbar1 = plot_by_id(23,axes=ax, label='Coax 5')
axes1,colorbar1 = plot_by_id(25,axes=ax, label='Coax 6')
ax.set_xlabel('Frequency (GHz)',size=30)
ax.set_ylabel('S11 (dB)',size=30)
ax.tick_params(labelsize=20) 
ax.set_title('RT reflection test - FB 25 May 2021 - database.db',size=30)
ax.grid()

ax.legend(fontsize=30)