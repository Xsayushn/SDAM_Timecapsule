import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './AuthContext.js';
import Login from './components/Login.js';
import Register from './components/Register.js';
import CapsuleApp from './components/CapsuleApp.js';
import Profile from './components/Profile.js';
import './App.css';

function App() {
  const { user, loading } = useAuth();
  const [showRegister, setShowRegister] = useState(false);

  if (loading) {
    return (
      <div className="loading-fullscreen">
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <Router>
      <Routes>
        {!user ? (
          <>
            <Route path="/" element={
              showRegister ? (
                <Register onSwitchToLogin={() => setShowRegister(false)} />
              ) : (
                <Login onSwitchToRegister={() => setShowRegister(true)} />
              )
            } />
            <Route path="*" element={<Navigate to="/" />} />
          </>
        ) : (
          <>
            <Route path="/" element={<CapsuleApp />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="*" element={<Navigate to="/" />} />
          </>
        )}
      </Routes>
    </Router>
  );
}

export default App;