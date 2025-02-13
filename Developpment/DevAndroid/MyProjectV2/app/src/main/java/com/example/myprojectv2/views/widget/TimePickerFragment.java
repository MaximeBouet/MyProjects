package com.example.myprojectv2.views.widget;

import android.app.Dialog;
import android.app.TimePickerDialog;
import android.os.Bundle;

import androidx.fragment.app.DialogFragment;

/**
 * A DialogFragment used to display a time picker dialog that allows the user to select a time.
 * It implements the TimePickerDialog.OnTimeSetListener interface which allows it to return the selected time to the calling activity.
 *
 * @author Maxime Bouet, Sebastien Bois, Paul Monsigny.
 */
public class TimePickerFragment extends DialogFragment {
    private int hours, minutes;
    TimePickerDialog.OnTimeSetListener onTimeSet;

    /**
     * Default constructor for the TimePickerFragment.
     */
    public TimePickerFragment() {

    }

    /**
     * Sets the OnTimeSetListener to be called when the user selects a time.
     *
     * @param onTime the OnTimeSetListener to be set.
     */
    public void setCallBack(TimePickerDialog.OnTimeSetListener onTime) {
        onTimeSet = onTime;
    }

    /**
     * Retrieves the arguments passed to the fragment and sets the hours and minutes.
     *
     * @param args the arguments passed to the fragment.
     */
    @Override
    public void setArguments(Bundle args) {
        super.setArguments(args);
        hours = args.getInt("hours");
        minutes = args.getInt("minutes");
    }

    /**
     * Creates and returns a new TimePickerDialog with the specified time.
     *
     * @param savedInstanceState the saved instance state of the fragment.
     *
     * @return a new TimePickerDialog.
     */
    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState){
        return new TimePickerDialog(getActivity(),onTimeSet, hours, minutes,true);
    }
}
