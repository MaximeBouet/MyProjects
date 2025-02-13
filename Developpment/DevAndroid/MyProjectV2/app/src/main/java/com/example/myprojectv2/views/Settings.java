package com.example.myprojectv2.views;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.res.Resources;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.CheckBox;
import android.widget.ImageButton;
import android.widget.Spinner;
import android.widget.Toast;
import androidx.appcompat.widget.Toolbar;

import com.example.myprojectv2.MainActivity;
import com.example.myprojectv2.R;
import com.example.myprojectv2.utils.Res;

/**
 * This class is used when the user want to access to the settings.
 * It allow the user to choose when he want to receive notifications,
 * Allow the user to choose the colo of the background,
 * Allow the user to choose if he want a music or not.
 *
 * @author Maxime Bouet, Sebastien Bois, Paul Monsigny.
 */
public class Settings extends AppCompatActivity{
    private Intent intent;
    private Boolean checkMusic;
    private Boolean originalMusicValue = false;
    private Boolean musicHasChanged = false;
    public Res res;
    public static String color = "Base_color",notification = "Off",music = "no";

    /** Description
     * This method is launched as soon as the user arrives at the activity.
     * It is used to display the buttons, information specified in the XML file.
     *
     * @param savedInstanceState Resumes the state of the activity where it was left
     *  */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        Toolbar toolbar = findViewById(R.id.toolbarSettings);

        Spinner notificationSpinner= (Spinner)findViewById(R.id.notificationSpinner);
        Spinner colorSpinner= (Spinner)findViewById(R.id.colorSpinner);
        CheckBox checkBoxYes = findViewById(R.id.checkBoxMusiqueYes);

        ArrayAdapter<CharSequence> notificationAdapter = ArrayAdapter.createFromResource(this,R.array.notification_array,android.R.layout.simple_spinner_item);
        ArrayAdapter<CharSequence> colorAdapter = ArrayAdapter.createFromResource(this,R.array.color_array,android.R.layout.simple_spinner_item);

        notificationAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        notificationSpinner.setAdapter(notificationAdapter);

        colorAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        colorSpinner.setAdapter(colorAdapter);

        //allow to check or not the box at the creation
        if (music.equals("yes")) checkMusic = true;
        else checkMusic = false;
        checkBoxYes.setChecked(checkMusic);
        notificationSpinner.setSelection(notificationAdapter.getPosition(notification));
        colorSpinner.setSelection(colorAdapter.getPosition(color));
        toolbar.setBackgroundColor(getResources().getColor(MainActivity.colorNumber));

        //We check if the user change the state of the checkbox
        originalMusicValue = checkBoxYes.isChecked();
        if (originalMusicValue) music = "yes";

        ImageButton imageButtonBack = findViewById(R.id.imageButtonBack);
        imageButtonBack.setBackgroundColor(getResources().getColor(MainActivity.colorNumber));
        imageButtonBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //get the value that the user selected on the color/notification spinner
                notification = notificationSpinner.getSelectedItem().toString();
                color = colorSpinner.getSelectedItem().toString();
                //get the value of the checkBox
                if(checkBoxYes.isChecked()){
                    music = "yes";
                }else {
                    music = "no";
                }

                Toast.makeText(Settings.this,"Settings saved",Toast.LENGTH_LONG).show();
                Intent intent = new Intent(Settings.this,MainActivity.class);

                //allow us to know if we have to start, stop the music (or nothing)
                if (music.equals("no") && !originalMusicValue){
                    musicHasChanged = false;
                }else if (music.equals("yes") && !originalMusicValue){
                    musicHasChanged = true;
                } else if (music.equals("no") && originalMusicValue) {
                    musicHasChanged = true;
                }else {
                    musicHasChanged = false;
                }
                intent.putExtra("musicHasChanged",musicHasChanged);

                startActivity(intent);
            }
        });
    }

    /** Description
     * This method is launched as soon as the user arrives at the activity.
     * It is used to display the buttons, information specified in the XML file.
     *
     * @param v Allow to identify the component with which the user interacted
     *  */
    public void onClickCheckBox(View v){
        CheckBox yes = (CheckBox)findViewById(R.id.checkBoxMusiqueYes);
        //We check if it is checked
        if (yes.isChecked())
            music = "yes";
        else {
            music = "no";
        }
    }

    /**
     * Overrides the getResources() method of the Context class to return a custom Resources object.
     * If the custom Resources object is not initialized, it initializes it with a new Res object that wraps the
     * original Resources object. The custom Resources object allows for the use of different resources depending on the
     * user's locale and enables easy switching between different locales.
     * Allow to set the right background color thanks to the Res class
     *
     * @return A custom Resources object that wraps the original Resources object and allows for the use of
     *         different resources depending on the user's locale.
     */
    @Override public Resources getResources() {
        if (res == null) {
            res = new Res(super.getResources());
        }
        return res;
    }

}