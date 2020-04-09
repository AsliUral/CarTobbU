using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ButtonController : MonoBehaviour
{

    PathFinder finder;
    GameObject agent;
    GameObject text;

    bool selectedButtonClicked = false;
    bool shortestButtonClicked = false;
    // Start is called before the first frame update
    void Start()
    {
        text = GameObject.FindGameObjectWithTag("DialogText");
        
        text.SetActive(false);
        agent = GameObject.FindGameObjectWithTag("PathAgent");
        if (agent != null)
        {
            finder = agent.GetComponent<PathFinder>();
            if (finder == null)
            {
                Debug.Log("Could not initialize component!");
            }
        }
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void InitializeSelectedClick()
    {
        if (selectedButtonClicked == true)
        {
            selectedButtonClicked = false;
            text.SetActive(false);
        }
        else
        {
            selectedButtonClicked = true;
            text.SetActive(true);
            finder.InitializeSelectedClick();
            finder.MoveOnSelectedClick();
            Debug.Log("Equalized true");
            
        }

    }


}
