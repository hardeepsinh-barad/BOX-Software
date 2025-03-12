import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu, Avatar } from 'antd';
import {
  UserOutlined,
  LogoutOutlined,
  ApartmentOutlined,
  TeamOutlined,
  DesktopOutlined,
  HistoryOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  DashboardOutlined
} from '@ant-design/icons';
import Cookies from 'js-cookie';
import * as jwt_decode from 'jwt-decode';

const { Sider } = Layout;

export default function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [collapsed, setCollapsed] = useState(false);
  const [selectedKeys, setSelectedKeys] = useState(['1']);
  const [userName, setUserName] = useState('');
  const [userEmail, setUserEmail] = useState('');

  // Check if the user is on the login page
  const isLoginPage = location.pathname === '/';

  useEffect(() => {
    const path = location.pathname;
    let key;

    switch (path) {
      case '/dashboard':
        key = '1';
        break;
      case '/organization':
        key = '2';
        break;
      case '/users':
        key = '3';
        break;
      case '/devices':
        key = '4';
        break;
      case '/logs':
        key = '5';
        break;
      default:
        key = '1';
        break;
    }

    setSelectedKeys([key]);
  }, [location.pathname]);

  useEffect(() => {
    const token = Cookies.get('token');
    if (token) {
      try {
        const decodedToken = jwt_decode.jwtDecode(token);
        setUserName(decodedToken.name || 'John Doe'); // Use a default if name is not in token
        setUserEmail(decodedToken.email || 'john.doe@example.com'); // Use a default if email is not in token
      } catch (error) {
        console.error('Error decoding token:', error);
        setUserName('John Doe');
        setUserEmail('john.doe@example.com');
      }
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  const toggleCollapsed = () => {
    setCollapsed(!collapsed);
  };

  const handleMenuClick = (key) => {
    switch (key) {
      case '1':
        navigate('/dashboard');
        break;
      case '2':
        navigate('/organization');
        break;
      case '3':
        navigate('/users');
        break;
      case '4':
        navigate('/devices');
        break;
      case '5':
        navigate('/logs');
        break;
      default:
        break;
    }
  };

  const items = [
    { key: '1', icon: <DashboardOutlined />, label: 'Dashboard' },
    { key: '2', icon: <ApartmentOutlined />, label: 'Organization Management' },
    { key: '3', icon: <TeamOutlined />, label: 'User Management' },
    { key: '4', icon: <DesktopOutlined />, label: 'Device Management' },
    { key: '5', icon: <HistoryOutlined />, label: 'Device Logs' },
  ];

  // Conditionally render the Sidebar
  if (isLoginPage) {
    return null; // Don't render the sidebar on the login page
  }

  return (
    <Sider
      collapsible
      collapsed={collapsed}
      onCollapse={toggleCollapsed}
      collapsedWidth={80}
      trigger={null}
      style={{ background: '#fff', height: '100%' }}
    >
    <div style={{ display:'flex', flexDirection: 'column', justifyContent: 'space-between', height: '100%' }}>
        <div>
        <div
        style={{
          height: '64px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#001529',
          color: 'white',
          fontSize: '20px',
        }}
      >
          {!collapsed && <span style={{ marginLeft: '1px' }}>Test</span>}
        {React.createElement(collapsed ? MenuUnfoldOutlined : MenuFoldOutlined, {
          className: 'trigger',
          onClick: toggleCollapsed,
          style: { color: 'white', fontSize: '20px',marginLeft: '26px' },
        })}
      </div>
    
     <Menu
        mode="inline"
        selectedKeys={selectedKeys}
        style={{ height: 'auto', borderRight: 0 }}
        onClick={(e) => handleMenuClick(e.key)}
        items={items}
      >
        
      </Menu>
        </div>
      <div style={{
        padding: '16px',
        textAlign: 'center',
        position: 'unset',
        bottom: 0,
        left: 0,
        right: 0,
        }}>
        <Avatar size="large" icon={<UserOutlined />} />
        <div style={{ marginTop: '8px' }}>{userName}</div>
        <div style={{ fontSize: '12px', color: 'rgba(0, 0, 0, 0.45)' }}>{userEmail}</div>
        <a onClick={handleLogout} style={{ color: '#1890ff', marginTop: '12px', display: 'block' }}>
          <LogoutOutlined /> Logout
        </a>
      </div>
     </div>
    </Sider>
  );
}
