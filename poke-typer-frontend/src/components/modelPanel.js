import Image from 'next/image'
const ModelPanel = () => {
  const headers = ['Model', 'Base', 'Training AUC', 'Validation AUC']

  const models = [
    { name: 'A', base: 'EfficientNetB0', train: 'XX.X%', val: 'XX.X%' },
    { name: 'B', base: 'EfficientNetB0', train: 'XX.X%', val: 'XX.X%' },
    { name: 'C', base: 'EfficientNetB0', train: 'XX.X%', val: 'XX.X%' },
    { name: 'D', base: 'ResNet50', train: 'XX.X%', val: 'XX.X%' },
    { name: 'E', base: 'ResNet50', train: 'XX.X%', val: 'XX.X%' }
  ]
  return (
    <div
      className='h-4/5 w-full bg-black font-mono text-sm p-2 overflow-hidden'
      data-augmented-ui='tl-2-clip-x tr-2-clip-x br-2-clip-x bl-2-clip-x r-clip-y both'
      style={{ '--aug-r-extend1': '50%' }}
    >
      <div className='h-full w-full text-green-400 px-4 py-2 overflow-y-auto [direction:rtl]'>
        <div className='[direction:ltr] text-left space-y-2'>
          <div className='border-1 text-green-800 mb-4'></div>
          <h2 className='text-2xl underline text-center'>MODEL COMPARISONS</h2>

          <span className='text-lg'>Models Trained:</span>
          <div className='grid grid-cols-[auto_auto_auto_auto] overflow-x-auto border text-green-400 text-sm'>
            {headers.map(h => (
              <div
                key={h}
                className='border border-green-700 px-3 py-1 bg-green-900/30 font-bold text-center'
              >
                {h}
              </div>
            ))}
            {models.map(m => (
              <>
                {[m.name, m.base, m.train, m.val].map((val, i) => (
                  <div
                    key={i + m.name}
                    className='border border-green-700 px-3 py-1 text-center'
                  >
                    {val}
                  </div>
                ))}
              </>
            ))}
          </div>

          <div className='border-1 text-green-800' />

          <span className='text-lg'>Differences:</span>
          <pre className='whitespace-pre-wrap'>
            {`- Base: EfficientNetB0 (A–C), ResNet50 (D–E)
- Slight adjustments in:
    • Image input size and training batch size
    • Data augmentation strength
    • Extra dropout layers added
    • Dense layers stacked on top of frozen base`}
          </pre>

          <div className='border-1 text-green-800' />
          <pre className='whitespace-pre-wrap'>
            {`Although the models have very similar AUCs, there is still possibility of them making different predictions. Below is a venn diagram showing label prediction similarity between Models A-C for the validation set.`}
          </pre>
          <div className='flex justify-center'>
            <Image
              src='/ENETdiff.png'
              alt='EfficientNet comparison'
              width={300}
              height={300}
              className='rounded-lg border border-green-700'
            />
          </div>
          <pre className='whitespace-pre-wrap'>
            {`Each model has a considerable amount of unique predictions. While they may be incorrect, I thought it would still be worth having multiple models to show more possible types per input.`}
          </pre>
          <div className='border-1 text-green-800' />
          <span className='text-lg'>Problems with the Results:</span>
          <pre className='whitespace-pre-wrap'>
            {`- Dataset size is small → high risk of overfitting
- Imbalanced distribution → some types underrepresented
- Pokemon designs don’t always align with typings (like how is Charizard not a dragon???)
- Fakemon designs and their typing can be unintuitive making an incorrect prediction "acceptable", so the correctness of the AUC may not be perfect`}
          </pre>
          <div className='border-1 text-green-800' />
        </div>
      </div>
    </div>
  )
}

export default ModelPanel
