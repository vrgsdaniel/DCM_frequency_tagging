import mne
import matplotlib.pyplot as plt
import numpy as np

from scipy.fftpack import fft


path = 'sham_preproc.fif'
raw = mne.io.read_raw_fif(path, preload=True)

# Load the default sensor positions
montage = mne.channels.read_montage('standard_1005', raw.ch_names)
raw.set_montage(montage)
# Filter into interesting frequency band
raw.filter(1, 30)

# Tell mne that the data are already properly referenced
raw.set_eeg_reference('average', projection=True)

events = mne.find_events(raw)
differences = np.diff(events[:, 0]) / raw.info.get('sfreq')

tol_shift, tol_percept = 2, 2
idx_shift, idx_percept = list(), list()
for i, e in enumerate(events[:-1, 2]):
    if (((e == 2 and events[i + 1, 2] == 3)
        or (e == 4 and events[i + 1, 2] == 1))
        and (differences[i] <= tol_shift)
       ):
        idx_shift.append(i)
        continue
        
    if (((e == 1 and events[i + 1, 2] == 2)
        or (e == 3 and events[i + 1, 2] == 4))
        and (differences[i] >= tol_percept)
       ):
        idx_percept.append(i)


lst_idx_percept =list(map(lambda x: (x, 1), idx_percept))
lst_idx_shift =list(map(lambda x: (x, 2), idx_shift))
indices = np.array(sorted(lst_idx_percept + lst_idx_shift))

new_events = events[indices[:, 0], :].copy()
new_events[:, -1] = indices[:, -1]

epochs = mne.Epochs(raw,new_events,tmin=-2,tmax=2,decim=4,preload=True)
epochs = mne.Epochs(raw,events,tmin=-3,tmax=3,decim=4,preload=True)
epochs.save('sham_160519_epo.fif')


events = mne.find_events(raw)
differences = np.diff(events[:, 0]) / raw.info.get('sfreq')
idx_dominances = np.where(((events[:-1,2] == 1) | (events[:-1,2] == 3)) & (differences > 2))[0]
events_dominances = events[idx_dominances]
epochs = mne.Epochs(raw,events_dominances,tmin=-2,tmax=2,decim=4,preload=True)
epochs.save('sham_230519_epo.fif')