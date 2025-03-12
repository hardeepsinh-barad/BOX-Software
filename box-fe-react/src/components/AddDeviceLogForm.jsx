import React from 'react';
import { Modal, Form, Input, Select } from 'antd';

const { Option } = Select;

const AddDeviceLogForm = ({ visible, onCreate, onCancel, devices, statuses }) => {
  const [form] = Form.useForm();

  return (
    <Modal
      open={visible}
      title="Add New Device Log"
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
        name="add_device_log_form"
      >
        <Form.Item
          name="device"
          label="Device"
          rules={[
            {
              required: true,
              message: 'Please select the device!',
            },
          ]}
        >
          <Select placeholder="Select a device">
            {devices.map((device) => (
              <Option key={device.key} value={device.key}>
                {device.name}
              </Option>
            ))}
          </Select>
        </Form.Item>
        <Form.Item
          name="status"
          label="Status"
          rules={[
            {
              required: true,
              message: 'Please select the status!',
            },
          ]}
        >
          <Select placeholder="Select a status">
            {statuses.map((status) => (
              <Option key={status} value={status}>
                {status}
              </Option>
            ))}
          </Select>
        </Form.Item>
        <Form.Item
          name="message"
          label="Message"
          rules={[
            {
              required: true,
              message: 'Please input the message!',
            },
          ]}
        >
          <Input />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default AddDeviceLogForm;
