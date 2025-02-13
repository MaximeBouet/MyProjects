package com.example.myprojectv2.views;

import android.content.Intent;
import android.content.res.Resources;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import com.example.myprojectv2.MainActivity;
import com.example.myprojectv2.R;
import com.example.myprojectv2.models.Rdv;
import com.example.myprojectv2.services.DatabaseHelper;
import com.example.myprojectv2.utils.Res;

/**
 * Details class shows the detailed information about a particular Rdv (Rendezvous) selected
 * from the Rdv list. It displays the name, date, time, description, address, phone number, and
 * state of the Rdv. Also, this class allows the user to edit, delete, open the location in the
 * maps, call, or share the Rdv with someone.
 *
 * @author Maxime Bouet, Sebastien Bois, Paul Monsigny.
 */
public class Details extends AppCompatActivity implements View.OnClickListener{
    private DatabaseHelper db;
    private Rdv rdv;
    private Intent intent;
    private Long id;
    public Res res;
    private Toolbar toolbar;


    /**
     * This method is called when the Details activity is created.
     * It sets the content view to activity_details and initializes the UI components.
     * The values of the TextViews in the UI components are set to the Rdv's values.
     * Also, the color of the Toolbar, Back button, Edit button, Delete button, Share button,
     * Call button, and Open Maps button is set to the color selected by the user.
     *
     * @param savedInstanceState It is a reference to a Bundle object that is passed into the
     *                             onCreate method of every Android Activity. It contains any
     *                             saved instance state information that the Activity may contain.
     */
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_details);

        toolbar = findViewById(R.id.toolbar3);

        ImageButton back =findViewById(R.id.btnBack);
        Button edit =findViewById(R.id.btnEdit);
        Button delete =findViewById(R.id.btnDelete);
        Button maps =findViewById(R.id.btnMaps);
        Button call =findViewById(R.id.btnCall);
        Button share =findViewById(R.id.btnShare);

        edit.setOnClickListener(Details.this);
        delete.setOnClickListener(Details.this);
        maps.setOnClickListener(Details.this);
        call.setOnClickListener(Details.this);
        share.setOnClickListener(Details.this);

        TextView descriptionTextView = findViewById(R.id.txtDescriptionDetails);
        TextView nameTextView = findViewById(R.id.txtNameDetails);
        TextView dateTextView = findViewById(R.id.txtDateDetails);
        TextView timeTextView = findViewById(R.id.txtTimeDetails);
        TextView addressTextView = findViewById(R.id.txtAddressDetails);
        TextView phoneNumberTextView = findViewById(R.id.txtPhoneNumberDetails);
        TextView stateTextView = findViewById(R.id.txtStateDetails);

        intent = getIntent();
        if (intent != null) {
            if (intent.hasExtra("id")) {
                id = intent.getLongExtra("id", 0);

                db = new DatabaseHelper(this);
                rdv = db.getRdv(id);

                Log.d("myTag", "This is my message");

                descriptionTextView.setText(rdv.getDescription());
                nameTextView.setText(rdv.getName());
                dateTextView.setText(rdv.getDate());
                timeTextView.setText(rdv.getTime());
                addressTextView.setText(rdv.getAddress());
                phoneNumberTextView.setText(rdv.getPhoneNumber());
                stateTextView.setText(rdv.getState());
            }
        }
        toolbar.setBackgroundColor(getResources().getColor(MainActivity.colorNumber));
        back.setBackgroundColor(getResources().getColor(MainActivity.colorNumber));
        delete.setBackgroundColor(getResources().getColor(MainActivity.colorNumber));
        edit.setBackgroundColor(getResources().getColor(MainActivity.colorNumber));
        share.setBackgroundColor(getResources().getColor(MainActivity.colorNumber));
        maps.setBackgroundColor(getResources().getColor(MainActivity.colorNumber));
        call.setBackgroundColor(getResources().getColor(MainActivity.colorNumber));
    }

    /**
     * Called when the user clicks on one of the buttons (Edit, Delete, Open Maps, Call, Share).
     * Based on the button's text, it navigates to a specific activity or performs a specific action.
     *
     * @param view The view that was clicked.
     */
    @Override
    public void onClick(View view) {
        Button v = (Button) view ;
        switch (v.getText().toString()) {
            case "Edit":
            case "Modifier":
                goEdit();
                break;
            case "Delete":
            case "Supprimer":
                goDelete();
                break;
            case "Open Maps":
            case "Ouvrir la carte":
                goMaps();
                break;

            case "Call":
            case "Appeler":
                goCall();
                break;
            case "Share":
            case "Partager":
                goShare();
                break;
        }
    }

    /**
     * Navigates back to the MainActivity and passes a string extra to indicate that the user came back from the Details activity.
     *
     * @param v The view that was clicked.
     */
    public void goBack(View v){
        Intent intentBack = new Intent(Details.this, MainActivity.class);
        intentBack.putExtra("BACK","come from back");
        startActivity(intentBack);
    }

    /**
     * Navigates to the Edit activity and passes the id of the current appointment to be edited.
     */
    public void goEdit(){
        Intent intentEdit = new Intent(Details.this, Edit.class);
        intentEdit.putExtra("ID",rdv.getId());
        startActivity(intentEdit);
    }

    /**
     * Deletes the current appointment, navigates back to the MainActivity, and displays a toast message to inform the user that the appointment has been deleted.
     */
    public void goDelete(){
        Intent intentBack = new Intent(Details.this, MainActivity.class);
        Toast.makeText(this,"You deleted a Rdv ",Toast.LENGTH_LONG).show();
        db.deleteRdv(rdv.getId());
        startActivity(intentBack);
    }

    /**
     * Opens Google Maps and shows the directions to the address of the current appointment.
     */
    public void goMaps(){
        if (rdv.getAddress().equals("")){
            Toast.makeText(Details.this,"Address is empty,",Toast.LENGTH_LONG).show();
        }else {
            Uri.Builder builder = new Uri.Builder();
            builder.scheme("https")
                    .authority("www.google.com")
                    .appendPath("maps")
                    .appendPath("dir")
                    .appendPath("")
                    .appendQueryParameter("api", "1")
                    .appendQueryParameter("destination", rdv.getAddress());
            String URL = builder.build().toString();
            Log.d("Directions", URL);
            Intent i = new Intent(android.content.Intent.ACTION_VIEW);
            i.setData(Uri.parse(URL));
            startActivity(i);
        }

    }

    /**
     * Initiates a phone call to the phone number of the current appointment.
     */
    public void goCall(){

        if (rdv.getPhoneNumber().equals("")){
            Toast.makeText(Details.this,"Phone number is empty,",Toast.LENGTH_LONG).show();
        }else {
            Intent intent = new Intent(Intent.ACTION_DIAL);
            intent.setData(Uri.parse("tel:"+rdv.getPhoneNumber()));
            startActivity(intent);
        }
    }

    /**
     * Shares the details of the current appointment with another user through an Intent that allows the user to choose how to share the information.
     */
    public void goShare(){
        String info = null;
        Intent sendIntent = new Intent();
        sendIntent.setAction(Intent.ACTION_SEND);

        if (rdv.getAddress().isEmpty() && rdv.getPhoneNumber().isEmpty()){
            info = ".";
        } else if (!rdv.getAddress().isEmpty() && rdv.getPhoneNumber().isEmpty()) {
            info = " at " + rdv.getAddress() + ".";
        } else if (rdv.getAddress().isEmpty() && !rdv.getPhoneNumber().isEmpty()){
            info = " and his number is : " + rdv.getPhoneNumber() + ".";
        }else info = " at " + rdv.getAddress() + " and his number is : " + rdv.getPhoneNumber() + ".";

        sendIntent.putExtra(Intent.EXTRA_TEXT, "I have a " + rdv.getDescription() + " with " + rdv.getName() + " on " + rdv.getDate() + "at " + rdv.getTime() + info);
        sendIntent.setType("text/plain");
        startActivity(sendIntent);
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
