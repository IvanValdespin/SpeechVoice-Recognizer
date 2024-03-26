package com.example.voiceapp;

import android.content.Context;

public interface AudioRecorder {

    void prepareRecord();

    void startRecord();
    void onRecord(boolean flag);
    void stopRecord();
    void deleteRecord();

}
