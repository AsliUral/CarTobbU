using System.Collections;
using System.Collections.Generic;
using UnityEngine;
public struct LineDrawer
{
    private LineRenderer lineRenderer;
    private float lineSize;

    public LineDrawer(float lineSize = 0.2f)
    {
        GameObject lineObj = new GameObject("LineObj");
        lineRenderer = lineObj.AddComponent<LineRenderer>();
        //Particles/Additive
        lineRenderer.material = new Material(Shader.Find("Hidden/Internal-Colored"));

        this.lineSize = lineSize;
    }

    private void init(float lineSize = 0.2f)
    {
        if (lineRenderer == null)
        {
            GameObject lineObj = new GameObject("LineObj");
            lineRenderer = lineObj.AddComponent<LineRenderer>();
            //Particles/Additive
            lineRenderer.material = new Material(Shader.Find("Hidden/Internal-Colored"));

            this.lineSize = lineSize;
        }
    }

    //Draws lines through the provided vertices
    public void DrawLineInGameView(Vector3 start, Vector3 end, Color color)
    {
        if (lineRenderer == null)
        {
            init(0.2f);
        }
    }
}
public class findClosest : MonoBehaviour
{
    // Start is called before the first frame update

public Lot to;
 public LineDrawer lineDrawer;
 void Start()
    {
    Update();
    lineDrawer = new LineDrawer();
    lineDrawer.DrawLineInGameView(this.transform.position,to.transform.position,Color.green);
    }
    void Update()
    {
        FindClosestLot();
    }

    // Update is called once per frame
    void FindClosestLot()
    {
        float distanceToClosestLot = Mathf.Infinity;
        Lot closestLot = null;
        Lot [] allLots  = GameObject.FindObjectsOfType<Lot>();

        foreach (Lot currentLot in allLots) {
            float distanceToLot = (currentLot.transform.position-this.transform.position).sqrMagnitude;
            if(distanceToLot < distanceToClosestLot){
                distanceToClosestLot = distanceToLot;
                closestLot = currentLot;
            }
        }
     
     to=closestLot;
     Debug.DrawLine(this.transform.position,closestLot.transform.position,Color.green, 2f,false);
    }

}



 



