const HowPanel = () => {
  return (
    <div
      className='h-4/5 w-full bg-black font-mono text-sm p-2 overflow-hidden'
      data-augmented-ui='tl-2-clip-x tr-2-clip-x br-2-clip-x bl-2-clip-x r-clip-y both'
      style={{ '--aug-r-extend1': '50%' }}
    >
      <div className='h-full w-full text-green-400 px-4 py-2 overflow-y-auto [direction:rtl]'>
        <div className='[direction:ltr] text-left space-y-2'>
          <div className='border-1 text-green-800 mb-4'></div>
          <h2 className='text-2xl underline text-center'>
            HOW THE MODEL WAS MADE
          </h2>
          <span className='text-lg'>Training Dataset Details:</span>
          <pre className='whitespace-pre-wrap'>
            {`- Small dataset of 721 images each with 18 possible types as one-hot vectors
- Random data augmentation with rotations, reflections, brightness, etc.
- Imbalanced distribution of Pokemon types
    - 118 water types (~16%)
    - 37 ice types (~5%)
`}
          </pre>

          <span className='text-lg'>Validation Dataset Details:</span>
          <pre className='whitespace-pre-wrap'>
            {`- Webscraped dataset of 280 fan-made pokemon (credits to phoenixsong)`}
          </pre>

          <div className='flex justify-center'>
            <span>v SOURCE LINKS v</span>
          </div>
          <div
            className='mt-1 mb-4 py-1 w-full flex flex-col items-center gap-2 '
            data-augmented-ui='l-step-xy r-step-xy border'
            style={{
              '--aug-border-bg': 'var(--color-green-400)',
              '--aug-border-all': '1px'
            }}
          >
            <div className='flex gap-4'>
              <a
                href='https://www.kaggle.com/datasets/kvpratama/pokemon-images-dataset'
                target='_blank'
                rel='noopener noreferrer'
                className='text-green-300 hover:text-green-100'
              >
                [kaggle images]
              </a>
              <a
                href='https://www.kaggle.com/datasets/rounakbanik/pokemon'
                target='_blank'
                rel='noopener noreferrer'
                className='text-green-300 hover:text-green-100'
              >
                [kaggle data]
              </a>
            </div>
            <a
              href='https://phoenixdex.alteredorigin.net/pokemon/'
              target='_blank'
              rel='noopener noreferrer'
              className='text-green-300 hover:text-green-100'
            >
              [phoenixsong fakemon data]
            </a>
          </div>

          <div className='border-1 text-green-800' />

          <span className='text-lg'>Building The Model:</span>
          <pre className='whitespace-pre-wrap'>
            {`> Step 1: Base model = EfficientNetB0 (pretrained on ImageNet)
> Step 2: Base frozen (no training on convolutional layers)
> Step 3: Added GlobalAveragePooling -> Dropout -> Dense(18, sigmoid)
> Step 4: Loss = BinaryCrossEntropy (multi-label setup)
> Step 5: Primary metric = AUC (captures performance across thresholds)`}
          </pre>

          <span>Refer to: </span>
          <a
            href='https://keras.io/examples/vision/image_classification_efficientnet_fine_tuning/#transfer-learning-from-pretrained-weights'
            target='_blank'
            rel='noopener noreferrer'
            className='text-green-300 hover:text-green-100'
          >
            [Keras Transfer Learning Guide]
          </a>
          <div className='border-1 text-green-800 mt-4' />
        </div>
      </div>
    </div>
  )
}

export default HowPanel
