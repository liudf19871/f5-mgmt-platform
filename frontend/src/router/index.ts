import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue')
  },
  {
    path: '/devices',
    name: 'Devices',
    component: () => import('@/views/Devices.vue')
  },
  {
    path: '/clusters',
    name: 'Clusters',
    component: () => import('@/views/Clusters.vue')
  },
  {
    path: '/monitor',
    name: 'Monitor',
    component: () => import('@/views/Monitor.vue')
  },
  {
    path: '/config',
    name: 'Config',
    component: () => import('@/views/Config.vue')
  },
  {
    path: '/logs',
    name: 'Logs',
    component: () => import('@/views/Logs.vue')
  },
  {
    path: '/reports',
    name: 'Reports',
    component: () => import('@/views/Reports.vue')
  },
  {
    path: '/batch',
    name: 'Batch',
    component: () => import('@/views/Batch.vue')
  },
  {
    path: '/users',
    name: 'Users',
    component: () => import('@/views/Users.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router