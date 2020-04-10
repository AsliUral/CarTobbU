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

public enum WhichLot
{
    mid,
    tm
}

public class PathFinder : MonoBehaviour
{
    public Camera cam;
    public GameObject pathAgent;
    public LineRenderer navigationLine;
    public bool clicked = false;
    public Vector3 initialPos;
    public GameObject pathDescriptor;
    public float respawnTime;
    public List<Vector3> pathCorners;
    public List<GameObject> pathDescription;
    public bool buttonClicked;
    public bool buttonResetted;
    public bool buttonShortestPathClicked;
    public Vector3 currentPositionHolder;
    public int index = 0;
    // Start is called before the first frame update
    public string whichParkingLot = "tm";
    public int Timer;
    public bool lineDrawed;

    void Start()
    {
        lineDrawed = false;
        Timer = 0;
        pathAgent = GameObject.FindGameObjectWithTag("PathAgent");
        whichParkingLot = "tm";
        currentPositionHolder = pathAgent.transform.position;
        buttonClicked = false;
        buttonResetted = false;
        buttonShortestPathClicked = false;
        respawnTime = 0.5f;
        pathCorners = new List<Vector3>();

        navigationLine = this.GetComponent<LineRenderer>();

        if (navigationLine == null)
        {
            Debug.Log("Line object created!");
            navigationLine = this.gameObject.AddComponent<LineRenderer>();
            navigationLine.material.color = Color.blue;
            navigationLine.startWidth = 0.1f;
            navigationLine.endWidth = 0.1f;
            navigationLine.startColor = Color.blue;
            navigationLine.endColor = Color.blue;
        }

        if(whichParkingLot.Equals("mid"))
        {
            print("mid otoparktayım");
            cam.transform.position = new Vector3(206.8f, 6.63f, -1.78f);
            pathAgent.transform.position = new Vector3(196.75f, 0.89f, 13.7f);
        }
        else if(whichParkingLot.Equals("tm"))
        {
            print("tm otoparktayım");
            cam.transform.position = new Vector3(206.8f, 6.63f, -46.78f);
            pathAgent.transform.position = new Vector3(190.92f, 0.89f, -33.68f);
            print(pathAgent.transform.position);
        }
        else
        {
            print("bambaska bir yerdeyim, alisveristeyim!!");
        }
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            if (buttonClicked)
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
                    GameObject.Find("DialogText").GetComponent<UnityEngine.UI.Text>().text = "Seçtiğiniz yere yönlendirildiniz!";
                    //MoveOnPath();
                    //GetVoiceNavigation(pathAgent);
                    //StartCoroutine(MoveOnPath());

                }
                else
                {
                    Debug.Log("Not hit!");
                }
            }
            
        }


    }

    public void MovePlayer()
    {
        Timer += (int)(1.0 * Time.deltaTime);
        currentPositionHolder = pathCorners[index];
    }

    public void InitializeSelectedClick()
    {
        buttonClicked = true;
    }

    public void MoveOnSelectedClick()
    {
        
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
        print("Getting shortest available parking spot!");
        Transform t = GetClosestParkingSpot(availableSpots);
        GenerateAgentPath(t.position);
        DrawLine();
    }

    public void ResetShortestPath()
    {

    }

    public void ResetEverything()
    {
        ResetClickedPath();
        ResetShortestPath();
        navigationLine.SetVertexCount(0);
        pathCorners.Clear();
        for(int i = 0; i < pathDescription.Count; i++)
        {
            Destroy(pathDescription[i]);
        }
    }
    

    public void GenerateAgentPath(Vector3 hitPointVector)
    {
        

        // YDB OTOPARK SECILDI

        if (whichParkingLot.Equals("tm"))
        {
            Debug.Log("GenerateAgentPath() ----- TM");
            Vector3 initialAgentPosition = pathAgent.transform.position;

            float initialY = initialAgentPosition.y;
            //beginning of the path
            pathCorners.Add(initialAgentPosition);
            pathCorners.Add(new Vector3(179.2f, initialY, -33.93f));

            float xDifference = hitPointVector.x - initialAgentPosition.x;
            float zDifference = hitPointVector.z - initialAgentPosition.z;

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
                else if (180.51 <= hitPointVector.x && hitPointVector.x <= 183.82)
                {
                    pathCorners.Add(new Vector3(183.28f, initialY, -21.76f));
                    pathCorners.Add(new Vector3(183.28f, initialY, hitPointVector.z));
                }
                else
                {
                    print("Burada park yeri bulunmuyor.");
                }

            }
            else // TM OTOPARK SECILDI
            {
                print("TM SECİLDİ!");
                Vector3 middleCorner;
                // end of the path
                if (152.46f <= hitPointVector.x && hitPointVector.x <= 156.57)
                {
                    pathCorners.Add(new Vector3(154.86f, initialY, initialAgentPosition.z));
                    pathCorners.Add(new Vector3(154.86f, initialY, hitPointVector.z));
                }
                else if (156.79 <= hitPointVector.x && hitPointVector.x <= 160.25)
                {
                    pathCorners.Add(new Vector3(158.57f, initialY, initialAgentPosition.z));
                    pathCorners.Add(new Vector3(158.57f, initialY, hitPointVector.z));
                }
                else if (160.47 <= hitPointVector.x && hitPointVector.x <= 163.86)
                {
                    pathCorners.Add(new Vector3(162.23f, initialY, initialAgentPosition.z));
                    pathCorners.Add(new Vector3(162.23f, initialY, hitPointVector.z));
                }
                else if (164.03 <= hitPointVector.x && hitPointVector.x <= 167.33)
                {
                    pathCorners.Add(new Vector3(165.5f, initialY, initialAgentPosition.z));
                    pathCorners.Add(new Vector3(165.5f, initialY, hitPointVector.z));
                }
                else if (167.58f <= hitPointVector.x && hitPointVector.x <= 171.02)
                {
                    pathCorners.Add(new Vector3(169.33f, initialY, initialAgentPosition.z));
                    pathCorners.Add(new Vector3(169.33f, initialY, hitPointVector.z));
                }
                else if (173.45f <= hitPointVector.x && hitPointVector.x <= 176.93f)
                {
                    pathCorners.Add(new Vector3(175.17f, initialY, initialAgentPosition.z));
                    pathCorners.Add(new Vector3(175.17f, initialY, hitPointVector.z));
                }
                else if (164.03 <= hitPointVector.x && hitPointVector.x <= 167.33)
                {
                    pathCorners.Add(new Vector3(165.5f, initialY, initialAgentPosition.z));
                    pathCorners.Add(new Vector3(165.5f, initialY, hitPointVector.z));
                }
                else if (177.15f <= hitPointVector.x && hitPointVector.x <= 180.7)
                {
                    pathCorners.Add(new Vector3(178.97f, initialY, initialAgentPosition.z));
                    pathCorners.Add(new Vector3(178.97f, initialY, hitPointVector.z));
                }
                else if (180.9 <= hitPointVector.x && hitPointVector.x <= 184.27)
                {
                    pathCorners.Add(new Vector3(179.12f, initialY, -51.81f));
                    pathCorners.Add(new Vector3(182.66f, initialY, -51.81f));
                    pathCorners.Add(new Vector3(182.66f, initialY, hitPointVector.z));
                }
                else if (184.48 <= hitPointVector.x && hitPointVector.x <= 187.99)
                {
                    pathCorners.Add(new Vector3(179.12f, initialY, -51.81f));
                    pathCorners.Add(new Vector3(186.28f, initialY, -51.81f));
                    pathCorners.Add(new Vector3(186.28f, initialY, hitPointVector.z));
                    pathCorners.Add(new Vector3(186.28f, initialY, hitPointVector.z));
                }
                else
                {
                    print("Tıkladığınız noktada bir park yeri yok!");
                }

                //pathCorners.Add(new Vector3(hitPointVector.x, initialY, initialAgentPosition.z));
            }

            pathCorners.Add(hitPointVector);
        }
        else if(whichParkingLot == "mid")
        {
            Debug.Log("GenerateAgentPath() ----- MID");
            Vector3 initialAgentPosition = pathAgent.transform.position;
            pathCorners.Add(initialAgentPosition);
            pathCorners.Add(new Vector3(hitPointVector.x, initialAgentPosition.y, initialAgentPosition.z));
            pathCorners.Add(hitPointVector);

        }
        else
        {
            print("destination is wrong!");
        }
        
    }

    

    public void CreatePathDescriptor()
    {
        Debug.Log("CreatePathDescriptor()");
        GameObject go = Instantiate(pathDescriptor) as GameObject;
        go.transform.position = new Vector3(pathAgent.transform.position.x,
                                            pathAgent.transform.position.y,
                                            pathAgent.transform.position.z);
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

        for (int i = 0; i < pathCorners.Count - 1; i++)
        {
            GameObject go = Instantiate(pathDescriptor) as GameObject;
            go.transform.position = new Vector3(pathCorners[i].x, pathCorners[i].y + 0.5f, pathCorners[i].z);
               
            if(pathCorners[i + 1].z < pathCorners[i].z && pathCorners[i + 1].x == pathCorners[i].x)
            {
                go.transform.Rotate(new Vector3(0.0f, -90.0f, 0.0f), Space.Self);
            }
            if (pathCorners[i + 1].z > pathCorners[i].z && pathCorners[i + 1].x == pathCorners[i].x)
            {
                go.transform.Rotate(new Vector3(0.0f, 90.0f, 0.0f), Space.Self);
            }
            if(pathCorners[i + 1].x > pathCorners[i].x)
            {
                go.transform.Rotate(new Vector3(0.0f, 135.0f, 0.0f), Space.Self);
            }

            pathDescription.Add(go);

        }

        lineDrawed = true;
    }
    

    public void MoveTowardParkingSpot(Vector3 toVector)
    {
        print("MoveTowardParkingSpot()");
        if(pathAgent.transform.position != toVector)
        {
            pathAgent.transform.position = Vector3.MoveTowards(pathAgent.transform.position,
                                                     toVector,
                                                     Timer);
        }
        else
        {
            print("index chagned!");
            MovePlayer();
        }
        
    }


    public void GetVoiceNavigation(NavMeshAgent agent)
    {
        print(agent.transform.position);
        // will return voice navigation by System.Speech;
        // the key point here is that creating true string to be read by system
    }

    public Transform GetClosestParkingSpot(Transform[] spots)
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
