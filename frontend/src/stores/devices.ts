import { defineStore } from 'pinia'
import { ref } from 'vue'
import request from '@/utils/request'

export interface Device {
  id: number
  name: string
  type: string
  ip_address: string
  port: number
  version: string | null
  status: string
  username: string | null
  created_at: string
  updated_at: string | null
}

export interface DeviceStatus {
  device_id: number
  name: string
  ip_address: string
  status: string
  version: string
  hostname: string
  cpu: {
    user: number
    system: number
    idle: number
  }
  memory: {
    total: number
    used: number
  }
}

export const useDevicesStore = defineStore('devices', () => {
  const devices = ref<Device[]>([])
  const deviceStatuses = ref<DeviceStatus[]>([])

  const fetchDevices = async () => {
    const response = await request.get('/devices')
    devices.value = response.data
    return response.data
  }

  const createDevice = async (data: Omit<Device, 'id' | 'version' | 'status' | 'created_at' | 'updated_at'>) => {
    const response = await request.post('/devices', data)
    return response.data
  }

  const updateDevice = async (id: number, data: Omit<Device, 'id' | 'version' | 'status' | 'created_at' | 'updated_at'>) => {
    const response = await request.put(`/devices/${id}`, data)
    return response.data
  }

  const deleteDevice = async (id: number) => {
    await request.delete(`/devices/${id}`)
  }

  const testConnection = async (id: number) => {
    const response = await request.post(`/devices/${id}/test-connection`)
    return response.data
  }

  const discoverDevice = async (id: number) => {
    const response = await request.post(`/devices/${id}/discover`)
    return response.data
  }

  const syncDeviceConfig = async (id: number) => {
    const response = await request.post(`/devices/${id}/sync`)
    return response.data
  }

  const fetchDeviceStatuses = async () => {
    const response = await request.get('/monitor/devices')
    deviceStatuses.value = response.data
    return response.data
  }

  const fetchDeviceMetrics = async (id: number) => {
    const response = await request.get(`/monitor/metrics/${id}`)
    return response.data
  }

  return {
    devices,
    deviceStatuses,
    fetchDevices,
    createDevice,
    updateDevice,
    deleteDevice,
    testConnection,
    discoverDevice,
    syncDeviceConfig,
    fetchDeviceStatuses,
    fetchDeviceMetrics
  }
})