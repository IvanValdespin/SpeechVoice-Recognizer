package com.example.voiceapp;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import android.Manifest;
import android.annotation.SuppressLint;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;

import java.util.Objects;

public class MainActivity extends AppCompatActivity {

    private static Context context;
    private WiFiConnection wifi;
    private AudioRecorder audiofile;
    private String audioFormat;
    private TextView text;
    private Text message;
    private String filename;
    private String filePath;
    private CountDownTimer timer;
    private boolean flag,newUser;
    private int count;
    Request request,newUserRequest;




    private static final int REQUEST_CODE_PERMISSIONS = 1;
    private static final String[] REQUIRED_PERMISSIONS = {
            Manifest.permission.ACCESS_WIFI_STATE,
            Manifest.permission.CHANGE_WIFI_STATE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE,
            Manifest.permission.RECORD_AUDIO,
            Manifest.permission.INTERNET,
            Manifest.permission.UPDATE_DEVICE_STATS,
            Manifest.permission.WAKE_LOCK
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        init();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.optionmenu,menu);
        return true;
    }

    @SuppressLint("NonConstantResourceId")
    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {

        int option = item.getItemId();

        switch (option){
            case R.id.sign_out:
                Logger.closeLogger();
                finish();
                return true;
            case R.id.new_user:
                this.newUser= true;
                count = 0;
                message.showMessage(getString(R.string.NewUser_Message));
                return true;
            case R.id.MP3:
                this.audioFormat = "mp3";
                return true;
            case R.id.MP4:
                this.audioFormat = "mp4";
                    return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }

    private void init() {

        if (!checkPermissions()) {
            ActivityCompat.requestPermissions(this, REQUIRED_PERMISSIONS, REQUEST_CODE_PERMISSIONS);
        }
        context = getApplicationContext();
        flag = false;
        this.newUser = false;
        count = 0;

        //wifi = new WiFiConnection(this.text);
        //wifi.connection();

        this.audioFormat = "mp3";
        this.filePath = getFilesDir().getAbsolutePath();
        this.filename = this.filePath +"/"+ getString(R.string.filename_request);

        text =findViewById(R.id.squaretext);
        String mess = getString(R.string.welcome_message);
        message = new Text(text);
        message.showMessage(mess);
    }

    private boolean checkPermissions() {
        for (String permission : REQUIRED_PERMISSIONS) {
            if (ActivityCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                return false;
            }
        }
        return true;
    }

    public static Context getAppContext(){
        return context;}

    public void makeRecord(int time, boolean newUser){

        int finalTime = time* 1000;
        flag = !flag;

        if(flag){
            audiofile = CreateAudioFileFactory.createAudio(this.audioFormat,this.filename);
            timer = new CountDownTimer(finalTime,200){
                @Override
                public void onTick(long l) {}

                @Override
                public void onFinish() {
                     flag = !flag;
                     audiofile.onRecord(flag);
                     if (!newUser) {
                         audiofile.deleteRecord();
                         message.showMessage(getString(R.string.timelimit));
                     }
                     else if (newUser && count == 0){
                         message.showMessage(getString(R.string.GetUserName));
                     }
                     else if (newUser && count > 1 && count < 9){
                         message.showMessage(getString(R.string.sample)+ (count - 2) +getString(R.string.sample1));
                     }
                     else if (newUser && count == 9){
                         message.showMessage(getString(R.string.finalSample));
                         newUserRequest = CreateRequestFactory.createRequest("newUser",filePath,text);
                         newUserRequest.makeRequest();
                     }
                }
            }.start();
        }

        if(!flag){
            timer.cancel();
            audiofile.onRecord(flag);
            if(!newUser){
                if(Objects.equals(this.audioFormat, "mp3")) {
                    request = CreateRequestFactory.createRequest("user",this.filename+getString(R.string.audioFile_MP3),text);
                } else request = CreateRequestFactory.createRequest("user",this.filename+getString(R.string.audioFile_MP4),text);
                request.makeRequest();
            }
            else if(newUser && count == 0){
                message.showMessage(getString(R.string.GetUserName));
            }

        } else{
        audiofile.onRecord(true);
        }
    }

    public void getRequest(View v){
        int time;


        if(this.newUser){
            if(count == 0){
                this.filename = filePath + "/" + getString(R.string.fileName_userName);
                time = 7;
                makeRecord(time,this.newUser);
                count = count + 1;}
            else if (count == 1){
                time = 7;
                makeRecord(time,this.newUser);
                message.showMessage(getString(R.string.GetUserName));
                count = count +1;
            }
            else if(count > 1 && count < 9){
                this.filename = filePath + "/" + getString(R.string.fileSample) + (count - 1);
                time = 2;
                makeRecord(time,this.newUser);
                count = count + 1;}
            else if(count == 9){
                this.newUser = false;
                time = 2;
                count = 0;
                this.filename = filePath + "/" + getString(R.string.fileSample) + (count - 1);
                makeRecord(time,this.newUser);
            }

        }
        else{

            this.filename =  this.filePath +"/"+ getString(R.string.filename_request);
            time = 7;
            makeRecord(time,this.newUser);
        }
    }


    public void readMessage(View v){
        message.readMessage();
    }

    public void makeBigger(View v){
        message.makeBigger();
    }

    public void makeSmaller(View v){
        message.makeSmaller();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        message.shutDown();
    }
}