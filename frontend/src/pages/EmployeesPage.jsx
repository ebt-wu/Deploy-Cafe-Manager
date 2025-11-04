import { useState, useMemo, useEffect, useRef } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Button, Space, Modal, message } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, ManOutlined, WomanOutlined } from '@ant-design/icons';
import { AgGridReact } from 'ag-grid-react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { getEmployees, deleteEmployee } from '../api/apiService';
import './GridStyles.css';
import '../styles/custom.css';

const ActionsRenderer = (props) => {
  const { onEdit, onDelete, data } = props;

  return (
    <Space>
      <Button
        size='small'
        icon={<EditOutlined />}
        onClick={() => onEdit(data.id)}
        className="custom-btn"
      />
      <Button
        size='small'
        icon={<DeleteOutlined />}
        danger
        onClick={() => onDelete(data.id)}
        className="custom-btn"      
      />
    </Space>
  );
};

const GenderRenderer = (props) => {
  const { value } = props;
  
  if (value === 'Male') {
    return <ManOutlined style={{ fontSize: '18px', color: '#1890ff' }} />;
  } else if (value === 'Female') {
    return <WomanOutlined style={{ fontSize: '18px', color: '#ff85c0' }} />;
  }
  return value;
};

const EmployeesPage = () => {
  const [searchParams] = useSearchParams();
  const cafeFilter = searchParams.get('cafeId') || ''; //this is the id 
  const cafeName = searchParams.get('cafeName') || '';
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const gridRef = useRef(null);
  const { data: employees = [], isLoading } = useQuery({
    queryKey: ['employees', cafeFilter],
    queryFn: () => getEmployees(cafeFilter),
  });

  const deleteMutation = useMutation({
    mutationFn: deleteEmployee,
    onSuccess: () => {
      message.success('Employee deleted successfully');
      queryClient.invalidateQueries(['employees']);
    },
    onError: () => {
      message.error('Failed to delete employee');
    },
  });

  const handleDelete = (id) => {
    console.log('Deleting employee with id:', id);
    Modal.confirm({
      title: 'Are you sure you want to delete this employee?',
      onOk: () => deleteMutation.mutate(id),
    });
  };

  const handleEdit = (id) => {
    navigate(`/employees/edit/${id}`);
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
      headerName: 'Employee ID', 
      field: 'id', 
      sortable: true,
      flex: 1,
      minWidth: 120,
      wrapText: true,
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
      headerName: 'Email', 
      field: 'email_address',
      flex: 2,
      minWidth: 150,
      wrapText: true,
      autoHeight: true,
    },
    { 
      headerName: 'Phone', 
      field: 'phone_number',
      flex: 1,
      minWidth: 120,
      autoHeight: true,
    },
    { 
      headerName: 'Gender', 
      field: 'gender',
      cellRenderer: GenderRenderer,
      flex: 1,
      minWidth: 100,
      autoHeight: true,
    },
    { 
      headerName: 'Days Worked', 
      field: 'days_worked', 
      sortable: true,
      flex: 1,
      minWidth: 120,
      autoHeight: true,
    },
    { 
      headerName: 'Café', 
      field: 'cafe',
      flex: 1,
      minWidth: 120,
      wrapText: true,
      autoHeight: true,
    },
    {
      headerName: 'Actions',
      cellRenderer: ActionsRenderer,
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
          <div>
            <h2 className="page-title">Employees</h2> 
            {cafeFilter && (
              <div className="custom-tag tag-active" style={{ marginTop: '8px' }}>
                Showing employees for Café Name: {cafeName}
              </div>
            )}
          </div>

        <Space>
            {cafeFilter && (
              <Button 
                onClick={() => navigate('/cafes')}
                className="custom-btn"
              >
                Back to Cafés
              </Button>
            )}
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={() => navigate('/employees/add')}
              className="custom-btn custom-btn-primary"
            >
              Add New Employee
            </Button>
          </Space>
        </div>

      <div className="ag-theme-alpine" style={{ height: 600, width: '100%' }}>
        <AgGridReact
          ref={gridRef}
          rowData={employees}
          columnDefs={columnDefs}
          defaultColDef={defaultColDef}
          pagination={true}
          paginationPageSize={10}
          loading={isLoading}
          onGridReady={onGridReady}
        />
      </div>
    </div>
    </div>
  );
};

export default EmployeesPage;
