import { useEffect, useState } from 'react';
import { Form, Button, Space, Upload, message, Modal } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import { useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { createCafe, updateCafe, getCafes, uploadLogo } from '../api/apiService';
import CustomTextbox from '../components/common/CustomTextBox';
import '../styles/custom.css';

const MAX_FILE_SIZE = 2 * 1024 * 1024;

const AddEditCafe = () => {
  const [form] = Form.useForm();
  const navigate = useNavigate();
  const { id } = useParams();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);
  const [logoFile, setLogoFile] = useState(null);
  const [hasChanges, setHasChanges] = useState(false); 
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { data: cafes } = useQuery({
    queryKey: ['cafes'],
    queryFn: () => getCafes(),
    enabled: isEdit,
  });

  useEffect(() => {
    if (isEdit && cafes) {
      const cafe = cafes.find(c => c.id === id);
      if (cafe) {
        form.setFieldsValue(cafe);
      }
    }
  }, [isEdit, cafes, id, form]);

  const handleFormChange = () => {
    if (!isSubmitting) {
      setHasChanges(true);
    }
  };

  const handleLogoFileChange = (file) => {
    setLogoFile(file);
    if (file) {
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
          navigate('/cafes');
        },
      });
    } else {
      navigate('/cafes');
    }
  };

  const mutation = useMutation({
    mutationFn: async (payload) => {
      let logoPath = payload.logo_url;
      if (logoFile) {
        if (logoFile.size > MAX_FILE_SIZE) {
          throw new Error(`File size must be less than 2MB`);
        }

        const formData = new FormData();
        formData.append('file', logoFile);
        const uploadResult = await uploadLogo(formData);
        logoPath = uploadResult.file_path;
      }

      const cafeData = { ...payload, logo_url: logoPath };
      return isEdit ? updateCafe(cafeData) : createCafe(cafeData);
    },
    onSuccess: () => {
      setHasChanges(false);
      setIsSubmitting(false);
      message.success(`Cafe ${isEdit ? 'updated' : 'created'} successfully`);
      queryClient.invalidateQueries(['cafes']);
      navigate('/cafes');
    },
    onError: (error) => {
      setIsSubmitting(false);
      message.error(error.message || `Failed to ${isEdit ? 'update' : 'create'} cafe`);
    },
  });

  const handleBeforeUpload = (file) => {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    
    if (!allowedTypes.includes(file.type)) {
      message.error('Only JPEG, PNG, GIF, and WebP images are allowed');
      return false;
    }

    if (file.size > MAX_FILE_SIZE) {
      message.error(`File size must be less than 2MB. Your file is ${(file.size / (1024 * 1024)).toFixed(2)}MB`);
      return false;
    }

    message.success('File selected successfully');
    handleLogoFileChange(file);
    return false;
  };

  const onFinish = (values) => {
    if (logoFile && logoFile.size > MAX_FILE_SIZE) {
      message.error(`File size must be less than 2MB`);
      setLogoFile(null);
      return;
    }

    setIsSubmitting(true);

    const payload = {
      ...values,
      logo_url: logoFile ? logoFile.name : values.logo_url,
    };

    if (isEdit) {
      payload.id = id;
    }

    mutation.mutate(payload);
  };

  return (
    <div className="page-container">
      <div className="form-container">
        <h2>{isEdit ? 'Edit Cafe' : 'Add New Cafe'}</h2>
        
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
            placeholder="Enter cafe name"
            maxLength={10}
          />

          <CustomTextbox
            label="Description"
            name="description"
            rules={[
              { required: true, message: 'Description is required' },
              { max: 256, message: 'Description must not exceed 256 characters' },
            ]}
            placeholder="Enter description"
            maxLength={256}
          />

          <Form.Item 
            label="Logo (Optional)" 
            name="logo_url"
            className="optional-field"
          >
            <Upload
              maxCount={1}
              beforeUpload={handleBeforeUpload}
              accept="image/*"
              className="custom-upload" 
            >
              <Button icon={<UploadOutlined />} className="custom-btn">
                Upload Logo (Max 2MB) - Optional
              </Button>
            </Upload>
          </Form.Item>

          <CustomTextbox
            label="Location"
            name="location"
            rules={[{ required: true, message: 'Location is required' }]}
            placeholder="Enter location"
          />

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

export default AddEditCafe;
