import argparse
import time
import numpy as np
import pandas as pd

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations


class Comms:

    def __init__(self):
        # self.data = []
        self.isRunning = False
        self.myBoardID = -1
        BoardShim.enable_dev_board_logger()
        params = BrainFlowInputParams()

        # Board IDS
        SYNTH_BOARD = int(-1)
        CYTON = int(0)
        MUSE2 = int(22)

        # Ports
        myCytonSerialPort = 'COM3'
        noSerial = ''

    def __init__(self, boardID):
        # self.data = []
        self.isRunning = False
        self.myBoardID = boardID
        BoardShim.enable_dev_board_logger()
        params = BrainFlowInputParams()

        # Board IDS
        SYNTH_BOARD = int(-1)
        CYTON = int(0)
        MUSE2 = int(22)

        # Ports
        myCytonSerialPort = 'COM3'
        noSerial = ''

    def startStream(self):
        """

        :return:
        """
        BoardShim.enable_dev_board_logger()
        params = BrainFlowInputParams()

        # BOARD IDs internally in brainflow
        SYNTH_BOARD = int(-1)
        CYTON = int(0)
        MUSE2 = int(22)

        if self.myBoardID == 0:
            serial = 'COM3'
        else:

            serial = ''

        params.serial_port = serial

        # create our board
        self.board = BoardShim(SYNTH_BOARD, params)
        self.board.prepare_session()
        # initiate stream
        self.board.start_stream(45000, '')
        self.isRunning = True
        self.board.log_message(LogLevels.LEVEL_INFO, "Start sleeping in the main thread")
        # time.sleep(sleepTime)  # sleep 30 seconds
        # get the data
        self.data = self.board.get_board_data()

    def getData(self):
        return self.board.get_board_data()

    def getCurrentData(self, num_samples: int):
        return self.board.get_current_board_data(num_samples)

    def get_samplingRate(self):
        return self.board.get_sampling_rate(self.myBoardID)

    def getEEGChannels(self):
        """
        Gets the EEG channels from the board being used
        :return:
        """
        return self.board.get_eeg_channels(self.myBoardID)

    def stopStream(self):
        """

        :return:
        """
        if (self.isRunning==True):
            print('Stopping Stream')
            self.board.stop_stream()
            self.board.release_session()
        else:
            print("BOARD WAS NEVER STARTED")

    def run(self, sleepTime : int):
        """

        :param sleepTime:
        :return:
        """
        BoardShim.enable_dev_board_logger()
        params = BrainFlowInputParams()

        # BOARD IDs internally in brainflow
        SYNTH_BOARD = int(-1)
        CYTON = int(0)
        MUSE2 = int(22)

        myCytonSerialPort = 'COM3'
        noSerial = ''

        params.serial_port = noSerial

        # create our board
        board = BoardShim(SYNTH_BOARD, params)
        board.prepare_session()

        # initiate stream
        board.start_stream(45000, '')
        board.log_message(LogLevels.LEVEL_INFO, "Start sleeping in the main thread")
        time.sleep(sleepTime)  # sleep 30 seconds

        # get the data
        self.data = board.get_board_data()

        # board.stop_stream()
        # board.release_session()

        print(self.data)  # for now print the data we can write it to a file

    def getBoard(self):
        """
        Lets us know what board we are using
        :return: The id of the board being used
        """
        if self.myBoardID==-1:
            print("Default Board is being used: SYNTHETIC")
        elif self.myBoardID==0:
            print("OpenBCI Cyton is being used: CYTON")
        elif self.myBoardID==22:
            print("Interaxon Muse 2 is being used: MUSE2")
        return self.myBoardID

    def setBoard(self, boardID: int):
        """
        Change the ID of the Board we are using
        :param boardID: -1 for Synth, 0 for Cyton, 22 for MUSE2
        """
        self.myBoardID = boardID

if __name__ == "__main__":
    # happy = Comms()
    # happy.run(60)
    restored_data = DataFilter.read_file('test.csv')
    restored_df = pd.DataFrame(np.transpose(restored_data))
    print(restored_df.head(10))
    # print(np.diff(restored_df[restored_df.columns[0]].values))
    '''
    channelData = []
    with open("test.csv", "r") as data:
        for line in data:
            # Format the data
            line = line.split(",")  # Convert to a list
            channelData.append(float(0))

    df = pd.read_csv("test.csv")
    '''