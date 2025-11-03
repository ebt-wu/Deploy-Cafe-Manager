import { BrowserRouter, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import { CoffeeOutlined, TeamOutlined } from '@ant-design/icons';
import CafesPage from './pages/CafesPage';
import EmployeesPage from './pages/EmployeesPage';
import AddEditCafe from './pages/AddEditCafe';
import AddEditEmployee from './pages/AddEditEmployee';

const { Header, Content } = Layout;

function AppContent() {
  const navigate = useNavigate();
  const location = useLocation();

  // Determine which menu item should be selected based on current path
  const selectedKey = location.pathname.startsWith('/employees') ? 'employees' : 'cafes';

  const menuItems = [
    {
      key: 'cafes',
      icon: <CoffeeOutlined />,
      label: 'Cafes',
      onClick: () => navigate('/cafes'),
    },
    {
      key: 'employees',
      icon: <TeamOutlined />,
      label: 'Employees',
      onClick: () => navigate('/employees'),
    },
  ];

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header>
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[selectedKey]}  // Use selectedKeys, not defaultSelectedKeys
          items={menuItems}  // Use items prop instead of Menu.Item children
        />
      </Header>
      <Content style={{ padding: '24px' }}>
        <Routes>
          <Route path="/" element={<Navigate to="/cafes" />} />
          <Route path="/cafes" element={<CafesPage />} />
          <Route path="/cafes/add" element={<AddEditCafe />} />
          <Route path="/cafes/edit/:id" element={<AddEditCafe />} />
          <Route path="/employees" element={<EmployeesPage />} />
          <Route path="/employees/add" element={<AddEditEmployee />} />
          <Route path="/employees/edit/:id" element={<AddEditEmployee />} />
        </Routes>
      </Content>
    </Layout>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;
