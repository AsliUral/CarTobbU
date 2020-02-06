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
            //UnityWebRequest www = UnityWebRequest.Get("http://localhost:3000/parkinglots");
            UnityWebRequest www = UnityWebRequest.Get("http://localhost:3000/parkinglots/P1");

            yield return www.SendWebRequest();
            if (www.isNetworkError || www.isHttpError){
                Debug.Log(www.error);
                Debug.Log("HAATAAAAAAA");
            }
            
            else{
              
                // Show results as text
                string str = www.downloadHandler.text;
                Debug.Log(www.downloadHandler.text);
            
                int status = 1;
                //bu statusu databaseten alınca bu kismi guncelle
                var cubeRenderer = thisObj.GetComponent<Renderer>();
                if(status == 1){
                    cubeRenderer.material.SetColor("_Color", Color.red);
                                
                }          
            }
            
            yield return new WaitForSeconds(5);
        }
    }
}



                /*
                var gameObject = new GameObject("newObj");
                var meshFilter = gameObject.AddComponent<MeshFilter>();
                gameObject.AddComponent<MeshRenderer>();
                meshFilter.sharedMesh = objectToCreate;
                gameObject.transform.position = transform.position;
                gameObject.transform.rotation = transform.rotation;
                */