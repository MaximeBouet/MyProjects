package com.example.myprojectv2.views.widget;

import android.app.DatePickerDialog;
import android.app.Dialog;
import android.os.Bundle;

import androidx.fragment.app.DialogFragment;

/**
 * A dialog fragment that displays a date picker dialog and returns the selected date.
 *
 * @author Maxime Bouet, Sebastien Bois, Paul Monsigny.
 */
public class DatePickerFragment extends DialogFragment {
    private int year, month, day;
    DatePickerDialog.OnDateSetListener onDateSet;

    /**
     Empty constructor for the fragment.
     */
    public DatePickerFragment() {
    }

    /**
     * Sets the callback to be called when a date is selected.
     *
     * @param onDate the callback to be called
     */
    public void setCallBack(DatePickerDialog.OnDateSetListener onDate) {
        onDateSet = onDate;
    }

    /**
     * Sets the arguments for the fragment.
     *
     * @param args the arguments to be set
     */
    @Override
    public void setArguments(Bundle args) {
        super.setArguments(args);
        year = args.getInt("year");
        month = args.getInt("month");
        day = args.getInt("day");
    }

    /**
     * Creates a new instance of the date picker dialog.
     *
     * @param savedInstanceState the saved instance state
     *
     * @return a new date picker dialog
     */
    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState) {
        return new DatePickerDialog(getActivity(), onDateSet, year, month, day);
    }
}