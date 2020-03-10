using UnityEngine;
using System.Collections;
using UnityEngine.Networking;
public class requestScript : MonoBehaviour{
public GameObject spawnee;
public GameObject car;
public Transform pos;
public Transform transform;

    public void Start(){
        StartCoroutine(coroutine());
    }
    
    public IEnumerator coroutine(){
        while (true){
            
            //UnityWebRequest www = UnityWebRequest.Get("https://smart-car-park-api.appspot.com/parkingLots/p11");
            UnityWebRequest www = UnityWebRequest.Get("https://smart-car-park-api.appspot.com/parkingLots/p2");

            yield return www.SendWebRequest();
           
            if (www.isNetworkError || www.isHttpError){
                Debug.Log(www.error);
                Debug.Log("ERROR!");
            }
            
            else{
               
                // Show results as text
                string available ="\"Available\"";
                string occupied = "\"Occupied\"";
                
                string data = www.downloadHandler.text;
                Debug.Log(www.downloadHandler.text);
                string[] allStatus;
                string parkingLotStatus = "";
                string[] dataSplit = data.Split(',');
                for(var i=0; i<dataSplit.Length; i++){
                    string parkId=dataSplit[0];
                    if(dataSplit[i].Contains("ParkingLotStatus")){
                        allStatus = dataSplit[i].Split(':');
                        parkingLotStatus = allStatus[1];
                        Debug.Log("parking lot status of "+ parkId+" -> " + parkingLotStatus);
                    }
               
                }
                var cubeRenderer = spawnee.GetComponent<Renderer>();
                var cubeRenderer2 = car.GetComponent<Renderer>();
                if(parkingLotStatus.Equals(available)){

                    Debug.Log("available");
                    Instantiate(spawnee,pos.position + new Vector3(0,(float)0.40,0),pos.rotation);                 
                }else if(parkingLotStatus.Equals(occupied)){
                    Debug.Log("occupied");
                    Instantiate(car,pos.position + new Vector3(0,(float)0,0),pos.rotation);
                    car.transform.Rotate(0,-90,0); 
                    
                }          
            }
            
            yield return new WaitForSeconds(5);
        }
    }
   
}
