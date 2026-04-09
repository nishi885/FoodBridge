import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import './App.css'
import AuthPage from './pages/AuthPage'
import DonorDashboard from './pages/DonorDashboard'
import NGODashboard from './pages/NGODashboard'

function App() {
  const [user, setUser] = useState(null)

  const handleLogout = () => {
    setUser(null)
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