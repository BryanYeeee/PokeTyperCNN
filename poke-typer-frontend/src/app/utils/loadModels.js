import * as tf from '@tensorflow/tfjs';

const modelCache = {};

export async function loadModel(name) {
  if (!modelCache[name]) {
    modelCache[name] = await tf.loadLayersModel(`/models/${name}/model.json`);
  }
  return modelCache[name];
}

export async function loadAllModels() {
  const names = ['A', 'B', 'C', 'D', 'E'];
  const models = {};
  for (const name of names) {
    models[name] = await loadModel(name);
  }
  return models;
}
