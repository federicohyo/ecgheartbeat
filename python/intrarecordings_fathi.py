## Copyright (C) 2018 - Federico Corradi
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.

## Author: (2018) Federico Corradi <federico@ini.phys.ethz.ch>

import sys
import numpy as np
import matplotlib.pyplot as plt

#add the python folder
sys.path.append('python/')

import levelcrossing                #deals with ecg files and conversion to spike
lv = levelcrossing.levelcrossing();

#load a chunck of data, pick from 2000 to 3000 index
raw_data = lv.read_amplifier_dat_file('data/amp-A-031.dat', startf=2000, endf=3000);

#convert signal into spikes
all_id = lv.recordings['id']
lv.spikify(all_id, thr_up = 0.5, thr_dn = 0.5, do_recontruction=True, interpfact=10000)

### do some plotting
plt.ion()
plt.subplot(2,1,1)
plt.plot(lv.recordings['reconstruction'][0][1], lv.recordings['reconstruction'][0][0], 'bx-', label='reconstructed form spikes')
plt.plot(lv.recordings['data'][0][:,0], lv.recordings['data'][0][:,1], 'rx-', label='original')
plt.ylabel('amplitude [uV]')
plt.legend(loc='best')
plt.subplot(2,1,2)
plt.plot(lv.recordings['upch'][0], np.repeat(1,len(lv.recordings['upch'][0])), 'mx', marker='^',  label='up ch spikes')
plt.plot(lv.recordings['dnch'][0], np.repeat(0.98,len(lv.recordings['dnch'][0])), 'gx', marker='v', label='dn ch spikes')
plt.ylim([0.88, 1.1])
plt.ylabel('channel id')
plt.xlabel('time [au]')
plt.legend(loc='best')
plt.show()
