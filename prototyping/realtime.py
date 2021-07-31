import time
import brainflow
import numpy as np
import threading

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

from transmission import Comms as boardComm


class DataThread(threading.Thread):

    def __init__(self, board: boardComm, boardID: int):
        threading.Thread.__init__(self)
        self.myBoard = board
        self.myBoard.setBoard(boardID)
        self.eeg_channels = self.myBoard.getEEGChannels()
        self.samplingRate = self.myBoard.get_samplingRate()

        self.keep_alive = True

    def run(self):
        win_size = 5
        sleeptime = 1
        points_per_update = win_size * self.samplingRate
        while self.keep_alive:
            time.sleep(sleeptime)

            # get the board data ; doesnt remove data from the internal buffer
            data = self.myBoard.getCurrentData(int(points_per_update))
            print('DataShape %s :' % (str(data.shape)) + ' ' + str(type(data)))

            for channel in self.eeg_channels:
                # make filters work in place
                # fftData = DataFilter.perform_fft(data[channel], 2)
                DataFilter.perform_bandstop(data[channel], self.samplingRate, 50.0, 4.0, 4,
                                            FilterTypes.BUTTERWORTH.value, 0)  # bandstop 48-52
                DataFilter.perform_bandstop(data[channel], self.samplingRate, 60.0, 4.0, 4,
                                            FilterTypes.BUTTERWORTH.value, 0)  # bandstop 58 - 62
                DataFilter.perform_bandpass(data[channel], self.samplingRate, 21.0, 20.0, 4,
                                            FilterTypes.BESSEL.value, 0)  # bandpass 11 - 31
            # print(fftData)


def main():
    BoardShim.enable_dev_board_logger()
    newBoard = boardComm()  # make a new board

    newBoard.startStream()
    dt = DataThread(newBoard, -1)
    # dt.start()
    dt.run()
    try:
        time.sleep(69)
    except:
        dt.keep_alive = False
        dt.join()

    newBoard.stopStream()


if __name__ == '__main__':
    main()
