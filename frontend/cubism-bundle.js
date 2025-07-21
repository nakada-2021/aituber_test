console.log('cubism-bundle.js loaded');
// Cubism Coreは別途<script>で読み込む前提
import { CubismFramework } from './live2d_sdk/Framework/dist/live2dcubismframework.js';
import { CubismModelSettingJson } from './live2d_sdk/Framework/dist/cubismmodelsettingjson.js';
import { ICubismModelSetting } from './live2d_sdk/Framework/dist/icubismmodelsetting.js';
import { ICubismAllocator } from './live2d_sdk/Framework/dist/icubismallcator.js';
import { CubismDefaultParameterId } from './live2d_sdk/Framework/dist/cubismdefaultparameterid.js';
import { CubismModel } from './live2d_sdk/Framework/dist/model/cubismmodel.js';
// import { CubismFrameworkConfig } from './live2d_sdk/Framework/dist/cubismframeworkconfig.js';

window.CubismFramework = CubismFramework;
window.CubismModelSettingJson = CubismModelSettingJson;
window.ICubismModelSetting = ICubismModelSetting;
window.ICubismAllocator = ICubismAllocator;
window.CubismDefaultParameterId = CubismDefaultParameterId;
window.CubismModel = CubismModel;
// window.CubismFrameworkConfig = CubismFrameworkConfig;
window.cubismSDKLoaded = true;
console.log('cubismSDKLoaded set to true'); 