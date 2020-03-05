using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
public class addMarker : MonoBehaviour
{

    public GameObject marker;
	public GameObject obj;
	private Transform pos;
   

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
                    obj = Instantiate(marker,pos.position + new Vector3(0,(float)0.40,0),pos.rotation);
                   
                }

            }

        }

    }


}
