using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class carExitTrigger : MonoBehaviour
{
    public Animator carExitAnim;
    // Start is called before the first frame update
    void Start()
    {
        carExitAnim = GetComponent<Animator>();
    }

    // Update is called once per frame
    void Update()
    {
        if(Input.GetKeyDown("1"))
        {
            carExitAnim.Play("carExit");
        }
    }
}
