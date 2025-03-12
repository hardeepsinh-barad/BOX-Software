import React from 'react';
import { Modal, Form, Input, Select } from 'antd';

const { Option } = Select;

const AddDeviceForm = ({ visible, onCreate, onCancel, organizations }) => {
  const [form] = Form.useForm();

  return (
    <Modal
      open={visible}
      title="Add New Device"
      okText="Create"
      cancelText="Cancel"
      onCancel={onCancel}
      onOk={() => {
        form
          .validateFields()
          .then((values) => {
            form.resetFields();
            onCreate(values);
          })
          .catch((info) => {
            console.log('Validate Failed:', info);
          });
      }}
    >
      <Form
        form={form}
        layout="vertical"
        name="add_device_form"
      >
        <Form.Item
          name="name"
          label="Name"
          rules={[
            {
              required: true,
              message: 'Please input the device name!',
            },
          ]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          name="uuid"
          label="UUID"
          rules={[
            {
              required: true,
              message: 'Please input the device UUID!',
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
            {organizations.map((org) => (
              <Option key={org.key} value={org.key}>
                {org.name}
              </Option>
            ))}
          </Select>
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default AddDeviceForm;
