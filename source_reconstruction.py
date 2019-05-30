import mne
import numpy as np
from mne.time_frequency import tfr_morlet, tfr_array_morlet
import os
from mne.channels import read_montage
import matplotlib.pyplot as plt
from mayavi import mlab
import operator
from mne.beamformer import make_lcmv, apply_lcmv_epochs
from mne.baseline import rescale


paths = ['vertical_strap_1.edf',
        'vertical_strap_2.edf',
        'vertical_strap_3.edf']
raw = mne.concatenate_raws([mne.io.read_raw_edf(path,preload=True) for path in paths])

# We have to set the channel names explicitly here because we didn't do it properly in the EEG software, this is usually not necessary
names = ['Fp1','Fp2','F3','F4','C3','C4','P3','P4','O1','O2','F7','F8','T7','T8','P7'
        ,'P8','Fz','Cz','Pz','Iz','FC1','FC2','CP1','CP2','FC5','FC6','CP5','CP6','TP9','TP10']
raw.rename_channels(dict(zip(raw.ch_names, names)))

# Load the default sensor positions
montage = read_montage('standard_1005',raw.ch_names)
raw.set_montage(montage)

# Filter into interesting frequency band
raw.filter(1,30)

# Tell mne that the data are already properly referenced
raw.set_eeg_reference('average', projection=True)

# Just make sure sensors are all in the right place
# raw.plot_sensors(show_names=True,show=False)
# plt.show()

# Directory where all parcellated structural T1-weighted MRI scans are saved by Freesurfer
subjects_dir = 'subjects'

# If forward model (lead field matrix from conductor model based on average brain) hasn't been created yet, create it
if not os.path.isfile('fwd.fif'):
    src = mne.setup_source_space('fsaverage', subjects_dir=subjects_dir)
    conductivity = (0.3, 0.006, 0.3)
    model = mne.make_bem_model(subject='fsaverage',conductivity=conductivity,subjects_dir=subjects_dir)
    bem = mne.make_bem_solution(model)
    # We don't need a transformation matrix because the montage that ships with MNE is already in the same coordinates as the fsaverage brain
    # Let's check that the sensors are aligned with the head properly just to be sure
    # mne.viz.plot_alignment(raw.info, trans=None, subject='fsaverage', subjects_dir=subjects_dir, eeg='projected')
    # mlab.show()
    fwd = mne.make_forward_solution(raw.info, trans=None, src=src, bem=bem, meg=False, eeg=True)
    fwd = mne.convert_forward_solution(fwd, surf_ori=True)
    mne.write_forward_solution('fwd.fif',fwd)
else:
    fwd = mne.read_forward_solution('fwd.fif')

# Get label for all sources in left or right V1 or V2
labels = mne.read_labels_from_annot('fsaverage',parc='PALS_B12_Visuotopic',subjects_dir=subjects_dir,regexp='.*(V1|V2).*')
label = reduce(operator.add,labels)

# Here we have events of just one type, the transition from vertical (left eye) to horizontal (right eye) percept
# In the future every dataset will have two types of events for both transitions
events = mne.find_events(raw)
epochs = mne.Epochs(raw,events,tmin=-3,tmax=3,decim=4,preload=True)

# Make covariance matrix and LCMV beamformer spatial filters
cov = mne.compute_covariance(epochs, method='oas')
filters = make_lcmv(raw.info, fwd, cov, pick_ori='max-power', weight_norm='unit-noise-gain', label=label, reduce_rank=True)

# Project the data to source space
epochs_stc = apply_lcmv_epochs(epochs,filters)

# Convert to ndarray
epochs_stc = np.array([e.data for e in epochs_stc])

# Compute TFR for every voxel in the V1/V2 source space and average the TFRs across voxels
# Note: this can take a long time because there are many voxels. Sometimes it's better to extract a single timeseries for the entire label.
# For this, see mne.extract_label_time_course()
freqs = np.linspace(10,20,50)
n_cycles = freqs*2
tfr = tfr_array_morlet(epochs_stc,sfreq=epochs.info['sfreq'],freqs=freqs,n_cycles=n_cycles,output='avg_power').mean(0)

# Plot averaged time-frequency in V1/V2
plt.pcolormesh(epochs.times, freqs, np.log(tfr.squeeze()), cmap='RdBu_r')
plt.title("Average TFR in V1/V2 around vertical to horizontal percept transition")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.show()