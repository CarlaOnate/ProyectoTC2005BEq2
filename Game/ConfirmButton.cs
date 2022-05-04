using System.Collections;
using UnityEngine;
using System;
using UnityEngine.Networking;



public class ConfirmButton : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {

    }

    IEnumerator SendData()
    {
        string data = "test";
        string json = JsonUtility.ToJson(data);

        WWWForm form = new WWWForm();
        form.AddField("bundle", "the data");
        string url = "http://localhost:8585/";
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(data);
            www.uploadHandler = (UploadHandler)new UploadHandlerRaw(bodyRaw);
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");

            yield return www.SendWebRequest();          // Talk to Python
            if (www.isNetworkError || www.isHttpError)
            {
                Debug.Log(www.error);
            }
            else
            {
                string txt = www.downloadHandler.text.Replace('\'', '\"');
                txt = txt.TrimStart('"', '{', 'd', 'a', 't', 'a', ':', '[');
                txt = "{\"" + txt;
                txt = txt.TrimEnd(']', '}');
                txt = txt + '}';
                string[] strs = txt.Split(new string[] { "}, {" }, StringSplitOptions.None);
                Debug.Log("GET: " + strs[0]);

            }
        }
    }

    public void Button1()
    {
        StartCoroutine(SendData());
    }

    // Update is called once per frame
    void Update()
    {
        
         if (Input.GetKeyDown(KeyCode.Return))
        {
            StartCoroutine(SendData());
        }

    }
}
