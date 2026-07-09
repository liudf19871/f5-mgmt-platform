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
  created_at: string
}

export const useDevicesStore = defineStore('devices', () => {
  const devices = ref<Device[]>([])

  const fetchDevices = async () => {
    const response = await request.get('/devices')
    devices.value = response.data
    return response.data
  }

  const createDevice = async (data: Omit<Device, 'id' | 'version' | 'status' | 'created_at'>) => {
    const response = await request.post('/devices', data)
    return response.data
  }

  const updateDevice = async (id: number, data: Omit<Device, 'id' | 'version' | 'status' | 'created_at'>) => {
    const response = await request.put(`/devices/${id}`, data)
    return response.data
  }

  const deleteDevice = async (id: number) => {
    await request.delete(`/devices/${id}`)
  }

  return { devices, fetchDevices, createDevice, updateDevice, deleteDevice }
})