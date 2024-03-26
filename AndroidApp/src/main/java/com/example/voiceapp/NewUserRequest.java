package com.example.voiceapp;

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

public class NewUserRequest implements Request{
    private final String filePath;
    private final String url;
    private final OkHttpClient client;
    private MultipartBody.Builder buldier;
    private final TextView text;
    private static final String CONNECTION_FAILURE = MainActivity.getAppContext().getString(R.string.CONNECTION_FAILURE);




    public NewUserRequest(String filePath, TextView text){
        this.url = MainActivity.getAppContext().getString(R.string.url_NewUser);
        this.filePath = filePath;
        this.client = new OkHttpClient();
        this.text = text;
        prepareRequest();

    }
    @Override
    public void prepareRequest() {
        String filename;
        File file;

        this.buldier = new MultipartBody.Builder()
                .setType(MultipartBody.FORM);

        for (int i = 0; i <= 7; i++) {

            if (i == 0) filename = this.filePath + "/" + MainActivity.getAppContext().getString(R.string.fileName_userName)+".mp3";
            else filename = this.filePath + "/" + MainActivity.getAppContext().getString(R.string.fileSample) + i + ".mp3";
            file = createFiles(filename);
            RequestBody  body = RequestBody.create(
                    MediaType.parse("audio/*"), file);
            this.buldier.addFormDataPart("archivos", file.getName(), body);
        }
    }

    @Override
    public void makeRequest() {
        RequestBody requestBody = this.buldier.build();
        okhttp3.Request request;

        request= new okhttp3.Request.Builder()
                .url(this.url)
                .post(requestBody)
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
    private File createFiles(String filename){
        return new File(filename);
    }
}
