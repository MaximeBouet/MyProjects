package com.example.myprojectv2.adapters;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.example.myprojectv2.R;
import com.example.myprojectv2.models.Rdv;

import java.util.List;

/**
 * This class represents an ArrayAdapter for the Rdv objects.
 *
 * @author Maxime Bouet, Sebastien Bois, Paul Monsigny.
 */
public class RdvAdapter extends ArrayAdapter<Rdv>
{
    /**
     * Constructor for the RdvAdapter.
     *
     * @param context the context of the adapter
     * @param rdvs the list of Rdv objects to be displayed in the adapter
     */
    public RdvAdapter(Context context, List<Rdv> rdvs)
    {
        super(context, 0,rdvs);
    }

    /**
     * This method is called to get a View object that displays the data at the specified position in the data set.
     *
     * @param position the position of the item within the adapter's data set
     * @param convertView the old view to reuse, if possible
     * @param parent the parent that this view will eventually be attached to
     *
     * @return the View object that displays the data at the specified position
     */
    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent)
    {
        Rdv rdv = getItem(position);
        if(convertView == null)
            convertView = LayoutInflater.from(getContext()).inflate(R.layout.activity_main, parent, false);
        TextView desc = convertView.findViewById(R.id.txtDescription);
        TextView date = convertView.findViewById(R.id.txtDate);
        TextView time = convertView.findViewById(R.id.txtTime);
        TextView name = convertView.findViewById(R.id.txtName);
        TextView address = convertView.findViewById(R.id.txtAdress);
        //TextView phoneNumber = convertView.findViewById(R.id.txtPhoneNumber);
        TextView state = convertView.findViewById(R.id.txtState);
        return convertView;
    }
}
