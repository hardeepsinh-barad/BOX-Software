import React from 'react';
import { Form, Input, Modal, Select } from 'antd';
import userService from '../services/userService';

const { Option } = Select;

const AddUserForm = ({visible,onCreate, onCancel, organizations }) => {
  const [form] = Form.useForm();

  return (
    <Modal
      open={visible}
      title="Add New User"
      okText="Create"
      cancelText="Cancel"
      onCancel={onCancel}
      onOk={() => {
        form
          .validateFields()
          .then(async (values) => {
            try {
              // Create user using userService
              await userService.createUser(values);
              form.resetFields();
              onCreate(values);
            } catch (error) {
              console.error("Failed to create user:", error);
              // Handle error appropriately (e.g., display an error message)
            }
          })
          .catch((info) => {
            console.log('Validate Failed:', info);
          });
      }}
    >
      <Form
        form={form}
        layout="vertical"
        name="form_in_modal"
      >
        <Form.Item
          name="name"
          label="Name"
          rules={[
            {
              required: true,
              message: 'Please enter the user name!',
            },
          ]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          name="contact_number"
          label="Contact Number"
          rules={[
            {
              required: true,
              message: 'Please enter the contact number!',
            },
          ]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          name="email"
          label="Email"
          rules={[
            {
              required: true,
              message: 'Please enter the user email!',
            },
            {
              type: 'email',
              message: 'Please enter a valid email!',
            },
          ]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          name="organization"
          label="Organization"
          rules={[
            {
              required: true,
              message: 'Please select the organization!',
            },
          ]}
        >
          <Select placeholder="Select an organization">
            {organizations.map(org => (
              <Option key={org.key} value={org.name}>{org.name}</Option>
            ))}
          </Select>
        </Form.Item>
        <Form.Item
          name="role"
          label="Role"
          rules={[
            {
              required: true,
              message: 'Please select the role!',
            },
          ]}
        >
          <Select placeholder="Select a role">
            <Option value="admin">Admin</Option>
            <Option value="user">User</Option>
          </Select>
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default AddUserForm;
