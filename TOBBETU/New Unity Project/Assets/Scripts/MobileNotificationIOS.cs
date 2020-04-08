using System.Collections;
using System;
using System.Collections.Generic;
using UnityEngine;
#if UNITY_IOS
using Unity.Notification.iOS;
#endif

public class MobileNotificationIOS : MonoBehaviour
{
  #if UNITY_IOS
    public string notificationID = "test_notification";
    private int identifier;
    // Start is called before the first frame update
    private void Start()
    {
        iOSNotificationTimeIntervalTrigger timeTrigger = new iOSNotificationTimeIntervalTrigger();
        {
            TimeInterval = new TimeSpan(0,0,10);
            Repeats = false;
        };

        iOSNotificationCalendarTrigger calendarTrigger = new iOSNotificationCalendarTrigger()
        {
            Hour = 12,
            Minute = 0,
            Repeats = false;
        };

        iOSNotificationLocationTrigger locationTrigger = new iOSNotificationLocationTrigger()
        {
          //bak buraya
        };

        iOSNotification notification = new iOSNotification(){
            identifier = "test_notification",
            Title = "Test Notification!",
            Subtitle = "A Unity CarTOBBU Test Notification",
            Body = "This is a test notification",
            ShowInForeground = true;
            ForegroundPresentationOption = (PresentationOption.Alert | PresentationOption.Sound),
            CategoryIdentifier = "category_a",
            ThreadIdentifier = "thread1",
            Trigger = timeTrigger,

        };

        iOSNotificationCenter.ScheduleNotification(notification);

        iOSNotificationCenter.OnRemoteNotificationReceived += receivedNotification =>
        {
            Debug.Log("Received notification" + notification.identifier+"!");
        };

        iOSNotification notificationIntentData = iOSNotificationCenter.GetLastRespondedNotification();

        if(notificationIntentData != null){
            Debug.Log("App was opened with notification!");
        }

    }

    private void OnApplicationPause(bool pause){

        iOSNotificationCenter.RemoveScheduledNotification(notificationId);

        iOSNotificationCenter.RemoveDeliveredNotification(notificationId);
    }

    #endif

}
