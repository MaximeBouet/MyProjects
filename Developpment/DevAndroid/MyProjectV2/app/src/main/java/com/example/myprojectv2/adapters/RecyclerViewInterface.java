package com.example.myprojectv2.adapters;

/**
 * An interface that provides a method for handling item click events in a RecyclerView.
 *
 * @author Maxime Bouet, Sebastien Bois, Paul Monsigny.
 */
public interface RecyclerViewInterface {
    /**
     * Called when an item in the RecyclerView is clicked.
     *
     * @param position The position of the clicked item in the RecyclerView.
     */
    void onItemClick(int position);
}