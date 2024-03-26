package com.example.voiceapp;


import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Date;

public class Logger {
    private static Logger instance;
    private static BufferedWriter logBuffer;

    private Logger(){
        try{
            FileWriter file = new FileWriter(
                    new File(MainActivity.getAppContext().getFilesDir().getAbsolutePath(),MainActivity.getAppContext().getString(R.string.Log)),true);
            logBuffer = new BufferedWriter(file);
        }catch (IOException e){
            e.printStackTrace();
        }
    }
    public static Logger getInstance(){
        if(instance == null){
            instance = new Logger();
            }

        return instance;
    }

    public static void addLog(String logMessage){
        try{
            logBuffer.write(new Date() + "." + logMessage);
            logBuffer.newLine();
            logBuffer.flush();
        }
        catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
    public static void closeLogger() {
        try {
            logBuffer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
