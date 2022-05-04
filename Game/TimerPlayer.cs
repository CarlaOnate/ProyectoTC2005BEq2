using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.Text.RegularExpressions;
using UnityEngine.SceneManagement;
using TMPro;
using UnityEngine.Networking;

public class TimerPlayer : MonoBehaviour
{
    public static TimerPlayer instanciar;
    public Text Cronometro;
    private TimeSpan tiempoCrono;
    private bool timerBool;
    private float tiempoTrans;
    public Persiste pers;
    public PlayerMovement player;

    private void Awake()
    {
        instanciar = this;
        Cronometro.text = "Time = 00:00:00";
        timerBool = false;
    }

    private void Start()
    {
        pers = GameObject.FindObjectOfType<Persiste>();
        player = GameObject.FindObjectOfType<PlayerMovement>();
        pers.usr.ToStr();
    }

    public void IniciarTiempo()
    {
        timerBool = true;
        tiempoTrans = 0F;

        StartCoroutine(ActUpdate());
    }

    public void FinTiempo()
    {
        timerBool = false;



        if (SceneManager.GetActiveScene() == SceneManager.GetSceneByName("Nivel1"))
        {
            pers.usr.difficulty = "1";

        }
        else if (SceneManager.GetActiveScene() == SceneManager.GetSceneByName("Nivel2"))
        {
            pers.usr.difficulty = "2";
        }
        else if (SceneManager.GetActiveScene() == SceneManager.GetSceneByName("Nivel3"))
        {
            pers.usr.difficulty = "3";
        }

        pers.usr.final_time = Cronometro.text;
        pers.usr.penalties = ((int)player.currentHealth.RuntimeValue - 6).ToString();
        string jsonInput = JsonUtility.ToJson(pers.usr);
        StartCoroutine(PostData(jsonInput));

    }


    private IEnumerator ActUpdate()
    {
        while (timerBool)
        {
            tiempoTrans += Time.deltaTime;
            tiempoCrono = TimeSpan.FromSeconds(tiempoTrans);
            string tiempoCronoSTR = tiempoCrono.ToString("mm':'ss':'ff");
            Cronometro.text = tiempoCronoSTR;

            yield return null;
        }
    }


    IEnumerator PostData(string json)
    {

        string url = "http://20.89.70.3:8000/game/level";
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
                pers.usr.SetPartyData(www.downloadHandler.text);

                if (pers.usr.difficulty == "3" || (SceneManager.GetActiveScene() == SceneManager.GetSceneByName("Nivel3")))
                {
                    StartCoroutine(PostDataParty(json));
                }

            }
        }

    }

    IEnumerator PostDataParty(string json)
    {

        string url = "http://20.89.70.3:8000/game/party";
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
