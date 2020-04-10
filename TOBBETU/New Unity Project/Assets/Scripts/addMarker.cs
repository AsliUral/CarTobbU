using UnityEngine;
using System.Collections;
using UnityEngine.UI;
using UnityEngine.Networking;
using System;
using System.Collections.Generic;

public class AddMarker : MonoBehaviour
{
 
    private Transform pos;
    public GameObject marker;
    private GameObject obj;
    public GameObject current;
    public float flag=0;
    RaycastHit hitInfo;
    //public float flag=0;
    public void Start()
    {
    }
    // Update is called once per frame
     void Update()
    {
        if(Login.apiKey!=null){
        /*UnityWebRequest www = UnityWebRequest.Get("https://smart-car-park-api.appspot.com/marking");
        yield return www.SendWebRequest();
        if (www.isNetworkError || www.isHttpError){
                Debug.Log(www.error);
                Debug.Log("HAATAAAAAAA");
        }else{
                string str = www.downloadHandler.text;
                string jsonString = fixJson(str);
                MarkingLots[] markingLotsArray = JsonHelper.FromJson<MarkingLots>(jsonString);
                foreach(MarkingLots marking in markingLotsArray){

                    
                    if(Login.apiKey.Equals("\""+marking.ApiKey+"\"")){
        
                        GameObject m=GameObject.Find(marking.ParkingLotID);
                        if(m!=null){
                            GameObject o= Instantiate(marker,m.transform.position + new Vector3(0,(float)0.60,0),m.transform.rotation);
                            o.transform.Rotate(90,0,0);
                            o.transform.name="MARK"+marking.ParkingLotID;
                            current=o;
                            flag=1;
                            break;
                        }
                       
                    }
                }*/
        

        if(Input.GetMouseButtonDown(0)){
       
            //Destroy(obj);
            var ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            
            if(Physics.Raycast(ray, out hitInfo)){
                
                var rig = hitInfo.collider.GetComponent<Rigidbody>();
                pos = hitInfo.collider.gameObject.transform;
               
                if(pos != null && hitInfo.transform.gameObject.tag.Equals("Lot")){
                 
                    if(show.flag==0 && GameObject.Find("CAR"+hitInfo.transform.gameObject.name)){

                        //obj = Instantiate(marker,pos.position + new Vector3(0,(float)0.60,0),pos.rotation);
                        //obj.transform.Rotate(90,0,0);
                        //obj.transform.name="MARK"+ hitInfo.transform.gameObject.name;
                        //current=obj;
                        StartCoroutine(coroutine1());
                        show.flag=1;
                        current=GameObject.Find(show.markObj);   
                            
                    }else{
                        current=show.sendObject;
                        if(("MARK"+hitInfo.transform.gameObject.name).Equals(show.markObj)){
                            /*MarkingLots mObj = new MarkingLots();
                            mObj.ParkingLotID=hitInfo.transform.gameObject.name;
                             
                            Debug.Log("BASILAN "+hitInfo.transform.gameObject.name);
                            Debug.Log("current "+current.transform.name);
                            string json = JsonUtility.ToJson(mObj);
                            Debug.Log(json);
                            string url="https://smart-car-park-api.appspot.com/marking/deleteMarking/"+Login.apiKey;
                            var uwr = new UnityWebRequest(url, "POST");
                            byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(json);
                            uwr.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend);
                            uwr.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
                            uwr.SetRequestHeader("Content-Type", "application/json");

                            yield return uwr.SendWebRequest();

                            if (uwr.isNetworkError){
                                Debug.Log("giderken hata oldu "+uwr.error);
                            }
                            else{
                                Debug.Log(uwr.downloadHandler.text);
                               
                            }   */
                            StartCoroutine(coroutine2());

                            if(current!=null){
                              
                                current.transform.position=new Vector3(0,0,-100);
                                Destroy(GameObject.Find("MARK"+hitInfo.transform.gameObject.name));
                            }
                            
                            current=null;
                            show.flag=0;
                        }
                    }
                    
                
              }
            }
            
        }

        }
     } 
    
     public string fixJson(string value)
    {

    value = "{\"Items\":" + value + "}";

    return value;

    }

    IEnumerator coroutine1(){
                        
                        
                        //MarkingLots mObj2 = new MarkingLots();
                        deleteMark mObj2 = new deleteMark();
                        mObj2.ParkingLotID=hitInfo.transform.gameObject.name;
                      
                       // Debug.Log("BAKKK"+hitInfo.transform.gameObject.name+" vee"+mObj2.ParkingLotID);
                        string json2 = JsonUtility.ToJson(mObj2);
                        string url2="https://smart-car-park-api.appspot.com/marking/handleMarking/"+Login.apiKey.Replace("\"","");
                        Debug.Log(Login.apiKey);
                        Debug.Log(url2);
                        var uwr2 = new UnityWebRequest(url2, "POST");
                        byte[] jsonToSend2 = new System.Text.UTF8Encoding().GetBytes(json2);
                        uwr2.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend2);
                        uwr2.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
                        uwr2.SetRequestHeader("Content-Type", "application/json");

                        yield return uwr2.SendWebRequest();

                        if (uwr2.isNetworkError){
                                Debug.Log("giderken hata oldu "+uwr2.error);
                        }
                        else{
                                Debug.Log(uwr2.downloadHandler.text);
                               
                        }

                         yield return new WaitForSeconds(5);
                           
    }
    IEnumerator coroutine2(){
                           deleteMark mObj = new deleteMark();
                            mObj.ParkingLotID=hitInfo.transform.gameObject.name;
                            //string delete=hitInfo.transform.gameObject.name;
                            Debug.Log("BASILAN "+hitInfo.transform.gameObject.name);
                           // Debug.Log("current "+current.transform.name);
                            string json = JsonUtility.ToJson(mObj);
                            Debug.Log("jsonhali"+json);
                            string url="https://smart-car-park-api.appspot.com/marking/deleteMarking/"+Login.apiKey.Replace("\"","");
                            var uwr = new UnityWebRequest(url, "DELETE");
                            byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(json);
                            uwr.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend);
                            uwr.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
                            uwr.SetRequestHeader("Content-Type", "application/json");

                            yield return uwr.SendWebRequest();

                            if (uwr.isNetworkError){
                                Debug.Log("giderken hata oldu "+uwr.error);
                            }
                            else{
                                Debug.Log(uwr.downloadHandler.text);
                               
                            } 
                             yield return new WaitForSeconds(5);
    }
}
