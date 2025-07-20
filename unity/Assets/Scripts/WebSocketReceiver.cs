
using UnityEngine;
using NativeWebSocket;
using Live2D.Cubism.Core;

public class WebSocketReceiver : MonoBehaviour
{
    WebSocket websocket;
    public CubismModel model;

    void Start()
    {
        websocket = new WebSocket("ws://localhost:8000/ws");
        websocket.OnMessage += (bytes) =>
        {
            string message = System.Text.Encoding.UTF8.GetString(bytes);
            var data = JsonUtility.FromJson<ExpressionData>(message);
            model.Parameters[model.GetParameterIndex("ParamEyeLOpen")].Value = data.eyeLeftOpen;
            model.Parameters[model.GetParameterIndex("ParamMouthOpenY")].Value = data.mouthOpen;
        };
        websocket.Connect();
    }

    void Update()
    {
        websocket.DispatchMessageQueue();
    }

    [System.Serializable]
    public class ExpressionData
    {
        public float eyeLeftOpen;
        public float mouthOpen;
    }
}
