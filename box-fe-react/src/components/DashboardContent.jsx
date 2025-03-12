import React from 'react';
import { Typography, Layout } from 'antd';

const { Content } = Layout;
const { Title } = Typography;

export default function DashboardContent() {
  return (
    <Content style={{ margin: '24px 16px', padding: 24, background: '#fff', minHeight: 360 }}>
      <Title level={2} style={{ textAlign: 'center' }}>Welcome to the Dashboard!</Title>
    </Content>
  );
}
