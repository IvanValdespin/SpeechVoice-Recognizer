package com.example.voiceapp;

import android.util.Log;
import android.widget.TextView;
import androidx.annotation.NonNull;
import java.io.File;
import java.io.IOException;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.RequestBody;
import okhttp3.Response;

public class UserRequest implements Request{

    private final String filePath;
    private final File file;
    private final String url;
    private final OkHttpClient client;
    private RequestBody body;
    private final TextView text;
    private static final String CONNECTION_FAILURE = MainActivity.getAppContext().getString(R.string.CONNECTION_FAILURE);
    
    

    public UserRequest(String filePath, TextView text){
        this.url = MainActivity.getAppContext().getString(R.string.url_whisper);
        this.filePath = filePath;
        this.client = new OkHttpClient();
        this.text = text;
        this.file = createFile();
        prepareRequest();

    }
    @Override
    public void prepareRequest() {
        this.body = new MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("file",file.getName(),
                        RequestBody.create(MediaType.parse(MainActivity.getAppContext().getString(R.string.audioFile_MP3)),createFile()))
                .build();
    }

    @Override
    public void makeRequest() {
        okhttp3.Request request;

        request= new okhttp3.Request.Builder()
                .url(this.url)
                .post(this.body)
                .build();

        this.client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NonNull Call call, @NonNull IOException e) {
                Logger.getInstance().addLog(CONNECTION_FAILURE);
                e.printStackTrace();
                Text message = new Text(text);
                message.showMessage(MainActivity.getAppContext().getString(R.string.CONNECTION_FAILURE_MESSAGE));
            }

            @Override
            public void onResponse(@NonNull Call call, @NonNull Response response) throws IOException {
                if (response.isSuccessful()){
                    String responseData = response.body().string();
                    Text message = new Text(text);
                    message.showMessage(responseData);

                }
            }
        });
    }



    private File createFile(){
        return new File(this.filePath);
    }
}
