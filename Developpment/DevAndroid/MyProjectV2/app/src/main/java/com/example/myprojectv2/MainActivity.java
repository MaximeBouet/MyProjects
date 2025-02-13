package com.example.myprojectv2;

import android.annotation.SuppressLint;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.res.Resources;
import android.os.Build;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;

import android.view.View;

import androidx.core.app.ActivityCompat;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;
import androidx.core.content.ContextCompat;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.view.Menu;
import android.view.MenuItem;
import android.widget.TextView;
import android.widget.Toast;

import com.example.myprojectv2.adapters.RecyclerViewAdapter;
import com.example.myprojectv2.databinding.ActivityMainBinding;
import com.example.myprojectv2.models.Rdv;
import com.example.myprojectv2.services.BackgroundMusic;
import com.example.myprojectv2.services.DatabaseHelper;
import com.example.myprojectv2.utils.Res;
import com.example.myprojectv2.views.AddRdv;
import com.example.myprojectv2.views.Details;
import com.example.myprojectv2.views.Settings;

import java.util.ArrayList;

/**
 * The MainActivity class represents the main activity of the application.
 * It displays a list of appointments and provides an interface to add, remove and modify appointments.
 * The class also provides access to the settings activity and the details activity.
 *
 * @author Maxime Bouet, Sebastien Bois, Paul Monsigny.
 */
public class MainActivity extends AppCompatActivity {
    private AppBarConfiguration appBarConfiguration;
    private ActivityMainBinding binding;
    private DatabaseHelper DB;
    private RecyclerView recyclerView;
    private RecyclerViewAdapter recyclerViewAdapter;
    private ArrayList<Rdv> rdv;
    private Intent intent;
    private Boolean musicHasChanged;
    private String dateNotification;
    public Res res;
    static final int MY_PERMISSIONS_REQUEST_READ_CONTACT = 62;
    public static int colorNumber = 202020;
    static int NOTIFICATION_ID = 100;
    static int REQUEST_CODE = 200;
    static String CHANNEL_ID = "channel_01";
    private TextView emptyView;

    /** Description
     * This method is launched as soon as the user arrives at the activity.
     * It is used to display the buttons, information specified in the XML file.
     *
     * @param savedInstanceState Resumes the state of the activity where it was left
     *  */
    @SuppressLint("ResourceType")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        //Allows you to retrieve what the activity looks like. (link to the XML file)
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        //Connection to the database
        DB = new DatabaseHelper(this);
        DB.open();

        //Recovery of the list of RDV
        rdv = DB.getRdvs();

        //Display the list of RDV
        emptyView = findViewById(R.id.tvEmptyRdv);
        recyclerView = findViewById(R.id.rvRDV);
        recyclerView.setLayoutManager(
                new LinearLayoutManager(this)
        );

        //Allows to make the connection (Bind) between the RecyclerView view and a list of data.
        recyclerViewAdapter = new RecyclerViewAdapter(R.layout.recycler_view_item, rdv, this);
        recyclerView.setAdapter(recyclerViewAdapter);

        //Declaration of the toolbar on the top of the activity
        setSupportActionBar(binding.toolbar);

        //Allow to make a menu on the toolbar
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment_content_main);
        appBarConfiguration = new AppBarConfiguration.Builder(navController.getGraph()).build();
        NavigationUI.setupActionBarWithNavController(this, navController, appBarConfiguration);

        //Prepares the click on the button that allows you to add an appointment.
        binding.fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //Change the activity to AddRdv Class
                Intent intent = new Intent(MainActivity.this, AddRdv.class);
                startActivity(intent);
            }
        });

        if (rdv.isEmpty()){
            recyclerView.setVisibility(View.GONE);
            emptyView.setVisibility(View.VISIBLE);
        }else {
            recyclerView.setVisibility(View.VISIBLE);
            emptyView.setVisibility(View.GONE);
        }

        //Allow to detect if before, we were in an other activity containing an id (from AddRdv class)
        intent = getIntent();
        if (intent != null) {
            if (intent.hasExtra("id")) {
                Intent intentDetails = new Intent(MainActivity.this, Details.class);
                intentDetails.putExtra("id", intent.getLongExtra("id", 0));
                startActivity(intentDetails);
            }
        }

        //Allow to check if the user accept to share his contact with the app
        checkPermissionContact();

        //Allow to check if the settings of the app has changed (from the settings activity)
        checkChangedSettings();
    }

    /** Description
     * This method is launched as soon as the user arrives at the activity.
     * It is used to display the menu on the action bar with the data contain on.
     *
     * @param menu Get menu in xml file
     *  */
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    /**
     * This method is called when an options menu item is selected.
     * It handles the item clicks on the action bar and performs the required operations based on the item clicked.
     *
     * @param item the MenuItem that was clicked
     *
     * @return true if the item was handled, false otherwise
     */
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        // Inspection of the item selected
        if (id == R.id.action_delete) {
            Toast.makeText(this, "All the appointments has been removed", Toast.LENGTH_LONG).show();
            //Go to the deleteAllRdv method present on the database class in order to delete oll the recycler view
            DB.deleteAllRdv();
            //Refresh the activity to see the change
            Intent i = new Intent(MainActivity.this, MainActivity.class);
            startActivity(i);
        } else if (id == R.id.action_settings) {
            //Go to Settings activity when clicked
            Intent i = new Intent(MainActivity.this, Settings.class);
            startActivity(i);
        }
        return super.onOptionsItemSelected(item);
    }

    /**
     * This method checks if the user came from the Settings activity,
     * and if so, it retrieves the new settings values and updates the appropriate parameters accordingly.
     * It also sets the color of the background according to the updated settings values.
     */
    public void checkChangedSettings() {
        intent = getIntent();
        //Allow to check if the user come from an activity
        if (intent != null) {
            //Allow to check if the user come from the right activity
            if (intent.hasExtra("musicHasChanged")) {
                //We change the value used to change the color background
                musicHasChanged = intent.getBooleanExtra("musicHasChanged", false);
                //Settings contain 3 parameters so we run the methods
                putMusic(Settings.music);
                putNotification(Settings.notification);
            }
        }
        putColor(Settings.color);
    }


    /**
     * This method checks if the app has permission to read contacts. If permission is granted, it displays a toast message to the user.
     * If permission is not granted, it requests permission to read contacts from the user.
     */
    public void checkPermissionContact() {
        //Check if read contacts permission is granted to app
        int permissionCheck = ContextCompat.checkSelfPermission(this, android.Manifest.permission.READ_CONTACTS);
        //Check if permission is granted, the method displays a Toast message to inform the user that permission has been granted.
        if (permissionCheck == PackageManager.PERMISSION_GRANTED) {
            Toast.makeText(this, "Permission granted", Toast.LENGTH_SHORT).show();
        } else { //If permission is not granted, request permission to read contacts from the user.
            ActivityCompat.requestPermissions(this, new String[]{android.Manifest.permission.READ_CONTACTS},
                    MY_PERMISSIONS_REQUEST_READ_CONTACT);
        }
    }

    /** Description
     * This method is launched if the user come from Settings activity
     * It is used to check if the app have to stop or start the music,
     * if the state of the checkbox has changed or not
     *
     * @param  isMusic Allow to know if the checkbox is checked or no
     *  */
    public void putMusic(String isMusic) {
        //If checkbox is checked and the state has change we start the music
        //If checkbox is not checked and the state has changed, we stop the music
        //else, the state has not changed so we do nothing
        if (isMusic.equals("yes") && musicHasChanged) {
            startService(new Intent(MainActivity.this, BackgroundMusic.class));
        } else if (isMusic.equals("no") && musicHasChanged) {
            stopService(new Intent(MainActivity.this, BackgroundMusic.class));
        } else {
            System.out.println("DO NOTHING");
        }
    }

    /** Description
     * This method is launched if the user come from Settings activity
     * This method takes a string parameter and sets the date for the notification according to the value of the string.
     *
     * @param  isNotification Allow to know when the user want to reciev notification
     *  */
    public void putNotification(String isNotification) {
        if (isNotification.equals(getString(R.string.oneDay))) {
            dateNotification = getString(R.string.notif1);
            sendNotification(dateNotification);
        } else if (isNotification.equals(getString(R.string.twoDays))) {
            dateNotification = getString(R.string.notif2);
            sendNotification(dateNotification);
        } else if (isNotification.equals(getString(R.string.oneWeek))) {
            dateNotification = getString(R.string.notif3);
            sendNotification(dateNotification);
        } else {
            dateNotification = ".";
        }
    }

    /**
     * Sends a notification to the user.
     * If the API version is greater than or equal to Oreo, it creates a notification channel and registers it with the NotificationManager.
     * The method initializes the notification, sets its icon, title, description, priority, action, and pending intent.
     * If the user has granted permission to post notifications, it sends the notification using the NotificationManagerCompat.
     * Otherwise, it returns without sending the notification.
     *
     * @param dateNotification the date for which the notification is set.
     */
    public void sendNotification(String dateNotification){
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            CharSequence name = "channel notif";
            int importance = NotificationManager.IMPORTANCE_DEFAULT;
            NotificationChannel channel = new NotificationChannel(CHANNEL_ID, name, importance);
            channel.setDescription("channel desc");
            // register the channel
            NotificationManager notificationManager = getSystemService(NotificationManager.class);
            notificationManager.createNotificationChannel(channel);
        }
        //Corresponds to the activity where the user will arrive when he clicks on the notification
        Intent intent = new Intent(this, MainActivity.class);
        PendingIntent pendingIntent = PendingIntent.getActivity(this, REQUEST_CODE, intent, PendingIntent.FLAG_ONE_SHOT);

        //Init of the notif
        NotificationManager mNotificationManager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);

        NotificationManagerCompat notificationManager = NotificationManagerCompat.from(this);
        NotificationCompat.Builder notifBuilder = new NotificationCompat.Builder(this, CHANNEL_ID)
                .setSmallIcon(R.drawable.ic_launcher_foreground)//We add an image
                .setContentTitle(getString(R.string.notifTitle))//We set the title
                .setContentText(getString(R.string.notifDesc) + dateNotification)//We set the description
                .setPriority(NotificationCompat.PRIORITY_DEFAULT)//We set the priority to default
                .setContentIntent(pendingIntent)//We set where the user will arrive when he clicks on
                .addAction(new NotificationCompat.Action(R.drawable.ic_launcher_foreground, getString(R.string.See), pendingIntent));
        // notificationId : unique identifier to define
        if (ActivityCompat.checkSelfPermission(this, android.Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
            return;
        }
        //We send the notification
        notificationManager.notify(NOTIFICATION_ID, notifBuilder.build());
    }

    /** Description
     * This method is launched if the user come from Settings activity
     * Allow to set the right background color and to change the final colorNumber variable
     *
     * @param  color Allow to know the color the user choose for the background
     *  */
    @SuppressLint("ResourceType")
    public void putColor(String color){
        if (color.equals(getString(R.string.Base_color))){
            colorNumber=202020;
            //We retrieve the color that corresponds to this number in the class Res
            binding.toolbar.setBackgroundColor(getResources().getColor(202020,getTheme()));
        } else if (color.equals(getString(R.string.Red))) {
            colorNumber=30000;
            binding.toolbar.setBackgroundColor(getResources().getColor(30000,getTheme()));
        } else if (color.equals(getString(R.string.Magenta))) {
            colorNumber=870883;
            binding.toolbar.setBackgroundColor(getResources().getColor(870883,getTheme()));
        } else if (color.equals(getString(R.string.Dark_Blue))) {
            colorNumber=141497;
            binding.toolbar.setBackgroundColor(getResources().getColor(141497,getTheme()));
        } else if (color.equals(getString(R.string.Brown))) {
            colorNumber=884909;
            binding.toolbar.setBackgroundColor(getResources().getColor(884909,getTheme()));
        } else if (color.equals(getString(R.string.Cyan))) {
            colorNumber=178697;
            binding.toolbar.setBackgroundColor(getResources().getColor(178697,getTheme()));
        } else if (color.equals(getString(R.string.Green))) {
            colorNumber=189025;
            binding.toolbar.setBackgroundColor(getResources().getColor(189025,getTheme()));
        } else if (color.equals(getString(R.string.Orange))) {
            colorNumber=178691;
            binding.toolbar.setBackgroundColor(getResources().getColor(178691,getTheme()));
        } else if (color.equals(getString(R.string.Yellow))) {
            colorNumber=178692;
            binding.toolbar.setBackgroundColor(getResources().getColor(178692,getTheme()));
        }
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