import { Form, Input } from 'antd';

const CustomTextbox = ({ label, name, rules, placeholder, maxLength, ...props }) => {
  return (
    <Form.Item
      label={label}
      name={name}
      rules={rules}
      labelCol={{ style: { fontWeight: 600, color: '#262626' } }}
    >
      <Input
        placeholder={placeholder}
        maxLength={maxLength}
        className="custom-input-field"
        {...props}
      />
    </Form.Item>
  );
};

export default CustomTextbox;
