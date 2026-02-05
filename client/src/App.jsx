import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [gridSize, setGridSize] = useState(10)
  const [robots, setRobots] = useState([])
  const [obstacles, setObstacles] = useState([])
  const [zones, setZones] = useState({ pickup: [], dropoff: [], charging: [] })

  const fetchStatus = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:5001/status')
      setRobots(res.data.robots)
      setObstacles(res.data.obstacles)
      setZones(res.data.zones)
      setGridSize(res.data.grid_size)
    } catch (error) {
      console.error("Connection Error:", error)
    }
  }

  const handleCellClick = async (r, c) => {
    try {
      await axios.post('http://127.0.0.1:5001/toggle_obstacle', { r, c })
      fetchStatus() 
    } catch (error) {
      console.error("Error toggling obstacle:", error)
    }
  }

  useEffect(() => {
    fetchStatus()
    const interval = setInterval(async () => {
      await axios.post('http://127.0.0.1:5001/tick')
      fetchStatus()
    }, 1000)
    return () => clearInterval(interval)
  }, [])

  const renderCell = (r, c) => {
    // 1. Obstacles
    if (obstacles.some(o => o[0] === r && o[1] === c)) return <div className="obstacle" />
    
    // 2. Zones
    if (zones.pickup && zones.pickup[0] === r && zones.pickup[1] === c) return <div className="pickup-zone">📦</div>
    if (zones.dropoff && zones.dropoff[0] === r && zones.dropoff[1] === c) return <div className="dropoff-zone">🚚</div>
    if (zones.charging && zones.charging[0] === r && zones.charging[1] === c) return <div className="charging-zone">⚡</div>

    // 3. Path Visualization (Ghost Tracks)
    // Check if this cell is in ANY robot's planned path
    for (let bot of robots) {
      if (bot.path && bot.path.some(p => p[0] === r && p[1] === c)) {
        return <div className="path-dot" style={{backgroundColor: bot.id === 1 ? '#ff9900' : bot.id === 2 ? '#2196f3' : '#9c27b0'}} />
      }
    }
    
    return null
  }

  return (
    <div className="container">
      <h1>AutoWare: Interactive Fleet Control</h1>
      <p style={{marginBottom: '10px', color: '#666'}}>Click any empty square to spawn a wall!</p>
      
      <div className="grid-board">
        {Array.from({ length: gridSize }).map((_, r) =>
          Array.from({ length: gridSize }).map((_, c) => (
            <div 
              key={`${r}-${c}`} 
              className="cell" 
              onClick={() => handleCellClick(r, c)}
            >
              {renderCell(r, c)}
            </div>
          ))
        )}

        {robots.map(bot => (
          <div
            key={bot.id}
            className="robot"
            style={{
              top: `${bot.pos[0] * 50}px`,
              left: `${bot.pos[1] * 50}px`,
              backgroundColor: bot.state === 'CHARGING' ? '#ff3d00' : '#ff9900'
            }}
          >
            {bot.state === 'CHARGING' ? '⚡' : '🤖'}
          </div>
        ))}
      </div>

      <div className="telemetry">
        <h3>Live Telemetry</h3>
        {robots.map(bot => (
          <div key={bot.id} style={{ marginBottom: '10px', borderBottom: '1px solid #eee', paddingBottom: '5px' }}>
             <strong>Bot {bot.id}:</strong> <span style={{ color: bot.state === "CHARGING" ? 'red' : 'green' }}>{bot.state}</span>
            <br/>
            🔋 {bot.battery}% | 📍 ({bot.pos[0]}, {bot.pos[1]})
          </div>
        ))}
      </div>
    </div>
  )
}

export default App