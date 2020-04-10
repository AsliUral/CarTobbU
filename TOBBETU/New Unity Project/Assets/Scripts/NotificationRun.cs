using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.Notifications.Android;
using UnityEngine.Networking;

public class NotificationRun : MonoBehaviour
{
   string content=">";
   int a=0;
   //public const string carEmo = "🚗";
   public const string carEmo = "🚙";
   public const string tickEmo = "✅";
   public const string xEmo = "❌";
   public const string cryEmo = "😢";
   public const string yesEmo = "👍";


   void Start(){

       CreateNotifChannel();
       SendNotification();
   }
   
   void CreateNotifChannel(){

       var c = new AndroidNotificationChannel(){

           Id = "notif1",
           Name = "AvailableParkLots",
           Importance = Importance.High,
           Description = "Shows the available parking lots number to User",

       };
       
       AndroidNotificationCenter.RegisterNotificationChannel(c);

   }

   void SendNotification(){
   

    if(MainMenu.num>0){

       var notification1 = new AndroidNotification();
       notification1.Title = "Current Available Lots";
       notification1.Text = "Available parking lots: "+MainMenu.num+yesEmo+carEmo;
       notification1.FireTime = System.DateTime.UtcNow.AddSeconds(1);
       notification1.LargeIcon = "icon_1";

        AndroidNotificationCenter.SendNotification(notification1,"notif1");

    }else{

       var notification2 = new AndroidNotification();
       notification2.Title = "Current Available Lots";
       notification2.Text = "Sorry"+cryEmo+" , all parking lots full!"+xEmo+carEmo;
       notification2.FireTime = System.DateTime.UtcNow.AddSeconds(1);
       notification2.LargeIcon = "icon_2";

       AndroidNotificationCenter.SendNotification(notification2,"notif1");
    }
      

      


          

   }

   
}
