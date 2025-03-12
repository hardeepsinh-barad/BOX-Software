import React, { useState, useEffect } from 'react';
import { Typography, Layout, Button, Table, Space, Input, Select } from 'antd';
import AddDeviceLogForm from './AddDeviceLogForm';
import ConfirmationModal from './ConfirmationModal';

const { Content } = Layout;
const { Title } = Typography;
const { Search } = Input;
const { Option } = Select;

export default function DeviceLogs() {
  const [deviceLogs, setDeviceLogs] = useState([]);
  const [addFormVisible, setAddFormVisible] = useState(false);
  const [confirmModalVisible, setConfirmModalVisible] = useState(false);
  const [recordToDelete, setRecordToDelete] = useState(null);
  const [searchText, setSearchText] = useState('');
  const [devices, setDevices] = useState([]);
  const [statuses, setStatuses] = useState(['Success', 'Failed', 'Pending']); // Example statuses

  useEffect(() => {
    // Fetch devices from API or use dummy data
    setDevices([
      { key: '1', name: 'Device 1' },
      { key: '2', name: 'Device 2' },
    ]);
  }, []);

  const handleAddDeviceLog = (values) => {
    setDeviceLogs([...deviceLogs, { ...values, key: deviceLogs.length + 1 }]);
    setAddFormVisible(false);
  };

  const handleEditDeviceLog = (record) => {
    // Implement edit functionality here
    console.log('Edit record:', record);
  };

  const handleDeleteDeviceLog = (record) => {
    setRecordToDelete(record);
    setConfirmModalVisible(true);
  };

  const confirmDelete = () => {
    setDeviceLogs(deviceLogs.filter(item => item.key !== recordToDelete.key));
    setConfirmModalVisible(false);
    setRecordToDelete(null);
  };

  const cancelDelete = () => {
    setConfirmModalVisible(false);
    setRecordToDelete(null);
  };

  const handleSearch = (e) => {
    setSearchText(e.target.value);
  };

  const filteredDeviceLogs = deviceLogs.filter(log =>
    log.message.toLowerCase().includes(searchText.toLowerCase())
  );

  const columns = [
    {
      title: 'Device',
      dataIndex: 'device',
      key: 'device',
      render: (text, record) => {
        const device = devices.find(device => device.key === text);
        return device ? device.name : 'Unknown';
      }
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
    },
    {
      title: 'Message',
      dataIndex: 'message',
      key: 'message',
    },
    {
      title: 'Action',
      key: 'action',
      render: (text, record) => (
        <Space size="middle">
          <Button onClick={() => handleEditDeviceLog(record)}>Edit</Button>
          <Button onClick={() => handleDeleteDeviceLog(record)}>Delete</Button>
        </Space>
      ),
    },
  ];

  return (
    <Content className="m-6 p-6 bg-white min-h-[360px]">
      <Title level={2} className="text-center">Device Log Management</Title>
      <Button type="primary" onClick={() => setAddFormVisible(true)} className="mb-4">
        Add Device Log
      </Button>
      <Search
        placeholder="Search text"
        allowClear
        onChange={handleSearch}
        style={{
          width: 204,
        }}
      />
      <Table columns={columns} dataSource={filteredDeviceLogs} />
      <AddDeviceLogForm
        visible={addFormVisible}
        onCreate={handleAddDeviceLog}
        onCancel={() => setAddFormVisible(false)}
        devices={devices}
        statuses={statuses}
      />
      <ConfirmationModal
        visible={confirmModalVisible}
        onConfirm={confirmDelete}
        onCancel={cancelDelete}
      />
    </Content>
  );
}
