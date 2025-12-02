import { forwardRef, useImperativeHandle, useState } from 'react'
import { predictType } from '@/utils/predict.js'
import { getPrediction, savePrediction } from '@/utils/indexedDB.js'

const emptyPred = {
  latest: 'A',
  A: { model: 'A', prediction: {} },
  B: { model: 'A', prediction: {} },
  C: { model: 'A', prediction: {} },
  D: { model: 'A', prediction: {} },
  E: { model: 'A', prediction: {} }
}

const models = ['A', 'B', 'C', 'D', 'E']

const Predictor = forwardRef(({ refreshDex }, ref) => {
  const [selectedModel, setSelectedModel] = useState('A')
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [predictions, setPredictions] = useState(emptyPred)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFileChange = async e => setTarget(e.target.files[0])

  const setTarget = async (f) => {
    setFile(f)
    setError(null)

    const cache = await getPrediction(f.name)
    if (cache) {
      const previewUrl = cache.imageBlob
        ? URL.createObjectURL(cache.imageBlob)
        : URL.createObjectURL(f)
      setPreview(previewUrl)
      setPredictions({ ...emptyPred, ...cache.predictions })
    } else {
      setPreview(URL.createObjectURL(f))
      setPredictions(emptyPred)
    }
  }

  useImperativeHandle(ref, () => ({
    setTarget: setTarget
  }))

  const handleSubmit = async () => {
    if (!file) {
      setError('Please select an image first.')
      return
    }
    setError(null)
    setLoading(true)

    try {
      const data = await predictType(file, selectedModel)
      console.log(data)

      await savePrediction(file.name, selectedModel, data, file)
      setPredictions({ ...predictions, [selectedModel]: data })
      refreshDex()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const changeModel = async m => {
    await setSelectedModel(m)
    if (Object.keys(predictions[m].prediction).length !== 0) {
      // setLoading(true)
      try {
        await savePrediction(file.name, m)
        setPredictions({ ...predictions, latest: m })
        refreshDex()
      } catch (err) {
        console.log('asddsddadsdsa')
        setError(err.message)
      } finally {
        // setLoading(false)
      }
    }
  }

  return (
    <div className='size-full border-amber-200 flex flex-col gap-4'>
      <div className='flex flex-col items-center space-y-3'>
        {/* Hidden file input */}
        <input
          id='fileInput'
          type='file'
          accept='image/*'
          onChange={handleFileChange}
          className='hidden'
        />
        <div className='flex justify-start items-start gap-4 w-full'>
          <div
            className='bg-grey'
            data-augmented-ui='bl-clip br-clip tr-clip tl-clip both'
          >
            <img
              src={preview}
              alt=''
              className='size-48 min-w-48 p-3 object-contain'
            />
          </div>
          <div className='flex flex-col items-start w-full gap-2'>
            <div className='flex justify-between w-full gap-2 relative'>
              <div className='absolute top-1/2 -translate-y-1/2 border-y-1 border-grey w-full' />
              {models.map(m => (
                <button
                  key={m}
                  onClick={() => changeModel(m)}
                  data-augmented-ui='tl-clip tr-clip br-clip bl-clip both'
                  className={`px-4 py-2 font-semibold transition-transform duration-200 hover:scale-110 ${
                    selectedModel === m
                      ? 'bg-[#06b6d4] text-white shadow'
                      : 'bg-gray-200 text-black hover:bg-gray-300'
                  }`}
                >
                  {m}
                </button>
              ))}
            </div>
            <div className='flex justify-between gap-4 w-full'>
              <label
                htmlFor='fileInput'
                className='text-center px-4 py-1 w-1/2 font-bold duration-200 hover:scale-110'
                data-augmented-ui='tl-clip tr-clip br-clip bl-clip both'
                style={{
                  '--aug-border-all': '2px',
                  '--aug-border-bg': '#06b6d4',
                  '--aug-inlay-bg': 'black',
                  color: '#86efac'
                }}
              >
                {file ? 'Change Image' : 'Browse Image'}
              </label>
              <button
                className='text-center px-4 py-1 w-1/2 text-xl font-bold text-black duration-200 hover:scale-110'
                data-augmented-ui='tl-clip tr-clip br-clip bl-clip both'
                style={{
                  '--aug-border-all': '3px',
                  '--aug-border-bg': 'black',
                  '--aug-inlay-bg': '#22c55e'
                }}
                onClick={handleSubmit}
                disabled={loading}
              >
                {loading ? 'Predicting...' : 'Predict Type'}
              </button>
            </div>

            <div
              className='h-4/5 w-full bg-black font-mono text-sm p-2 overflow-hidden'
              data-augmented-ui='bl-clip br-clip tr-clip tl-clip both'
            >
              <div className='h-full w-full text-green-400 px-4 py-2'>
                {error ? (
                  <p className='text-red-500'>{error}</p>
                ) : file ? (
                  file.name
                ) : (
                  'No file selected'
                )}
                <div className='border-b-1 my-1' />
                For better results, upload a png with a transparent background
              </div>
            </div>
          </div>
        </div>
      </div>

      <div
        className='h-full w-full bg-black text-green-400 font-mono text-sm px-2 py-4 overflow-hidden'
        data-augmented-ui='bl-clip br-clip tr-clip tl-clip both'
      >
        <h2 className='text-lg font-semibold mb-2 px-4'>
          <span className='underline'>Predictions:</span> Model {selectedModel}
        </h2>
        <div className='h-full w-full overflow-y-auto px-4'>
          <ul className='space-y-1 text-sm'>
            {Object.entries(predictions[selectedModel].prediction)
              .sort((a, b) => b[1] - a[1])
              .map(([type, prob], i) => (
                <li
                  key={type}
                  className={`px-1 flex justify-between ${
                    i < 2 ? 'text-[#06b6d4] bg-slate-800 border' : ''
                  }`}
                >
                  <span className='font-medium'>{type}</span>
                  <span>{prob.toFixed(4)}</span>
                </li>
              ))}
          </ul>
        </div>
      </div>
      {/* )} */}
    </div>
  )
})

export default Predictor