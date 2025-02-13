package com.example.myprojectv2.services;

import android.app.Service;
import android.content.Intent;
import android.media.MediaPlayer;
import android.os.IBinder;
import android.util.Log;

import androidx.annotation.Nullable;

import com.example.myprojectv2.R;

import java.util.ServiceConfigurationError;

/**
 * BackgroundMusic is a service class for playing background music in the application
 *
 * @author Maxime Bouet, Sebastien Bois, Paul Monsigny.
 */
public class BackgroundMusic extends Service {
    /*
    The MediaPlayer object to play the background music.
    */
    private MediaPlayer mediaPlayer;

    /**
     * Called when the service is first created.
     */
    @Override
    public void onCreate() {
        super.onCreate();
        Log.d("mylog", "On Create Service Music");
    }

    /**
     * This method must be implemented but is not used in this service.
     *
     * @param intent The intent that was used to bind to this service.
     *
     * @return Always returns null.
     */
    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    /**
     * Called when the service is started.
     * Initializes the MediaPlayer and starts playing the background music.
     *
     * @param intent The intent that started this service.
     * @param flags Additional data about this start request.
     * @param startId A unique integer representing this specific request to start.
     *
     * @return Returns super.onStartCommand(intent, flags, startId).
     */
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.d("mylog", "Starting playing");
        mediaPlayer = MediaPlayer.create(this, R.raw.backgroundsound);
        mediaPlayer.setLooping(true);
        mediaPlayer.start();
        return super.onStartCommand(intent, flags, startId);
    }

    /**
     * Called when the service is stopped.
     *
     * @param name The intent that was used to bind to this service.
     *
     * @return Returns super.stopService(name).
     */
    @Override
    public boolean stopService(Intent name) {
        Log.d("mylog", "Stoping playing");
        return super.stopService(name);
    }

    /**
     * Called when the service is destroyed.
     * Stops and releases the MediaPlayer object.
     */
    @Override
    public void onDestroy() {
        super.onDestroy();
        mediaPlayer.stop();
        mediaPlayer.release();
        mediaPlayer = null;

    }
}
