import transmission as boardComm
import time
import numpy
from brainflow import BoardShim, DataFilter, NoiseTypes
import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


# SEE REALTIME.PY


def runLocalFilterTest(inputTime: int):
    timeout = time.time() + inputTime
    lt = __localTester()
    isRunning = True
    # lt.start(-1)
    try:
        lt.start(-1)
        isRunning = True
    except:
        print('failed')
        pass

    while (isRunning):
        # end when timeer runs out
        if time.time() > timeout:
            break
        data = lt.getCurrentData(10000)
        # demo how to convert it to pandas DF and plot data
        eeg_channels = BoardShim.get_eeg_channels(-1)
        df = pd.DataFrame(np.transpose(data))
        # plt.figure()
        # print(df)
        # df[eeg_channels].plot(subplots=True)
        # plt.savefig('before_processing.png')
        filter = rtFilter()
        for channel in eeg_channels:
            filter.runFilter(df, channel)
            print(df)


class __localTester():
    def __init__(self):
        self.isRunning = False
        self.bc = boardComm.Comms() # use parenthesis when importing
        print('rtFilter created. Enter <rtFilterName>.start() to start')

    def start(self, boardID):

        self.bc.setBoard(boardID)
        self.isRunning = True
        self.bc.startStream()

    def stop(self):
        try:
            self.bc.stopStream()
        except:
            print('Board was never started!')

    def getCurrentData(self, num_samples):
        return self.bc.getCurrentData(num_samples)


class rtFilter:

    def __init__(self):
        pass

    def runFilter(self, input: numpy.ndarray, channel):
        DataFilter.remove_environmental_noise(input[channel], BoardShim.get_sampling_rate(-1),
                                              NoiseTypes.FIFTY.value)

    # def update(self):
    #

if __name__ == '__main__':
    runLocalFilterTest(45000)
