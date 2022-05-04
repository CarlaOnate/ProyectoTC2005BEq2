using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;
using TMPro;
using UnityEngine.Networking;

public class Menu : MonoBehaviour
{
    public Persiste pers;

    // Start is called before the first frame update
    void Start()
    {
        pers = GameObject.FindWithTag("Persistente").GetComponent<Persiste>();
    }

    // Update is called once per frame
    void Update()
    {

    }

    public void playGame()
    {
        SceneManager.LoadScene("Intro");
    }

    

    public void quitDesktop()
    {
        string jsonInput = JsonUtility.ToJson(pers.usr);
        StartCoroutine(Logout(jsonInput));
        Application.Quit();
    }

    IEnumerator Logout(string json)
    {

        string url = "http://127.0.0.1:8000/game/logout";
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

                Debug.Log(www.downloadHandler.text);


            }
        }

    }
}