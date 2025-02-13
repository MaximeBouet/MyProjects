package com.example.myprojectv2.views;

import android.annotation.SuppressLint;
import android.app.ListActivity;
import android.content.Intent;
import android.content.res.Resources;
import android.database.Cursor;
import android.os.Bundle;
import android.provider.ContactsContract;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.SimpleCursorAdapter;

import androidx.appcompat.widget.Toolbar;

import com.example.myprojectv2.MainActivity;
import com.example.myprojectv2.R;
import com.example.myprojectv2.utils.Res;

/**
 * The ContactList class displays a list of contacts from the device's address book.
 * When a contact is clicked, it launches an activity to create a new appointment
 * with the selected contact's name and phone number.
 *
 * @author Maxime Bouet, Sebastien Bois, Paul Monsigny.
 */
public class ContactList extends ListActivity{
    private ListView listView;
    private String name;
    private String number;
    public Res res;
    private Intent intent;
    private Toolbar toolbar;

    /**
     * Called when the activity is created. Sets up the ListView to display the list of contacts,
     * and sets an OnItemClickListener to handle clicks on individual contacts.
     *
     * @param savedInstanceState the saved state of the activity.
     */
    @SuppressLint({"MissingInflatedId", "CutPasteId"})
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_contact);
        listView = findViewById(android.R.id.list);

        toolbar = findViewById(R.id.toolbarContact);

        Cursor cursor = getContentResolver().query(ContactsContract.CommonDataKinds.Phone.CONTENT_URI,null,null,null,null);
        startManagingCursor(cursor);

        String[] from = {ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME,ContactsContract.CommonDataKinds.Phone.NUMBER,
                ContactsContract.CommonDataKinds.Phone._ID};

        int[] to = {android.R.id.text1,android.R.id.text2};

        ListAdapter adapter = new SimpleCursorAdapter(this, android.R.layout.simple_list_item_2,cursor,from,to);
        listView.setAdapter(adapter);
        listView.setChoiceMode(ListView.CHOICE_MODE_MULTIPLE);
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @SuppressLint("Range")
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                name = cursor.getString(cursor.getColumnIndex(ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME));
                number = cursor.getString(cursor.getColumnIndex(ContactsContract.CommonDataKinds.Phone.NUMBER));

                Intent intent = new Intent(ContactList.this, AddRdv.class);
                intent.putExtra("Name",name);
                intent.putExtra("Number",number);
                startActivity(intent);

            }
        });
        toolbar.setBackgroundColor(getResources().getColor(MainActivity.colorNumber));
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
