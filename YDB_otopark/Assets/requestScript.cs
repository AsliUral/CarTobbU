using UnityEngine;
using System.Collections;
using UnityEngine.Networking;
public class requestScript : MonoBehaviour{
public GameObject thisObj;

    public void Start(){
        StartCoroutine(coroutine());
    }
    
    public IEnumerator coroutine(){
        while (true){
            
            UnityWebRequest www = UnityWebRequest.Get("https://smart-car-park-api.appspot.com/parkingLots/p2");

            yield return www.SendWebRequest();
            if (www.isNetworkError || www.isHttpError){
                Debug.Log(www.error);
                Debug.Log("HAATAAAAAAA");
            }
            
            else{
              
                // Show results as text
                string str = www.downloadHandler.text;
                Debug.Log(www.downloadHandler.text);
                string[] statusArr;
                string status = "";
                string[] strSplit = str.Split(',');
                for(var i=0; i<strSplit.Length; i++){
                    if(strSplit[i].Contains("ParkingLotStatus")){
                        statusArr = strSplit[i].Split(':');
                        status = statusArr[1];
                        Debug.Log("status:(p2) " + status);
                    }
                //Debug.Log(strSplit[i]);
                }
                //bu statusu databaseten alınca bu kismi guncelle
                var cubeRenderer = thisObj.GetComponent<Renderer>();
                if(status.Equals("\"Available\"")){
                    Debug.Log("true");
                    cubeRenderer.material.SetColor("_Color", Color.green);                
                }          
            }
            
            yield return new WaitForSeconds(5);
        }
    }
}


