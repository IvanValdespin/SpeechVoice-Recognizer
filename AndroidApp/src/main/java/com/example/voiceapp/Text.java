package com.example.voiceapp;

import android.content.Context;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

public class Text {


    private TextView text;
    private Reader reader;

    public Text(TextView text){

        this.text = text;
        this.reader = new Reader(MainActivity.getAppContext());
        this.reader.init();
    }
    protected void showMessage(String message){
        this.text.setText(message);}

    protected void readMessage(){

        this.reader.initQueue( this.text.getText().toString());
    }
    protected void shutDown(){
        reader.shutDown();
    }

    protected void makeBigger(){
        float currentSize = text.getTextSize()/ MainActivity.getAppContext().getResources().getDisplayMetrics().scaledDensity;
        float nextSize = currentSize + 1;
        text.setTextSize(nextSize);

    }

    protected void makeSmaller(){
        float currentSize = text.getTextSize()/ MainActivity.getAppContext().getResources().getDisplayMetrics().scaledDensity;
        float nextSize = currentSize - 1;
        text.setTextSize(nextSize);}
}
