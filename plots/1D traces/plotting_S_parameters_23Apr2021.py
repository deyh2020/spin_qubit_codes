# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 17:47:54 2020

@author: T7
"""

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
ax.set_title('RT transmission test',size=30)
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
ax.set_title('RT reflection test',size=30)
ax.grid()

ax.legend(fontsize=30)