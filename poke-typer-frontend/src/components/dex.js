const Dex = ({ dexList }) => {
  return (
    <div className='w-full min-h-full'>
      <div
        className='w-full h-20 px-12 bg-darkgrey flex items-center justify-between'
        data-augmented-ui='
  tl-clip tr-clip br-clip bl-clip both'
      >
        <div className='bg-green-400 size-10'></div>
      </div>
      <div className='space-y-4 py-4 px-4'>
        {dexList.map((mon, i) => (
          <div
            className='w-full h-12 px-4'
            data-augmented-ui='
  tl-clip br-2-clip-x both'
            style={{ '--aug-br-extend2': '50%' }}
            key={i}
          >
            {mon}
          </div>
        ))}
      </div>
    </div>
  )
}

export default Dex
