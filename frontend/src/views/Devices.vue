<template>
  <div class="devices">
    <Sidebar />
    <div class="main-content">
      <Header title="设备管理" />
      <div class="content">
        <div class="content-header">
          <div>
            <h2 class="content-title">设备管理</h2>
            <p class="content-subtitle">管理所有F5设备的注册、配置和状态监控</p>
          </div>
          <div class="content-actions">
            <el-button type="primary" @click="showAddDialog = true">
              <el-icon><Plus /></el-icon>
              添加设备
            </el-button>
          </div>
        </div>

        <div class="filter-bar">
          <el-select v-model="filterType" placeholder="设备类型" class="filter-item">
            <el-option label="全部" value="" />
            <el-option label="BIG-IP" value="bigip" />
            <el-option label="DNS" value="dns" />
          </el-select>
          <el-select v-model="filterStatus" placeholder="状态" class="filter-item">
            <el-option label="全部" value="" />
            <el-option label="在线" value="online" />
            <el-option label="离线" value="offline" />
            <el-option label="健康" value="healthy" />
            <el-option label="异常" value="unhealthy" />
          </el-select>
          <el-input 
            v-model="searchQuery" 
            placeholder="搜索设备名称或IP" 
            class="filter-search"
            prefix-icon="Search"
          />
        </div>

        <div class="device-grid">
          <div 
            v-for="device in devices" 
            :key="device.id" 
            class="device-card"
            @click="viewDevice(device)"
          >
            <div class="device-card-header">
              <div class="device-status-indicator" :class="device.status"></div>
              <span class="device-type" :class="device.type">{{ device.type === 'bigip' ? 'BIG-IP' : 'DNS' }}</span>
            </div>
            <h3 class="device-name">{{ device.name }}</h3>
            <div class="device-info">
              <div class="info-item">
                <el-icon><Monitor /></el-icon>
                <span>{{ device.ip_address }}</span>
              </div>
              <div class="info-item">
                <el-icon><Key /></el-icon>
                <span>端口 {{ device.port }}</span>
              </div>
              <div class="info-item">
                <el-icon><InfoFilled /></el-icon>
                <span>版本 {{ device.version }}</span>
              </div>
            </div>
            <div class="device-metrics-bar">
              <div class="metric-bar">
                <div class="metric-label">CPU</div>
                <div class="metric-track">
                  <div class="metric-fill" :style="{ width: getRandomMetric() + '%' }"></div>
                </div>
              </div>
              <div class="metric-bar">
                <div class="metric-label">内存</div>
                <div class="metric-track">
                  <div class="metric-fill memory" :style="{ width: getRandomMetric() + '%' }"></div>
                </div>
              </div>
            </div>
            <div class="device-card-footer">
              <span class="device-status-text" :class="device.status">{{ getStatusLabel(device.status) }}</span>
              <div class="device-actions">
                <button class="action-btn" @click.stop="editDevice(device)" title="编辑">
                  <el-icon><Edit /></el-icon>
                </button>
                <button class="action-btn danger" @click.stop="deleteDevice(device.id)" title="删除">
                  <el-icon><Delete /></el-icon>
                </button>
              </div>
            </div>
          </div>
        </div>

        <el-pagination
          class="pagination"
          :current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next, jumper"
          @current-change="handlePageChange"
        />

        <el-dialog v-model="showAddDialog" :title="isEdit ? '编辑设备' : '添加设备'" width="500px" class="device-dialog">
          <el-form :model="form" label-width="100px" class="device-form">
            <el-form-item label="设备名称" required>
              <el-input v-model="form.name" placeholder="请输入设备名称" />
            </el-form-item>
            <el-form-item label="设备类型" required>
              <el-select v-model="form.type" placeholder="请选择设备类型">
                <el-option label="BIG-IP" value="bigip" />
                <el-option label="DNS" value="dns" />
              </el-select>
            </el-form-item>
            <el-form-item label="IP地址" required>
              <el-input v-model="form.ip_address" placeholder="请输入IP地址" />
            </el-form-item>
            <el-form-item label="端口">
              <el-input v-model="form.port" type="number" placeholder="默认443" />
            </el-form-item>
            <el-form-item label="用户名">
              <el-input v-model="form.username" placeholder="请输入用户名" />
            </el-form-item>
            <el-form-item label="密码">
              <el-input v-model="form.password" type="password" placeholder="请输入密码" />
            </el-form-item>
          </el-form>
          <template #footer>
            <el-button @click="showAddDialog = false">取消</el-button>
            <el-button type="primary" @click="handleSave">{{ isEdit ? '保存修改' : '添加设备' }}</el-button>
          </template>
        </el-dialog>

        <el-dialog v-model="showDetailDialog" title="设备详情" width="700px" class="detail-dialog">
          <div v-if="selectedDevice" class="device-detail">
            <div class="detail-header">
              <div class="detail-title">
                <span class="device-status-indicator large" :class="selectedDevice.status"></span>
                <div>
                  <h3>{{ selectedDevice.name }}</h3>
                  <span class="device-type" :class="selectedDevice.type">{{ selectedDevice.type === 'bigip' ? 'BIG-IP' : 'DNS' }}</span>
                </div>
              </div>
              <span class="device-status-badge" :class="selectedDevice.status">{{ getStatusLabel(selectedDevice.status) }}</span>
            </div>

            <el-tabs v-model="activeTab" class="detail-tabs">
              <el-tab-pane label="基本信息" name="basic">
                <div class="detail-section">
                  <div class="detail-grid">
                    <div class="detail-item">
                      <label>设备ID</label>
                      <span class="monospace">{{ selectedDevice.id }}</span>
                    </div>
                    <div class="detail-item">
                      <label>设备名称</label>
                      <span>{{ selectedDevice.name }}</span>
                    </div>
                    <div class="detail-item">
                      <label>设备类型</label>
                      <span>{{ selectedDevice.type === 'bigip' ? 'BIG-IP' : 'DNS' }}</span>
                    </div>
                    <div class="detail-item">
                      <label>状态</label>
                      <span class="device-status-text" :class="selectedDevice.status">{{ getStatusLabel(selectedDevice.status) }}</span>
                    </div>
                    <div class="detail-item">
                      <label>IP地址</label>
                      <span class="monospace">{{ selectedDevice.ip_address }}</span>
                    </div>
                    <div class="detail-item">
                      <label>端口</label>
                      <span>{{ selectedDevice.port }}</span>
                    </div>
                    <div class="detail-item">
                      <label>版本</label>
                      <span>{{ selectedDevice.version || '-' }}</span>
                    </div>
                    <div class="detail-item">
                      <label>用户名</label>
                      <span>{{ selectedDevice.username || '-' }}</span>
                    </div>
                  </div>
                </div>
              </el-tab-pane>
              <el-tab-pane label="时间信息" name="timeline">
                <div class="detail-section">
                  <div class="detail-grid">
                    <div class="detail-item">
                      <label>创建时间</label>
                      <span>{{ formatDateTime(selectedDevice.created_at) }}</span>
                    </div>
                    <div class="detail-item">
                      <label>更新时间</label>
                      <span>{{ formatDateTime(selectedDevice.updated_at) || '-' }}</span>
                    </div>
                  </div>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>
          <template #footer>
            <el-button @click="showDetailDialog = false">关闭</el-button>
            <el-button type="primary" @click="handleEditFromDetail">编辑设备</el-button>
          </template>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import Header from '@/components/Header.vue'
import { Plus, Monitor, Key, InfoFilled, Edit, Delete } from '@element-plus/icons-vue'
import { useDevicesStore } from '@/stores/devices'

const devicesStore = useDevicesStore()
const devices = ref<any[]>([])
const showAddDialog = ref(false)
const showDetailDialog = ref(false)
const isEdit = ref(false)
const selectedDevice = ref<any>(null)
const filterType = ref('')
const filterStatus = ref('')
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(6)
const total = ref(12)
const activeTab = ref('basic')

const form = reactive({
  id: 0,
  name: '',
  type: 'bigip',
  ip_address: '',
  port: 443,
  username: '',
  password: ''
})

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    online: '在线',
    offline: '离线',
    healthy: '健康',
    unhealthy: '异常'
  }
  return labels[status] || status
}

const formatDateTime = (dateTime: string) => {
  if (!dateTime) return '-'
  const date = new Date(dateTime)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const handleEditFromDetail = () => {
  showDetailDialog.value = false
  editDevice(selectedDevice.value)
}

const getRandomMetric = () => {
  return Math.floor(Math.random() * 60) + 20
}

const handleSave = async () => {
  try {
    if (isEdit.value) {
      await devicesStore.updateDevice(form.id, form)
    } else {
      await devicesStore.createDevice(form)
    }
    showAddDialog.value = false
    resetForm()
    await fetchDevices()
  } catch (error) {
    console.error(error)
  }
}

const resetForm = () => {
  Object.assign(form, {
    name: '',
    type: 'bigip',
    ip_address: '',
    port: 443,
    username: '',
    password: ''
  })
  isEdit.value = false
}

const viewDevice = (device: any) => {
  selectedDevice.value = device
  showDetailDialog.value = true
}

const editDevice = (device: any) => {
  Object.assign(form, device)
  isEdit.value = true
  showAddDialog.value = true
}

const deleteDevice = async (id: number) => {
  try {
    await devicesStore.deleteDevice(id)
    await fetchDevices()
  } catch (error) {
    console.error(error)
  }
}

const handlePageChange = (page: number) => {
  currentPage.value = page
}

const fetchDevices = async () => {
  devices.value = await devicesStore.fetchDevices()
}

fetchDevices()
</script>

<style scoped>
.devices {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--color-surface);
  margin-left: var(--sidebar-width);
}

.content {
  padding: var(--space-lg);
  padding-top: calc(var(--header-height) + var(--space-lg));
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-xl);
}

.content-title {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0;
  line-height: var(--line-height-tight);
}

.content-subtitle {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  margin: var(--space-sm) 0 0 0;
}

.content-actions {
  display: flex;
  gap: var(--space-sm);
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  margin-bottom: var(--space-lg);
  padding: var(--space-md);
  background: var(--color-white);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
}

.filter-item {
  width: 140px;
}

.filter-search {
  flex: 1;
  max-width: 300px;
}

.device-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-md);
  margin-bottom: var(--space-xl);
}

.device-card {
  background: var(--color-white);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  border: 1px solid var(--color-border);
  cursor: pointer;
  transition: all var(--transition-normal);
}

.device-card:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--color-primary);
}

.device-card-header {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-md);
}

.device-status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-text-secondary);
}

.device-status-indicator.large {
  width: 12px;
  height: 12px;
}

.device-status-indicator.online,
.device-status-indicator.healthy {
  background: var(--color-success);
  box-shadow: 0 0 8px var(--color-success);
}

.device-status-indicator.offline,
.device-status-indicator.unhealthy {
  background: var(--color-danger);
}

.device-type {
  font-size: var(--font-size-xs);
  font-weight: 500;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
}

.device-type.bigip {
  background: var(--color-info-light);
  color: var(--color-info);
}

.device-type.dns {
  background: var(--color-success-light);
  color: var(--color-success);
}

.device-name {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--space-md) 0;
}

.device-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  margin-bottom: var(--space-lg);
}

.info-item {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.info-item el-icon {
  font-size: var(--font-size-sm);
}

.device-metrics-bar {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
  margin-bottom: var(--space-lg);
}

.metric-bar {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.metric-label {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  width: 40px;
}

.metric-track {
  flex: 1;
  height: 6px;
  background: var(--color-surface-raise);
  border-radius: 3px;
  overflow: hidden;
}

.metric-fill {
  height: 100%;
  background: var(--color-primary);
  border-radius: 3px;
  transition: width var(--transition-slow);
}

.metric-fill.memory {
  background: var(--color-success);
}

.device-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--space-md);
  border-top: 1px solid var(--color-border);
}

.device-status-text {
  font-size: var(--font-size-xs);
  font-weight: 500;
  color: var(--color-text-secondary);
}

.device-status-text.online,
.device-status-text.healthy {
  color: var(--color-success);
}

.device-status-text.offline,
.device-status-text.unhealthy {
  color: var(--color-danger);
}

.device-actions {
  display: flex;
  gap: var(--space-xs);
}

.action-btn {
  background: none;
  border: none;
  padding: var(--space-xs);
  border-radius: var(--radius-sm);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.action-btn:hover {
  background: var(--color-surface-raise);
  color: var(--color-text-primary);
}

.action-btn.danger:hover {
  background: var(--color-danger-light);
  color: var(--color-danger);
}

.pagination {
  display: flex;
  justify-content: center;
  padding: var(--space-lg);
}

.device-dialog :deep(.el-dialog__header) {
  border-bottom: 1px solid var(--color-border);
  padding: var(--space-lg);
}

.device-dialog :deep(.el-dialog__title) {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
}

.device-dialog :deep(.el-dialog__body) {
  padding: var(--space-lg);
}

.device-dialog :deep(.el-dialog__footer) {
  border-top: 1px solid var(--color-border);
  padding: var(--space-lg);
}

.device-form {
  max-height: 400px;
  overflow-y: auto;
}

.device-detail {
  padding: var(--space-sm);
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-xl);
  padding-bottom: var(--space-lg);
  border-bottom: 1px solid var(--color-border);
}

.detail-title {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.detail-title h3 {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.detail-section {
  margin-bottom: var(--space-lg);
}

.detail-section h4 {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--space-md) 0;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-md);
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.detail-item label {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
}

.detail-item span {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  font-weight: 500;
}

.detail-item span.monospace {
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', 'Fira Mono', 'Roboto Mono', monospace;
}

.device-status-badge {
  font-size: var(--font-size-sm);
  font-weight: 500;
  padding: 4px 12px;
  border-radius: var(--radius-full);
}

.device-status-badge.online,
.device-status-badge.healthy {
  background: var(--color-success-light);
  color: var(--color-success);
}

.device-status-badge.offline,
.device-status-badge.unhealthy {
  background: var(--color-danger-light);
  color: var(--color-danger);
}

.detail-dialog :deep(.el-dialog__header) {
  border-bottom: 1px solid var(--color-border);
  padding: var(--space-lg);
}

.detail-dialog :deep(.el-dialog__title) {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
}

.detail-dialog :deep(.el-dialog__body) {
  padding: 0;
}

.detail-dialog :deep(.el-dialog__footer) {
  border-top: 1px solid var(--color-border);
  padding: var(--space-lg);
}

.detail-tabs {
  margin-top: var(--space-sm);
}

.detail-tabs :deep(.el-tabs__header) {
  margin: 0;
  padding: 0 var(--space-lg);
  border-bottom: 1px solid var(--color-border);
}

.detail-tabs :deep(.el-tabs__nav-wrap) {
  padding: var(--space-md) 0;
}

.detail-tabs :deep(.el-tabs__item) {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-secondary);
}

.detail-tabs :deep(.el-tabs__item.is-active) {
  color: var(--color-primary);
}

.detail-tabs :deep(.el-tabs__content) {
  padding: var(--space-lg);
}

@media (max-width: 768px) {
  .device-grid {
    grid-template-columns: 1fr;
  }
  
  .filter-bar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-item {
    width: 100%;
  }
  
  .filter-search {
    max-width: none;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>