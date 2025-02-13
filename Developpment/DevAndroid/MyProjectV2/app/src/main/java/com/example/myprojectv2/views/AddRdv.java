package com.example.myprojectv2.views;

import android.annotation.SuppressLint;
import android.app.DatePickerDialog;
import android.app.TimePickerDialog;
import android.content.Intent;
import android.content.res.Resources;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.TimePicker;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import com.example.myprojectv2.views.widget.DatePickerFragment;
import com.example.myprojectv2.MainActivity;
import com.example.myprojectv2.R;
import com.example.myprojectv2.views.widget.TimePickerFragment;
import com.example.myprojectv2.models.Rdv;
import com.example.myprojectv2.services.DatabaseHelper;
import com.example.myprojectv2.utils.Res;

import java.text.DateFormat;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Calendar;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

/**
 * Activity for adding a new RDV (Rendez-vous).
 *
 * @author Maxime Bouet, Sebastien Bois, Paul Monsigny.
 */
public class AddRdv extends AppCompatActivity implements View.OnClickListener{
    private EditText etDescription, etAddress, etPhoneNumber, etName;
    private int year,month,day;
    private int hours, minutes;
    private Button btnPickDate;
    private EditText etDate;
    private Button btnPickTime;
    private EditText etTime;
    private Button btnSave,btnContact;
    private Toolbar toolbar;
    private Intent intent;
    private String contactNameRecup,contactNumberRecup;
    public Res res;

    /**
     * Initializes the activity layout and its components.
     *
     * @param savedInstanceState A Bundle object containing the activity's previously saved state.
     */
    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_rdv);

        toolbar = findViewById(R.id.toolbar4);
        setSupportActionBar(toolbar);
        getSupportActionBar().setTitle("New RDV");

        Log.d("Test","onCreate");

        etDescription = findViewById(R.id.editTextDescription);
        etAddress = findViewById(R.id.editTextAddress);
        etPhoneNumber = findViewById(R.id.editTextPhoneNumber);
        etName = findViewById(R.id.editTextName);
        btnPickDate= findViewById(R.id.btnPickDate);
        etDate= findViewById(R.id.etDate);

        btnPickDate.setOnClickListener(this::pickDate);
        btnPickTime= findViewById(R.id.btnPickTime);
        etTime= findViewById(R.id.etTime);
        btnPickTime.setOnClickListener(this::pickTime);
        btnSave= findViewById(R.id.btnSave);
        btnContact = findViewById(R.id.btnContact);
        btnSave.setOnClickListener(AddRdv.this);
        btnContact.setOnClickListener(AddRdv.this);

        etDescription.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {
                if (charSequence.length() != 0){
                    getSupportActionBar().setTitle(charSequence);
                }
            }

            @Override
            public void afterTextChanged(Editable editable) {

            }
        });
        intent = getIntent();
        if (intent != null) {
            if (intent.hasExtra("Name")) {
                contactNameRecup = intent.getStringExtra("Name");
                contactNumberRecup = intent.getStringExtra("Number");

                etName.setText(contactNameRecup);
                etPhoneNumber.setText(contactNumberRecup);
            }
        }

        toolbar.setBackgroundColor(getResources().getColor(MainActivity.colorNumber));
        toolbar.setBackgroundColor(getResources().getColor(MainActivity.colorNumber));
        btnPickDate.setBackgroundColor(getResources().getColor(MainActivity.colorNumber));
        btnPickTime.setBackgroundColor(getResources().getColor(MainActivity.colorNumber));
        btnContact.setBackgroundColor(getResources().getColor(MainActivity.colorNumber));
    }

    /**
     * Handles clicks on the activity's buttons.
     *
     * @param view The view that was clicked.
     */
    @Override
    public void onClick(View view) {
        Button v = (Button) view ;
        switch (v.getText().toString()) {
            case "Sauvegarder":
            case "Save":
                if (etDescription.getText().length() != 0 && etDate.getText().length() != 0 && etTime.getText().length() != 0 && etName.getText().length() != 0) {
                    String description = String.valueOf(etDescription.getText());
                    String address = String.valueOf(etAddress.getText());
                    String name = String.valueOf(etName.getText());
                    String phoneNumber = String.valueOf(etPhoneNumber.getText());
                    String date = String.valueOf(etDate.getText());
                    String time = String.valueOf(etTime.getText());
                    String state = checkState(date);

                    Rdv rdv = new Rdv(description, date, time, name, address, phoneNumber, state);
                    DatabaseHelper db = new DatabaseHelper(this);
                    db.addRdv(rdv);

                    Intent intent = new Intent(AddRdv.this, MainActivity.class);
                    Toast.makeText(this, "You saved a Rdv ", Toast.LENGTH_LONG).show();
                    startActivity(intent);
                } else {
                    if (etDescription.getText().length() == 0) {
                        etDescription.setError("Description can not be Blank");
                    } else if (etDate.getText().length() == 0) {
                        etDate.setError("Date can not be Blank");
                    } else if (etTime.getText().length() == 0) {
                        etTime.setError("Time can not be Blank");
                    } else if (etName.getText().length() == 0) {
                        etName.setError("Name can not be Blank");
                    }
                }
                break;
            case "Liste de contacts":
            case "Contact list":
                Intent intent = new Intent(AddRdv.this, ContactList.class);
                startActivity(intent);
                break;
        }

    }

    /**
     * Method to show the date picker dialog
     *
     * @param view the view that calls this method
     */
    public void pickDate(View view){
        showDatePicker();
    }

    /**
     * Method to show the time picker dialog
     *
     * @param view the view that calls this method
     */
    public void pickTime(View view){
        showTimePicker();
    }

    /**
     * Listener for the date picker dialog, updates the text in the date EditText field
     */
    DatePickerDialog.OnDateSetListener onDate = new DatePickerDialog.OnDateSetListener() {
        @Override
        public void onDateSet(DatePicker view, int selectedYear, int selectedMonth, int selectedDay)
        {
            year = selectedYear;
            month = selectedMonth;
            day = selectedDay;
            etDate.setText(new StringBuilder().append(month +1).
                    append("/").append(day).append("/").append(year).append(" "));
        }
    };

    /**
     * Listener for the time picker dialog, updates the text in the time EditText field
     */
    TimePickerDialog.OnTimeSetListener onTime = new TimePickerDialog.OnTimeSetListener() {
        @Override
        public void onTimeSet(TimePicker view, int hour, int minute) {
            hours = hour;
            minutes = minute;

            etTime.setText(new StringBuilder().append(hours).append(":").append(minutes));
        }
    };

    /**
     * Method to show the date picker dialog
     */
    private void showDatePicker() {
        DatePickerFragment date= new DatePickerFragment();
        final Calendar c = Calendar.getInstance();
        year = c.get(Calendar.YEAR);
        month = c.get(Calendar.MONTH);
        day = c.get(Calendar.DAY_OF_MONTH);
        Bundle args = new Bundle();
        args.putInt("year",year);
        args.putInt("month",month);
        args.putInt("day",day);
        date.setArguments(args);
        date.setCallBack(onDate);
        date.show(getSupportFragmentManager(),"Date Picker");
    }

    /**
     * Method to show the time picker dialog
     */
    private void showTimePicker() {
        TimePickerFragment time= new TimePickerFragment();
        final Calendar c = Calendar.getInstance();
        int hours = c.get(Calendar.HOUR_OF_DAY);
        int minutes = c.get(Calendar.MINUTE);
        Bundle args = new Bundle();
        args.putInt("hours",hours);
        args.putInt("minutes",minutes);
        time.setArguments(args);
        time.setCallBack(onTime);
        time.show(getSupportFragmentManager(),"Time Picker");
    }

    /**
     * Method to check the state of the appointment
     *
     * @param state the current state of the appointment
     *
     * @return the updated state of the appointment
     */
    @SuppressLint("ResourceType")
    private String checkState(String state){
        String temp;
        Date aujourdhui = new Date();
        DateFormat shortDateFormat = DateFormat.getDateInstance(DateFormat.SHORT, Locale.ENGLISH);
        if (shortDateFormat instanceof SimpleDateFormat) {
            SimpleDateFormat sdf = (SimpleDateFormat) shortDateFormat;
            // To show Locale specific short date expression with full year
            String pattern = sdf.toPattern().replaceAll("y+", "yyyy");
            sdf.applyPattern(pattern);
            temp = sdf.format(aujourdhui) + " ";
        }
        else{
            temp = shortDateFormat.format(aujourdhui)+ " ";
        }

        String[] splitDate = etDate.getText().toString().split("/");
        String parse = "";
        if (splitDate[1].length() == 2){
            parse = "M/dd/yyyy ";
        } else if (splitDate[1].length() == 1) {
            parse = "M/d/yyyy ";
        } else if (splitDate[0].length() == 2) {
            parse = "MM/d/yyyy ";
        } else if (splitDate[0].length() == 1) {
            parse = "M/d/yyyy ";
        }

        DateTimeFormatter f = DateTimeFormatter.ofPattern( parse );

        LocalDate start = LocalDate.parse( temp , f ) ;
        LocalDate stop = LocalDate.parse( etDate.getText().toString() , f ) ;
        boolean isBefore = start.isBefore( stop ) ;

        if (temp.equals(etDate.getText().toString())){
            state = getString(R.string.stateToday);
        } else if (isBefore) {
            state = getString(R.string.stateNotToday);
        } else {
            state = getString(R.string.statePassed);
        }
        return state;
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
