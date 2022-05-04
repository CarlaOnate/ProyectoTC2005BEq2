using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Persiste : MonoBehaviour
{
    // Start is called before the first frame update
    public User usr;

    void Awake()
    {
        usr = new User();
        DontDestroyOnLoad(this.gameObject);
    }
}
