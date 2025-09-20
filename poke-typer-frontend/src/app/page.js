import Image from 'next/image'
import DexCircles from './components/dexCircles'
import TextPanel from './components/textPanel'
import StartPanel from './components/startPanel'

export default function Home () {
  return (
    <div
      id='bg-svg'
      className='h-screen grid grid-cols-2 py-12 px-48 gap-4 items-end'
    >
      <div className='h-full relative'>
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
              <StartPanel />
            </div>
          </div>
        </div>
      </div>
      <div
        className='asd h-17/20 w-full foreground flex items-center px-12 pt-[4rem] overflow-hidden'
        data-augmented-ui='bl-clip br-clip tr-2-clip-x both'
        style={{
          '--aug-tr1': '4rem',
          '--aug-tr-extend1': 'calc(50% - 15px)',
          '--aug-tr2': '15px'
        }}
      >
        <TextPanel />
      </div>
    </div>
  )
}
