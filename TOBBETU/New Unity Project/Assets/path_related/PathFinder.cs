using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class NewBehaviourScript : MonoBehaviour
{
    public Camera cam;
    public NavMeshAgent pathAgent;
    public LineRenderer navigationLine;
    public bool clicked = false;
    public Vector3 initialPos;

    public List<Vector3> pathCorners;

    // Start is called before the first frame update
    void Start()
    {
        pathCorners = new List<Vector3>();

        navigationLine = this.GetComponent<LineRenderer>();
        if (navigationLine == null)
        {
            navigationLine = this.gameObject.AddComponent<LineRenderer>();
            navigationLine.SetWidth(1.0f, 1.0f);
            navigationLine.SetColors(Color.yellow, Color.yellow);
        }
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            clicked = true;
            Ray ray = cam.ScreenPointToRay(Input.mousePosition);

            RaycastHit hit;

            if (Physics.Raycast(ray, out hit))
            {
                Vector3 hitPoint = new Vector3(hit.point.x, hit.point.y, hit.point.z);
                GenerateAgentPath(hitPoint);
                //pathAgent.SetDestination(hit.point);
                //hit.transform.gameObject.name
                MoveTowardParkingSpot(hit.point);
                GetVoiceNavigation(pathAgent);
            }

        }

    }

    public void GenerateAgentPath(Vector3 hitPointVector)
    {
        
        Vector3 initialAgentPosition = pathAgent.transform.position;
        float initialY = initialAgentPosition.y;
        pathCorners.Add(initialAgentPosition);

        float xDifference = hitPointVector.x - initialAgentPosition.x;
        float zDifference = hitPointVector.z - initialAgentPosition.z;

        pathCorners.Add(new Vector3(hitPointVector.x, initialY, initialAgentPosition.z));
        pathCorners.Add(hitPointVector);
        pathCorners.Add(hitPointVector);


    }

    public void DrawLine()
    {

    }

    public void InstantiateObjetsOnLine()
    {

    }

    public void MoveTowardParkingSpot(Vector3 toVector)
    {

    }

    public void GetVoiceNavigation(NavMeshAgent agent)
    {
        
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
