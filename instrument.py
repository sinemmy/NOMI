class Theremin(Instrument):
    pass

class Trumpet(Instrument):
        self.period = 1.54
        self.minamp = 0.1

class Fiddle(Instrument):
        self.


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


class Instrument:
    # theremin is default
    def __init__(self, RATE=[], CHUNK=[], PITCH=[], tonerange=[], period=[], minamp=[],amprange=[] ):
        self.RATE = 44100 # for pyaudio
        self.CHUNK = 1024 # for pyaudio
        self.PITCH = 442 # for pyaudio
        self.tonerange = 2  
        self.period = 0.01
        self.minamp=0.1
        self.amprange=0.5