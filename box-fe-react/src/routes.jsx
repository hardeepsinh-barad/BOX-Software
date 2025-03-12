import React from 'react';
import { Route } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

const routes = [
  {
    path: "/",
    element: <Login />,
  },
  {
    path: "/dashboard",
    element: <Dashboard />,
  },
];

export default routes;
