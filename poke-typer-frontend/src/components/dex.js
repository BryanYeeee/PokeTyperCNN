import { useState } from 'react'

const models = ['Latest', 'A', 'B', 'C', 'D', 'E']

const Dex = ({ dexList, setPredictor }) => {
  const [selectedModel, setSelectedModel] = useState('A')
  return (
    <div className='w-full h-full flex flex-col'>
      <div
        className='w-full h-20 px-8 bg-darkgrey flex items-center'
        data-augmented-ui='tl-clip tr-clip br-clip bl-clip both'
      >
        <div className='flex flex-col items-start w-full gap-2'>
          <div className='flex justify-between w-full gap-2 relative'>
            <div className='absolute top-1/2 -translate-y-1/2 border-y-1 border-grey w-full' />
            <div className='text-white'>FILTER</div>
            {models.map(m => (
              <button
                key={m}
                onClick={() => setSelectedModel(m)}
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
        </div>
      </div>
      <div className='font-mono space-y-4 py-4 pl-4 pr-8 flex-1 w-full overflow-y-auto overflow-x-hidden'>
        {dexList.map((mon, i) => (
          <div
            className='w-full h-12 px-4 pt-1 flex justify-between bg-red-300 duration-200 origin-left hover:scale-105'
            data-augmented-ui='tl-clip br-2-clip-x both'
            style={{ '--aug-br-extend2': '50%' }}
            onClick={() => setPredictor(mon)}
            key={mon.name}
          >
            <div className='flex gap-4'>
              <img
                src={mon.img}
                alt=''
                className='h-[2.5rem] aspect-square object-contain'
              />
              {mon.name}
            </div>
            <div className='flex gap-4'>
              {/* {JSON.stringify(mon.predictions[selectedModel])} */}
              {Object.entries(
                mon.predictions[
                  selectedModel == 'Latest'
                    ? mon.predictions.latest
                    : selectedModel
                ].prediction
              )
                .sort((a, b) => b[1] - a[1])
                .slice(0, 2)
                .map(([type, prob], i) => (
                  <div className='w-20 text-center' key={mon.name + type}>
                    {type}
                  </div>
                  // <div></div>
                ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Dex
