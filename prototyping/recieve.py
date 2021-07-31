import numpy

import transmission
import transmission as boardComm
import time
import argparse
import numpy as np

import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, NoiseTypes


class BoardRelay:
    """
    The Signal Relay which takes data from the board communicator
    """

    def __init__(self, boardID: int):
        self.myBoardComm = boardComm.Comms()
        self.myBoardComm.setBoard(boardID)

    def run(self, desiredTime: int):
        """
        Runs the code for a desired
        :param desiredTime:
        :return:
        """
        self.myBoardComm.startStream()
        timeout = time.time() + desiredTime
        # Signal Filter object is made up here
        while self.myBoardComm.isRunning:  # while the thing is running
            if time.time() > timeout:
                break
            myData = self.myBoardComm.data

            # myCData = self.myBoardComm.getMostRecentData()

            self.mySignalFilter = SF

            myCData = self.myBoardComm.getCurrentData(1)
            print(myCData)
            # currentIndex = numpy.where(myCData[2, 2]) # how to get np array thing
            # try:
            # out = self.mySignalFilter.filter1(float(currentIndex[0]))
            # except:
            #     out = 1
            # filter data = SignalFilter.Notch(myCData)
            # print(str(out))

        self.myBoardComm.stopStream()

    def test(self):
        """
        Runs the Signal Relay A for a period of 69 seconds, EPIC
        """
        self.run(69)

    # --> board --> Board Relay --> raw data
    # --> raw data --> Signal Filter --> filtered data
    # --> filtered data --> Feature Extractor --> Features
    # --> Features --> Feature Relay --> Music Maker


class SF:
    def __init__(self):
        print("signal filter created")

    def filter1(self, inputData):
        # print(str(inputData))
        outputData = inputData
        outputData += 5
        # print(str(outputData))
        return float(outputData)

    def butterfilt(self, data, channel):
        DataFilter.perform_highpass(data[channel], BoardShim.get_sampling_rate(-1), 3.0, 4,
                                    FilterTypes.BUTTERWORTH.value, 0)

    # class SignalFilter:
    #     """
    #     Filters the signal
    #     """
    #     def __init__(self, myRawData):
    #
    #
    #         self.rawData = myRawData
    #         eeg_channels = BoardShim.get_eeg_channels(board_id)
    #         df = pd.DataFrame(np.transpose(myRawData))
    #         plt.figure()
    #         df[eeg_channels].plot(subplots=True)
    #         plt.savefig('before_processing.png')
    #
    #     def __filter(self):
    #         for count, channel in enumerate(eeg_channels):
    #             # filters work in-place
    #             if count == 0:
    #                 DataFilter.perform_bandpass(data[channel], BoardShim.get_sampling_rate(board_id), 15.0, 6.0, 4,
    #                                             FilterTypes.BESSEL.value, 0)
    #             elif count == 1:
    #                 DataFilter.perform_bandstop(data[channel], BoardShim.get_sampling_rate(board_id), 30.0, 1.0, 3,
    #                                             FilterTypes.BUTTERWORTH.value, 0)
    #             elif count == 2:
    #                 DataFilter.perform_lowpass(data[channel], BoardShim.get_sampling_rate(board_id), 20.0, 5,
    #                                            FilterTypes.CHEBYSHEV_TYPE_1.value, 1)
    #             elif count == 3:
    #                 DataFilter.perform_highpass(data[channel], BoardShim.get_sampling_rate(board_id), 3.0, 4,
    #                                             FilterTypes.BUTTERWORTH.value, 0)
    #             elif count == 4:
    #                 DataFilter.perform_rolling_filter(data[channel], 3, AggOperations.MEAN.value)
    #             else:
    #                 DataFilter.remove_environmental_noise(data[channel], BoardShim.get_sampling_rate(board_id),
    #                                                       NoiseTypes.FIFTY.value)


# Pretend that this is Signal-Converter Relay


if __name__ == "__main__":
    myFirstSCR = BoardRelay(-1)
    myFirstSCR.test()

# Format possibly:
# board_communicator > inside > signal-converter-relay > inside > music maker

# Train model to detect teeth clenching -> Instrument use (Will add user ability to pause between sounds)
# Model should have both cases of non teeth clenching and teeth clenching
# Mins and maxes of respective channel average pairs (can be obtained from training data set)
# Mins and maxes will be used to map eeg data to given (screen) theremin amp and freq params
