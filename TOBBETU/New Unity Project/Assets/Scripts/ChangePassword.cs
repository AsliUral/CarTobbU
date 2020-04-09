using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;
public class ChangePassword : MonoBehaviour
{
    public InputField EmailInputField;
    public Button submitButton;
    private string email;
    // Start is called before the first frame update
    void Start(){
        
    }

    // Update is called once per frame
    void Update(){
        
    }

    public void CallChangePW(){
        StartCoroutine(ChangePW());

    }

    IEnumerator ChangePW(){
        email = EmailInputField.text;
        var uwr = new UnityWebRequest("https://smart-car-park-api.appspot.com/user/forgotMyPassword/" + email, "GET");
    
        yield return uwr.SendWebRequest();

        if (uwr.isNetworkError){
            Debug.Log("giderken hata oldu "+uwr.error);
        }
        else{
            //Debug.Log(uwr.downloadHandler.text);
            UnityEngine.SceneManagement.SceneManager.LoadScene(2);
        }
    
    }

    public void backToMenuScene(){
        UnityEngine.SceneManagement.SceneManager.LoadScene(0);
    }
}
