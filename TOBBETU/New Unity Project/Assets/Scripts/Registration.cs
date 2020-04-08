using System.Collections;
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;
public class Registration : MonoBehaviour
{
    [Serializable]
    public class User{
        public string username;
        public string password;
        public string personFullName;
        public string userType;
        public string studentID;
        public string allowedCarParks;
        public string personIsDisabled;
    }
    public InputField nameField;
    public InputField passwordField;
    public InputField fullNameField;
    public Transform userDropdown;
    public InputField studentIDField;
    public Button submitButton;

    

    //using coroutine; while we are waiting for server
    //game can work in the mean time.
    public void CallRegister(){
        StartCoroutine(Register());
    }

    IEnumerator Register(){

        //get the selected index
         int menuIndex = userDropdown.GetComponent<Dropdown> ().value;
 
     //get all options available within this dropdown menu
         List<Dropdown.OptionData> menuOptions = userDropdown.GetComponent<Dropdown> ().options;
 
     //get the string value of the selected index
         string value = menuOptions [menuIndex].text;
       
        User thisUser = new User();
        thisUser.username = nameField.text;
        thisUser.password = passwordField.text;
        thisUser.personFullName = fullNameField.text;
        Debug.Log("FULL NAME of this user: "+thisUser.personFullName);
        Debug.Log("full name input " + fullNameField.text);
        thisUser.userType = value;
        thisUser.studentID = studentIDField.text;
        thisUser.allowedCarParks = "Main Car Park, Foreign Languages Car Park";
        thisUser.personIsDisabled = "no";
        string json = JsonUtility.ToJson(thisUser);
        Debug.Log(json);

        var uwr = new UnityWebRequest("https://smart-car-park-api.appspot.com/user/register", "POST");
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
            UnityEngine.SceneManagement.SceneManager.LoadScene(2);
        }
 
    
    }

    
    public void VerifyInputs(){
        submitButton.interactable = (nameField.text.Length >=8 && passwordField.text.Length >= 8);
        //submitButton.interactable = buraya serverda bu isim var mi yok mu KONTROLU
    }

    public void backToMenuScene(){
        UnityEngine.SceneManagement.SceneManager.LoadScene(0);
    }

  
  
}
