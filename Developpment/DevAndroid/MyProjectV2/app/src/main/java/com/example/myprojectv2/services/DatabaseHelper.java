package com.example.myprojectv2.services;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.util.Log;

import com.example.myprojectv2.models.Rdv;

import java.util.ArrayList;

/**
 * DatabaseHelper class is responsible for managing the SQLite database for the RDV application.
 *
 * @author Maxime Bouet, Sebastien Bois, Paul Monsigny.
  */
public class DatabaseHelper extends SQLiteOpenHelper {
    private SQLiteDatabase database;

    // Table Name
    public static final String TABLE_NAME = "RDVS";
    // Table columns
    public static final String _ID = "id";
    public static final String DESCRIPTION = "dscription";
    public static final String NAME = "name";
    public static final String MDATE = "date";
    public static final String MTIME = "time";
    public static final String ADDRESS = "address";
    public static final String PHONENUMBER = "phonenumber";
    public static final String STATE = "state";
    // Database Information
    static final String DB_NAME = "Userdata.DB";
    // database version
    static final int DB_VERSION = 1;
    // Creating table query
    private static final String CREATE_TABLE = "CREATE TABLE " + TABLE_NAME + "(" + _ID
            + " INTEGER PRIMARY KEY AUTOINCREMENT, " + DESCRIPTION + " TEXT NOT NULL, " + NAME +
            " TEXT NOT NULL, " + MDATE + " TEXT NOT NULL, " + MTIME + " TEXT NOT NULL, " + ADDRESS + " TEXT NOT NULL, " + PHONENUMBER +
            " TEXT NOT NULL, " + STATE + " CHAR(250));";

    /**
     *  a new DatabaseHelper with the given context.
     *
     * @param context the context of the application.
     */
    public DatabaseHelper(Context context) {
        super(context, DB_NAME, null, DB_VERSION);
    }

    /**
     * Called when the database is created for the first time.
     *
     * @param db the SQLiteDatabase object.
     */
    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL(CREATE_TABLE);
    }

    /**
     * Called when the database needs to be upgraded.
     *
     * @param db the SQLiteDatabase object.
     * @param oldVersion the old version number of the database.
     * @param newVersion the new version number of the database.
     */
    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_NAME);
        onCreate(db);
    }

    /**
     * Adds a new RDV to the database.
     *
     * @param rdv the RDV object to be added.
     *
     * @return the ID of the new RDV.
     */
    public long addRdv(Rdv rdv){
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues c = new ContentValues();
        c.put(DESCRIPTION, rdv.getDescription());
        c.put(NAME, rdv.getName());
        c.put(MDATE, rdv.getDate());
        c.put(MTIME, rdv.getTime());
        c.put(ADDRESS, rdv.getAddress());
        c.put(PHONENUMBER, rdv.getPhoneNumber());
        c.put(STATE, rdv.getState());
        long ID = db.insert(TABLE_NAME,null,c);
        return ID;
    }

    /**
     * Retrieves a single appointment by its ID from the database table
     *
     * @param id the ID of the appointment to retrieve
     *
     * @return a Rdv object containing information about the retrieved appointment
     */
    public Rdv getRdv(long id){
        //sect * from dataBaseTable where id=1
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.query(TABLE_NAME,new String[]{_ID,DESCRIPTION,MDATE,MTIME,NAME,ADDRESS,PHONENUMBER,STATE},_ID+"=?", new String[]{String.valueOf(id)},null,null,null);
        if (cursor != null){
            cursor.moveToFirst();
        }
        return new Rdv(cursor.getLong(0),cursor.getString(1),cursor.getString(2),cursor.getString(3),cursor.getString(4), cursor.getString(5),cursor.getString(6),cursor.getString(7));
    }

    /**
     * Retrieves all appointments from the database table
     *
     * @return an ArrayList containing Rdv objects representing all appointments in the table
     */
    public ArrayList<Rdv> getRdvs(){
        SQLiteDatabase db = this.getReadableDatabase();
        ArrayList<Rdv> allRdvs = new ArrayList<>();

        String query = "SELECT * FROM "+TABLE_NAME;

        Cursor cursor = db.rawQuery(query,null);
        if (cursor.moveToFirst()){
            do {
                Rdv rdv = new Rdv();
                rdv.setId(cursor.getLong(0));
                rdv.setDescription(cursor.getString(1));
                rdv.setName(cursor.getString(2));
                rdv.setDate(cursor.getString(3));
                rdv.setTime(cursor.getString(4));
                rdv.setAddress(cursor.getString(5));
                rdv.setPhoneNumber(cursor.getString(6));
                rdv.setState(cursor.getString(7));
                allRdvs.add(rdv);
            }while (cursor.moveToNext());
        }
        return allRdvs;
    }

    /**
     * Updates an existing appointment in the database
     *
     * @param rdv the Rdv object representing the appointment to update
     *
     * @return the number of rows affected by the update operation
     */
    public int editRdv(Rdv rdv){
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues c = new ContentValues();
        c.put(DESCRIPTION,rdv.getDescription());
        c.put(NAME,rdv.getName());
        c.put(MDATE,rdv.getDate());
        c.put(MTIME,rdv.getTime());
        c.put(ADDRESS,rdv.getAddress());
        c.put(PHONENUMBER,rdv.getPhoneNumber());
        c.put(STATE,rdv.getState());
        return db.update(TABLE_NAME,c,_ID+"=?",new String[]{String.valueOf(rdv.getId())});
    }

    /**
     * Deletes a single appointment by its ID from the database table
     *
     * @param id the ID of the appointment to delete
     */
    public void deleteRdv(long id){
        SQLiteDatabase db = this.getWritableDatabase();
        db.delete(TABLE_NAME, _ID+"=?",new String[]{String.valueOf(id)});
        db.close();
    }

    /**
     * Deletes all appointments from the database table
     */
    public void deleteAllRdv(){
        SQLiteDatabase db = this.getWritableDatabase();
        db.delete(TABLE_NAME, null,null);
        db.close();
    }

    /**
     * Opens a connection to the database
     *
     * @throws SQLException if an error occurs while opening the connection
     */
    public void open() throws SQLException {
        database = this.getWritableDatabase();
    }

    /**
     * Closes the connection to the database
     */
    public void close() {
        database.close();
    }
}
