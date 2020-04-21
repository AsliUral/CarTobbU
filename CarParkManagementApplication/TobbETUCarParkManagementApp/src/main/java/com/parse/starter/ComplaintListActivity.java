package com.parse.starter;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Build;
import android.provider.MediaStore;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.HttpResponse;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.parse.ParseException;
import com.parse.ParseFile;
import com.parse.ParseObject;
import com.parse.ParseUser;
import com.parse.SaveCallback;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.ArrayList;

public class ComplaintListActivity extends AppCompatActivity {

    private static final int CAMERA_REQUEST = 1888;
    private ImageView imageView;
    private static final int MY_CAMERA_PERMISSION_CODE = 100;
    private ArrayList<Complaint> complaints = new ArrayList<Complaint>();

    public void getPhoto() {

        Intent intent = new Intent(getApplicationContext(), ReportActivity.class);
        startActivity(intent);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == MY_CAMERA_PERMISSION_CODE)
        {
            if (grantResults[0] == PackageManager.PERMISSION_GRANTED)
            {
                Toast.makeText(this, "camera permission granted", Toast.LENGTH_LONG).show();
                Intent cameraIntent = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
                startActivityForResult(cameraIntent, CAMERA_REQUEST);
            }
            else
            {
                Toast.makeText(this, "camera permission denied", Toast.LENGTH_LONG).show();
            }
        }
        /*
        if (requestCode == 1) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                getPhoto();
            }
        }
        */
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {

        MenuInflater menuInflater = getMenuInflater();

        menuInflater.inflate(R.menu.share_menu, menu);

        return super.onCreateOptionsMenu(menu);

    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {

        if (item.getItemId() == R.id.share) {

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {

                if (checkSelfPermission(Manifest.permission.READ_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {

                    requestPermissions(new String[]{Manifest.permission.READ_EXTERNAL_STORAGE}, 1);

                } else {
                    getPhoto();

                }

            } else {

                getPhoto();

            }

        } else if (item.getItemId() == R.id.logout) {

            ParseUser.logOut();

            Intent intent = new Intent(getApplicationContext(), MainActivity.class);
            startActivity(intent);

        }

        return super.onOptionsItemSelected(item);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == 1 && resultCode == RESULT_OK && data != null) {

            Uri selectedImage = data.getData();

            try {

                Bitmap bitmap = MediaStore.Images.Media.getBitmap(this.getContentResolver(), selectedImage);

                Log.i("Photo", "Received");

                ByteArrayOutputStream stream = new ByteArrayOutputStream();

                bitmap.compress(Bitmap.CompressFormat.PNG, 100, stream);

                byte[] byteArray = stream.toByteArray();

                ParseFile file = new ParseFile("image.png", byteArray);

                ParseObject object = new ParseObject("Image");

                object.put("image", file);

                object.put("username", ParseUser.getCurrentUser().getUsername());

                object.saveInBackground(new SaveCallback() {
                    @Override
                    public void done(ParseException e) {

                        if (e == null) {

                            Toast.makeText(ComplaintListActivity.this, "Image Shared!", Toast.LENGTH_SHORT).show();

                        } else {

                            Toast.makeText(ComplaintListActivity.this, "Image could not be shared - please try again later.", Toast.LENGTH_SHORT).show();

                        }

                    }
                });


            } catch (IOException e) {
                e.printStackTrace();
            }

        }

    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_complaint_list);
        setTitle("Complaints");
        final ArrayList<String> complaintsList = new ArrayList<String>();
        final ListView userListView = (ListView) findViewById(R.id.userListView);
        userListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                Intent intent = new Intent(getApplicationContext(), ComplaintFeedActivity.class);
                Complaint temp = complaints.get(i);

                intent.putExtra("note", temp.getNotes());
                intent.putExtra("carplate", temp.getCarPlate());
                intent.putExtra("date", temp.getDate());
                intent.putExtra("fullname", temp.getFullname());
                intent.putExtra("time", temp.getTime());
                intent.putExtra("phone", temp.getPhoneNumber());


                startActivity(intent);
            }
        });
        final ArrayAdapter arrayAdapter = new ArrayAdapter(this, android.R.layout.simple_list_item_1, complaintsList);
        //ParseQuery<ParseUser> query = ParseUser.getQuery();
        //query.whereNotEqualTo("username", ParseUser.getCurrentUser().getUsername());
        //query.addAscendingOrder("username");


        // Instantiate the RequestQueue.
        RequestQueue queue = Volley.newRequestQueue(this);
        String url ="https://smart-car-park-api.appspot.com/getPenalties";

// Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        // Display the first 500 characters of the response string.
                        JSONArray jsonArray = null;
                        try {
                            jsonArray = new JSONArray(response);
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }


                        for (int i = 0; i < jsonArray.length(); i++) {
                            try {
                                JSONObject explrObject = jsonArray.getJSONObject(i);
                                if (explrObject.get("type").toString().equals("null")){
                                    String date = explrObject.get("date").toString();
                                    String time = explrObject.get("time").toString();
                                    String notes = explrObject.get("notes").toString();
                                    String carPlate = explrObject.get("carPlate").toString();
                                    String fullname = explrObject.get("fullname").toString();
                                    String phoneNumber = explrObject.get("phoneNumber").toString();
                                    complaints.add(new Complaint(date, time, carPlate, notes, fullname, phoneNumber));
                                    complaintsList.add(notes);
                                }
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                        }
                        userListView.setAdapter(arrayAdapter);

                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
            }
        });

// Add the request to the RequestQueue.
        queue.add(stringRequest);


    }



        /*
        query.findInBackground(new FindCallback<ParseUser>() {
            @Override
            public void done(List<ParseUser> objects, ParseException e) {
                if (e == null) {
                    if (objects.size() > 0) {
                        for (ParseUser user : objects) {
                            usernames.add(user.getUsername());
                        }
                        userListView.setAdapter(arrayAdapter);
                    }
                } else {
                    e.printStackTrace();
                }
            }
        });
        */
    }

