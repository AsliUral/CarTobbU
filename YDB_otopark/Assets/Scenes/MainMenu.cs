using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class MainMenu : MonoBehaviour
{
   public void GoToRegister(){
       SceneManager.LoadScene(2);
       /*
       scene 0 = parkinglot scene
       scene 1 = main menu scene
       scene 2 = register scene
       scene 3 = login scene
   
        */
   }

   public void GoToLogin(){
      SceneManager.LoadScene(3);
   }
}
