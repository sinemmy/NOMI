import pyaudio
from itertools import chain
import numpy as np
import pyautogui
import keyboard
import random
import time
#print(pyautogui.position()[0])
from numpy import arange, cumsum, sin, linspace
from numpy import pi
import pandas as pd

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

# class MusicMaker:
#     def __init__(self):
#         pass
#     def generate_music(self, features):
#         # features from signal_converter_ from
#         pass
#     def play_sound(self):
#         pass

#
#     def play_audio(self):
#         p = pyaudio.PyAudio()
#         stream = p.open(format=pyaudio.paFloat32,
#                         channels=1,
#                         rate=self.RATE,
#                         frames_per_buffer=self.CHUNK,
#                         output=True)
#         freq_old = self.minfreq
#         amp_old = self.minamp
#         phaze = 0
#
#         while True:
#             try:
#                 if keyboard.is_pressed('q'):
#                     stream.close()
#                     break  # finishing the loop
#                 else:
#                     freq_new = self.tonemapping()
#                     amp_new = self.ampmapping()
#                     if self.instrument == 'sine':
#
#                         tone = self.make_time_varying_sine(freq_old, freq_new, amp_old, amp_new,
#                                                       self.infodict[self.instrument]['RATE'], self.infodict[self.instrument]['period'],
#                                                       phaze)
#                     elif self.instrument == 'fiddle1':
#                         tone = self.varying_tone(self.fiddle1_mod, freq_new, amp_new, self.infodict[self.instrument]['RATE'],
#                                             self.infodict[self.instrument]['period'])
#                     elif self.instrument == 'fiddle2':
#                         tone = self.varying_tone(self.fiddle2_mod, freq_new, amp_new, self.infodict[self.instrument]['RATE'],
#                                             self.infodict[self.instrument]['period'])
#                     elif self.instrument == 'trumpet':
#                         tone = self.varying_tone(self.trumpet_mod, freq_new, amp_new, self.infodict[self.instrument]['RATE'],
#                                             self.infodict[self.instrument]['period'])
#
#                     self.play_wave(stream, tone[0])
#                     freq_old = freq_new
#                     amp_old = amp_new
#                     phaze = tone[1]
#             except:
#                 continue
#
#     def testInstrument(self):
#         pass


class Theremin:
    """
    Makes a Theremin to use for fun music making!
    """

    def __init__(self):

        self.infodict = {'fiddle1': {'RATE': 44100, 'CHUNK': 1024, 'PITCH': 442, 'tonerange': 2, 'period': 2.06, 'minamp': 0.1,
                                'amprange': 0.5},
                    'fiddle2': {'RATE': 44100, 'CHUNK': 1024, 'PITCH': 442, 'tonerange': 2, 'period': 2.06, 'minamp': 0.1,
                                'amprange': 0.5},
                    'sine': {'RATE': 44100, 'CHUNK': 1024, 'PITCH': 442, 'tonerange': 2, 'period': 0.01, 'minamp': 0.1,
                             'amprange': 0.5},
                    'trumpet    ': {'RATE': 44100,   'CHUNK': 1024, 'PITCH': 442, 'tonerange': 2, 'period': 1.5441269841269842,
                                'minamp': 0.1, 'amprange': 0.5}}
        self.instrument = 'sine'
        self.RATE = self.infodict[self.instrument]['RATE']  # Sampling frequency
        self.CHUNK = self.infodict[self.instrument]['CHUNK']  # buffer
        self.PITCH = self.infodict[self.instrument]['PITCH']  # pitch
        self.minfreq = self.infodict[self.instrument]['PITCH'] / 2 * 2 ** (3 / 12)
        self.tonerange = self.infodict[self.instrument]['tonerange']
        self.period = self.infodict[self.instrument]['period']
        self.minamp = self.infodict[self.instrument]['minamp']
        self.amprange = self.infodict[self.instrument]['amprange']

    def distance(self):
        """
        Gets the The x and y from the pyautogui
        :return:
        """
        x, y = pyautogui.position()
        # x_dist = np.sqrt((x-window_size.width/2)**2)
        # y_dist = abs(y-window_size.height)
        # x_max = np.sqrt((window_size.width/2)**2)
        # y_max = window_size.height
        # x_ratio = x_dist/x_max
        # y_ratio = y_dist/y_max
        # return x_ratio, y_ratio
        return x, y

    def tonemapping_eeg(self, freq_channel):
        # maybe series or arrays later
        # mult5 for instruments 15 for sine
        # ratio = distance()
        # freq = minfreq*2**(tonerange*ratio[1])
        freq = abs(freq_channel) * 15
        return freq

    def ampmapping_eeg(self, amp_channel):
        # ratio = distance()
        # amp = minamp+amprange*ratio[0]
        amp = self.minamp + self.amprange * abs(amp_channel) / 2000
        return amp

    def make_time_varying_sine(self, start_freq, end_freq, start_A, end_A, fs, sec, phaze_start):
        freqs = linspace(start_freq, end_freq, num=int(round(fs * sec)))
        A = linspace(start_A, end_A, num=int(round(fs * sec)))
        phazes_diff = 2. * pi * freqs / fs  # Amount of change in angular frequency
        phazes = cumsum(phazes_diff) + phaze_start  # phase
        phaze_last = phazes[-1]
        ret = A * sin(phazes)  # Sine wave synthesis
        return ret, phaze_last

    def varying_tone(self, wave_data, freq, amp, fs, sec):
        relfreq = freq / 800
        relfreq += ((1 - relfreq) / 1.1)
        mult = relfreq // 1
        rem = relfreq % 1
        df = pd.DataFrame({'randvals': np.random.rand(len(wave_data)), 'data': wave_data})
        df['newmask'] = df['randvals'] <= rem
        outdata = (df['data'][df['newmask']])
        return (amp * np.array(outdata), -1)

    def play_eegaudio(self, df):
        """
        Plays audio, maybe from an eeg strean
        :return:
        """
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=self.RATE,
                        frames_per_buffer=self.CHUNK,
                        output=True)
        freq_old = self.minfreq
        amp_old = self.minamp
        phaze = 0

        instrument = self.instrument

        for i in range(len(df)):

            if True: #df['Non-ClenchedTeeth'].values[i]:
                amp_new = self.ampmapping_eeg(df['ABS(AF)SUM'].values[i])
                freq_new = self.tonemapping_eeg(df['ABS(TP)SUM'].values[i])
                print(freq_new, amp_new)
                if instrument == 'sine':

                    tone = self.make_time_varying_sine(freq_old, freq_new, amp_old, amp_new, self.infodict[instrument]['RATE'],
                                                  self.infodict[instrument]['period'], phaze)
                elif instrument == 'fiddle1':
                    tone = self.varying_tone(self.fiddle1_mod, freq_new, amp_new, self.infodict[instrument]['RATE'],
                                        self.infodict[instrument]['period'])
                elif instrument == 'fiddle2':
                    tone = self.varying_tone(self.fiddle2_mod, freq_new, amp_new, self.infodict[instrument]['RATE'],
                                        self.infodict[instrument]['period'])
                elif instrument == 'trumpet':
                    tone = self.varying_tone(self.trumpet_mod, freq_new, amp_new, self.infodict[instrument]['RATE'],
                                        self.infodict[instrument]['period'])

                self.play_wave(stream, tone[0])
                freq_old = freq_new
                amp_old = amp_new
                phaze = tone[1]
            else:
                time.sleep(1)

    def playcumulative_eegaudio(self, df):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=self.RATE,
                        frames_per_buffer=self.CHUNK,
                        output=True)
        freq_old = self.minfreq
        amp_old = self.minamp
        phaze = 0
        instrument = self.instrument

        counter = 0
        for i in range(len(df)):
            cumsum_amps = [0, 0, 0, 0, 0]
            cumsum_freqs = [0, 0, 0, 0, 0]

            if True: #df['Non-ClenchedTeeth'].values[i]:
                cumsum_amps = cumsum_amps[1:]
                cumsum_freqs = cumsum_freqs[1:]
                cumsum_amps.append(df[df.columns[1]].values[i])
                cumsum_freqs.append(df['ABS(TP)SUM'].values[i])
                if counter >= 5:
                    amp_new = self.ampmapping_eeg(np.array(cumsum_amps).mean())
                    freq_new = self.tonemapping_eeg(np.array(cumsum_freqs).mean())
                else:
                    amp_new = self.ampmapping_eeg(df['ABS(AF)SUM'].values[i])
                    freq_new = self.tonemapping_eeg(df['ABS(TP)SUM'].values[i])
                print(freq_new, amp_new)
                if instrument == 'sine':

                    tone = self.make_time_varying_sine(freq_old, freq_new, amp_old, amp_new, self.infodict[instrument]['RATE'],
                                                  self.infodict[instrument]['period'], phaze)
                elif instrument == 'fiddle1':
                    tone = self.varying_tone(self.fiddle1_mod, freq_new, amp_new, self.infodict[instrument]['RATE'],
                                        self.infodict[instrument]['period'])
                elif instrument == 'fiddle2':
                    tone = self.varying_tone(self.fiddle2_mod, freq_new, amp_new, self.infodict[instrument]['RATE'],
                                        self.infodict[instrument]['period'])
                elif instrument == 'trumpet':
                    tone = self.varying_tone(self.trumpet_mod, freq_new, amp_new, self.infodict[instrument]['RATE'],
                                        self.infodict[instrument]['period'])

                self.play_wave(stream, tone[0])
                freq_old = freq_new
                amp_old = amp_new
                phaze = tone[1]
                counter += 1
                strcounter = str(counter)
            else:
                time.sleep

    def ampmapping_eeg(self, amp_channel):
        # ratio = distance()
        # amp = minamp+amprange*ratio[0]
        amp = self.minamp + self.amprange * self.distance()[0] / 2000
        return amp


    def testInstrument(self):
        pass

if __name__ == "__main__":
    # RUN YOUR CODE HERE
    myTheremin = Theremin()

    restored_data = DataFilter.read_file('myNEWData.csv')
    df = pd.DataFrame(np.transpose(restored_data))
    # with open('myNEWData.csv') as f:
    #     packagepackage = f.read()

    df2 = pd.DataFrame(np.transpose(df))

    myTheremin.play_eegaudio(df2)
    time.sleep(20)
    myTheremin.playcumulative_eegaudio(df)

