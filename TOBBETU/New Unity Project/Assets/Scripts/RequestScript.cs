using UnityEngine;
using UnityEditor;
using System;
using System.Threading;
using System.Collections.Generic;
using System.Collections;
using System.Globalization;
using UnityEngine.Networking;
public class RequestScript : MonoBehaviour{
public static ParkingLots[] parkingLotsArray;
public string userType;
Cars[] carsArray;
public static int numAvailable;
public GameObject car;
private List<GameObject> carList;
private int count =0;
    public void Start(){
            Debug.Log("tttt"+DateTime.Now);
            StartCoroutine(check());
  
    }
    
    public IEnumerator coroutineStudent(){
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

                    foreach(ParkingLots s in parkingLotsArray){
                      if(s.SelectTime!=null && !s.SelectTime.Equals("")){
                        DateTime dtSelect = DateTime.Parse(s.SelectTime);
                        //DateTime dateValue;
                        //DateTime.TryParse(s.SelectTime, out dateValue);
                        //Debug.Log("gelen"+s.SelectTime);
                        //DateTime dateValue = parseTime(s.SelectTime);
                        //DateTime dateValue = DateTime.ParseExact(s.SelectTime, "dd.MM.yyyy HH:mm:ss",CultureInfo.InvariantCulture,DateTimeStyles.None);
                        DateTime dtNow = DateTime.Now;
                       // double diff = TimeDifferenceInMinutes(dtSelect,dtNow);
                        TimeSpan diff = dtNow - dtSelect;
                        int days = diff.Days;
                        int hours=diff.Hours;
                        int min=diff.Minutes;
                        int sec=diff.Seconds;
                        int sn = min*60+sec;

                        if(sn>=60){
                           StartCoroutine(deleteTime(s));
                           
                       }
                      }  
                       
                    }   
                       

                   
                    
                    thisObj=GameObject.Find(lot.ParkingLotID);
                
                  if(thisObj!=null){
                    pos=thisObj.transform;
                    string nameObj=thisObj.gameObject.name;
                    var cubeRenderer = thisObj.GetComponent<Renderer>();
                    if(lot.FirstPoint!=""){
                        
                    }
                    if((lot.ParkingLotStatus+"").Equals("Available") && (lot.SelectedStatus.Equals("") || lot.SelectedStatus.Equals("False"))){
                        if(!lot.ParkZoneName.Equals("Mid Car Park")){
                            cubeRenderer.material.SetColor("_Color", Color.green);
                        }
                        
                            numAvailable++;
                            string cn="CAR"+lot.ParkingLotID;
                            GameObject ex=GameObject.Find(cn);
                            if(ex!=null){
                               Destroy(ex);

                            }
                        
                    }else if((lot.ParkingLotStatus+"").Equals("Available") && lot.SelectedStatus.Equals("True")){
                        if(!lot.ParkZoneName.Equals("Mid Car Park")){
                            cubeRenderer.material.SetColor("_Color", Color.blue);
                        }

                    }else if(lot.ParkingLotStatus.Equals("Occupied") ){

                       if(!lot.ParkZoneName.Equals("Mid Car Park")){
                           cubeRenderer.material.SetColor("_Color", Color.red);
                       }
                        
                    
                        
                      
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
       props.SetColor("_Color", col);
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

    public IEnumerator coroutineLecturer(){
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

                    foreach(ParkingLots s in parkingLotsArray){
                      if(s.SelectTime!=null && !s.SelectTime.Equals("")){
                         //  Debug.Log("gelen"+s.SelectTime);
                        DateTime dtSelect = DateTime.Parse(s.SelectTime);
                        //Debug.Log("cevir"+dtSelect);
                       // DateTime dateValue;
                         // DateTime dateValue = parseTime(s.SelectTime);
                      //  DateTime.TryParse(s.SelectTime, out dateValue);
                      //  DateTime dateValue = DateTime.ParseExact(s.SelectTime,"dd.MM.yyyy HH:mm:ss",System.Globalization.CultureInfo.InvariantCulture,System.Globalization.DateTimeStyles.None);
                        DateTime dtNow = DateTime.Now;
                        //TimeSpan diff = dtNow.Subtract(dtSelect);
                       // double diff = TimeDifferenceInMinutes(dtSelect,dtNow);
                        TimeSpan diff = dtNow - dtSelect;
                         //Debug.Log("diff"+diff);
                        int days = diff.Days;
                        int hours=diff.Hours;
                        int min=diff.Minutes;
                        int sec=diff.Seconds;
                        int sn = min*60+sec;
                        if(sn>=60){
                            Debug.Log("girdik"+diff);
                            StartCoroutine(deleteTime(s));
                            
                       }
                      }  
                       
                    }   
                      
                    thisObj=GameObject.Find(lot.ParkingLotID);
                
                  if(thisObj!=null){
                    pos=thisObj.transform;
                    string nameObj=thisObj.gameObject.name;
                    var cubeRenderer = thisObj.GetComponent<Renderer>();
                
                    if((lot.ParkingLotStatus+"").Equals("Available") && (lot.SelectedStatus.Equals("") || lot.SelectedStatus.Equals("False"))){
                        cubeRenderer.material.SetColor("_Color", Color.green);
                            numAvailable++;
                            string cn="CAR"+lot.ParkingLotID;
                            GameObject ex=GameObject.Find(cn);
                            if(ex!=null){
                               Destroy(ex);

                            }
                        
                    }else if((lot.ParkingLotStatus+"").Equals("Available") && lot.SelectedStatus.Equals("True")){
                     
                            cubeRenderer.material.SetColor("_Color", Color.blue);
                       

                    }else if(lot.ParkingLotStatus.Equals("Occupied") ){
                        if(lot.SelectedStatus.Equals("True")){
                            StartCoroutine(deleteTime(lot));
                        }
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
       props.SetColor("_Color", col);
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

public IEnumerator check(){
  if(Login.apiKey!=null){
    string url1 = "https://smart-car-park-api.appspot.com/user/"+Login.apiKey.Replace("\"","");
    UnityWebRequest www1 = UnityWebRequest.Get(url1);
        yield return www1.SendWebRequest();
    if(www1.isNetworkError || www1.isHttpError){
                Debug.Log(www1.error);
                Debug.Log("HAATAAAAAAA");
                
    }else{
           
                
            string str = www1.downloadHandler.text;
            string[] typeArr;
            string type = "";
            string key = "";
            string[] strSplit = str.Split(',');
            for(var i=0; i<strSplit.Length; i++){
                if(strSplit[i].Contains("UserType")){
                    typeArr = strSplit[i].Split(':');
                    type = typeArr[1];
                  
                }
                if(strSplit[i].Contains("ApiKey")){
                    typeArr = strSplit[i].Split(':');
                    key = typeArr[1];
                }
            }
       
            if(key!="null"){
               
                if(type.Equals("\""+"Student"+"\"")){
                    userType="Student";
                }else{
                    userType="Acedemic";
                }
            }else{
                    userType= "Review";
            }
              Debug.Log("sadad"+userType);
      if(userType.Equals("Student")){
          if(System.DateTime.Now.DayOfWeek == System.DayOfWeek.Saturday || System.DateTime.Now.DayOfWeek == System.DayOfWeek.Sunday ){
              StartCoroutine(coroutineLecturer());
          }else{
              StartCoroutine(coroutineStudent());
          }
          
      }else if(userType.Equals("Acedemic")){
          Debug.Log("dasdsdadasdad abbbbbbb");
             StartCoroutine(coroutineLecturer());
      }else{
          //sadece bakacaklar icin guncelle
          //StartCoroutine(coroutineLecturer());
      }

            
    }

  }else{
      StartCoroutine(coroutineLecturer());
  }
    
 }
        IEnumerator deleteTime(ParkingLots lot){
                        
                        lot.SelectTime="";
                        SelectLot.flag=0;
                        lot.SelectedStatus="";
                        //MarkingLots mObj2 = new MarkingLots();
                        deleteMark mObj1 = new deleteMark();
                        setApiKey mObj2 = new setApiKey();
                        mObj2.ApiKey=null;
                        mObj1.ParkingLotID=lot.ParkingLotID;
                        string s1="";
                        STime sTime2 = new  STime();
                        sTime2.SelectTime="";
                       // Debug.Log("BAKKK"+hitInfo.transform.gameObject.name+" vee"+mObj2.ParkingLotID);
                        string json1 = JsonUtility.ToJson(s1);
                        string json2 = JsonUtility.ToJson(mObj2);
                        string json3 = JsonUtility.ToJson(sTime2);
                        string url3="https://smart-car-park-api.appspot.com/setSelectTime/"+mObj1.ParkingLotID;
                        var uwr3 = new UnityWebRequest(url3, "PUT");
                        byte[] jsonToSend3 = new System.Text.UTF8Encoding().GetBytes(json3);
                        uwr3.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend3);
                        uwr3.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
                        uwr3.SetRequestHeader("Content-Type", "application/json");
                        yield return uwr3.SendWebRequest();
                        string url1="https://smart-car-park-api.appspot.com/handleUnSelect/"+mObj1.ParkingLotID;
                        string url2="https://smart-car-park-api.appspot.com/setApiKey/"+mObj1.ParkingLotID;
                        Debug.Log(url1);
                        var uwr1 = new UnityWebRequest(url1, "PUT");
                        var uwr2 = new UnityWebRequest(url2, "PUT");
                        byte[] jsonToSend1 = new System.Text.UTF8Encoding().GetBytes(json1);
                        uwr1.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend1);
                        uwr1.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
                        uwr1.SetRequestHeader("Content-Type", "application/json");
                        byte[] jsonToSend2 = new System.Text.UTF8Encoding().GetBytes(json2);
                        uwr2.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend2);
                        uwr2.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
                        uwr2.SetRequestHeader("Content-Type", "application/json");
                       

                        yield return uwr1.SendWebRequest();
                        yield return uwr2.SendWebRequest();
                     

                        if (uwr1.isNetworkError){
                                Debug.Log("giderken hata oldu "+uwr1.error);
                        }else if(uwr2.isNetworkError){
                                Debug.Log("giderken hata oldu "+uwr2.error);
                        }else if(uwr3.isNetworkError){
                                Debug.Log("giderken hata oldu "+uwr3.error);
                        }else{
                                Debug.Log(uwr1.downloadHandler.text);
                               
                        }

                         
                           
    }

    public static double TimeDifferenceInMinutes(DateTime dateone, DateTime datetwo)
        {
            var duration = datetwo - dateone;
            return duration.TotalMinutes;
        }
    public DateTime parseTime(string s){
        //DateTime dateTime = new DateTime(2016, 7, 15, 3, 15, 0);
        //10.04.2020 00.48.50
        s.Replace(" ",".");
        string[] strSplit = s.Split(',');
        int a=0,b=0,c=0,d=0,e=0,f=0;
        for(int i=0;i<strSplit.Length;i++){
            Debug.Log("ay"+strSplit[i]);
            if(i==0){
                a=Int32.Parse(strSplit[i]);
            }else if(i==1){
                b=Int32.Parse(strSplit[i]);
            }else if(i==2){
                c=Int32.Parse(strSplit[i]);
            }else if(i==3){
                d=Int32.Parse(strSplit[i]);
            }else if(i==4){
                e=Int32.Parse(strSplit[i]);
            }else{
                f=Int32.Parse(strSplit[i]);
            }
        }
        DateTime time = new DateTime(a, b, c, d, e, f);
        Debug.Log("ceviri"+a+""+b+""+c+""+d+""+e+""+f);
        return time;
    }
}


