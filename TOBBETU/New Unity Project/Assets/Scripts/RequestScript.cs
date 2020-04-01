using UnityEngine;
using System.Collections;
using UnityEngine.Networking;
public class RequestScript : MonoBehaviour{
public GameObject thisObj;
public GameObject car;
public Transform pos;
public Transform transform;

    public void Start(){
        StartCoroutine(coroutine());
    }
    
    public IEnumerator coroutine(){
        while (true){
            
            UnityWebRequest www = UnityWebRequest.Get("https://smart-car-park-api.appspot.com/parkingLots");
            UnityWebRequest www2 = UnityWebRequest.Get("https://smart-car-park-api.appspot.com/marking");

            yield return www.SendWebRequest();
            yield return www2.SendWebRequest();
            if (www.isNetworkError || www.isHttpError){
                Debug.Log(www.error);
                Debug.Log("HAATAAAAAAA");
            }else if(www2.isNetworkError || www2.isHttpError){
                Debug.Log(www.error);
                Debug.Log("HAATAAAAAAA");
            }else{
              
                // Show results as text
                string nameObj=thisObj.gameObject.name;
                var cubeRenderer = thisObj.GetComponent<Renderer>();
                
                string str = www.downloadHandler.text;
                string str2= www2.downloadHandler.text;
                string jsonString = fixJson(str);
                string jsonString2 = fixJson(str2);
                ParkingLots[] parkingLotsArray = JsonHelper.FromJson<ParkingLots>(jsonString);
                MarkingLots[] markingLotsArray = JsonHelper.FromJson<MarkingLots>(jsonString2);
                foreach ( ParkingLots lot in parkingLotsArray){
                   // Debug.Log(lot.ParkingLotID+" ve "+lot.ParkingLotStatus+ " veee "+ nameObj);
                    if((lot.ParkingLotStatus+"").Equals("Available") && (nameObj).Equals(lot.ParkingLotID+"") ){
                        cubeRenderer.material.SetColor("_Color", Color.green);
                        break;
                    }else if(lot.ParkingLotStatus.Equals("Occupied") && (nameObj).Equals(lot.ParkingLotID) ){
                        cubeRenderer.material.SetColor("_Color", Color.red);
                        
                           // string nameColor=marking.CarColor;
                           // Color carColor = Color.clear; 
                           // ColorUtility.TryParseHtmlString (nameColor, out carColor);
                         //  Material m_Material;
                           //m_Material = GetComponent<Renderer>().material;
                            //var cubeRenderer2 = car.GetComponent<Renderer>();
                           // cubeRenderer2.material.SetColor("_Color", Color.red);
                            //m_Material.Color=Color.red;
                         
                            Instantiate(car,pos.position + new Vector3(0,(float)0,(float)-0.3),pos.rotation);
                            //var cubeRenderer2 = car.GetComponent<Renderer>();
                            //cubeRenderer2.material.SetColor("_Color", Color.green);
                            
                           
                       
                        break;
                    }

                }
              
                     
                
              /*  Debug.Log(www.downloadHandler.text);
                string[] statusArr;
                string status = "";
                string id = "";
                string[] strSplit = str.Split(',');
                for(var i=0; i<strSplit.Length; i++){
                    
                   
                     if(strSplit[i].Contains("ParkingLotID")){
                        statusArr = strSplit[i].Split(':');
                        id = statusArr[1];
                        Debug.Log(" ID===> " + id+ " ve status "+ status);
                    }
                    if(strSplit[i].Contains("ParkingLotStatus")){
                        statusArr = strSplit[i].Split(':');
                        status = statusArr[1];
                    }
                    if(status.Equals("\"Available\"") && (nameObj).Equals(id)){
                            Debug.Log("true");
                            cubeRenderer.material.SetColor("_Color", Color.green);                
                    }else if(status.Equals("\"Occupied\"") && (nameObj).Equals(id)){
                            Debug.Log("DOLUUU"+ id + " ve obje " + nameObj);
                            cubeRenderer.material.SetColor("_Color", Color.red);
                    } 
                   
                   
                }*/
                //bu statusu databaseten alınca bu kismi guncelle
                /*var cubeRenderer = thisObj.GetComponent<Renderer>();
                Debug.Log("helllo"+thisObj.gameObject.name +" ve "+ id);
                if(status.Equals("\"Available\"") && (thisObj.gameObject.name).Equals(id)){
                    Debug.Log("true");
                    cubeRenderer.material.SetColor("_Color", Color.green);                
                }    */      
            }
            
            yield return new WaitForSeconds(5);
        }
    }

    public string fixJson(string value)
{
    value = "{\"Items\":" + value + "}";
    return value;
}

}


