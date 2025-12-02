import { useEffect, useState, useCallback } from 'react'
import { getAllPredictions } from '@/utils/indexedDB.js'

const emptyPred = {
  latest: 'A',
  A: { model: 'A', prediction: {} },
  B: { model: 'A', prediction: {} },
  C: { model: 'A', prediction: {} },
  D: { model: 'A', prediction: {} },
  E: { model: 'A', prediction: {} }
}

export default function useDexList () {
  const [dexList, setDexList] = useState([])

  const refreshDex = useCallback(async () => {
    try {
      const entries = await getAllPredictions()
    //   console.log(entries)
      const formatted = entries.map(({ key, value }) => ({
        name: key,
        img: URL.createObjectURL(value.imageBlob),
        predictions: {...emptyPred, ...value.predictions} // contains A/B/C/D/E and latest
      }))
    //   console.log('asdss')
      console.log(formatted)
        setDexList(formatted);
    } catch (err) {
      console.error('Dex load failed:', err)
    }
  }, [])

  useEffect(() => {
    refreshDex()
  }, [refreshDex])

  return { dexList, refreshDex }
}
