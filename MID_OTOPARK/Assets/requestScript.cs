using UnityEngine;
using System.Collections;
using UnityEngine.Networking;
public class requestScript : MonoBehaviour{

public GameObject spawnee;
public Transform pos;

    public void Start(){
        StartCoroutine(coroutine());
    }
    
    public IEnumerator coroutine(){
        while (true){
            //UnityWebRequest www = UnityWebRequest.Get("http://localhost:3000/parkinglots");
            UnityWebRequest www = UnityWebRequest.Get("http://localhost:3000/parkinglots/P1");

            yield return www.SendWebRequest();
            if (www.isNetworkError || www.isHttpError){
                Debug.Log(www.error);
                Debug.Log("ERROR");
            }
            
            else{
              
                // Show results as text
                string str = www.downloadHandler.text;
                Debug.Log(www.downloadHandler.text);
            
                int status = 1;
              
                //bu statusu databaseten alınca bu kismi guncelle
                
                if(status == 1){
                    Instantiate(spawnee,pos.position + new Vector3(0,(float)0.40,0),pos.rotation);
                              
                }
     
                
             
                }          
            }
            
            yield return new WaitForSeconds(5);
        }
    }

