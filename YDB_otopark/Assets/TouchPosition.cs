using UnityEngine;
using System.Collections;
using UnityEngine.UIElements;

public class TouchPosition : MonoBehaviour
{
 
    private Transform pos;
    public GameObject mark;
   public GameObject obj;

    // Update is called once per frame
    void Update()
    {
        if(Input.GetMouseButtonDown(0)){
            Destroy(obj);
            var ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            RaycastHit hitInfo;
            if(Physics.Raycast(ray, out hitInfo)){
                var rig = hitInfo.collider.GetComponent<Rigidbody>();
                pos = hitInfo.collider.gameObject.transform;
                if(pos != null){
                    obj = Instantiate(mark,pos.position + new Vector3(0,(float)0.60,0),pos.rotation);
                    obj.transform.Rotate(90,90,0);
                }

            }
            
        }
        
    }
}
