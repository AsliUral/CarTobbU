using System.Collections;
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;

public class Login : MonoBehaviour
{
    [Serializable]
    public class User{
        public string username;
        public string password;
    }
    public InputField nameField;
    public InputField passwordField;
    public Button submitButton;

    public void CallLogin(){
        StartCoroutine(LoginUser());
    }

    IEnumerator LoginUser(){
        User thisUser = new User();
        thisUser.username = nameField.text;
        thisUser.password = passwordField.text;
        string json = JsonUtility.ToJson(thisUser);

        var uwr = new UnityWebRequest("https://smart-car-park-api.appspot.com/user/login", "POST");
        byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(json);
        uwr.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend);
        uwr.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
         uwr.SetRequestHeader("Content-Type", "application/json");

        yield return uwr.SendWebRequest();

        if (uwr.isNetworkError){
            Debug.Log("giderken hata oldu "+uwr.error);
        }
        else{
            Debug.Log(uwr.downloadHandler.text);
            UnityEngine.SceneManagement.SceneManager.LoadScene(3);
        }
 

    }


    public void VerifyInputs(){
        submitButton.interactable = (nameField.text.Length>=8 && passwordField.text.Length>=8);
    }

    
}
