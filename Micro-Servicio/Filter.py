from abc import abstractclassmethod
from scipy.io import wavfile
from scipy.signal import butter, filtfilt
from Interfaces import IFilter
import numpy as np





class BandFilter(IFilter):
    def __init__(self) -> None:
        
        self.__fc_high = 7900
        self.__fc_low = 100
        self.__order = 5

    def create_filter(self, folder_path,audio_file,sample) -> None:
        
        audio_path = folder_path + audio_file

        sample_rate, audio_data = wavfile.read(audio_path)
        audio_data = audio_data.astype(np.float32) / np.max(np.abs(audio_data))
        duration = len(audio_data) / sample_rate
        time = np.linspace(0., duration, len(audio_data))
        nyquist = 0.5*sample_rate
        low = self.__fc_low/nyquist
        high = self.__fc_high/nyquist
        b, a = butter(self.__order,[low,high],btype='band')
        filtered_audio = filtfilt(b, a, audio_data)
        filtered_audio = filtered_audio / np.max(np.abs(filtered_audio))
        filtered_audio = (filtered_audio * 32767).astype(np.int16)
        wavfile.write(folder_path+audio_file, sample_rate, filtered_audio)


class FilterFactory():
        
    @staticmethod
    def build_filter(filter_type,folder_path: __name__,audio_file:__name__,sample:int):
        if filter_type == "band":
            filt = BandFilter()
            return filt.create_filter(folder_path,audio_file,sample)
        

