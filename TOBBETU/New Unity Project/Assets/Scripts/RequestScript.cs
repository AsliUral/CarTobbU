using UnityEngine;
using UnityEditor;
using System;
using System.Collections.Generic;
using System.Collections;
using UnityEngine.Networking;
public class RequestScript : MonoBehaviour{
ParkingLots[] parkingLotsArray;
Cars[] carsArray;
public GameObject car;
private List<GameObject> carList;

    public void Start(){
       
        StartCoroutine(coroutine());
    }
    
    public IEnumerator coroutine(){
        carList=new List<GameObject>();
        GameObject thisObj;
        Transform pos;
        while (true){
          
            UnityWebRequest www = UnityWebRequest.Get("https://smart-car-park-api.appspot.com/parkingLots");
            UnityWebRequest www2 = UnityWebRequest.Get("https://smart-car-park-api.appspot.com/cars");

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
               
                
                string str = www.downloadHandler.text;
                string str2= www2.downloadHandler.text;
                string jsonString = fixJson(str);
                string jsonString2 = fixJson(str2);
                parkingLotsArray = JsonHelper.FromJson<ParkingLots>(jsonString);
                carsArray = JsonHelper.FromJson<Cars>(jsonString2);
                float count=0;
                foreach ( ParkingLots lot in parkingLotsArray){
                    thisObj=GameObject.Find(lot.ParkingLotID);
                
                  if(thisObj!=null){
                    pos=thisObj.transform;
                    string nameObj=thisObj.gameObject.name;
                    var cubeRenderer = thisObj.GetComponent<Renderer>();

                    if((lot.ParkingLotStatus+"").Equals("Available")){
                        cubeRenderer.material.SetColor("_Color", Color.green);
                            string cn="CAR"+lot.ParkingLotID+"(Clone)";
                            GameObject ex=GameObject.Find(cn);
                            if(ex!=null){
                               Destroy(ex);

                            }
                        
                    }else if(lot.ParkingLotStatus.Equals("Occupied") ){
                        cubeRenderer.material.SetColor("_Color", Color.red);
                    
                        
                      
                        foreach(Cars personCar in carsArray){

                          if(GameObject.Find("CAR"+lot.ParkingLotID)==null){
                            //Transform t=Instantiate(pos);
                            //t.Rotate(0.0f, -90.0f, 0.0f);
                            Color newColor=Color.clear;
                            Color carColorP=Color.clear;
                            GameObject newCar = Instantiate(car,pos.position + new Vector3(0,(float)0.1,0),pos.rotation);
                            newCar.transform.Rotate(0.0f, -90.0f, 0.0f);
                            create(newCar,Color.green,lot.ParkingLotID); 
                            newColor=Color.clear;
                            count++;
                          
                          }  
                            
                             
                                
                        }
    
                             //Debug.Log( lot.ParkingLotID +" ve "+ personCar.CurrentParkingLot+" ve "+ personCar.PersonID);
                            /*if(lot.ParkingLotID.Equals("y15") && personCar.CurrentParkingLot.Equals("y15") &&  personCar.PersonID.Equals("10") ){
                                
                                //Debug.Log("IDDD "+lot.ParkingLotID);
                               // Debug.Log("NAME COLOR "+personCar.CarColor);
                                ColorUtility.TryParseHtmlString (personCar.CarColor, out carColorP);
                               // Debug.Log("car COLOR "+carColorP);
                                newColor=carColorP;
                               // Debug.Log("ıd y15 "+ lot.ParkingLotID+ " newColor"+ newColor+ personCar.CarColor);
                                Instantiate(create(car,Color.green,lot.ParkingLotID),pos.position + new Vector3(0,(float)0.1,0),t.rotation);
                                
                            }else if(!lot.ParkingLotID.Equals("y15") && personCar.CurrentParkingLot.Equals("") ){
                                //Debug.Log("ıd diger "+ lot.ParkingLotID);
                                Instantiate(create(car,Color.yellow,lot.ParkingLotID),pos.position + new Vector3(0,(float)0.1,0),t.rotation);

                            }*/
                           
                       
                    
                    }
                    
                }

                }
              
                     
                
        
            }
         //   Array.Clear(parkingLotsArray,0,parkingLotsArray.Length);
          //  Array.Clear(carsArray,0,carsArray.Length);
            yield return new WaitForSeconds(5);
        }
    

    string fixJson(string value)
{
    value = "{\"Items\":" + value + "}";
    return value;
}
    GameObject create(GameObject newCar,Color col,string id){
       
       //car.GetComponent<Renderer>().sharedMaterial.SetColor("_Color",color);
        
       //newCar.gameObject.GetComponent<Renderer>().material = Instantiate(origin.gameObject.GetComponent<Renderer>().material);
        //newCar.GetComponent<Renderer>().material.SetColor("_Color",color);
       MaterialPropertyBlock props = new MaterialPropertyBlock();
       props.AddColor("_Color", col);
       newCar.GetComponent<Renderer>().SetPropertyBlock(props);
       newCar.GetComponent<Renderer>().material.SetColor("_Color",col);
        //newCar.SetColor(col);
        string n=id;
        newCar.transform.name ="CAR"+id;
        string s="CAR"+id;
        //GameObject go = GameObject.Find(s);
       // go.GetComponent<MeshRenderer>().material.color = col;
      //  Debug.Log("yeni obj "+ newCar.transform.name + " rengi  "+ col.ToString());
        carList.Add(newCar);
        
        return newCar;
    }
    }
}


