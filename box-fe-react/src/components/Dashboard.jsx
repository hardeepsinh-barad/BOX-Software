import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Layout } from 'antd';
import DashboardContent from './DashboardContent';

const { Content } = Layout;

export default function Dashboard() {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/');
    }
  }, [navigate]);

  return (
    <Layout style={{  }}>
      <Layout>
        <Content>
          <DashboardContent />
        </Content>
      </Layout>
    </Layout>
  );
}
