import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Layout } from 'antd';
import Sidebar from './components/Sidebar';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import OrganizationManagement from './components/OrganizationManagement';
import UserManagement from './components/UserManagement';
import DeviceManagement from './components/DeviceManagement';
import DeviceLogs from './components/DeviceLogs';
import './index.css';

const { Content } = Layout;

function App() {
  return (
    <Router basename="/">
      <Layout style={{ height: '100%', display: 'flex' }}>
        <Sidebar />
          <Content style={{
            marginLeft: 200,
            overflowY: 'auto',
            overflowX: 'hidden',
            margin: 5, // Reset margin
            padding: 5, // Reset padding
          }}>
            <Routes>
              <Route path="/" element={<Login />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/organization" element={<OrganizationManagement />} />
              <Route path="/users" element={<UserManagement />} />
              <Route path="/devices" element={<DeviceManagement />} />
              <Route path="/logs" element={<DeviceLogs />} />
            </Routes>
          </Content>
      </Layout>
    </Router>
  );
}

export default App;