using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.Text.RegularExpressions;
using UnityEngine.SceneManagement;
using TMPro;
using UnityEngine.Networking;


public class Login : MonoBehaviour
{
    public GameObject username;
    public GameObject password;

    private string Username;
    private string Password;
    private string form;
    private bool uservalid = false;
    private TextMeshProUGUI response;

    public Persiste pers;

    // Start is called before the first frame update
    void Start()
    {
        pers = GameObject.FindWithTag("Persistente").GetComponent<Persiste>();
        GameObject.Find("confirm").GetComponent<Button>().onClick.AddListener(PostDataCall);
    }

    public void Register()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex + 1);
    }

    // Update is called once per frame
    void Update()
    {

        if (Input.GetKeyDown(KeyCode.Tab))
        {
            if (username.GetComponent<InputField>().isFocused)
            {
                password.GetComponent<InputField>().Select();
            }
        }

        if (Input.GetKeyDown(KeyCode.Return))
        {
            Username = username.GetComponent<InputField>().text;
            Password = password.GetComponent<InputField>().text;

            if (Username != "" && Password != "")
            {
                PostDataCall();
            }
        }

    }

    void PostDataCall()
    {
        Username = GameObject.Find("username").GetComponent<InputField>().text;
        Password = GameObject.Find("password").GetComponent<InputField>().text;
        Debug.Log(Username);
        pers.usr.username = Username;
        pers.usr.password = Password;
        string jsonInput = JsonUtility.ToJson(pers.usr);
        StartCoroutine(PostData(jsonInput));
    }

    IEnumerator PostData(string json)
    {

        string url = "http://20.89.70.3:8000/game/login";
        WWWForm form = new WWWForm();
        form.AddField("bundle", "json");

        using (UnityWebRequest www = UnityWebRequest.Post(url, form))
        {
            var request = new UnityWebRequest(url, "POST");
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(json);
            www.uploadHandler = (UploadHandler)new UploadHandlerRaw(bodyRaw);
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");


            yield return www.SendWebRequest();

            if (www.isNetworkError || www.isHttpError)
            {
                Debug.Log(www.error);
            }
            else
            {
                response = GameObject.Find("Mensaje").GetComponent<TextMeshProUGUI>();

                Debug.Log(www.downloadHandler.text);

                Debug.Log(www.downloadHandler.text.IndexOf("error"));

                if (www.downloadHandler.text.IndexOf("error") == -1)
                {

                    pers.usr.SetLoginData(www.downloadHandler.text);
                    response.text = "Welcome " + Username + "!";
                    pers.usr.ToStr();
                    Register();
                }
                else
                {
                    response.text = "Incorrect username or password";
                }


            }
        }

    }
}
