using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;


public class show : MonoBehaviour
{

    public GameObject marker;
    public static float flag=0;
    public static string markObj;
    public static string id;
    public static GameObject sendObject;
    public GameObject obj;
    // Start is called before the first frame update
    void Start()
    {
         StartCoroutine(coroutine());
    }

    // Update is called once per frame
    public IEnumerator coroutine()
    {
      
        while(true){
            UnityWebRequest www = UnityWebRequest.Get("https://smart-car-park-api.appspot.com/marking");
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
                            flag=1;
                            obj= Instantiate(marker,m.transform.position + new Vector3(0,(float)0.60,0),m.transform.rotation);
                            obj.transform.Rotate(90,0,0);
                            obj.transform.name="MARK"+marking.ParkingLotID;
                            id=marking.ParkingLotID;
                            markObj=obj.transform.name;
                            sendObject=obj;
                           
                        }
                        if(flag==0){
                            obj.transform.position=new Vector3(0,0,-100);
                            Destroy(GameObject.Find("MARK"+id));
                        }
                    }
                }
                
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
