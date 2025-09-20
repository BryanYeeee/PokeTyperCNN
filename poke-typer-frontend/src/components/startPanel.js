'use client'
import BoltDecal from '@/components/BoltDecal'
import { useRouter } from 'next/navigation'

const StartPanel = ({ curPanel, setCurPanel }) => {
  const router = useRouter() // initialize router

  const handleGetStarted = () => {
    router.push('/customdex') // replace with your desired route
  }

  return (
    <div className='h-4/5 w-full flex flex-col items-center justify-start text-center space-y-6'>
      <div
        className='h-1/2 w-full bg-grey font-mono p-10 flex flex-col items-center justify-center relative'
        data-augmented-ui='tr-clip tl-clip br-2-clip-y bl-2-clip-y both'
        style={{ '--aug-border-all': '10px' }}
      >
        <h1 className='text-3xl font-bold tracking-widest'>POKE TYPER CNN</h1>
        <p className='mt-2 text-lg opacity-80'>by Bryan Yee</p>

        <svg
          className='absolute bottom-4 left-1/2 -translate-x-1/2'
          width='360'
          height='2'
          viewBox='0 0 240 2'
          xmlns='http://www.w3.org/2000/svg'
        >
          <line
            x1='0'
            y1='1'
            x2='240'
            y2='1'
            stroke='white'
            strokeWidth='2'
            strokeDasharray='6 4'
          />
        </svg>
        <BoltDecal pos={'top-4 left-4'}/>
        <BoltDecal pos={'top-4 right-4'}/>
      </div>
      <div className='flex flex-col items-center space-y-8'>
        <div className='flex flex-col items-center space-y-8'>
          <div className='flex space-x-8'>
            {[
              ['how', 'How It’s Made'],
              ['model', 'Model Details']
            ].map(b => (
              <button
                key={b[0]}
                className={
                  'px-8 py-3 font-bold relative transition-transform duration-200 ' +
                  (curPanel === b[0] ? 'underline' : 'hover:scale-110')
                }
                data-augmented-ui='tl-clip tr-clip br-clip bl-clip both'
                style={{
                  '--aug-border-all': '2px',
                  '--aug-border-bg': '#06b6d4',
                  '--aug-inlay-bg': curPanel === b[0] ? '#06b6d4' : 'black',
                  color: curPanel === b[0] ? 'black' : '#86efac'
                }}
                onClick={() => setCurPanel(b[0])}
              >
                {b[1]}
              </button>
            ))}
          </div>
        </div>

        <button
          className='px-14 py-3 text-xl font-bold text-black relative transition-transform duration-200 hover:scale-110'
          data-augmented-ui='tl-clip tr-clip br-clip bl-clip both'
          style={{
            '--aug-border-all': '3px',
            '--aug-border-bg': 'black',
            '--aug-inlay-bg': '#22c55e'
          }}
          onClick={handleGetStarted}
        >
          Get Started
        </button>
      </div>
    </div>
  )
}

export default StartPanel
