import React, { useState, useEffect } from 'react';
import { Typography, Layout, Button, Table, Space, Input, message } from 'antd';
import AddOrganizationForm from './AddOrganizationForm';

const { Content } = Layout;
const { Title } = Typography;
const { Search } = Input;

export default function OrganizationManagement() {
  const [organizations, setOrganizations] = useState([]);
  const [addFormVisible, setAddFormVisible] = useState(false);
  const [searchText, setSearchText] = useState('');
  const [editingRecord, setEditingRecord] = useState(null);

  useEffect(() => {
    // Fetch organizations from API
    const fetchOrganizations = async () => {
      try {
        const response = await fetch('http://192.168.1.27:8000/organizations/'); // Replace with your API endpoint
        const data = await response.json();

        // Ensure each item has a unique key
        const organizationsWithKeys = data.map((org, index) => ({
          ...org,
          key: org.id || index.toString(), // Use org.id if available, otherwise use index
        }));

        setOrganizations(organizationsWithKeys);
      } catch (error) {
        console.error('Error fetching organizations:', error);
      }
    };

    fetchOrganizations();
  }, []); // Empty dependency array ensures this runs only once on component mount

  const handleAddOrganization = (values) => {
    setOrganizations([...organizations, { ...values, key: organizations.length + 1 }]);
    setAddFormVisible(false);
  };

  const handleEditOrganization = (record) => {
    setEditingRecord(record);
    // Implement edit functionality here, e.g., open a modal form
    console.log('Edit record:', record);
  };

  const handleDeleteOrganization = async (record) => {
    console.log("Deleting record:", record); // Debugging: Check if record is being set correctly
    try {
      const response = await fetch(`http://192.168.1.27:8000/organizations/${record.id}`, { // Replace with your API endpoint
        method: 'DELETE',
      });

      if (response.ok) {
        setOrganizations(organizations.filter(item => item.id !== record.id));
        message.success('Organization deleted successfully'); // Success message
      } else {
        message.error('Failed to delete organization'); // Error message
      }
    } catch (error) {
      console.error('Error deleting organization:', error);
      message.error('Error deleting organization'); // Error message
    }
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
        onChange={handleSearch}
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
    </Content>
  );
}
