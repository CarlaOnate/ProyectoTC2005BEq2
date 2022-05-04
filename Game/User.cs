using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

[System.Serializable]

public class User
{
    public string username;//
    public string password;
    public string party_id;
    public string user_id; //
    public string session_id;//
    public string age;//
    public string countryName; //
    public string countryId;
    public string countryNickname;
    public string difficulty;
    public string final_time;
    public string penalties;
    public string total_score;


    private PartyData pd;
    private LoginData ld;

    public void SetPartyData(string jsonS)
    {
        pd = JsonUtility.FromJson<PartyData>(jsonS);
        party_id = pd.party_id;
    }

    public void SetLoginData(string jsonS)
    {
        ld = JsonUtility.FromJson<LoginData>(jsonS);
        username = ld.username;
        user_id = ld.user_id; //
        session_id = ld.session_id;//
        age = ld.age;//
        countryName = ld.countryName; //
        countryId = ld.countryId;
        countryNickname = ld.countryNickname;
    }


    public void ToStr()
    {
        Debug.Log("Actual user: " + username + ", id: " + user_id);
    }


}
