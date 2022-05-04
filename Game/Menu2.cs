using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Menu2 : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void returnMenu()
    {
        SceneManager.LoadScene("Menu");
        if (Input.GetKeyDown(KeyCode.Return))
        {
            SceneManager.LoadScene("Menu");
        }
    }
}
