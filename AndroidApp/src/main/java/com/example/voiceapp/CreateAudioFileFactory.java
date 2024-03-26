package com.example.voiceapp;

import java.util.Objects;

public class CreateAudioFileFactory {

    public static AudioRecorder createAudio(String format, String filename){

        if (Objects.equals(format, "mp3"))  return new AudioMP3(filename);

        else if (Objects.equals(format, "mp4")) return new AudioMP4(filename);

        return  null;
    }

}
