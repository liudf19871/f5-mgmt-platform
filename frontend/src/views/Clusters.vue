<template>
  <div class="clusters">
    <Sidebar />
    <div class="main-content">
      <Header title="集群管理" />
      <div class="content">
        <div class="content-header">
          <h1>集群管理</h1>
          <el-button type="primary" @click="showAddDialog = true">创建集群</el-button>
        </div>
        <div class="clusters-grid">
          <el-card v-for="cluster in clusters" :key="cluster.id" class="cluster-card">
            <div class="cluster-header">
              <h3>{{ cluster.name }}</h3>
              <el-tag :type="getClusterStatusType(cluster.status)">
                {{ getClusterStatusLabel(cluster.status) }}
              </el-tag>
            </div>
            <div class="cluster-info">
              <div class="info-item">
                <span class="label">类型:</span>
                <span>{{ getClusterTypeLabel(cluster.type) }}</span>
              </div>
              <div class="info-item">
                <span class="label">成员数:</span>
                <span>{{ cluster.members.length }}</span>
              </div>
            </div>
            <div class="members-list">
              <div v-for="member in cluster.members" :key="member.device_id" class="member-item">
                <el-tag :type="member.role === 'primary' ? 'danger' : 'info'">
                  {{ member.role === 'primary' ? '主' : '备' }}
                </el-tag>
                <span>设备{{ member.device_id }}</span>
                <el-tag :type="member.status === 'active' ? 'success' : 'warning'">
                  {{ member.status }}
                </el-tag>
              </div>
            </div>
            <div class="cluster-actions">
              <el-button size="small" @click="handleFailover(cluster.id)">故障切换</el-button>
              <el-button size="small" @click="showAddMember(cluster.id)">添加成员</el-button>
            </div>
          </el-card>
        </div>

        <el-dialog v-model="showAddDialog" title="创建集群" width="500px">
          <el-form :model="clusterForm" label-width="100px">
            <el-form-item label="集群名称">
              <el-input v-model="clusterForm.name" />
            </el-form-item>
            <el-form-item label="集群类型">
              <el-select v-model="clusterForm.type">
                <el-option label="主备集群" value="active-standby" />
                <el-option label="N+M集群" value="n-plus-m" />
              </el-select>
            </el-form-item>
          </el-form>
          <template #footer>
            <el-button @click="showAddDialog = false">取消</el-button>
            <el-button type="primary" @click="handleCreate">确定</el-button>
          </template>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import Header from '@/components/Header.vue'
import { useClustersStore } from '@/stores/clusters'

const clustersStore = useClustersStore()
const clusters = ref<any[]>([])
const showAddDialog = ref(false)

const clusterForm = reactive({
  name: '',
  type: 'active-standby'
})

const getClusterStatusType = (status: string) => {
  const types: Record<string, string> = {
    healthy: 'success',
    warning: 'warning',
    critical: 'danger'
  }
  return types[status] || 'info'
}

const getClusterStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    healthy: '健康',
    warning: '告警',
    critical: '故障'
  }
  return labels[status] || status
}

const getClusterTypeLabel = (type: string) => {
  const labels: Record<string, string> = {
    'active-standby': '主备集群',
    'n-plus-m': 'N+M集群'
  }
  return labels[type] || type
}

const handleCreate = async () => {
  try {
    await clustersStore.createCluster(clusterForm)
    showAddDialog.value = false
    await fetchClusters()
  } catch (error) {
    console.error(error)
  }
}

const handleFailover = async (clusterId: number) => {
  try {
    await clustersStore.failover(clusterId)
    await fetchClusters()
  } catch (error) {
    console.error(error)
  }
}

const showAddMember = (clusterId: number) => {
  console.log('Add member to cluster:', clusterId)
}

const fetchClusters = async () => {
  clusters.value = await clustersStore.fetchClusters()
}

onMounted(fetchClusters)
</script>

<style scoped>
.clusters {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

.content {
  padding: 20px;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.clusters-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.cluster-card {
  padding: 20px;
}
</style>