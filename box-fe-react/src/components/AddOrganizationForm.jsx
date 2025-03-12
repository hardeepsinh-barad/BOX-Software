import React, { useState } from 'react';
import { Form, Input, Button, Modal } from 'antd';

const AddOrganizationForm = ({ visible, onCreate, onCancel }) => {
  const [form] = Form.useForm();

  return (
    <Modal
      title="Add New Organization"
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
        name="form_in_modal"
      >
        <Form.Item
          name="name"
          label="Name"
          rules={[
            {
              required: true,
              message: 'Please enter the organization name!',
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
              message: 'Please enter the organization email!',
            },
            {
              type: 'email',
              message: 'Please enter a valid email!',
            },
          ]}
        >
          <Input />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default AddOrganizationForm;
