import { useEffect, useState } from 'react';
import { Form, Button, Space, Radio, Select, message, Modal } from 'antd';
import { ManOutlined, WomanOutlined } from '@ant-design/icons';
import { useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { createEmployee, updateEmployee, getEmployees, getCafes } from '../api/apiService';
import CustomTextbox from '../components/common/CustomTextBox';
import '../styles/custom.css';

const AddEditEmployee = () => {
  const [form] = Form.useForm();
  const navigate = useNavigate();
  const { id } = useParams();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);
  const [hasChanges, setHasChanges] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { data: employees } = useQuery({
    queryKey: ['employees'],
    queryFn: () => getEmployees(),
    enabled: isEdit,
  });

  const { data: cafes = [] } = useQuery({
    queryKey: ['cafes'],
    queryFn: () => getCafes(),
  });

  useEffect(() => {
    if (isEdit && employees) {
      const employee = employees.find(e => e.id === id);
      if (employee) {
        form.setFieldsValue({
          name: employee.name,
          email_address: employee.email_address,
          phone_number: employee.phone_number,
          gender: employee.gender,
          cafe_id: employee.cafe,
        });
      }
    }
  }, [isEdit, employees, id, form]);

  const handleFormChange = () => {
    if (!isSubmitting) {
      setHasChanges(true);
    }
  };

  useEffect(() => {
    const handleBeforeUnload = (event) => {
      if (hasChanges && !isSubmitting) {
        event.preventDefault();
        event.returnValue = '';
      }
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => window.removeEventListener('beforeunload', handleBeforeUnload);
  }, [hasChanges, isSubmitting]);

  const handleCancel = () => {
    if (hasChanges) {
      Modal.confirm({
        title: 'Unsaved Changes',
        content: 'You have unsaved changes. Are you sure you want to leave?',
        okText: 'Yes, Leave',
        cancelText: 'No, Stay',
        okButtonProps: { danger: true },
        onOk: () => {
          setHasChanges(false);
          navigate('/employees');
        },
      });
    } else {
      navigate('/employees');
    }
  };

  const mutation = useMutation({
    mutationFn: isEdit ? updateEmployee : createEmployee,
    onSuccess: () => {
      setHasChanges(false);
      setIsSubmitting(false);
      message.success(`Employee ${isEdit ? 'updated' : 'created'} successfully`);
      queryClient.invalidateQueries(['employees']);
      navigate('/employees');
    },
    onError: (error) => {
      setIsSubmitting(false);
      message.error(error.response?.data?.detail || `Failed to ${isEdit ? 'update' : 'create'} employee`);
    },
  });

  const onFinish = (values) => {
    setIsSubmitting(true);
    const payload = isEdit ? { ...values, id } : values;
    mutation.mutate(payload);
  };

  return (
    <div className="page-container">
      <div className="form-container"> 
        <h2>{isEdit ? 'Edit Employee' : 'Add New Employee'}</h2>
      
        {hasChanges && (
          <div className="unsaved-indicator">
            You have unsaved changes
          </div>
        )}

        <Form 
          form={form} 
          layout="vertical" 
          onFinish={onFinish}
          onValuesChange={handleFormChange}
        >
          <CustomTextbox
            label="Name"
            name="name"
            rules={[
              { required: true, message: 'Name is required' },
              { min: 6, max: 10, message: 'Name must be 6-10 characters' },
            ]}
            placeholder="Enter employee name"
            maxLength={10}
          />

          <CustomTextbox
            label="Email Address"
            name="email_address"
            rules={[
              { required: true, message: 'Email is required' },
              { type: 'email', message: 'Please enter a valid email' },
            ]}
            placeholder="Enter email"
          />

          <CustomTextbox
            label="Phone Number"
            name="phone_number"
            rules={[
              { required: true, message: 'Phone number is required' },
              { 
                pattern: /^[89]\d{7}$/,
                message: 'Phone must start with 8 or 9 and have 8 digits'
              },
            ]}
            placeholder="Enter phone number"
          />

          <Form.Item
            label="Gender"
            name="gender"
            rules={[{ required: true, message: 'Gender is required' }]}
          >
            <Radio.Group>
              <Radio value="Male">
                <ManOutlined style={{ color: '#1890ff', marginRight: 8 }} />
                Male
              </Radio>
              <Radio value="Female">
                <WomanOutlined style={{ color: '#ff85c0', marginRight: 8 }} />
                Female
              </Radio>
            </Radio.Group>
          </Form.Item>

          <Form.Item label="Assigned Café" name="cafe_id">
            <Select 
              placeholder="Select a cafe" 
              allowClear
              loading={cafes.length === 0}
            >
              {cafes.map(cafe => (
                <Select.Option key={cafe.id} value={cafe.id}>
                  {cafe.name}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item>
            <Space>
              <Button 
                type="primary" 
                htmlType="submit" 
                loading={mutation.isPending}
                disabled={!hasChanges}
                className="custom-btn custom-btn-primary"
              >
                Submit
              </Button>
              <Button 
                onClick={handleCancel}
                className="custom-btn"
              >
                  Cancel
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </div>
    </div>
  );
};

export default AddEditEmployee;
