import React, { useState } from 'react';
import { Typography, Layout, Button, Table, Space, Input } from 'antd';
import { AudioOutlined } from '@ant-design/icons';
import AddOrganizationForm from './AddOrganizationForm';
import ConfirmationModal from './ConfirmationModal';

const { Content } = Layout;
const { Title } = Typography;
const { Search } = Input;

export default function OrganizationManagement() {
  const [organizations, setOrganizations] = useState([]);
  const [addFormVisible, setAddFormVisible] = useState(false);
  const [confirmModalVisible, setConfirmModalVisible] = useState(false);
  const [recordToDelete, setRecordToDelete] = useState(null);
  const [searchText, setSearchText] = useState('');

  const handleAddOrganization = (values) => {
    setOrganizations([...organizations, { ...values, key: organizations.length + 1 }]);
    setAddFormVisible(false);
  };

  const handleEditOrganization = (record) => {
    // Implement edit functionality here
    console.log('Edit record:', record);
  };

  const handleDeleteOrganization = (record) => {
    setRecordToDelete(record);
    setConfirmModalVisible(true);
  };

  const confirmDelete = () => {
    setOrganizations(organizations.filter(item => item.key !== recordToDelete.key));
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

  const filteredOrganizations = organizations.filter(org =>
    org.name.toLowerCase().includes(searchText.toLowerCase()) ||
    org.email.toLowerCase().includes(searchText.toLowerCase())
  );

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: 'Sequence',
      dataIndex: 'sequence',
      key: 'sequence',
    },
    {
      title: 'Action',
      key: 'action',
      render: (text, record) => (
        <Space size="middle">
          <Button onClick={() => handleEditOrganization(record)}>Edit</Button>
          <Button onClick={() => handleDeleteOrganization(record)}>Delete</Button>
        </Space>
      ),
    },
  ];

  return (
    <Content className="m-6 p-6 bg-white min-h-[360px]">
      <Title level={2} className="text-center">Organization Management</Title>
      <Button type="primary" onClick={() => setAddFormVisible(true)} className="mb-4">
        Add Organization
      </Button>
      <Search
        placeholder="Search text"
        allowClear
        onSearch={handleSearch}
        style={{
          width: 204,
        }}
      />
      <Table columns={columns} dataSource={filteredOrganizations} />
      <AddOrganizationForm
        visible={addFormVisible}
        onCreate={handleAddOrganization}
        onCancel={() => setAddFormVisible(false)}
      />
      <ConfirmationModal
        visible={confirmModalVisible}
        onConfirm={confirmDelete}
        onCancel={cancelDelete}
      />
    </Content>
  );
}
