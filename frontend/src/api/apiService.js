import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Cafes
export const getCafes = async (location = '') => {
  const params = location ? { location } : {};
  const { data } = await api.get('/cafes', { params });
  return data;
};

export const createCafe = async (cafeData) => {
  const { data } = await api.post('/cafes', cafeData);
  return data;
};

export const updateCafe = async (cafeData) => {
  const { data } = await api.put('/cafes', cafeData);
  return data;
};

export const deleteCafe = async (cafeId) => {
  const { data } = await api.delete(`/cafes?id=${cafeId}`);
  return data;
};

export const getEmployeesByCafe = async (cafeId) => {
  const { data } = await api.get('/employees', {
    params: { cafe: cafeId }
  });
  return data;
};

export const uploadLogo = async (formData) => {
  const { data } = await api.post('/cafes/upload-logo', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return data;  // Returns { file_path: '/uploads/cafes/filename.jpg' }
};
// Employees
export const getEmployees = async (cafe = '') => {
  const params = cafe ? { cafe } : {};
  const { data } = await api.get('/employees', { params });
  return data;
};

export const createEmployee = async (employeeData) => {
  const { data } = await api.post('/employees', employeeData);
  return data;
};

export const updateEmployee = async (employeeData) => {
  const { data } = await api.put('/employees', employeeData);
  return data;
};

export const deleteEmployee = async (employeeId) => {
  console.log(employeeId);
  
  const { data } = await api.delete(`/employees?id=${employeeId}`);
  return data;
};