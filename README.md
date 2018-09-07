# ecgheartbeat
ECG Heartbeat using Spiking Neural Networks

execute the code from ipython and from the parent folder, as follow:

<br/>
<br/>
(venv) federico@nmorph1:~/ecgheartbeat$ ipython<br/>
<br/>
In [1]: run python/ecg_to_spikes.py<br/>
adding recording id: 231 <br/>
adding recording id: 219 <br/>
adding recording id: 124 <br/>
adding recording id: 209 <br/>
adding recording id: 233 <br/>
adding recording id: 116 <br/>
adding recording id: 119 <br/>
adding recording id: 212 <br/>
adding recording id: 103 <br/>
adding recording id: 210 <br/>
adding recording id: 106 <br/>
adding recording id: 113 <br/>
adding recording id: 205 <br/>
adding recording id: 222 <br/>
adding recording id: 202 <br/>
... <br/>
<br/>
after processing all the files in the data folder, it will produce an output image.
<br/>
<img src="https://raw.githubusercontent.com/federicohyo/ecgheartbeat/master/figures/ecg_spikes.png", width=800>
<br/>
This figure shows a sample of ECG signal converted into a temporal spikes train (2 channels). It also shows the reconstruction from the spike activity.
Spike activity is obtained from a 2 channel delta modulator. Spikes from the UP and DN channels are shown in the subplot at the bottom.
