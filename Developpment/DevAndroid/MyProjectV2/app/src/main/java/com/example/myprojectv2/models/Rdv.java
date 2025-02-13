package com.example.myprojectv2.models;

import androidx.annotation.NonNull;

import java.io.Serializable;
import java.util.ArrayList;

/**
 * The Rdv class represents an appointment object, with various properties such as ID, description, date, time, name, address,
 * phone number and state. It can be used to store and manipulate appointment data.
 * @author Maxime Bouet, Sebastien Bois, Paul Monsigny.
 */
public class Rdv implements Serializable {
    public static ArrayList<Rdv> rdvArrayList = new ArrayList<>();
    private long ID;
    private String description;
    private String date;
    private String time;
    private String name;
    private String address;
    private String phoneNumber;
    private String state;

    /**
     * Constructs a new Rdv object with the specified properties.
     *
     * @param description The description of the Rdv.
     * @param date The date of the Rdv.
     * @param time The time of the Rdv.
     * @param name The name of the Rdv.
     * @param address The address of the Rdv.
     * @param phoneNumber The phone number associated with the Rdv.
     * @param state The state of the Rdv.
     */
    public Rdv(String description, String date, String time, String name, String address, String phoneNumber, String state) {
        this.description = description;
        this.date = date;
        this.time = time;
        this.name = name;
        this.address = address;
        this.phoneNumber = phoneNumber;
        this.state = state;
    }

    /**
     * Constructs a new Rdv object with the specified properties, including the ID.
     *
     * @param id The ID of the Rdv.
     * @param description The description of the Rdv.
     * @param date The date of the Rdv.
     * @param time The time of the Rdv.
     * @param name The name of the Rdv.
     * @param address The address of the Rdv.
     * @param phoneNumber The phone number associated with the Rdv.
     * @param state The state of the Rdv.
     */
    public Rdv(long id, String description, String date, String time, String name, String address, String phoneNumber, String state) {
        this.ID = id;
        this.description = description;
        this.date = date;
        this.time = time;
        this.name = name;
        this.address = address;
        this.phoneNumber = phoneNumber;
        this.state = state;
    }

    /**
     * Constructs a new, empty Rdv object.
     */
    public Rdv() {

    }

    /**
     * Returns the ID of the Rdv.
     *
     * @return The ID of the Rdv.
     */
    public long getId() {
        return ID;
    }

    /**
     * Returns the description of the Rdv.
     *
     * @return The description of the Rdv.
     */
    public String getDescription() {
        return description;
    }

    /**
     * Returns the date of the Rdv.
     *
     * @return The date of the Rdv.
     */
    public String getDate() {
        return date;
    }

    /**
     * Returns the time of the Rdv.
     *
     * @return The time of the Rdv.
     */
    public String getTime() {
        return time;
    }
    /**
     * Returns the name of the contact.
     * @return the name of the contact.
     */
    public String getName() {
        return name;
    }

    /**
     * Returns the address of the Rdv.
     *
     * @return the address of the Rdv.
     */
    public String getAddress() {
        return address;
    }

    /**
     * Returns the phone number of the Contact.
     *
     * @return the phone number of the Contact.
     */
    public String getPhoneNumber() {
        return phoneNumber;
    }

    /**
     * Returns the state of the Rdv.
     *
     * @return the state of the Rdv.
     */
    public String getState() {
        return state;
    }

    /**
     * Sets the ID of the Rdv.
     *
     * @param id the new ID for the Rdv.
     */
    public void setId(long id) {
        this.ID = id;
    }

    /**
     * Sets the description of the Rdv.
     *
     * @param description the new description for the Rdv.
     */
    public void setDescription(String description) {
        this.description = description;
    }

    /**
     * Sets the date of the Rdv.
     *
     * @param date the new date for the Rdv.
     */
    public void setDate(String date) {
        this.date = date;
    }

    /**
     * Sets the time of the Rdv.
     *
     * @param time the new time for the Rdv.
     */
    public void setTime(String time) {
        this.time = time;
    }

    /**
     * Sets the name of the Contact.
     *
     * @param name the new name for the Contact.
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * Sets the address of the Rdv.
     *
     * @param address the new address for the Rdv.
     */
    public void setAddress(String address) {
        this.address = address;
    }

    /**
     * Sets the phone number of the Contact.
     *
     * @param phoneNumber the new phone number for the Contact.
     */
    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    /**
     * Sets the state of the Rdv.
     *
     * @param state the new state for the Rdv.
     */
    public void setState(String state) {
        this.state = state;
    }

    /**
     * Returns a String representation of the Rdv object.
     *
     * @return a String representation of the Rdv object in the format of "description : date".
     */
    @NonNull
    @Override
    public String toString() {
        return description + " : " + date;
    }
}
