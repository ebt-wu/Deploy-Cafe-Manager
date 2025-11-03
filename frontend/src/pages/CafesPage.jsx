import { useState, useMemo, useEffect, useRef } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Button, Input, Space, Modal, message } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { AgGridReact } from 'ag-grid-react';
import { useNavigate } from 'react-router-dom';
import { getCafes, deleteCafe } from '../api/apiService';
import './GridStyles.css';
import '../styles/custom.css';


const ActionsCellRenderer = (props) => {
  const { onEdit, onDelete, data } = props;

  return (
    <Space>
      <Button
        size='small'
        icon={<EditOutlined />}
        onClick={() => onEdit(data.id)}
      />
      <Button
        size='small'
        icon={<DeleteOutlined />}
        danger
        onClick={() => onDelete(data.id)}
      />
    </Space>
  );
};


const CafesPage = () => {
  const [location, setLocation] = useState('');
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const gridRef = useRef(null);
  
  const [selectedImage, setSelectedImage] = useState(null);
  const [isImageModalVisible, setIsImageModalVisible] = useState(false);


  const { data: cafes = [], isLoading } = useQuery({
    queryKey: ['cafes', location],
    queryFn: () => getCafes(location),
  });


  const deleteMutation = useMutation({
    mutationFn: deleteCafe,
    onSuccess: () => {
      message.success('Cafe deleted successfully');
      queryClient.invalidateQueries(['cafes']);
    },
    onError: () => {
      message.error('Failed to delete cafe');
    },
  });


  const handleDelete = (id) => {
    Modal.confirm({
      title: 'Are you sure you want to delete this cafe?',
      content: 'This will also delete all employees under this cafe.',
      onOk: () => deleteMutation.mutate(id),
    });
  };


  const handleEdit = (id) => {
    navigate(`/cafes/edit/${id}`);
  };

  const handleImageClick = (imagePath) => {
    setSelectedImage(`/${imagePath}`);
    setIsImageModalVisible(true);
  };


  const onGridReady = (params) => {
    gridRef.current = params.api;
    params.api.sizeColumnsToFit();
  };


  useEffect(() => {
    const handleResize = () => {
      if (gridRef.current) {
        gridRef.current.sizeColumnsToFit();
      }
    };


    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);


  const columnDefs = useMemo(() => [
    {
      headerName: 'Logo',
      field: 'logo_url',
      cellRenderer: (params) => {
        if (!params.value) {
          return null;
        }
        
        const imageUrl = `/${params.value}`;
        
        return (
          <img 
            src={imageUrl}
            alt="logo" 
            style={{ 
              width: 40, 
              height: 40, 
              objectFit: 'contain',
              cursor: 'pointer'
            }}
            onClick={() => handleImageClick(params.value)} 
            onError={(e) => {
              console.error('Image load failed for:', imageUrl);
              console.error('Failed URL was:', e.target.src);
            }}
            onLoad={() => {
              console.log('Image loaded successfully:', imageUrl);
            }}
          />
        );
      },
      flex: 1,
      minWidth: 100,
      maxWidth: 150,
      autoHeight: true,
    },
    { 
      headerName: 'Name', 
      field: 'name', 
      sortable: true, 
      filter: true,
      flex: 2,
      minWidth: 150,
      wrapText: true,
      autoHeight: true,
    },
    { 
      headerName: 'Description', 
      field: 'description', 
      flex: 3,
      minWidth: 200,
      wrapText: true,
      autoHeight: true,
    },
    {
      headerName: 'Employees',
      field: 'employees',
      sortable: true,
      cellRenderer: (params) => (
        <a onClick={() => {
          const queryString = new URLSearchParams({
            cafeId: params.data.id,
            cafeName: params.data.name
          }).toString();
          navigate(`/employees?${queryString}`);
        }}>
          {params.value}
        </a>
      ),
      flex: 1,
      minWidth: 120,
      autoHeight: true,
    },
    { 
      headerName: 'Location', 
      field: 'location', 
      sortable: true, 
      filter: true,
      flex: 2,
      minWidth: 150,
      wrapText: true,
      autoHeight: true,
    },
    {
      headerName: 'Actions',
      cellRenderer: ActionsCellRenderer,
      cellRendererParams: {
        onEdit: handleEdit,
        onDelete: handleDelete,
      },
      flex: 1,
      minWidth: 120,
      maxWidth: 150,
      autoHeight: true,
    },
  ], [navigate]);


  const defaultColDef = useMemo(() => ({
    resizable: true,
    cellStyle: { 
      textAlign: 'center',
      lineHeight: '1.5',
    },
  }), []);


  return (
    <div className="page-container"> 
      <div className="table-card"> 
        <div className="table-header">
          <Space style={{ marginBottom: 16 }}>
            <Input
              placeholder="Filter by location"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              style={{ width: 200 }}
            />
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={() => navigate('/cafes/add')}
              className='custom-btn custom-btn-primary'
            >
              Add New Cafe
            </Button>
          </Space>
        </div>


      <div className="ag-theme-alpine" style={{ height: 600, width: '100%' }}>
        <AgGridReact
          ref={gridRef}
          rowData={cafes}
          columnDefs={columnDefs}
          defaultColDef={defaultColDef}
          pagination={true}
          paginationPageSize={10}
          loading={isLoading}
          onGridReady={onGridReady}
        />
      </div>
      
      <Modal
        title="Logo Preview"
        open={isImageModalVisible}
        onCancel={() => setIsImageModalVisible(false)}
        footer={null}
        width={800}
      >
        {selectedImage && (
          <img 
            src={selectedImage} 
            alt="Logo" 
            style={{ width: '100%', height: 'auto' }}
          />
        )}
      </Modal>
    </div>
  </div>
  );
};


export default CafesPage;
