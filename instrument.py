
'''
 Instrument(RATE=[], CHUNK=[], PITCH=[], tonerange=[], period=[], minamp=[],amprange=[] )
'''
class Theremin(Instrument):
    def make_tone(self, freq_old, freq_new, amp_old, amp_new):
        # make_time_varying_sine
         pass

class Trumpet(Instrument):
        self.period = 1.54
        self.minamp = 0.1
        def make_tone(self, freq_old, freq_new, amp_old, amp_new):
            # self.varying_tone(self.trumpet_mod, freq_new, amp_new, self.infodict[self.instrument]['RATE'], self.infodict[self.instrument]['period'])

class TimeVaryingInstrument(Instrument):
    def make_tone(self, freq_old, freq_new, amp_old, amp_new):
        ## COULD MAKE TIME VARYING SINE HERE ##


class Instrument:
    # theremin is default
    # how do you do optional arguments ?
    def __init__(self, RATE= (), CHUNK = () PITCH=(), tonerange=(), period=(), minamp=(),amprange=() ):
        self.RATE = 44100 # for pyaudio
        self.CHUNK = 1024 # for pyaudio
        self.PITCH = 442 # for pyaudio
        self.tonerange = 2  
        self.period = 0.01
        self.minamp = 0.1
        self.amprange = 0.5''

    def make_tone(self, freq_old, freq_new, amp_old, amp_new):
        # This was time-varying-sine or varying-tone before
        pass

    def play_wave(self,stream, samples):
        stream.write(samples.astype(np.float32).tostring())

    def play_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=self.RATE,
                        frames_per_buffer=self.CHUNK,
                        output=True)
        freq_old = self.minfreq
        amp_old = self.minamp
        phaze = 0

        while True:
            try:
                if keyboard.is_pressed('q'):
                    stream.close()
                    break  # finishing the loop
                else:
                    freq_new = self.tonemapping()
                    amp_new = self.ampmapping()

                    tone = self.make_tone(freq_old, freq_new, amp_old, amp_new)

                    self.play_wave(stream, tone[0])
                    freq_old = freq_new
                    amp_old = amp_new
                    phaze = tone[1]
            except:
                continue
