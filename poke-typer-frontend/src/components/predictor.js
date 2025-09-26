import { useEffect, useState } from 'react'
import { loadAllModels } from '@/utils/loadModels'
import * as tf from '@tensorflow/tfjs'

const Predictor = () => {
  const [models, setModels] = useState(null)

  useEffect(() => {
    async function init () {
      const loaded = await loadAllModels()
      setModels(loaded)
    }
    init()
  }, [])

  async function handlePredict (imgTensor) {
    if (!models) return
    const preds = await models.poke1.predict(imgTensor.expandDims(0))
    console.log(preds.arraySync())
  }

  return (
    <div className='size-full'>
      <h1>Pokémon Type Classifier</h1>
      <button onClick={() => handlePredict(tf.randomNormal([224, 224, 3]))}>
        Test Prediction
      </button>
    </div>
  )
}

export default Predictor
