package com.example.voiceapp;

import android.content.Context;
import android.speech.tts.TextToSpeech;
import android.util.Log;

import java.util.Locale;

public class Reader {
    private String language, country;

    private boolean isloaded;
    private TextToSpeech tts;
    private Context context;

    private final static String LANGUAGE_FAIL = MainActivity.getAppContext().getString(R.string.LANGUAGE_FAIL);
    private final static  String TTS = MainActivity.getAppContext().getString(R.string.TTS);
    private final static  String TTS_FAIL = MainActivity.getAppContext().getString(R.string.TSS_FAIL);
    public Reader(Context context){
        this.language = MainActivity.getAppContext().getString(R.string.Language);
        this.country = MainActivity.getAppContext().getString(R.string.Country);
        this.tts = null;
        this.isloaded = false;
        this.context = context;

    }
    public void init(){
        try{

            tts = new TextToSpeech(this.context, new TextToSpeech.OnInitListener() {
                @Override
                public void onInit(int status) {

                    if (status == TextToSpeech.SUCCESS) {
                        Locale Laguage = new Locale(language, country);
                        int result = tts.setLanguage(Laguage);
                        isloaded =true;

                        if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                            Logger.getInstance().addLog(LANGUAGE_FAIL);
                        }
                    } else {
                        Logger.getInstance().addLog(TTS);}
                }
            });
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    public void initQueue(String text){

        if(this.isloaded){
            tts.speak(text,TextToSpeech.QUEUE_FLUSH,null);
        }else{
            Logger.getInstance().addLog(TTS_FAIL);
        }
    }
   public void shutDown(){
        tts.shutdown();
    }

}
