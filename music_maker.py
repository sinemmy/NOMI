import pyaudio
from itertools import chain
import numpy as np
import pyautogui
import keyboard
import random
import time
#print(pyautogui.position()[0])
from scipy import arange, cumsum, sin, linspace
from scipy import pi as mpi

'''
class MusicMaker:
    def __init__(self):

    def generate_music(self, features):
        # features from signal_converter_ from
        pass
    def play_sound(self):
        pass

    def testInstrument(self):
        pass
'''

class Theremin(MusicMaker):
    infodict = {'fiddle1': {'RATE': 44100, 'CHUNK': 1024, 'PITCH': 442, 'tonerange': 2, 'period': 2.06, 'minamp': 0.1,
                            'amprange': 0.5},
                'fiddle2': {'RATE': 44100, 'CHUNK': 1024, 'PITCH': 442, 'tonerange': 2, 'period': 2.06, 'minamp': 0.1,
                            'amprange': 0.5},
                'sine': {'RATE': 44100, 'CHUNK': 1024, 'PITCH': 442, 'tonerange': 2, 'period': 0.01, 'minamp': 0.1,
                         'amprange': 0.5},
                'trumpet    ': {'RATE': 44100,   'CHUNK': 1024, 'PITCH': 442, 'tonerange': 2, 'period': 1.5441269841269842,
                            'minamp': 0.1, 'amprange': 0.5}}
    instrument = 'sine'
    RATE = infodict[instrument]['RATE']  # Sampling frequency
    CHUNK = infodict[instrument]['CHUNK']  # buffer
    PITCH = infodict[instrument]['PITCH']  # pitch
    minfreq = infodict[instrument]['PITCH'] / 2 * 2 ** (3 / 12)
    tonerange = infodict[instrument]['tonerange']
    period = infodict[instrument]['period']
    minamp = infodict[instrument]['minamp']
    amprange = infodict[instrument]['amprange'    def get_window_size():
        window_size = pyautogui.size()
        return window_size

    def distance():
        window_size = get_window_size()
        x, y = pyautogui.position()
        # x_dist = np.sqrt((x-window_size.width/2)**2)
        # y_dist = abs(y-window_size.height)
        # x_max = np.sqrt((window_size.width/2)**2)
        # y_max = window_size.height
        # x_ratio = x_dist/x_max
        # y_ratio = y_dist/y_max
        # return x_ratio, y_ratio
        return x, y

    def tonemapping_eeg(freq_channel):
        # maybe series or arrays later
        # mult5 for instruments 15 for sine
        # ratio = distance()
        # freq = minfreq*2**(tonerange*ratio[1])
        freq = abs(freq_channel) * 15
        return freq

    def ampmapping_eeg(amp_channel):
        # ratio = distance()
        # amp = minamp+amprange*ratio[0]
        amp = minamp + amprange * abs(amp_channel) / 2000
        return amp

    def make_time_varying_sine(start_freq, end_freq, start_A, end_A, fs, sec, phaze_start):
        freqs = linspace(start_freq, end_freq, num=int(round(fs * sec)))
        A = linspace(start_A, end_A, num=int(round(fs * sec)))
        phazes_diff = 2. * mpi * freqs / fs  # Amount of change in angular frequency
        phazes = cumsum(phazes_diff) + phaze_start  # phase
        phaze_last = phazes[-1]
        ret = A * sin(phazes)  # Sine wave synthesis
        return ret, phaze_last

    def varying_tone(wave_data, freq, amp, fs, sec):
        relfreq = freq / 800
        relfreq += ((1 - relfreq) / 1.1)
        mult = relfreq // 1
        rem = relfreq % 1
        df = pd.DataFrame({'randvals': np.random.rand(len(wave_data)), 'data': wave_data})
        df['newmask'] = df['randvals'] <= rem
        outdata = (df['data'][df['newmask']])
        return (amp * np.array(outdata), -

    def play_eegaudio(df):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=RATE,
                        frames_per_buffer=CHUNK,
                        output=True)
        freq_old = minfreq
        amp_old = minamp
        phaze = 0

        for i in range(len(df)):

            if df['Non-ClenchedTeeth'].values[i]:
                amp_new = ampmapping_eeg(df['ABS(AF)SUM'].values[i])
                freq_new = tonemapping_eeg(df['ABS(TP)SUM'].values[i])
                print(freq_new, amp_new)
                if instrument == 'sine':

                    tone = make_time_varying_sine(freq_old, freq_new, amp_old, amp_new, infodict[instrument]['RATE'],
                                                  infodict[instrument]['period'], phaze)
                elif instrument == 'fiddle1':
                    tone = varying_tone(fiddle1_mod, freq_new, amp_new, infodict[instrument]['RATE'],
                                        infodict[instrument]['period'])
                elif instrument == 'fiddle2':
                    tone = varying_tone(fiddle2_mod, freq_new, amp_new, infodict[instrument]['RATE'],
                                        infodict[instrument]['period'])
                elif instrument == 'trumpet':
                    tone = varying_tone(trumpet_mod, freq_new, amp_new, infodict[instrument]['RATE'],
                                        infodict[instrument]['period'])

                play_wave(stream, tone[0])
                freq_old = freq_new
                amp_old = amp_new
                phaze = tone[1]
            else:
                time.sleep(1)

    def play_eegaudio(df):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=RATE,
                        frames_per_buffer=CHUNK,
                        output=True)
        freq_old = minfreq
        amp_old = minamp
        phaze = 0

        counter = 0
        for i in range(len(df)):
            cumsum_amps = [0, 0, 0, 0, 0]
            cumsum_freqs = [0, 0, 0, 0, 0]

            if df['Non-ClenchedTeeth'].values[i]:
                cumsum_amps = cumsum_amps[1:]
                cumsum_freqs = cumsum_freqs[1:]
                cumsum_amps.append(df['ABS(AF)SUM'].values[i])
                cumsum_freqs.append(df['ABS(TP)SUM'].values[i])
                if counter >= 5:
                    amp_new = ampmapping_eeg(np.array(cumsum_amps).mean())
                    freq_new = tonemapping_eeg(np.array(cumsum_freqs).mean())
                else:
                    amp_new = ampmapping_eeg(df['ABS(AF)SUM'].values[i])
                    freq_new = tonemapping_eeg(df['ABS(TP)SUM'].values[i])
                print(freq_new, amp_new)
                if instrument == 'sine':

                    tone = make_time_varying_sine(freq_old, freq_new, amp_old, amp_new, infodict[instrument]['RATE'],
                                                  infodict[instrument]['period'], phaze)
                elif instrument == 'fiddle1':
                    tone = varying_tone(fiddle1_mod, freq_new, amp_new, infodict[instrument]['RATE'],
                                        infodict[instrument]['period'])
                elif instrument == 'fiddle2':
                    tone = varying_tone(fiddle2_mod, freq_new, amp_new, infodict[instrument]['RATE'],
                                        infodict[instrument]['period'])
                elif instrument == 'trumpet':
                    tone = varying_tone(trumpet_mod, freq_new, amp_new, infodict[instrument]['RATE'],
                                        infodict[instrument]['period'])

                play_wave(stream, tone[0])
                freq_old = freq_new
                amp_old = amp_new
                phaze = tone[1]
                counter += 1
                strcounter = str(counter)
            else:
                time.sleep(1)

    play_eegaudio(df)

    def ampmapping_eeg(amp_channel):
        # ratio = distance()
        # amp = minamp+amprange*ratio[0]
        amp = minamp + amprange * distance()[0] / 2000
        return amp

    ampmapping_eeg(365)


    def testInstrument(self):
        pass
