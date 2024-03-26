import os
import wave 
from pydub import AudioSegment
import math
from Filter import FilterFactory



class AudioFile():

    def __init__(self) -> None:
        self.counter = 0
    
    def createWavFile(self,audio_data_array,output_file):

        with wave.open(output_file, 'wb') as wf:
            wf.setnchannels(1)  # 1 channel
            wf.setsampwidth(2)  # Number of bytes per sample
            wf.setframerate(16000)  # Sample rate
            wf.writeframes(audio_data_array.tobytes())
    
        FilterFactory.build_filter("band","",output_file,1)

    def saveFile(self, file: __name__, folder_path: __name__, flag:bool) -> __name__:
        
        self.counter = 1
        path = "request/"
        file_path = os.path.join(folder_path, file.filename)
        file.save(file_path)
        audio = AudioSegment.from_file(file_path)
        os.remove(file_path)

        if(flag == True):
            filename = f"request"+str(self.counter) + ".wav"
            file_path = os.path.join(path,filename)
            
            while  os.path.exists(file_path) == True:
                self.counter +=1
                filename = f"request"+str(self.counter) + ".wav"
                file_path = os.path.join(path,filename)

            audio.export(file_path, format="wav")  
            FilterFactory.build_filter("band",path,filename,self.counter)     

        return file_path

    def saveFiles(self,files: __name__ , folder_path: __name__ ) -> None:    
        self.counter = 0
        for archivo in files:
            
            file_path = os.path.join(folder_path, archivo.filename)
            archivo.save(file_path)
            audio = AudioSegment.from_file(file_path)

            if self.counter == 0:
                filename = f'/name.wav'
            else:
                filename = f'/sample_{self.counter}.wav'

            audio.export(folder_path + filename, format="wav")
            FilterFactory.build_filter("band",folder_path,filename,self.counter)

            os.remove(file_path);
            self.counter += 1

    def fileSegmentation(self,folder_path:__name__) -> None:
        
        __segmentation_time = 1 # Time in seconds that a file is going to be cut off.
        self.counter = 0

        filenames = os.listdir(folder_path)
        

        for file in filenames:
            self.counter += 1
            segment = AudioSegment.from_file(folder_path + "/" + file)
            batch_size = __segmentation_time * 1000
            duration = segment.duration_seconds
            batches = math.ceil(duration / __segmentation_time)

            inicio = 0
            j = 0;

            for i in range(batches):
                j = batches*(self.counter - 1) + i
                muestra = segment[inicio: inicio + batch_size]
                filename = f'/subsample_{j}.wav'
                muestra.export(folder_path+filename, format='wav') 
                inicio+= batch_size
    


