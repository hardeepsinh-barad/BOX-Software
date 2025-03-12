import React, { useState, useEffect } from 'react';
import { Typography, Layout, Button, Table, Space, Input, Select } from 'antd';
import AddDeviceForm from './AddDeviceForm';
import ConfirmationModal from './ConfirmationModal';

const { Content } = Layout;
const { Title } = Typography;
const { Search } = Input;
const { Option } = Select;

export default function DeviceManagement() {
  const [devices, setDevices] = useState([]);
  const [addFormVisible, setAddFormVisible] = useState(false);
  const [confirmModalVisible, setConfirmModalVisible] = useState(false);
  const [recordToDelete, setRecordToDelete] = useState(null);
  const [searchText, setSearchText] = useState('');
  const [organizations, setOrganizations] = useState([]);

  useEffect(() => {
    // Fetch organizations from API or use dummy data
    setOrganizations([
      { key: '1', name: 'Org 1' },
      { key: '2', name: 'Org 2' },
    ]);
  }, []);

  const handleAddDevice = (values) => {
    setDevices([...devices, { ...values, key: devices.length + 1 }]);
    setAddFormVisible(false);
  };

  const handleEditDevice = (record) => {
    // Implement edit functionality here
    console.log('Edit record:', record);
  };

  const handleDeleteDevice = (record) => {
    setRecordToDelete(record);
    setConfirmModalVisible(true);
  };

  const confirmDelete = () => {
    setDevices(devices.filter(item => item.key !== recordToDelete.key));
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

  const filteredDevices = devices.filter(device =>
    device.name.toLowerCase().includes(searchText.toLowerCase()) ||
    device.uuid.toLowerCase().includes(searchText.toLowerCase())
  );

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'UUID',
      dataIndex: 'uuid',
      key: 'uuid',
    },
    {
      title: 'Organization',
      dataIndex: 'organization',
      key: 'organization',
      render: (text, record) => {
        const org = organizations.find(org => org.key === text);
        return org ? org.name : 'Unknown';
      }
    },
    {
      title: 'Action',
      key: 'action',
      render: (text, record) => (
        <Space size="middle">
          <Button onClick={() => handleEditDevice(record)}>Edit</Button>
          <Button onClick={() => handleDeleteDevice(record)}>Delete</Button>
        </Space>
      ),
    },
  ];

  return (
    <Content className="m-6 p-6 bg-white min-h-[360px]">
      <Title level={2} className="text-center">Device Management</Title>
      <Button type="primary" onClick={() => setAddFormVisible(true)} className="mb-4">
        Add Device
      </Button>
      <Search
        placeholder="Search text"
        allowClear
        onChange={handleSearch}
        style={{
          width: 204,
        }}
      />
      <Table columns={columns} dataSource={filteredDevices} />
      <AddDeviceForm
        visible={addFormVisible}
        onCreate={handleAddDevice}
        onCancel={() => setAddFormVisible(false)}
        organizations={organizations}
      />
      <ConfirmationModal
        visible={confirmModalVisible}
        onConfirm={confirmDelete}
        onCancel={cancelDelete}
      />
    </Content>
  );
}
