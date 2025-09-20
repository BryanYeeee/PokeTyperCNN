const BoltDecal = ({ pos }) => {
  return (
    <svg
      className={'absolute opacity-60 ' + pos}
      width='24'
      height='24'
      viewBox='0 0 24 24'
      fill='none'
      stroke='white'
      strokeWidth='2'
    >
      <circle cx='12' cy='12' r='8' />
      <line x1='4' y1='4' x2='20' y2='20' />
      <line x1='20' y1='4' x2='4' y2='20' />
    </svg>
  )
}

export default BoltDecal
