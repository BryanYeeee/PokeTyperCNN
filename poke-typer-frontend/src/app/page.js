'use client'
import DexCircles from '@/components/dexCircles'
import HowPanel from '@/components/howPanel'
import StartPanel from '@/components/startPanel'
import ModelPanel from '@/components/modelPanel'
import BoltDecal from '@/components/BoltDecal'
import { useState } from 'react'

export default function Home () {
  const [curPanel, setCurPanel] = useState('how')

  return (
    <div
      id='bg-svg'
      className='h-screen grid grid-cols-2 py-12 px-48 gap-2 items-end -z-20 relative'
    >
      <div className='w-10 h-[60%] absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-7/20 bg-[image:var(--darkred)] bg-cover bg-center' />
      <div className='h-full relative min-w-100'>
        <div //calc(15%+4rem+10px)
          className='h-[calc(15%+4rem-5px)] w-full foreground absolute p-8 flex items-center'
          data-augmented-ui='tl-clip tr-clip both'
          style={{
            '--aug-inlay-bg': '#b21f1db8'
          }}
        >
          <DexCircles />
        </div>
        <div className='h-[calc(85%+5px)] w-full absolute bottom-0'>
          <div
            className='size-full foreground  flex justify-center items-end'
            data-augmented-ui='bl-clip br-clip  tl-clip-x'
            style={{
              '--aug-tl1': '4rem',
              '--aug-tl-inset1': '50%'
            }}
          >
            <div
              className='h-[calc(100%-5px)] w-full foreground flex items-center px-12 pt-[4rem]'
              data-augmented-ui='bl-clip br-clip  tl-clip-x both'
              style={{
                '--aug-tl1': '4rem',
                '--aug-tl-inset1': '50.5%'
              }}
            >
              <StartPanel curPanel={curPanel} setCurPanel={setCurPanel} />
            </div>
          </div>
        </div>
        <BoltDecal pos={'bottom-8 left-8'}/>
        <BoltDecal pos={'bottom-8 right-8'}/>
      </div>
      <div
        className='relative h-17/20 w-full min-w-100 foreground flex items-center px-12 pt-[4rem] overflow-hidden'
        data-augmented-ui='bl-clip br-clip tr-2-clip-x both'
        style={{
          '--aug-tr1': '4rem',
          '--aug-tr-extend1': 'calc(50% - 15px)',
          '--aug-tr2': '15px'
        }}
      >
        {curPanel == 'how' ? <HowPanel /> : <ModelPanel />}
        <BoltDecal pos='bottom-8 left-8'/>
        <BoltDecal pos='bottom-8 right-8'/>
      </div>
    </div>
  )
}


