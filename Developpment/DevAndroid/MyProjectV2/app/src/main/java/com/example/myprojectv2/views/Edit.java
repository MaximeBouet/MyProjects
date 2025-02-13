package com.example.myprojectv2.views;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import android.annotation.SuppressLint;
import android.app.DatePickerDialog;
import android.app.TimePickerDialog;
import android.content.Intent;
import android.content.res.Resources;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.TimePicker;
import android.widget.Toast;

import com.example.myprojectv2.MainActivity;
import com.example.myprojectv2.R;
import com.example.myprojectv2.models.Rdv;
import com.example.myprojectv2.services.DatabaseHelper;
import com.example.myprojectv2.utils.Res;
import com.example.myprojectv2.views.widget.DatePickerFragment;
import com.example.myprojectv2.views.widget.TimePickerFragment;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;

/**
 * The Edit class represents the activity for editing an appointment (Rdv object).
 * It allows the user to edit and save the appointment's details including the
 * name, description, address, phone number, date, and time.
 * The class extends AppCompatActivity and implements the OnClickListener interface.
 *
 * @author Maxime Bouet, Sebastien Bois, Paul Monsigny.
 */
public class Edit extends AppCompatActivity implements View.OnClickListener{
    private EditText etDescription, etAddress, etPhoneNumber, etName,etDate,etTime;
    private int year,month,day;
    private int hours, minutes;
    private Toolbar toolbar;
    private DatabaseHelper db;
    private Rdv rdv;
    public Res res;

    /**
     * This method initializes the activity and its components
     * It sets the content view to activity_edit.xml layout file
     * It retrieves the appointment ID from the previous activity and retrieves the appointment from the database using the ID
     * It sets the appointment's details to the corresponding EditTexts
     * It initializes the toolbar and sets its title to the appointment's description
     * It sets up the onClick listeners for the save button, pick date button, and pick time button
     * It sets up a TextWatcher for the description EditText to dynamically update the toolbar title
     * It sets the background colors for the toolbar and pick date and pick time buttons
     */
    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_edit);

        Intent intent = getIntent();
        Long id = intent.getLongExtra("ID", 0);
        db = new DatabaseHelper(this);
        rdv = db.getRdv(id);

        toolbar = findViewById(R.id.toolbarEdit);
        toolbar.setTitleTextColor(getResources().getColor(R.color.white));
        setSupportActionBar(toolbar);
        getSupportActionBar().setTitle(rdv.getDescription());

        Button btnSave = findViewById(R.id.btnSave);
        Button btnPickDate = findViewById(R.id.btnPickDate);
        Button btnPickTime = findViewById(R.id.btnPickTime);

        btnSave.setOnClickListener(Edit.this);
        btnPickDate.setOnClickListener(this::pickDate);
        btnPickTime.setOnClickListener(this::pickTime);


        etDescription = findViewById(R.id.editTextDescription);
        etAddress = findViewById(R.id.editTextAddress);
        etPhoneNumber = findViewById(R.id.editTextPhoneNumber);
        etName = findViewById(R.id.editTextName);
        etDate = findViewById(R.id.etDate);
        etTime = findViewById(R.id.etTime);

        etDescription.setText(rdv.getDescription());
        etName.setText(rdv.getName());
        etDate.setText(rdv.getDate());
        etTime.setText(rdv.getTime());
        etAddress.setText(rdv.getAddress());
        etPhoneNumber.setText(rdv.getPhoneNumber());

        Toast.makeText(this, rdv.getDate(), Toast.LENGTH_LONG).show();

        etDescription.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {
                if (charSequence.length() != 0) {
                    getSupportActionBar().setTitle(charSequence);
                }
            }

            @Override
            public void afterTextChanged(Editable editable) {

            }
        });
        toolbar.setBackgroundColor(getResources().getColor(MainActivity.colorNumber));
        btnPickDate.setBackgroundColor(getResources().getColor(MainActivity.colorNumber));
        btnPickTime.setBackgroundColor(getResources().getColor(MainActivity.colorNumber));
    }

    /**
     * This method is called when the user clicks on a button in the activity.
     * It checks whether the EditText fields for the appointment's name, date, time, and description are filled,
     * and if so, updates the corresponding fields of the appointment object with the values entered by the user.
     * It then stores the updated appointment in the database, and starts a new activity to show the details of the updated appointment.
     * If any of the required fields are empty, it displays an error message on the corresponding EditText fields.
     *
     * @param view The View object that was clicked.
     */
    @Override
    public void onClick(View view) {
        Button v = (Button) view ;

        if (etDescription.getText().length() != 0 && etDate.getText().length() != 0 && etTime.getText().length() != 0 && etName.getText().length() != 0) {
            rdv.setDescription(etDescription.getText().toString());
            rdv.setName(etName.getText().toString());
            rdv.setDate(etDate.getText().toString());
            rdv.setTime(etTime.getText().toString());
            rdv.setAddress(etAddress.getText().toString());
            rdv.setPhoneNumber(etPhoneNumber.getText().toString());
            rdv.setState(checkState(etDate.getText().toString()));

            db.editRdv(rdv);

            Intent intent = new Intent(Edit.this, Details.class);
            intent.putExtra("id", rdv.getId());
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