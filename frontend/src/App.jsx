import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import './App.css'
import AuthPage from './pages/AuthPage'
import DonorDashboard from './pages/DonorDashboard'
import NGODashboard from './pages/NGODashboard'

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const checkAuth = () => {
      try {
        const storedUser = localStorage.getItem('user')
        const token = localStorage.getItem('token')

        if (storedUser && token) {
          const userData = JSON.parse(storedUser)
          setUser(userData)
        }
      } catch (error) {
        localStorage.removeItem('user')
        localStorage.removeItem('token')
      } finally {
        setLoading(false)
      }
    }

    checkAuth()
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
  }

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        background: 'linear-gradient(135deg, #4CAF50 0%, #388E3C 100%)'
      }}>
        <div style={{ textAlign: 'center', color: 'white' }}>
          <div style={{
            width: '40px',
            height: '40px',
            border: '4px solid rgba(255,255,255,0.3)',
            borderTop: '4px solid white',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 20px'
          }}></div>
          <h2>Loading FoodBridge...</h2>
        </div>
        <style>{`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    )
  }

  return (
    <Router>
      <Routes>
        <Route path="/" element={<AuthPage setUser={setUser} />} />

        <Route
          path="/donor"
          element={
            user?.role === 'donor'
              ? <DonorDashboard user={user} onLogout={handleLogout} />
              : <Navigate to="/" />
          }
        />

        <Route
          path="/ngo"
          element={
            user?.role === 'ngo'
              ? <NGODashboard user={user} onLogout={handleLogout} />
              : <Navigate to="/" />
          }
        />

        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  )
}

export default App