using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ColorChanger : MonoBehaviour
{
    private MeshRenderer meshRenderer;
    

    private void OnEnable()
    {
        meshRenderer =GetComponent<MeshRenderer>();
    }

    public void SetColor(Color newColor)
    {
        meshRenderer.material.color = newColor;
    }
}