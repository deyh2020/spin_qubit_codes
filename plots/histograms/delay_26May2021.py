# -*- coding: utf-8 -*-
"""
Created on Wed May 26 17:42:20 2021

@author: Triton4acq
"""
import numpy as np
import matplotlib.pyplot as plt
vdelay = np.array([844, 845, 846, 850, 843, 846, -278,-230, -278,-275,-277,-283,-298,-313,-296,-277,-273])
vstd = np.array([16, 20,19, 17,16,17,28,23,26,28,29,34,37,31,26,15,15])
coaxes =  [str(x) for x in range(1,18)]

x_pos = np.arange(len(coaxes))
CTEs = vdelay
error = vstd

# Build the plot
fig, ax = plt.subplots()
ax.bar(x_pos, CTEs, yerr=error, align='center', alpha=0.5, color = 'red',ecolor='black', capsize=14)
ax.set_ylabel('time (ps)', fontsize = 16)
ax.set_xlabel('Coax #', fontsize = 16)
ax.set_xticks(x_pos)
ax.set_xticklabels(coaxes,fontsize = 16)
ax.set_title('T4 coax lines - delay wrt trigger - FB 25 May 2021', fontsize = 16)
ax.yaxis.grid(True)
fig.show()

# %%
vdelay_rel = vdelay - vdelay[0]
vstd_rel = np.sqrt(vstd**2+vstd[0]**2)
vdelay_rel = np.delete(vdelay_rel,0)
vstd_rel = np.delete(vstd_rel,0)

coaxes =  [str(x) for x in range(2,18)]

x_pos = np.arange(len(coaxes))
CTEs = vdelay_rel
error = vstd_rel

# Build the plot
fig, ax = plt.subplots()
ax.bar(x_pos, CTEs, yerr=error, align='center', alpha=0.5, color = 'blue',ecolor='black', capsize=14)
ax.set_ylabel('time (ps)', fontsize = 16)
ax.set_xlabel('Coax #', fontsize = 16)
ax.set_xticks(x_pos)
ax.set_xticklabels(coaxes,fontsize = 16)
ax.set_title('T4 coax lines - delay wrt Coax 17 - FB 25 May 2021', fontsize = 16)
ax.yaxis.grid(True)
fig.show()
