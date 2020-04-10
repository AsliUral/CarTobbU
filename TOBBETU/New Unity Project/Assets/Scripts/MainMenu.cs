using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.Networking;

public class MainMenu : MonoBehaviour
{
   ParkingLots[] availableLotsArray;
   ParkingLots[] availableLotsArray2;
   public static int num;
   public static int num2;
   void Start(){

        StartCoroutine(coroutine());
        //StartCoroutine(coroutine2());
        
   }

   public void GoToRegister(){
       SceneManager.LoadScene(1);
 
   }

   public void GoToLogin(){
      SceneManager.LoadScene(2);
   }

   public void GoToParkingScene(){
      SceneManager.LoadScene(3);
   }

      /*
       scene 3 = parkinglot scene
       scene 0 = main menu scene
       scene 1 = register scene
       scene 2 = login scene
   
        */

   IEnumerator coroutine(){
       
     UnityWebRequest www = UnityWebRequest.Get("https://smart-car-park-api.appspot.com/availableParkingLots");
     yield return www.SendWebRequest();
     if (www.isNetworkError || www.isHttpError){
            Debug.Log(www.error);
            Debug.Log("HAATAAAAAAA");
     }else{
        string str = www.downloadHandler.text;
        string jsonString = fixJson(str);
        availableLotsArray = JsonHelper.FromJson<ParkingLots>(jsonString);
        foreach ( ParkingLots lot in availableLotsArray){
           num++;
        }
      
     }


   }
   
 /*  IEnumerator coroutine2(){
   int a=0;
   while(true){
     UnityWebRequest www2 = UnityWebRequest.Get("https://smart-car-park-api.appspot.com/availableParkingLots");
     yield return www2.SendWebRequest();
     if (www2.isNetworkError || www2.isHttpError){
            Debug.Log(www2.error);
            Debug.Log("HAATAAAAAAA");
     }else{
        string str2 = www2.downloadHandler.text;
        string jsonString2 = fixJson(str2);
        availableLotsArray2 = JsonHelper.FromJson<ParkingLots>(jsonString2);
        foreach ( ParkingLots lot2 in availableLotsArray2){
           a++;
        }
      
     }
      num2=a;
      a=0;

   }
   }*/
     

   string fixJson(string value){
    value = "{\"Items\":" + value + "}";
    return value;
   }    
}
