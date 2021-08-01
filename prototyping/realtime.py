import time
import brainflow
import numpy as np
import threading


import pandas as pd
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations

from brainflow.ml_model import MLModel, BrainFlowMetrics, BrainFlowClassifiers, BrainFlowModelParams



from transmission import Comms as boardComm




# def predictFromEEG(data, channels, samplingrate, concentrationOrRelaxation=0 ):
#
#     def initialize_metrics(concentrationOrRelaxation) :
#         # 0 for relaxation, 1 for concentration
#         if concentrationOrRelaxation not in [0,1]:
#             print('Please input 0 for relaxation and 1 for concentration')
#             return
#
#         if concentrationOrRelaxation == 0: # relaxation
#             state_params =  BrainFlowModelParams(BrainFlowMetrics.CONCENTRATION.value, BrainFlowClassifiers.REGRESSION.value)
#             # note in the example they used KNN not REGRESSION but in the widget, they use regression
#         else:
#             state_params = BrainFlowModelParams(BrainFlowMetrics.RELAXATION.value, BrainFlowClassifiers.REGRESSION.value)
#
#         brainstate_model  = MLModel(state_params)
#         brainstate_model.prepare()
#         return brainstate_model
#
#     # get band powers
#     bands = DataFilter.get_avg_band_powers(data, channels, samplingrate, True)
#     feature_vector = np.concatenate((bands[0], bands[1]))
#
#     mymodel = initialize_metrics(concentrationOrRelaxation)
#     prediction = mymodel.predict(feature_vector)
#
#     # should be at the end of the processes
#     mymodel.release()
#
#     return prediction
#

class DataThread(threading.Thread):

    def __init__(self, myBoardComm: boardComm):
        threading.Thread.__init__(self)
        self.myBoard = myBoardComm
        # self.myBoard = boardComm(boardID)
        # self.myBoard.setBoard(boardID)
        self.eeg_channels = self.myBoard.getEEGChannels()
        self.samplingRate = self.myBoard.get_samplingRate()

        self.keep_alive = True

    def prepare_model(self, concentrationOrRelaxation=0):
        if concentrationOrRelaxation not in [0, 1]:
            print('Please input 0 for relaxation and 1 for concentration')
            return

        if concentrationOrRelaxation == 0:  # relaxation
            state_params = BrainFlowModelParams(BrainFlowMetrics.RELAXATION.value,
                                                BrainFlowClassifiers.REGRESSION.value)
            my_params = (state_params)
            # note in the example they used KNN not REGRESSION but in the widget, they use regression
        else:
            state_params = BrainFlowModelParams(BrainFlowMetrics.CONCENTRATION.value,
                                                BrainFlowClassifiers.REGRESSION.value)

        brainstate_model = MLModel(state_params)
        brainstate_model.prepare()
        return brainstate_model

    def predict_from_model(self, feature_vector, mymodel):
        # get band powers
        prediction = mymodel.predict(feature_vector)
        return prediction

    def release_model(self, mymodel):
        mymodel.release()

    def run(self, concentrationOrRelaxation=0):
        if concentrationOrRelaxation not in [0, 1]:
            print('Please pick concentration or relaxation model. \n '
                   '0: Relaxation \n'
                   '1: Concentration \n'
                   'Default is (0) Relaxation')
            return


        modelString = ('Relaxation', 'Concentration')
        print(f"Preparing model for {modelString[concentrationOrRelaxation]}")
        brain_state_model = self.prepare_model(concentrationOrRelaxation)

        win_size = 20
        sleeptime = 1
        points_per_update = win_size * self.samplingRate
        print("length eeg channels: ",len(self.eeg_channels))
        print(self.samplingRate)
        while self.keep_alive:
            time.sleep(sleeptime)


            # get the board data ; doesnt remove data from the internal buffer
            data = self.myBoard.getCurrentData(int(points_per_update))

            if data.shape[1] < 2000:
                print(data.shape)
                continue
            # data = self.myBoard
            #print(data)
            #print('ppu: ',points_per_update)
            #reshape_data = data.T
            #print(reshape_data.shape, data.shape)

            #df = pd.DataFrame(reshape_data)
            #fft_data = np.fft.fft2(reshape_data)
            #fft_df = pd.DataFrame(fft_data)
            #df = df.transpose()
            #print(df.values[0],df.values[2])

            #print(len(reshape_data))
            # print('DataShape %s :' % (str(data.shape)) + str(type(data)))

            nfft = DataFilter.get_nearest_power_of_two(self.samplingRate)
            myLen = len(data)
            sizeB = data.size
            shapeOfYou = data.shape
            print(nfft)
            print(len(data))
            print(data.size)
            # time.sleep(20)

            # USING BRAINFLOW'S RELAXATION/CONCENTRATION ML PREDICTION
            # They recommend 4s of data
            bands = DataFilter.get_avg_band_powers(data, self.eeg_channels, self.samplingRate, True)
            feature_vector = np.concatenate((bands[0], bands[1]))

            brain_state_prediction = self.predict_from_model(feature_vector, brain_state_model)
            print(f"{modelString[concentrationOrRelaxation]} prediction: {brain_state_prediction}")

            # relaxationPrediction = predictFromEEG(data, self.eeg_channels, self.samplingRate)
            # concentrationPrediction = predictFromEEG(data, self.eeg_channels, self.samplingRate, 1)
            #print(f"Concentration prediction: {concentrationPrediction}")



            for channel in self.eeg_channels[0:7]:

                # make filters work in place
                # fftData = DataFilter.perform_fft(data[channel], 2)
                # DataFilter.perform_bandstop(data[channel], self.samplingRate, 50.0, 4.0, 4,
                #                             FilterTypes.BUTTERWORTH.value, 0)  # bandstop 48-52
                # DataFilter.perform_bandstop(data[channel], self.samplingRate, 60.0, 4.0, 4,
                #                             FilterTypes.BUTTERWORTH.value, 0)  # bandstop 58 - 62
                # DataFilter.perform_bandpass(data[channel], self.samplingRate, 21.0, 20.0, 4,
                #                             FilterTypes.BESSEL.value, 0)  # bandpass 11 - 31

                # DataFilter.detrend(data[channel], DetrendOperations.LINEAR.value)
                # DataFilter.detrend(data[channel], DetrendOperations.LINEAR.value)
                DataFilter.perform_rolling_filter(data[channel], 3, AggOperations.MEDIAN.value)
                DataFilter.perform_lowpass(data[channel], self.samplingRate, 50.0, 5,
                                           FilterTypes.CHEBYSHEV_TYPE_1.value, 1)

                psd = DataFilter.get_psd_welch(data[channel], nfft, nfft // 2, self.samplingRate,
                                               WindowFunctions.BLACKMAN_HARRIS.value)

                band_power_alpha = DataFilter.get_band_power(psd, 7.0, 13.0)
                band_power_beta = DataFilter.get_band_power(psd, 14.0, 30.0)

                outputFile = open("output.txt", "w")
                outputFile.write('[' + str(time.time()) + '] Alpha: ' +  str(band_power_alpha) + 'Beta: ' + str(band_power_beta) + '\n  ')
                print("alpha/beta:%f", band_power_alpha / band_power_beta )

        # releasing model at the end
        self.release_model(brain_state_model)
            # print(fftData)


def main():
    BoardShim.enable_dev_board_logger()
    newBoard = boardComm(-1)  # make a new board

    newBoard.startStream()
    dt = DataThread(newBoard)
    # dt.start()

    # 1 for concentration, 0 for relaxation
    concentrationOrRelaxation = 1

    dt.run(concentrationOrRelaxation)
    try:
        # timeout = time.time() + 60 # run for 60 seconds
        #
        # while True:
        time.sleep(60)

    except:
        dt.keep_alive = False
        dt.join()

    newBoard.stopStream()


if __name__ == '__main__':
    main()
