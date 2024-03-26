import os
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow import keras
from DataSet import DataSet
import numpy as np
import time 

class Model():

    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    def __init__(self) -> None:
        self.BATCH_SIZE = 128
        self.EPOCHS = 100
        self.SHUFFLE_SEED = 43
        self.VALID_SPLIT = 0.1
        self.SAMPLING_RATE = 44100
        self.data = DataSet()
        self.class_names = os.listdir("audio")




    def residual_block(self,x, filters, conv_num=3, activation="relu"):
    # Shortcut
        s = keras.layers.Conv1D(filters, 1, padding="same")(x)
        for i in range(conv_num - 1):
            x = keras.layers.Conv1D(filters, 3, padding="same")(x)
            x = keras.layers.Activation(activation)(x)
        x = keras.layers.Conv1D(filters, 3, padding="same")(x)
        x = keras.layers.Add()([x, s])
        x = keras.layers.Activation(activation)(x)
        return keras.layers.MaxPool1D(pool_size=2, strides=2)(x)


    def build_model(self,input_shape, num_classes):
        inputs = keras.layers.Input(shape=input_shape, name="input")

        x = self.residual_block(inputs, 16, 2)
        x = self.residual_block(x, 32, 2)
        x = self.residual_block(x, 64, 3)
        x = self.residual_block(x, 128, 3)
        x = self.residual_block(x, 128, 3)

        x = keras.layers.AveragePooling1D(pool_size=3, strides=3)(x)
        x = keras.layers.Flatten()(x)
        x = keras.layers.Dense(256, activation="relu")(x)
        x = keras.layers.Dense(128, activation="relu")(x)

        outputs = keras.layers.Dense(num_classes, activation="softmax", name="output")(x)

        return keras.models.Model(inputs=inputs, outputs=outputs)
    
    def train_model(self):
        t1 = time.time()
        self.data.classify_dataset()
        self.data.shuffle_dataset()
        training_database, valid_database= self.data.create_dataset()
        training_database = training_database.map(lambda x, y: (self.data.audio_to_fft(x), y), num_parallel_calls=tf.data.AUTOTUNE)
        training_database = training_database.prefetch(tf.data.AUTOTUNE)

        valid_database = valid_database.map(lambda x, y: (self.data.audio_to_fft(x), y), num_parallel_calls=tf.data.AUTOTUNE)
        valid_database = valid_database.prefetch(tf.data.AUTOTUNE)


        model = self.build_model((self.SAMPLING_RATE // 2, 1), len(self.class_names))
        model.summary()

        model.compile(
            optimizer="Adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
        )

        model_save_filename = "model_test.h5"

        earlystopping_cb = keras.callbacks.EarlyStopping(
            monitor = 'val_accuracy',patience=20, restore_best_weights=True)
        mdlcheckpoint_cb = keras.callbacks.ModelCheckpoint(
            model_save_filename, monitor="val_accuracy", save_best_only=True)

        model.fit(
            training_database,
            epochs=self.EPOCHS,
            validation_data=valid_database,
            callbacks=[earlystopping_cb, mdlcheckpoint_cb],)
        t4 =time.time()
        print(model.evaluate(valid_database))
        print("Tiempo de entrenamiento: {}".format(t4-t1))

    
    def use_model(self,audiopath):
        audio = self.data.read_audio(audiopath)
        audio = tf.expand_dims(audio, axis = 0)
        audio = self.data.audio_to_fft(audio)
        model_path = "model_test.h5"
        model = tf.keras.models.load_model(model_path)

        prediction = model.predict(audio)
        print(max(prediction))
        prediction = np.argmax(prediction,axis=-1)
        if prediction[0] >= 0.90000:
            print(" Predicted: {}".format(self.class_names[prediction[0]]))
            return True
        else:
            return False


