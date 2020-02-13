using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class cameraView : MonoBehaviour
{

    public Camera m_OrthographicCamera;
    float m_ViewPositionX, m_ViewPositionY, m_ViewWidth, m_ViewHeight;

    // Start is called before the first frame update
    void Start()
    {
        //This sets the Camera view rectangle to be in the bottom corner of the screen
        m_ViewPositionX = 0;
        m_ViewPositionY = 0;

        //This sets the Camera view rectangle to be smaller so you can compare the orthographic view of this Camera with the perspective view of the Main Camera
        m_ViewWidth = 0.4f;
        m_ViewHeight = 0.4f;

        //This enables the Camera (the one that is orthographic)
        m_OrthographicCamera.enabled = true;

        //If the Camera exists in the inspector, enable orthographic mode and change the size
        if (m_OrthographicCamera)
        {
            //This enables the orthographic mode
            m_OrthographicCamera.orthographic = true;
            //Set the size of the viewing volume you'd like the orthographic Camera to pick up (5)
            m_OrthographicCamera.orthographicSize = 5.0f;
            //Set the orthographic Camera Viewport size and position
            m_OrthographicCamera.rect = new Rect(m_ViewPositionX, m_ViewPositionY, m_ViewWidth, m_ViewHeight);
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
