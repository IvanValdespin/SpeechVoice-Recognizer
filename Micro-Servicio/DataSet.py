import os
import numpy as np
from scipy.io import wavfile
from pathlib import Path
import tensorflow as tf
import librosa 
from sklearn.model_selection import train_test_split
from tensorflow import keras
import time




class DataSet():


    def __init__(self) -> None:
        self.audio_path = "audio"
        self.audio_paths = []
        self.labels = []
        self.__SEED = 5

    
    def get_classnames(self) -> __name__:
        return os.listdir(self.audio_path)
    
    def classify_dataset(self):
        
        class_names = self.get_classnames()

        for label, name in enumerate(class_names):
            direction_path = Path(self.audio_path) / name
            user_sample_paths = [os.path.join(direction_path,filepath) 
                                 for filepath in os.listdir(direction_path)
                                   if filepath.endswith(".wav")]
            self.audio_paths += user_sample_paths
            self.labels += [label] * len(user_sample_paths)

    def shuffle_dataset(self):

        data = np.random.RandomState(self.__SEED)
        data.shuffle(self.audio_paths)
        data = np.random.RandomState(self.__SEED)
        data.shuffle(self.labels)
    
    def read_audio(self,path):
        """Reads and decodes an audio file."""
        audio = tf.io.read_file(path)
        audio,sample_rate = tf.audio.decode_wav(audio, 1, 44100)
        return audio

    def create_dataset(self):

        v_audio_paths,t_audio_paths,v_labels,t_labels = train_test_split(self.audio_paths,self.labels, train_size=0.1)
        path_training_dataset = tf.data.Dataset.from_tensor_slices(t_audio_paths)
        audio_training_dataset= path_training_dataset.map(lambda x: self.read_audio(x))
        label__training_dataset = tf.data.Dataset.from_tensor_slices(t_labels)
        training_database = tf.data.Dataset.zip((audio_training_dataset,label__training_dataset))        
        training_database = training_database.shuffle(buffer_size = 128*8, seed = self.__SEED).batch(128)

        path_valid_dataset = tf.data.Dataset.from_tensor_slices(v_audio_paths)
        audio_valid_dataset= path_valid_dataset.map(lambda x: self.read_audio(x))
        label__valid_dataset = tf.data.Dataset.from_tensor_slices(v_labels)
        valid_database = tf.data.Dataset.zip((audio_valid_dataset,label__valid_dataset))
        valid_database = valid_database.shuffle(buffer_size = 32*8,seed = self.__SEED).batch(32)

        return training_database, valid_database

    def audio_to_fft(self,audio:__name__) :
    
        audio = tf.squeeze(audio, axis=-1)
        fft = tf.signal.fft(
            tf.cast(tf.complex(real=audio, imag=tf.zeros_like(audio)), tf.complex64)
        )
        fft = tf.expand_dims(fft, axis=-1)
        return tf.math.abs(fft[:, : (audio.shape[1] // 2)])
    

        






