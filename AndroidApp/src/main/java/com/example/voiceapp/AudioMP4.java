package com.example.voiceapp;

import android.media.MediaRecorder;
import android.widget.Toast;
import java.io.File;
import java.io.IOException;

public class AudioMP4 implements AudioRecorder{

    private final int sampling, bitRate, channel;
    private final String filename;
    private final MediaRecorder record;
    private final static String LOG_TAG = MainActivity.getAppContext().getString(R.string.LOG_AUDIOTEST);
    private final static String FILE_NOT_FOUND = MainActivity.getAppContext().getString(R.string.FILE_NOT_FOUND);
    private final static String DELETE_FILE_ERROR = MainActivity.getAppContext().getString(R.string.DELETE_FILE_ERROR);


    public AudioMP4(String filename){
        this.sampling = 44100;
        this.bitRate = 64000;
        this.channel = 1;
        this.record = new MediaRecorder();
        this.filename = filename + MainActivity.getAppContext().getString(R.string.audioFile_MP4);
        prepareRecord();
    }
    @Override
    public void prepareRecord() {
        this.record.setAudioChannels(this.channel);
        this.record.setAudioSource(MediaRecorder.AudioSource.VOICE_RECOGNITION);
        this.record.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4);
        this.record.setOutputFile(this.filename);
        this.record.setAudioEncoder(MediaRecorder.AudioEncoder.HE_AAC);
        this.record.setAudioSamplingRate(this.sampling);
        this.record.setAudioEncodingBitRate(this.bitRate);

        try{
            this.record.prepare();}
        catch (IOException e) {
            Logger.getInstance().addLog(LOG_TAG);}
    }


    @Override
    public void startRecord() {
        this.record.start();
    }

    @Override
    public void onRecord(boolean flag) {
        String recordMessage;
        if(flag){
            startRecord();
            recordMessage = MainActivity.getAppContext().getString(R.string.Record);
            Toast.makeText(MainActivity.getAppContext(),recordMessage,Toast.LENGTH_SHORT).show();
        }
        else {
            stopRecord();
            recordMessage = MainActivity.getAppContext().getString(R.string.Stop_recording);
            Toast.makeText(MainActivity.getAppContext(),recordMessage,Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public void stopRecord() {
        this.record.stop();
        this.record.release();
    }

    @Override
    public void deleteRecord() {
        File file = new File(this.filename);
        if (file.exists()){
            if(!file.delete()) Logger.getInstance().addLog(DELETE_FILE_ERROR);
        }
        else Logger.getInstance().addLog(FILE_NOT_FOUND);
    }
}
