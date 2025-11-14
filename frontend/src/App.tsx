import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className="flex flex-col justify-center gap-3 max max-w-7xl m-auto">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
      </div>
    
    </>
  )
}

export default App
