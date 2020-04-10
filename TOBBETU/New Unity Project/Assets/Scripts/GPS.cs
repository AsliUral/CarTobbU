using System.Collections;
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Android;

public class GPS : MonoBehaviour
{
    public Text gpsOut;
    public bool isUpdating;
    public static float Latitude;
    public static float Longitude;

    private void Update(){
        if(!isUpdating){
            StartCoroutine(GetLocation());
            isUpdating = !isUpdating;
        }
    }

    IEnumerator GetLocation(){
        Latitude=0;
        Longitude=0;
        if(!Permission.HasUserAuthorizedPermission(Permission.FineLocation)){
            Permission.RequestUserPermission(Permission.FineLocation);
            Permission.RequestUserPermission(Permission.CoarseLocation);

        }

        if(!Input.location.isEnabledByUser)
            yield return new WaitForSeconds(3);
        
        Input.location.Start();

        int maxWait=3;

        while(Input.location.status == LocationServiceStatus.Initializing && maxWait > 0){
            yield return new WaitForSeconds(1);
            maxWait--;
        }
        if(maxWait < 1){
            gpsOut.text =" Timed Out";
            print("Timed out");
            yield break;

        }
        
        if(Input.location.status == LocationServiceStatus.Failed){
            gpsOut.text =" Unable";
            print("Unable");
            yield break;

        }else{
            gpsOut.text = "Location"+Input.location.lastData.latitude+" "+Input.location.lastData.longitude+" ";
            print("Location:"+ Input.location.lastData.latitude+" "+Input.location.lastData.longitude+" ");
            Longitude=Input.location.lastData.longitude;
            Latitude=Input.location.lastData.latitude;
        }

        isUpdating =!isUpdating;
        Input.location.Stop();
    }
   
}