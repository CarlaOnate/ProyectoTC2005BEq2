using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using UnityEngine.UI;
using UnityEngine.Networking;

public class PostAgregarUsr : MonoBehaviour
{
    public User1 someUser;

    private void Start()
    {
        someUser = new User1();
        GameObject.Find("agregarUser").GetComponent<Button>().onClick.AddListener(PostDataCall);
    }

    void PostDataCall()
    {
        someUser.comment = GameObject.Find("inputComment").GetComponent<TMP_InputField>().text;
        someUser.username = GameObject.Find("inputUsername").GetComponent<TMP_InputField>().text;
        string user = JsonUtility.ToJson(someUser);
        StartCoroutine(PostData(user));
    }

    IEnumerator PostData(string json)
    {

        string url = "http://20.89.70.3:8000/alta";
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
