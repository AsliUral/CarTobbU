package com.parse.starter;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;

import com.parse.FindCallback;
import com.parse.GetDataCallback;
import com.parse.ParseException;
import com.parse.ParseFile;
import com.parse.ParseObject;
import com.parse.ParseQuery;

import java.util.List;

public class ComplaintFeedActivity extends AppCompatActivity {


    EditText notesText;
    EditText carPlateText;
    EditText nameText;
    EditText phoneText;
    EditText timeText;
    EditText dateText;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_complaint_feed);



        Intent intent = getIntent();

        String activeUsername = intent.getStringExtra("note");
        String carPlateString = intent.getStringExtra("carplate");
        String dateString = intent.getStringExtra("date");
        String fullNameString = intent.getStringExtra("fullname");
        String timeString = intent.getStringExtra("time");
        String phoneString = intent.getStringExtra("phone");



        notesText= (EditText) findViewById(R.id.notes_text);
        notesText.setText(activeUsername);

        carPlateText= (EditText) findViewById(R.id.carPlateText);
        carPlateText.setText(carPlateString);

        dateText= (EditText) findViewById(R.id.dateText);
        dateText.setText(dateString);


        nameText= (EditText) findViewById(R.id.nameText);
        nameText.setText(fullNameString);

        timeText= (EditText) findViewById(R.id.timeText);
        timeText.setText(timeString);

        phoneText= (EditText) findViewById(R.id.phoneText);
        phoneText.setText(phoneString);




        setTitle(fullNameString + "'s Complaint");

        ParseQuery<ParseObject> query = new ParseQuery<ParseObject>("Image");

        query.whereEqualTo("username", activeUsername);
        query.orderByDescending("createdAt");

        query.findInBackground(new FindCallback<ParseObject>() {
            @Override
            public void done(List<ParseObject> objects, ParseException e) {

                if (e == null) {

                    if (objects.size() > 0) {

                        for (ParseObject object : objects) {

                            ParseFile file = (ParseFile) object.get("image");

                            file.getDataInBackground(new GetDataCallback() {
                                @Override
                                public void done(byte[] data, ParseException e) {

                                    if (e == null && data != null) {

                                        Bitmap bitmap = BitmapFactory.decodeByteArray(data, 0, data.length);

                                        ImageView imageView = new ImageView(getApplicationContext());

                                        imageView.setLayoutParams(new ViewGroup.LayoutParams(
                                                ViewGroup.LayoutParams.MATCH_PARENT,
                                                ViewGroup.LayoutParams.WRAP_CONTENT
                                        ));

                                        imageView.setImageBitmap(bitmap);

                                        //linearLayout.addView(imageView);

                                    }


                                }
                            });

                        }

                    }

                }

            }
        });




    }
}
