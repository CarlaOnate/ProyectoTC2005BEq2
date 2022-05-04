using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

[CreateAssetMenu]
public class SignalSlender : ScriptableObject
{
    public List<SignalListener> listeners;

    void Start()
    {
        listeners = new List<SignalListener>();
        
    }

    public void Raise()
    {
        Debug.Log(listeners.Count);
        for(int i = listeners.Count - 1; i >= 0; i--)
        {
            if(listeners[i] != null)
            {
                listeners[i].OnSignalRaised();
            }
            
        }
    }

    public void RegisterListener(SignalListener listener)
    {
        listeners.Add(listener);
    }
    
    public void DeRegisterListener(SignalListener listener)
    {
        listeners.Remove(listener);
    }
}
