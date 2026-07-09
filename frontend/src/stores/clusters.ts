import { defineStore } from 'pinia'
import { ref } from 'vue'
import request from '@/utils/request'

export interface ClusterMember {
  device_id: number
  role: string
  priority: number
  status: string
}

export interface Cluster {
  id: number
  name: string
  type: string
  status: string
  members: ClusterMember[]
  created_at: string
}

export const useClustersStore = defineStore('clusters', () => {
  const clusters = ref<Cluster[]>([])

  const fetchClusters = async () => {
    const response = await request.get('/clusters')
    clusters.value = response.data
    return response.data
  }

  const createCluster = async (data: Omit<Cluster, 'id' | 'status' | 'created_at' | 'members'>) => {
    const response = await request.post('/clusters', data)
    return response.data
  }

  const addMember = async (clusterId: number, member: { device_id: number; role: string; priority: number }) => {
    const response = await request.post(`/clusters/${clusterId}/members`, member)
    return response.data
  }

  const failover = async (clusterId: number) => {
    const response = await request.post(`/clusters/${clusterId}/failover`)
    return response.data
  }

  return { clusters, fetchClusters, createCluster, addMember, failover }
})