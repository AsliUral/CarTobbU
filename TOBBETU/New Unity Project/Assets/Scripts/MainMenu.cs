using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class MainMenu : MonoBehaviour
{
   public void GoToRegister(){
       SceneManager.LoadScene(1);
 
   }

   public void GoToLogin(){
      SceneManager.LoadScene(2);
   }

   public void GoToParkingScene(){
      SceneManager.LoadScene(3);
   }

      /*
       scene 3 = parkinglot scene
       scene 0 = main menu scene
       scene 1 = register scene
       scene 2 = login scene
   
        */
}
