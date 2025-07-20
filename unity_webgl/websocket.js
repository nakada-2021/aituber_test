
const ws = new WebSocket("ws://localhost:8000/ws");
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (window.model) {
        if(data.eyeLeftOpen !== undefined) window.model.internalModel.coreModel.setParameterValueById("ParamEyeLOpen", data.eyeLeftOpen);
        if(data.mouthOpen !== undefined) window.model.internalModel.coreModel.setParameterValueById("ParamMouthOpenY", data.mouthOpen);
    }
};
