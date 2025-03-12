import React from 'react';
import { Modal } from 'antd';

const ConfirmationModal = ({ visible, onConfirm, onCancel }) => {
  return (
    <Modal
      title="Confirm Deletion"
      onOk={onConfirm}
      onCancel={onCancel}
    >
      <p className="text-red-500">Are you sure you want to delete this organization?</p>
    </Modal>
  );
};

export default ConfirmationModal;
