package com.example.voiceapp;

import android.widget.TextView;
import java.util.Objects;

public class CreateRequestFactory {
    
    public static Request createRequest(String format, String filename, TextView text){

        if (Objects.equals(format, "user")) return new UserRequest(filename,text);

        else if (Objects.equals(format, "newUser")) return new NewUserRequest(filename,text);

        return  null;
    }
}
