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
    //public String apiKey{get; private set;}
    public static string apiKey;

    public Text message;
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
        
        //user needs to activate
        if(uwr.downloadHandler.text.Contains("Message")){
            Debug.Log("This user have not activated their account yet.");
            message.GetComponent<Text>().text = "Please activate your account.";
        }

        //user activated and can continue with parking scene
        else{
            Debug.Log(uwr.downloadHandler.text);
            string str = uwr.downloadHandler.text;
            string[] strSplit = str.Split(',');
            string[] statusArr = strSplit[0].Split(':');
            apiKey = statusArr[1];
            Debug.Log("apikeeeey "+apiKey);
            UnityEngine.SceneManagement.SceneManager.LoadScene(3);
        }
    }

    public void VerifyInputs(){
        submitButton.interactable = (nameField.text.Length>=8 && passwordField.text.Length>=8);
    }

    public string getApiKey(){
        return apiKey;
    }

    public void backToMenuScene(){
        UnityEngine.SceneManagement.SceneManager.LoadScene(0);
    }

    public void SignInWithGoogleScene(){
        UnityEngine.SceneManagement.SceneManager.LoadScene(4);
    }

    public void forgotPasswordScene(){
        UnityEngine.SceneManagement.SceneManager.LoadScene(5);
    }
}
