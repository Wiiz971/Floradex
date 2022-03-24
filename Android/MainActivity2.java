package fr.wiiz.floradex.floradex_identification;


import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.DefaultRetryPolicy;

import org.json.JSONException;
import org.json.JSONObject;


    public class MainActivity2 extends AppCompatActivity {

        Button button;
        TextView species,family,commonNames,images;
        String json_url = "https://my-api.plantnet.org/v1/identify/all?images=http://www.lagons-plages.com/images/fleur-frangipanier.jpg&organs=flower&lang=fr&api-key=2a10BNtywoBeNpeXTpZzTmG3z";



        @Override
        protected void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_main);
            button = (Button)findViewById(R.id.bn);
            species = (TextView) findViewById(R.id.sps);
            family = (TextView)findViewById(R.id.fml);
            commonNames = (TextView)findViewById(R.id.cn);
            images = (TextView) findViewById(R.id.img);
            button.setOnClickListener(new View.OnClickListener() {


                @Override
                public void onClick(View v) {
                    JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.GET, json_url,(String) null,
                            new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    try {
                                        species.setText(response.getString("Spieces"));
                                        family.setText(response.getString("Family"));
                                        commonNames.setText(response.getString("CommonName"));
                                        images.setText(response.getString("Images"));

                                    };
                                    catch (JSONException e;
                                    e) {

                                    }


                                }
                            }, new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {

                            Toast.makeText(MainActivity2.this,"Something went wrong",Toast.LENGTH_SHORT).show();
                            error.printStackTrace();
                        }

                    });

                    MySingleton.getInstance(MainActivity2.this).addToRequestque(jsonObjectRequest);


                }
            });
        }
    }
    // https://developer.mozilla.org/fr/docs/Web/HTML/Element/Input/file
    // https://acesyde.developpez.com/tutoriels/android/appareil-photo-android/
