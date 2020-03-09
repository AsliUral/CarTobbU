using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
public class Registration : MonoBehaviour
{
    public InputField nameField;
    public InputField passwordField;
    public Button submitButton;


    public void CallRegister(){
        StartCoroutine(Register());
    
    }

    IEnumerator Register(){
        //acces db UPDATE LATER
        
        WWWForm form = new WWWForm();
        form.AddField("name", nameField.text);
        form.AddField("password", passwordField.text);
        WWW www = new WWW("http://localhost/register",form); 
        yield return www;
        
        if(www.text == "0"){
            //www.text=0 means there were no errors
            Debug.Log("user created successfully");
            UnityEngine.SceneManagement.SceneManager.LoadScene(0);
        }
        else{
            Debug.Log("user creation failed. Error #"+www.text);
        }
    }

    public void VerifyInputs(){
        submitButton.interactable = (nameField.text.Length >=8 && passwordField.text.Length >= 8);
        //submitButton.interactable = buraya dbde bu isim var mi yok mu KONTROLU
    }
}
