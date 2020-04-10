using UnityEngine;
using System.Collections;
using UnityEngine.UI;
using UnityEngine.Networking;
using System.Collections;
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;

public class SelectLot : MonoBehaviour{
    private Transform pos;
    private GameObject thisObj;
    public static float flag=0;
    public float currentTime=0f;
    public float startTime=60f;
    public float finishTime=0f;
    RaycastHit hitInfo;
    GameObject currentSelect;

    public void Start()
    {

       
    }
    public void Update(){
     if(Login.apiKey!=null){

      if(GameObject.FindGameObjectsWithTag("mark")==null){     
        if(Input.GetMouseButtonDown(0)){
           
            //Destroy(thisObj);
            var ray = Camera.main.ScreenPointToRay(Input.mousePosition);
        
            if(Physics.Raycast(ray, out hitInfo)){
           
                var rig = hitInfo.collider.GetComponent<Rigidbody>();
                pos = hitInfo.collider.gameObject.transform;
                currentSelect=hitInfo.collider.gameObject;
              
                if(pos != null && hitInfo.transform.gameObject.tag.Equals("Lot")){
                
                    if(!GameObject.Find("CAR"+hitInfo.transform.gameObject.name)){
                        
                        foreach(ParkingLots lot in RequestScript.parkingLotsArray){
                               thisObj=GameObject.Find(lot.ParkingLotID);
                               
                          
                          if(thisObj!=null){
                              if(lot.ParkingLotStatus.Equals("Available") && lot.SelectedStatus.Equals("False") && lot.ParkingLotID.Equals(hitInfo.transform.gameObject.name) && flag==0 && lot.ApiKey.Equals("")){
                                Debug.Log("a6");
                                flag=1;
                                Debug.Log("cur"+currentSelect.name);
                                StartCoroutine(coroutine1()); 
                                Debug.Log("ekledi flag"+flag);
                                
                                 break;
                              
                              }
                              if(lot.ParkingLotStatus.Equals("Available") && lot.SelectedStatus.Equals("True") && lot.ParkingLotID.Equals(currentSelect.name) && flag==1 && lot.ApiKey.Equals(Login.apiKey.Replace("\"",""))){
                                Debug.Log("a7");
                                flag=0;
                                Debug.Log("sildi flag"+flag);
                                StartCoroutine(coroutine2()); 
                                break;
                              }
                          }     
                            
                        }

                         
                            
                    }
                    
                
              }
            }
            
        }
      }   
    }
        
    }

    IEnumerator coroutine1(){
                        
                        
                        //MarkingLots mObj2 = new MarkingLots();
                        deleteMark mObj2 = new deleteMark();
                        setApiKey mObj1 = new setApiKey();
                        STime sTime = new  STime();
                        sTime.SelectTime=""+DateTime.Now;
                        mObj2.ParkingLotID=currentSelect.name;
                        mObj1.ApiKey=Login.apiKey.Replace("\"","");
                        string s="";
                       // Debug.Log("BAKKK"+hitInfo.transform.gameObject.name+" vee"+mObj2.ParkingLotID);
                        string json3 = JsonUtility.ToJson(sTime);
                        string json2 = JsonUtility.ToJson(s);
                        string json1 = JsonUtility.ToJson(mObj1);
                        string url3="https://smart-car-park-api.appspot.com/setSelectTime/"+mObj2.ParkingLotID;
                        string url2="https://smart-car-park-api.appspot.com/handleSelect/"+mObj2.ParkingLotID;
                        string url1="https://smart-car-park-api.appspot.com/setApiKey/"+mObj2.ParkingLotID;
                        
                        Debug.Log(url2);
                        var uwr3 = new UnityWebRequest(url3, "PUT");
                        var uwr2 = new UnityWebRequest(url2, "PUT");
                        var uwr1 = new UnityWebRequest(url1, "PUT");
                        byte[] jsonToSend3 = new System.Text.UTF8Encoding().GetBytes(json3);
                        byte[] jsonToSend2 = new System.Text.UTF8Encoding().GetBytes(json2);
                        byte[] jsonToSend1 = new System.Text.UTF8Encoding().GetBytes(json1);
                        uwr3.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend3);
                        uwr2.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend2);
                        uwr1.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend1);
                        uwr3.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
                        uwr2.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
                        uwr1.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
                        uwr3.SetRequestHeader("Content-Type", "application/json");
                        uwr2.SetRequestHeader("Content-Type", "application/json");
                        uwr1.SetRequestHeader("Content-Type", "application/json");
                        yield return uwr3.SendWebRequest();
                        yield return uwr2.SendWebRequest();
                        yield return uwr1.SendWebRequest();
                        
                        if (uwr2.isNetworkError){
                                Debug.Log("giderken hata oldu "+uwr2.error);
                        }else if(uwr1.isNetworkError){
                                Debug.Log("giderken hata oldu "+uwr1.error);
                        }else if(uwr3.isNetworkError){
                                Debug.Log("giderken hata oldu "+uwr3.error);
                        }else{
                                Debug.Log(uwr2.downloadHandler.text);
                               
                        }
                        

                         yield return new WaitForSeconds(5);
                           
    }

    
    IEnumerator coroutine2(){
                        
                        
                        //MarkingLots mObj2 = new MarkingLots();
                        deleteMark mObj1 = new deleteMark();
                        setApiKey mObj2 = new setApiKey();
                        mObj2.ApiKey=null;
                        mObj1.ParkingLotID=currentSelect.name;
                        string s1="";
                        STime sTime2 = new  STime();
                        sTime2.SelectTime="";
                       // Debug.Log("BAKKK"+hitInfo.transform.gameObject.name+" vee"+mObj2.ParkingLotID);
                        string json1 = JsonUtility.ToJson(s1);
                        string json2 = JsonUtility.ToJson(mObj2);
                        string json3 = JsonUtility.ToJson(sTime2);
                        string url1="https://smart-car-park-api.appspot.com/handleUnSelect/"+mObj1.ParkingLotID;
                        string url2="https://smart-car-park-api.appspot.com/setApiKey/"+mObj1.ParkingLotID;
                        string url3="https://smart-car-park-api.appspot.com/setSelectTime/"+mObj1.ParkingLotID;
                        Debug.Log(url1);
                        var uwr1 = new UnityWebRequest(url1, "PUT");
                        var uwr2 = new UnityWebRequest(url2, "PUT");
                        var uwr3 = new UnityWebRequest(url3, "PUT");
                        byte[] jsonToSend1 = new System.Text.UTF8Encoding().GetBytes(json1);
                        uwr1.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend1);
                        uwr1.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
                        uwr1.SetRequestHeader("Content-Type", "application/json");
                        byte[] jsonToSend2 = new System.Text.UTF8Encoding().GetBytes(json2);
                        uwr2.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend2);
                        uwr2.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
                        uwr2.SetRequestHeader("Content-Type", "application/json");
                        byte[] jsonToSend3 = new System.Text.UTF8Encoding().GetBytes(json3);
                        uwr3.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend3);
                        uwr3.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
                        uwr3.SetRequestHeader("Content-Type", "application/json");

                        yield return uwr1.SendWebRequest();
                        yield return uwr2.SendWebRequest();
                        yield return uwr3.SendWebRequest();

                        if (uwr1.isNetworkError){
                                Debug.Log("giderken hata oldu "+uwr1.error);
                        }else if(uwr2.isNetworkError){
                                Debug.Log("giderken hata oldu "+uwr2.error);
                        }else if(uwr3.isNetworkError){
                                Debug.Log("giderken hata oldu "+uwr3.error);
                        }else{
                                Debug.Log(uwr1.downloadHandler.text);
                               
                        }

                         yield return new WaitForSeconds(5);
                           
    }

   

}