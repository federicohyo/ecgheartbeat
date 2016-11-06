## Copyright (C) 2016 - Federico Corradi
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

## Author: (2016) Federico Corradi <federico@ini.phys.ethz.ch>

from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import numpy as np
import re
from scipy.interpolate import interp1d


####################################################
# This class deals with the ECG data and labels
# also encodes ECG signals to spikes UP/DN channels
####################################################

class levelcrossing:
    def __init__(self):
        self.recordings = {'id': [],                #recording/person id
                           'data': [],              #ecg signal
                           'rpeak': [],             #rpeak signal index
                           'ppeak': [],             #ppeak signal index
                           'qpeak': [],             #1peak signal index
                           'thrup': [],
                           'thrdn': [],
                           'upch': [],              # up ch adc
                           'dnch': [],              # dn ch adc
                           'reconstruction': []}    # from up/dn spikes
        self.n_data = 0;
        self.n_label = 0;
    
    def load_data(self, data_folder = 'data/', do_plot = False, partial_load = False):
        '''
            Load all data from data_folder
        '''
        #find all ecg files in folder
        onlyfiles = [f for f in listdir(data_folder) if isfile(join(data_folder, f)) and re.match(r'ecg*', f)]

        #load data
        for this_file in onlyfiles:
            id_rec = int(this_file.split('.')[2])
            try:
                self.recordings['id'].index(id_rec)
            except ValueError:
                print("adding recording id: " + str(id_rec))
                self.recordings['id'].append(id_rec)
            this_indx = self.recordings['id'].index(id_rec)
            if(partial_load):
                self.recordings['data'].append(np.loadtxt(data_folder + this_file)[0:500])
            else:
                self.recordings['data'].append(np.loadtxt(data_folder + this_file))
            if(do_plot):
                plt.figure()
                plt.hold(True)
                plt.title("raw_signal_with_peaks")
                plt.plot(self.recordings['data'][this_indx][:,0],self.recordings['data'][this_indx][:,1])
            
            self.n_data += 1;
    
        #find all rpeak files in folder
        onlyfiles = [f for f in listdir(data_folder) if isfile(join(data_folder, f)) and re.match(r'rpeak*', f)]
        
        for this_file in onlyfiles:
            id_rec = int(this_file.split('.')[2])
            try:
                self.recordings['id'].index(id_rec)
            except ValueError:
                print("adding label id" + id_rec)
                self.recordings['id'].append(id_rec)
            this_indx = self.recordings['id'].index(id_rec)
            self.recordings['rpeak'].append(np.loadtxt(data_folder + this_file))
                
            if(do_plot):
                plt.title("lables_signal_with_peaks")
                index_r = self.recordings['rpeak'][this_indx].astype(int)
                plt.plot(self.recordings['data'][this_indx][index_r],
                         np.repeat(1,np.shape(self.recordings['rpeak'][this_indx])[0]), 'rx')
            self.n_label += 1;

        if(do_plot):
            plt.show()


    def spikify(self, id_to_spike, thr_up = 0.005, thr_dn = 0.005, do_plot = False, do_recontruction = False, interpfact=10000):
        '''
            convert ecg signals to spikes (ideal asynch level crossing ADC with 2 output channel)
               id_to_spike: ids of recordings to pass to adcs and create up/dn spikes
        '''
        #convert to spikes
        for this_indx in id_to_spike:
            counter = 0;
            id_rec = self.recordings['id'].index(this_indx)
            actual_dc = self.recordings['data'][id_rec][0,1]   #first dc is actual dc
            spike_up = []
            spike_dn = []
            #data = self.recordings['data'][id_rec]
            #interpolate ecg data
            f = interp1d(self.recordings['data'][0][:,0], self.recordings['data'][0][:,1])
            rangeint = np.round((np.max(self.recordings['data'][0][:,0]) - np.min(self.recordings['data'][0][:,0]))*interpfact)
            xnew = np.linspace(np.min(self.recordings['data'][0][:,0]), np.max(self.recordings['data'][0][:,0]),
                               num=int(rangeint), endpoint=True)
            data = np.reshape([xnew, f(xnew)], (2, len(xnew))).T
            
            for i in range(len(data)):
                if( (actual_dc + thr_up) < data[i,1] ):
                    spike_up.append(data[i,0])  #spike up
                    actual_dc = data[i,1]       # update current dc value
                elif( (actual_dc - thr_dn) > data[i,1] ):
                    spike_dn.append(data[i,0])  #spike dn
                    actual_dc = data[i,1]       # update current dc value

            self.recordings['upch'].append(np.transpose(spike_up))  #add to rec
            self.recordings['dnch'].append(np.transpose(spike_dn))

            if(do_plot):
                plt.figure()
                plt.title("id ", str(this_indx))
                plt.subplot(2,1,1)
                plt.plot(self.recordings['data'][id_rec][:,0],self.recordings['data'][id_rec][:,1], 'bx', label='orig')
                plt.plot(data[:,0][0:10000], data[:,1][0:10000], 'gx-', label='interp')
                plt.subplot(2,1,2)
                plt.plot(self.recordings['upch'][id_rec], np.repeat(1,len(self.recordings['upch'][id_rec])), 'rx', label='up ch')
                plt.plot(self.recordings['dnch'][id_rec], np.repeat(0.98,len(self.recordings['dnch'][id_rec])), 'gx', label='dn ch')

            if(do_recontruction == True):
                tot_spk = len(self.recordings['upch'][id_rec])+len(self.recordings['dnch'][id_rec])
                current_val = self.recordings['data'][0][0][1] #first spike
                signal_rec = []
                time_rec = []
                counter_up = 0
                counter_dn = 0
                for i in range(tot_spk):
                    if(self.recordings['upch'][id_rec][counter_up] < self.recordings['dnch'][id_rec][counter_dn]):
                        current_val = current_val + thr_up
                        signal_rec.append(current_val)
                        time_rec.append(self.recordings['upch'][id_rec][counter_up])
                        if(counter_up < len(self.recordings['upch'][id_rec])-1):
                            counter_up += 1
                    elif(self.recordings['upch'][id_rec][counter_up] > self.recordings['dnch'][id_rec][counter_dn]):
                        current_val = current_val - thr_dn
                        signal_rec.append(current_val)
                        time_rec.append(self.recordings['dnch'][id_rec][counter_dn])
                        if(counter_dn < len(self.recordings['dnch'][id_rec])-1):
                            counter_dn +=1
    
                self.recordings['reconstruction'].append([signal_rec, time_rec])

        if(do_plot):
            plt.show()

