import React, { useState, useEffect } from 'react';
import { Typography, Layout, Button, Table, Space, Input } from 'antd';
import AddUserForm from './AddUserForm';
import ConfirmationModal from './ConfirmationModal';
import userService from '../../../src/services/userService';

const { Content } = Layout;
const { Title } = Typography;
const { Search } = Input;

export default function UserManagement() {
  const [users, setUsers] = useState([]);
  const [addFormVisible, setAddFormVisible] = useState(false);
  const [confirmModalVisible, setConfirmModalVisible] = useState(false);
  const [recordToDelete, setRecordToDelete] = useState(null);
  const [searchText, setSearchText] = useState('');
  const [organizations, setOrganizations] = useState([]); // Dummy organization data

  useEffect(() => {
    // Fetch organizations from API or use dummy data
    setOrganizations([
      { key: '1', name: 'Org 1' },
      { key: '2', name: 'Org 2' },
    ]);

    // Fetch users from API
    const fetchUsers = async () => {
      try {
        const usersData = await userService.getUsers();
        setUsers(usersData);
      } catch (error) {
        console.error("Failed to fetch users:", error);
      }
    };

    fetchUsers();
  }, []);

  const handleAddUser = (values) => {
    setUsers([...users, { ...values, key: users.length + 1 }]);
    setAddFormVisible(false);
  };

  const handleEditUser = (record) => {
    // Implement edit functionality here
    console.log('Edit record:', record);
  };

  const handleDeleteUser = async (record) => {
    setRecordToDelete(record);
    setConfirmModalVisible(true);
  };

  const confirmDelete = async () => {
    try {
      await userService.deleteUser(recordToDelete.id); // Assuming record has an 'id' field
      setUsers(users.filter(item => item.id !== recordToDelete.id));
      setConfirmModalVisible(false);
      setRecordToDelete(null);
    } catch (error) {
      console.error("Failed to delete user:", error);
      // Handle error appropriately (e.g., display an error message)
    }
  };

  const cancelDelete = () => {
    setConfirmModalVisible(false);
    setRecordToDelete(null);
  };

  const handleSearch = (e) => {
    setSearchText(e.target.value);
  };

  const filteredUsers = users.filter(user =>
    user.name.toLowerCase().includes(searchText.toLowerCase()) ||
    user.email.toLowerCase().includes(searchText.toLowerCase())
  );

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Contact Number',
      dataIndex: 'contact_number',
      key: 'contact_number',
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: 'Organization',
      dataIndex: 'organization',
      key: 'organization',
    },
    {
      title: 'Role',
      dataIndex: 'role',
      key: 'role',
    },
    {
      title: 'Action',
      key: 'action',
      render: (text, record) => (
        <Space size="middle">
          <Button onClick={() => handleEditUser(record)}>Edit</Button>
          <Button onClick={() => handleDeleteUser(record)}>Delete</Button>
        </Space>
      ),
    },
  ];

  return (
    <Content className="m-6 p-6 bg-white min-h-[360px]">
      <Title level={2} className="text-center">User Management</Title>
      <Button type="primary" onClick={() => setAddFormVisible(true)} className="mb-4">
        Add User
      </Button>
      <Search
        placeholder="Search text"
        allowClear
        onSearch={handleSearch}
        style={{ 
          width: 204,
        }}
      />
      <Table columns={columns} dataSource={filteredUsers} />
      <AddUserForm
        visible={addFormVisible}
        onCreate={handleAddUser}
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
