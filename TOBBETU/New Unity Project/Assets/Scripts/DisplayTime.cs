using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
public class DisplayTime : MonoBehaviour
{
    public GameObject theDisplay;
    public int seconds;
    public int hour;
    public int minutes;
    // Start is called before the first frame update
    void Start()
    {
        
        
    }

    // Update is called once per frame
    void Update()
    {
        hour=System.DateTime.Now.Hour;
        seconds=System.DateTime.Now.Second;
        minutes=System.DateTime.Now.Minute;
        theDisplay.GetComponent<Text>().text="   Hi!"+"\n"+hour+":"+minutes+":"+seconds;
        
    }
}
