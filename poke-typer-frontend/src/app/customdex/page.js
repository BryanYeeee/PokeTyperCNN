'use client'
import BoltDecal from '@/components/BoltDecal'
import Dex from '@/components/dex'
import DexCircles from '@/components/dexCircles'
import Predictor from '@/components/predictor'
import { useState } from 'react'

const CustomDex = () => {
  const [dexList, setDexList] = useState(['a', 'b', 'c'])

  return (
    <div
      id='bg-svg'
      className='h-[200vh] md:h-screen flex md:flex-row flex-col items-center justify-center py-4 px-12 gap-2 relative'
    >
      <div className='hidden md:inline w-10 h-[60%] absolute top-1/2 md:left-1/2 md:-translate-x-1/2 -translate-y-1/2 bg-[image:var(--darkred)] bg-cover bg-center' />
      <div className='h-[calc(100%-4rem)] relative min-w-100 w-1/2'>
        <div //calc(15%+4rem+10px)
          className='h-[calc(15%+4rem-5px)] w-full foreground absolute p-8 flex items-center'
          data-augmented-ui='tl-clip tr-clip both'
          style={{
            '--aug-inlay-bg': '#b21f1db8'
          }}
        >
          <DexCircles />
        </div>
        <div className='h-[calc(85%+5px)] w-full absolute top-[calc(15%-5px)] md:bottom-0'>
          <div
            className='size-full foreground  flex justify-center items-end'
            data-augmented-ui='bl-clip br-clip  tl-clip-x'
            style={{
              '--aug-tl1': '4rem',
              '--aug-tl-inset1': '50%'
            }}
          >
            <div
              className='h-[calc(100%-5px)] w-full foreground flex items-center p-16 pt-[calc(4rem+15px+(4rem-15px))]'
              data-augmented-ui='bl-clip br-clip  tl-clip-x both'
              style={{
                '--aug-tl1': '4rem',
                '--aug-tl-inset1': '50.5%'
              }}
            >
              <Predictor setDexList={setDexList} />
              <BoltDecal pos={'bottom-8 left-8'} />
              <BoltDecal pos={'bottom-8 right-8'} />
            </div>
          </div>
        </div>
      </div>
      <div
        className='relative h-full w-1/2 min-w-100 foreground flex items-center p-16 overflow-hidden'
        data-augmented-ui='bl-clip br-clip tr-clip tl-clip both'
      >
        <Dex dexList={dexList} />
        <BoltDecal pos='top-8 left-8' />
        <BoltDecal pos='top-8 right-8' />
        <BoltDecal pos='bottom-8 left-8' />
        <BoltDecal pos='bottom-8 right-8' />
      </div>
    </div>
  )
}

export default CustomDex
