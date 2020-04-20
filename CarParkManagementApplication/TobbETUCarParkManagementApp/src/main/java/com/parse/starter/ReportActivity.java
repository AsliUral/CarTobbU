package com.parse.starter;

import android.Manifest;
import android.annotation.TargetApi;
import android.app.TimePickerDialog;
import android.content.ContentValues;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.provider.SyncStateContract;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;

import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.TimePicker;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.NetworkResponse;
import com.android.volley.NoConnectionError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.TimeoutError;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.Callback;

public class ReportActivity extends AppCompatActivity {
    private static final int PERMISSION_CODE = 1000;
    private static final int IMAGE_CAPTURE_CODE = 1001;
    private static final int CAMERA_REQUEST = 1888;
    private static final int MY_CAMERA_PERMISSION_CODE = 100;


    ImageView mImageView;
    private Bitmap bitmap;
    private String filPath;
    private static final String UploadUrl = "https://smart-car-park-api.appspot.com/penalty";

    Button mCpatureBtn;
    Button submitPenaltyButton;
    Button selectTimeBtn;
    Uri image_uri;
    EditText dateTextEdit;
    EditText notesText;
    EditText carPlateText;
    Spinner penaltyTimeSpinner;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_image_capture);


        String date = new SimpleDateFormat("dd-MM-yyyy", Locale.getDefault()).format(new Date());


        dateTextEdit = (EditText) findViewById(R.id.dateText);
        dateTextEdit.setText(date);

        dateTextEdit.setEnabled(false);

        notesText = (EditText) findViewById(R.id.notes_text);

        carPlateText = (EditText) findViewById(R.id.carPlateText);
        penaltyTimeSpinner = (Spinner) findViewById(R.id.penaltyTime);

        selectTimeBtn = (Button) findViewById(R.id.time_select_btn);

        selectTimeBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // TODO Auto-generated method stub
                Calendar mcurrentTime = Calendar.getInstance();
                int hour = mcurrentTime.get(Calendar.HOUR_OF_DAY);
                int minute = mcurrentTime.get(Calendar.MINUTE);

                TimePickerDialog mTimePicker;
                mTimePicker = new TimePickerDialog(ReportActivity.this, new TimePickerDialog.OnTimeSetListener() {
                    @Override
                    public void onTimeSet(TimePicker timePicker, int selectedHour, int selectedMinute) {
                        selectTimeBtn.setText( selectedHour + ":" + selectedMinute);
                    }
                }, hour, minute, true);//Yes 24 hour time
                mTimePicker.setTitle("Select Time");
                mTimePicker.show();

            }
        });


        mImageView = (ImageView) findViewById(R.id.report_image);
        mCpatureBtn = (Button) findViewById(R.id.capture_image_btn);

        mCpatureBtn.setOnClickListener(new View.OnClickListener()
        {
            @TargetApi(Build.VERSION_CODES.M)
            @Override
            public void onClick(View v)
            {
                if (checkSelfPermission(Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED)
                {
                    requestPermissions(new String[]{Manifest.permission.CAMERA}, MY_CAMERA_PERMISSION_CODE);
                }
                else
                {
                    Intent cameraIntent = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
                    startActivityForResult(cameraIntent, CAMERA_REQUEST);
                }
            }
        });

        submitPenaltyButton = (Button) findViewById(R.id.submit_report_btn);
        submitPenaltyButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                reportPenalty();
                Toast.makeText(ReportActivity.this, "Penalty is reported successfuly...", Toast.LENGTH_LONG).show();
            }
        });
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        switch (requestCode){
            case PERMISSION_CODE:{
                if (grantResults.length > 0 && grantResults[0] ==
                        PackageManager.PERMISSION_GRANTED){
                    try {
                        openCamera();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }else{
                    Toast.makeText(this, "Permission denied...", Toast.LENGTH_SHORT).show();
                }
            }
        }
    }

    private void openCamera() throws IOException {
        ContentValues values = new ContentValues();
        values.put(MediaStore.Images.Media.TITLE, "New Picture");
        values.put(MediaStore.Images.Media.DESCRIPTION, "From the Camera");
        image_uri = getContentResolver().insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values);
        Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, image_uri);
        startActivityForResult(cameraIntent, IMAGE_CAPTURE_CODE);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == 1888 && resultCode == ReportActivity.RESULT_OK)
        {
            Bitmap photo = (Bitmap) data.getExtras().get("data");
            bitmap = photo;
            mImageView.setImageBitmap(photo);
        }
    }

    public byte[] getFileDataFromDrawable(Bitmap bitmap) {
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        //bitmap.compress(Bitmap.CompressFormat.PNG, 80, byteArrayOutputStream);
        return byteArrayOutputStream.toByteArray();
    }

    private void reportPenalty() {
        // loading or check internet connection or something...
        // ... then
        String url = "https://smart-car-park-api.appspot.com/penalty";
        VolleyMultipartRequest multipartRequest = new VolleyMultipartRequest(Request.Method.POST, url, new Response.Listener<NetworkResponse>() {
            @Override
            public void onResponse(NetworkResponse response) {
                String resultResponse = new String(response.data);
                try {
                    JSONObject result = new JSONObject(resultResponse);
                    String status = result.getString("status");
                    String message = result.getString("message");

                    if (true) {
                        // tell everybody you have succed upload image and post strings
                        Log.i("Messsage", message);
                    } else {
                        Log.i("Unexpected", message);
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                NetworkResponse networkResponse = error.networkResponse;
                String errorMessage = "Unknown error";
                if (networkResponse == null) {

                    if (error.getClass().equals(TimeoutError.class)) {
                        errorMessage = "Request timeout";

                    } else if (error.getClass().equals(NoConnectionError.class)) {
                        errorMessage = "Failed to connect server";
                    }
                } else {
                    String result = new String(networkResponse.data);
                    try {
                        JSONObject response = new JSONObject(result);
                        String status = response.getString("status");
                        String message = response.getString("message");

                        Log.e("Error Status", status);
                        Log.e("Error Message", message);

                        if (networkResponse.statusCode == 404) {
                            errorMessage = "Resource not found";
                        } else if (networkResponse.statusCode == 401) {
                            errorMessage = message+" Please login again";
                        } else if (networkResponse.statusCode == 400) {
                            errorMessage = message+ " Check your inputs";
                        } else if (networkResponse.statusCode == 500) {
                            errorMessage = message+" Something is getting wrong";
                        }
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
                Log.i("Error", errorMessage);
                error.printStackTrace();
            }
        }) {
            @Override
            protected Map<String, String> getParams() {
                String noteReq = notesText.getText().toString();
                String dateReq = dateTextEdit.getText().toString();
                String timeReq = selectTimeBtn.getText().toString();
                String typeReq = penaltyTimeSpinner.getSelectedItem().toString();
                String carPlateReq = carPlateText.getText().toString();
                Uri penaltyImageUri = image_uri;

                Map<String, String> params = new HashMap<>();
                params.put("date", dateReq);
                params.put("time", timeReq);
                params.put("type", typeReq);
                params.put("carPlate", carPlateReq);
                params.put("notes", noteReq);
                return params;
            }

            @Override
            protected Map<String, DataPart> getByteData() {
                Map<String, DataPart> params = new HashMap<>();
                String timeReqImageName = selectTimeBtn.getText().toString();
                String carPlateReqImageName = carPlateText.getText().toString().replace(" ", "-");
                String dateReqImageName = dateTextEdit.getText().toString();
                String imageName = "Pen" + "_" + dateReqImageName + "_" + timeReqImageName.replace(":", "-") + "_" + carPlateReqImageName + ".jpg";
                // file name could found file base or direct access from real path
                // for now just get bitmap data from ImageView
                params.put("penaltyImage", new DataPart(imageName, AppHelper.getFileDataFromDrawable(getBaseContext(), mImageView.getDrawable()), "image/jpeg"));

                return params;
            }
        };

        VolleySingleton.getInstance(getBaseContext()).addToRequestQueue(multipartRequest);
    }

    public void postNewPenalty(){
        //mPostCommentResponse.requestStarted();
        Log.i("Burasi calisti", "En azindan");

        RequestQueue queue = Volley.newRequestQueue(ReportActivity.this);
        StringRequest sr = new StringRequest(Request.Method.POST,"https://smart-car-park-api.appspot.com/penalty", new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                Log.i("onResponse", response);
                //mPostCommentResponse.requestCompleted();
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                error.printStackTrace();
                Log.i("onResponseError", error.toString());
                //mPostCommentResponse.requestEndedWithError(error);
            }
        }){
            @Override
            protected Map<String,String> getParams(){
                String noteReq = notesText.getText().toString();
                String dateReq = dateTextEdit.getText().toString();
                String timeReq = selectTimeBtn.getText().toString();
                String typeReq = penaltyTimeSpinner.getSelectedItem().toString();
                String carPlateReq = carPlateText.getText().toString();
                Uri penaltyImageUri = image_uri;

                Log.i("noteReq", noteReq);
                Log.i("dateReq", dateReq);
                Log.i("timeReq", timeReq);
                Log.i("typeReq", typeReq);
                Log.i("carPlateReq", carPlateReq);
                Log.i("penaltyImageUri", penaltyImageUri.toString());




                Map<String,String> params = new HashMap<String, String>();
                params.put("date",dateReq);
                params.put("time",timeReq);
                params.put("penaltyImage", imageToString(bitmap));
                params.put("type",typeReq);
                params.put("carPlate",carPlateReq);
                params.put("notes",noteReq);


                return params;
            }

            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {

                String noteReq = notesText.getText().toString();
                String dateReq = dateTextEdit.getText().toString();
                String timeReq = selectTimeBtn.getText().toString();
                String typeReq = penaltyTimeSpinner.getSelectedItem().toString();
                String carPlateReq = carPlateText.getText().toString();
                Uri penaltyImageUri = image_uri;

                Map<String,String> params = new HashMap<String, String>();
                params.put("Content-Type","application/form-data");
                params.put("date",dateReq);
                params.put("time",timeReq);
                params.put("penaltyImage", imageToString(bitmap));
                params.put("type",typeReq);
                params.put("carPlate",carPlateReq);
                params.put("notes",noteReq);
                return params;
            }
        };
        //queue.add(sr);
    }
    private String imageToString(Bitmap bitmap){
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG, 100, byteArrayOutputStream);
        byte[] imgBytes = byteArrayOutputStream.toByteArray();
        return Base64.encodeToString(imgBytes, Base64.DEFAULT);
    }
}





