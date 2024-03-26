package com.example.voiceapp;

import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.wifi.WifiManager;
import android.util.Log;
import android.widget.TextView;

public class WiFiConnection {
    private ConnectivityManager chekconnection;
    private NetworkInfo activeNetwork;
    WifiManager wifi;
    private final TextView text;

    public WiFiConnection(TextView text){
        this.text = text;
        this.chekconnection = (ConnectivityManager)MainActivity.getAppContext().getSystemService(MainActivity.getAppContext().CONNECTIVITY_SERVICE);
        this.activeNetwork = chekconnection.getActiveNetworkInfo();
        this.wifi = (WifiManager)MainActivity.getAppContext().getSystemService(Context.WIFI_SERVICE);
    }

    public void connection() {
        Text message = new Text(this.text);

        if(wifi == null){
            Log.e("ENTRO WIFI","ENTRO");
            message.showMessage(MainActivity.getAppContext().getString(R.string.Wifi_connection));
        }

    }

}
