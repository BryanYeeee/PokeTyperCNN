const DB_NAME = 'PredictionCacheDB'
const STORE_NAME = 'predictions'
const DB_VERSION = 1

export function openDB () {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION)

    request.onerror = () => reject(request.error)

    request.onupgradeneeded = () => {
      const db = request.result

      if (!db.objectStoreNames.contains(STORE_NAME)) {
        db.createObjectStore(STORE_NAME)
      }
    }

    request.onsuccess = () => {
      resolve(request.result)
    }
  })
}

export async function savePrediction (fileName, model, data) {
  const db = await openDB()

  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readwrite')
    const store = tx.objectStore(STORE_NAME)

    const getReq = store.get(fileName)

    getReq.onsuccess = () => {
      const existing = getReq.result || { predictions: {} }

      existing.predictions['latest'] = model
      if (data) existing.predictions[model] = data

      const putReq = store.put(existing, fileName)

      putReq.onsuccess = () => resolve(existing)
      putReq.onerror = () => reject(putReq.error)
    }

    getReq.onerror = () => reject(getReq.error)
  })
}

export async function getPrediction (key) {
  const db = await openDB()

  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readonly')
    const store = tx.objectStore(STORE_NAME)

    const request = store.get(key)

    request.onsuccess = () => resolve(request.result)
    request.onerror = () => reject(request.error)
  })
}

export async function deleteItem (key) {
  const db = await openDB()

  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readwrite')
    const store = tx.objectStore(STORE_NAME)

    const request = store.delete(key)

    request.onsuccess = () => resolve(true)
    request.onerror = () => reject(request.error)
  })
}

export async function clearStore () {
  const db = await openDB()

  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readwrite')
    const store = tx.objectStore(STORE_NAME)

    const request = store.clear()

    request.onsuccess = () => resolve(true)
    request.onerror = () => reject(request.error)
  })
}
