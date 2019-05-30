import mne
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame()
all_paths = [['data/rivalry_12hz_amtacs.edf'],['data/rivalry_15hz_amtacs.edf'],['data/rivalry_sham.edf'],['data/rivalry_12hz_1.edf','data/rivalry_12hz_2.edf','data/rivalry_12hz_3.edf'],
['data/rivalry_15hz_tacs.edf']]
freqs = ['12 (AM-TACS)','15 (AM-TACS)','Sham','12 (TACS)','15 (TACS)']

for paths,freq in zip(all_paths,freqs):
    raw = mne.concatenate_raws([mne.io.read_raw_edf(path,preload=True) for path in paths])
    events = mne.find_events(raw,shortest_event=0)
    von = events[events[:,2]==1][:,0]
    voff = events[events[:,2]==2][:,0]
    hon = events[events[:,2]==3][:,0]
    hoff = events[events[:,2]==4][:,0]
    durs_v = []
    for ev in von:
        diffs = voff-ev
        diffs = diffs[diffs > 0]
        durs_v.append(np.min(diffs)*raw.times[1])
    durs_h = []
    for ev in hon:
        diffs = hoff-ev
        diffs = diffs[diffs > 0]
        durs_h.append(np.min(diffs)*raw.times[1])
    v_durs = np.array(durs_v)
    h_durs = np.array(durs_h)
    df = df.append(pd.DataFrame({'Stimulation Frequency (Hz)':[str(freq)]*v_durs.size,
        'Percept':['Vertical']*v_durs.size, 'Dominance Duration (s)':v_durs}))
    df = df.append(pd.DataFrame({'Stimulation Frequency (Hz)':[str(freq)]*h_durs.size,
        'Percept':['Horizontal']*h_durs.size, 'Dominance Duration (s)':h_durs}))

sns.violinplot(x='Stimulation Frequency (Hz)',y='Dominance Duration (s)', 
hue='Percept', data=df, palette='husl')
plt.show()