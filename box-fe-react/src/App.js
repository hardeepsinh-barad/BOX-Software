import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import routes from './routes';
import './index.css';

function App() {
  return (
    <Router basename="/Box/">
      <div style={{ display: 'flex', height: '100vh' }}>
        <Sidebar /> {/* Temporarily remove the Sidebar component */}
        <div style={{ flex: 1, overflow: 'auto' }}>
          <Routes>
            {routes.map((route, index) => (
              <Route key={index} path={route.path} element={route.element} />
            ))} 
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
