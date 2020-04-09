using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public enum LaneOrder
{
    firstLane,
    secondLane,
    thirdLane,
    forthLane,
    fifthLane,
    sixthLane,
    seventhLane
}


public class PathFinder : MonoBehaviour
{
    public Camera cam;
    public NavMeshAgent pathAgent;
    public LineRenderer navigationLine;
    public bool clicked = false;
    public Vector3 initialPos;
    public GameObject pathDescriptor;
    public float respawnTime;
    public List<Vector3> pathCorners;

    // Start is called before the first frame update
    void Start()
    {
        respawnTime = 0.5f;
        pathCorners = new List<Vector3>();

        navigationLine = this.GetComponent<LineRenderer>();

        if (navigationLine == null)
        {
            Debug.Log("Line object created!");
            navigationLine = this.gameObject.AddComponent<LineRenderer>();
            navigationLine.material.color = Color.blue;
            navigationLine.startWidth = 0.4f;
            navigationLine.endWidth = 0.4f;
            navigationLine.startColor = Color.blue;
            navigationLine.endColor = Color.blue;
        }
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);

            RaycastHit hit;

            if (Physics.Raycast(ray, out hit))
            {
                clicked = true;
                Debug.Log("Hit!");
                Vector3 hitPoint = new Vector3(hit.point.x, hit.point.y, hit.point.z);
                GenerateAgentPath(hitPoint);
                DrawLine();
                MoveTowardParkingSpot(hit.point);
                GetVoiceNavigation(pathAgent);

            }
            else
            {
                Debug.Log("Not hit!");
            }
        }

        if (clicked)
        {
            StartCoroutine(YieldPathDescriptor());
        }

    }

    public void GenerateAgentPath(Vector3 hitPointVector)
    {
        Debug.Log("GenerateAgentPath()");
        Vector3 initialAgentPosition = pathAgent.transform.position;

        float initialY = initialAgentPosition.y;
        //beginning of the path
        pathCorners.Add(initialAgentPosition);
        pathCorners.Add(new Vector3(179.2f, initialY, -33.93f));

        float xDifference = hitPointVector.x - initialAgentPosition.x;
        float zDifference = hitPointVector.z - initialAgentPosition.z;

        // YDB OTOPARK SECILDI
        if (zDifference > 0)
        {
            print("YDB SEÇİLDİ");
            pathCorners.Add(new Vector3(174.59f, initialY, -32.94f));
            pathCorners.Add(new Vector3(174.59f, initialY, -24.3f));

            if (172.1 <= hitPointVector.x && hitPointVector.x <= 176.19)
            {
                pathCorners.Add(new Vector3(174.15f, initialY, hitPointVector.z));
            }
            else if (176.44 <= hitPointVector.x && hitPointVector.x <= 180.89)
            {
                pathCorners.Add(new Vector3(178.7f, initialY, -22.73f));
                pathCorners.Add(new Vector3(178.7f, initialY, hitPointVector.z));
            }
            else if(180.51 <= hitPointVector.x && hitPointVector.x <= 183.82)
            {
                pathCorners.Add(new Vector3(183.28f, initialY, -21.76f));
                pathCorners.Add(new Vector3(183.28f, initialY, hitPointVector.z));
            }
            else
            {
                print("Burada park yeri bulunmuyor.");
            }

        }

    }

    public void CreatePathDescriptor()
    {
        Debug.Log("CreatePathDescriptor()");
        GameObject go = Instantiate(pathDescriptor) as GameObject;
        go.transform.position = pathAgent.transform.position;
    }

    IEnumerator YieldPathDescriptor()
    {
        Debug.Log("YieldPathDescriptor()");
        while (true)
        {
            yield return new WaitForSeconds(respawnTime);
            CreatePathDescriptor();
        }
    }

    public void DrawLine()
    {
        Debug.Log("DrawLine()");
        navigationLine.positionCount = pathCorners.Count;
        for (int i = 0; i < pathCorners.Count; i++)
        {
            navigationLine.SetPosition(i, pathCorners[i]);
        }
    }


    public void MoveTowardParkingSpot(Vector3 toVector)
    {
        pathAgent.transform.position += Vector3.Slerp(pathAgent.transform.position, toVector, 0.2f);
    }

    public void InitializeSelectedClick()
    {
        buttonClicked = true;
    }

    public void MoveOnSelectedClick()
    {
        for(int i = 0; i < pathCorners.Count; i++)
        {
            MoveTowardParkingSpot(pathCorners[i]);
        }
    }

    public void ResetClickedPath()
    {
        buttonClicked = false;
        buttonResetted = true;
    }

    public void InitializeShortestClick()
    {

    }

    public void MoveOnShortestClick()
    {

    }

    public void ResetShortestPath()
    {

    }

    public void GetVoiceNavigation(NavMeshAgent agent)
    {
        print(agent.transform.position);
        // will return voice navigation by System.Speech;
        // the key point here is that creating true string to be read by system
    }

    public Transform getClosestParkingSpot(Transform[] spots)
    {
        Transform tMin = null;
        float minDist = Mathf.Infinity;
        Vector3 currentPos = pathAgent.transform.position;
        foreach (Transform t in spots)
        {
            float dist = Vector3.Distance(t.position, initialPos);
            if (dist < minDist)
            {
                tMin = t;
                minDist = dist;
            }
        }
        print(tMin);
        return tMin;
    }
}
