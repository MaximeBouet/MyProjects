package com.example.myprojectv2.adapters;

import android.content.Context;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.myprojectv2.MainActivity;
import com.example.myprojectv2.R;
import com.example.myprojectv2.models.Rdv;

import java.util.ArrayList;
import java.util.List;

/**
 * RecyclerViewAdapter is an adapter for a RecyclerView that displays a list of Rdv objects.
 *
 * @author Maxime Bouet, Sebastien Bois, Paul Monsigny.
 */
public class RecyclerViewAdapter extends RecyclerView.Adapter<RecyclerViewAdapter.ViewHolder> {
    private final int recyclerItemRes;
    private static List<Rdv> rdvs;
    private final Context context;

    /**
     * Constructs a RecyclerViewAdapter with the specified layout resource ID, list of Rdv objects, and context.
     *
     * @param recyclerItemRes The layout resource ID for the RecyclerView items.
     * @param rdvs The list of Rdv objects to display in the RecyclerView.
     * @param context The context in which the RecyclerView is being displayed.
     */
    public RecyclerViewAdapter(int recyclerItemRes, ArrayList<Rdv> rdvs, Context context) {
        this.recyclerItemRes = recyclerItemRes;
        this.rdvs = rdvs;
        this.context = context;
    }

    /**
     * ViewHolder class for the RecyclerViewAdapter that holds references to the views in the RecyclerView item layout.
     */
    public static class ViewHolder extends RecyclerView.ViewHolder {
        private final TextView txtDescription;
        private final TextView txtDate;
        private final TextView txtTime;
        private final TextView txtName;
        private final TextView txtAddress;
        //private final TextView txtPhoneNumber;
        private final TextView txtState;
        int colorNumber;

        /**
         * Constructs a ViewHolder with the specified view.
         *
         * @param itemView The view for the RecyclerView item.
         */
        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            txtDescription = (TextView) itemView.findViewById(R.id.txtDescription);
            txtDate = (TextView) itemView.findViewById(R.id.txtDate);
            txtTime = (TextView) itemView.findViewById(R.id.txtTime);
            txtName = (TextView) itemView.findViewById(R.id.txtName);
            txtAddress = (TextView) itemView.findViewById(R.id.txtAdress);
            //txtPhoneNumber = (TextView) itemView.findViewById(R.id.txtPhoneNumber);
            txtState = (TextView) itemView.findViewById(R.id.txtState);
            itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    Intent intent = new Intent(view.getContext(), MainActivity.class);
                    intent.putExtra("id",rdvs.get(getAdapterPosition()).getId());
                    view.getContext().startActivity(intent);
                }
            });

        }

        /**
         * Binds an Rdv object to the views in the ViewHolder.
         *
         * @param rdv The Rdv object to bind.
         */
        void setRDV(Rdv rdv){
            txtDescription.setText(rdv.getDescription());
            txtDate.setText(rdv.getDate());
            txtTime.setText(rdv.getTime());
            txtName.setText(rdv.getName());
            txtState.setText(rdv.getState());
            if (rdv.getAddress().trim().isEmpty()){
                txtAddress.setVisibility(View.GONE);
            }
            else {
                txtAddress.setText(rdv.getAddress());
            }
        }

    }

    /**
     * Creates a new ViewHolder with the specified layout resource ID and returns it.
     *
     * @param parent The parent ViewGroup of the ViewHolder.
     * @param viewType The view type of the ViewHolder.
     *
     * @return The new ViewHolder.
     */
    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(recyclerItemRes,parent,false);
        return new ViewHolder(view);
    }

    /**
     * Binds an Rdv object to the ViewHolder at the specified position.
     *
     * @param holder The ViewHolder to bind the Rdv object to.
     * @param position the position of the Rdv object in the rdvs list
     */
    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        holder.setRDV(rdvs.get(position));
    }

    /**
     * This method returns the number of items in the rdvs list.
     *
     * @return the number of items in the rdvs list
     */
    @Override
    public int getItemCount() {
        if(rdvs!=null)
            return rdvs.size();
        else return 0;
    }

    /**
     * This method returns the view type of the item at the given position in the rdvs list.
     *
     * @param position the position of the item in the rdvs list
     *
     * @return the view type of the item
     */
    @Override
    public int getItemViewType(int position){
        return position;
    }

}



