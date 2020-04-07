using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public enum ParkArea
{
    none,
    middleSpace,
    technologyCenter,
}

public class LocationService : MonoBehaviour
{
    private double middleParkLocation = 32.799809;
    private double technologyCenterLocation = 32.800266;

    private LocationInfo userLocation;

    IEnumerator Start()
    {
        // First, check if user has location service enabled
        if (!Input.location.isEnabledByUser)
            yield break;

        // Start service before querying location
        Input.location.Start();

        // Wait until service initializes
        int maxWait = 20;
        while (Input.location.status == LocationServiceStatus.Initializing && maxWait > 0)
        {
            yield return new WaitForSeconds(1);
            maxWait--;
        }

        // Service didn't initialize in 20 seconds
        if (maxWait < 1)
        {
            print("Timed out");
            yield break;
        }

        // Connection has failed
        if (Input.location.status == LocationServiceStatus.Failed)
        {
            print("Unable to determine device location");
            yield break;
        }
        else
        {
            // Access granted and location value could be retrieved
            print("Location: " + Input.location.lastData.latitude + " " + Input.location.lastData.longitude + " " + Input.location.lastData.altitude + " " + Input.location.lastData.horizontalAccuracy + " " + Input.location.lastData.timestamp);
            userLocation = Input.location.lastData;
            
        }

        // Stop service if there is no need to query location updates continuously
        Input.location.Stop();
    }

    public ParkArea GetLocationInformation()
    {
        if (userLocation.latitude >= 32.799809 && userLocation.latitude <= 32.799809)
        {
            Debug.Log("Sadece ara otoparka parkedebilirsiniz!");
            return ParkArea.middleSpace;
        }
        else if (userLocation.latitude >= 32.799809 && userLocation.latitude <= 32.799809)
        {
            Debug.Log("Teknoloji Merkezine parkedebilirsiniz!");
            return ParkArea.technologyCenter;
        }
        else
        {
            Debug.Log("You are not in the parking area!");
            return ParkArea.none;
        }

    }

}
