using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.Networking;

public class MainMenu : MonoBehaviour
{
   ParkingLots[] availableLotsArray;
   public static int num;
   void Start(){

        StartCoroutine(coroutine());
        
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

   string fixJson(string value){
    value = "{\"Items\":" + value + "}";
    return value;
   }    
}
