using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
public class Registration : MonoBehaviour{
    public InputField nameField;
    public InputField passwordField;
    public Button submitButton;

    public void CallRegister(){
        StartCoroutine(Register());
    }
    IEnumerator Register(){
        WWWForm form = new WWWForm();
        form.AddField("name", nameField.text);
        form.AddField("password", passwordField.text);


        //make a call to a url
        WWW www = new WWW("http://localhost:3000/",form);
        yield return www;
        if(www.text == "0"){ //no errors
            Debug.Log("User created succesfully");
            UnityEngine.SceneManagement.SceneManager.LoadScene(1);  

        }
        else{ //error
            Debug.Log("User creation failed. Error " + www.text);
        }
    }

    public void VerifyInputs(){
        submitButton.interactable = (nameField.text.Length >= 8 && passwordField.text.Length >=8);


    }


}
