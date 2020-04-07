using System.Collections;
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using Assets.SimpleAndroidNotifications;

public class Notify : MonoBehaviour
{
    ParkingLots[] availableLotsArray;
    private List<ParkingLots> lots;
    private string title = "Notification Title";
    public string content = "Content";
    float currentTime;
    float startTime;
    float finishTime;
    public const string cryEmo = "😭";
    public const string sillyEmo = "😜";
    public const string flushedEmo = "😳";
    public const string blushEmo = "😊";
    public const string smirkEmo = "😏";
    public const string grinEmo = "😁";
    public const string sleepyEmo = "😪";

   void OnApplicationPause(bool isPause){

      #if UNITY_ANDROID

      NotificationManager.CancelAll();

      if(isPause){
        
        DateTime timeToNotify = DateTime.Now.AddMinutes(86400);
        TimeSpan time = timeToNotify - DateTime.Now;
        
      if (System.DateTime.Now.DayOfWeek == System.DayOfWeek.Monday){
          content="Today is tuesday!"+flushedEmo+" How about checking the TOBB ETU paeking lots?";
          NotificationManager.SendWithAppIcon(time, title, content, Color.red, NotificationIcon.Bell);
      }else if(System.DateTime.Now.DayOfWeek == System.DayOfWeek.Tuesday){
          content="Today is wednesday!"+blushEmo+" How about checking the TOBB ETU paeking lots?";
          NotificationManager.SendWithAppIcon(time, title, content, Color.red, NotificationIcon.Bell);
      }else if(System.DateTime.Now.DayOfWeek == System.DayOfWeek.Wednesday){
          content="Today is thursday!"+smirkEmo+" How about checking the TOBB ETU paeking lots?";
          NotificationManager.SendWithAppIcon(time, title, content, Color.red, NotificationIcon.Bell);
      }else if(System.DateTime.Now.DayOfWeek == System.DayOfWeek.Thursday){
          content="Today is friday!"+sillyEmo+" How about checking the TOBB ETU paeking lots?";
          NotificationManager.SendWithAppIcon(time, title, content, Color.red, NotificationIcon.Bell);
      }else if(System.DateTime.Now.DayOfWeek == System.DayOfWeek.Friday){
          content="Today is saturday!"+grinEmo+" How about checking the TOBB ETU paeking lots?";
          NotificationManager.SendWithAppIcon(time, title, content, Color.red, NotificationIcon.Bell);
      }else if(System.DateTime.Now.DayOfWeek == System.DayOfWeek.Saturday){
          content="Today is sunday!"+sleepyEmo+" How about checking the TOBB ETU paeking lots?";
          NotificationManager.SendWithAppIcon(time, title, content, Color.red, NotificationIcon.Bell);
      }else if(System.DateTime.Now.DayOfWeek == System.DayOfWeek.Sunday){
          content="Today is monday!"+cryEmo+" How about checking the TOBB ETU paeking lots?";
          NotificationManager.SendWithAppIcon(time, title, content, Color.red, NotificationIcon.Bell);
      }

       
        
      }
    

      #endif
  }

}
