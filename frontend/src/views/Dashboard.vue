<template>
  <div class="dashboard">
    <Sidebar />
    <div class="main-content">
      <Header title="首页" />
      <div class="content">
        <div class="content-header">
          <div>
            <h2 class="content-title">欢迎回来</h2>
            <p class="content-subtitle">实时监控您的F5设备集群运行状态</p>
          </div>
          <div class="content-actions">
            <el-button type="primary" @click="refreshData">
              <el-icon><Refresh /></el-icon>
              刷新数据
            </el-button>
          </div>
        </div>

        <div class="stats-section">
          <div class="stat-card">
            <div class="stat-header">
              <span class="stat-label">设备总数</span>
              <el-icon class="stat-icon"><Monitor /></el-icon>
            </div>
            <div class="stat-body">
              <span class="stat-value">{{ stats.totalDevices }}</span>
              <div class="stat-trend positive">
                <el-icon><TrendCharts /></el-icon>
                <span>+2 本周</span>
              </div>
            </div>
            <div class="stat-footer">
              <span class="status-item success">{{ stats.onlineDevices }} 在线</span>
              <span class="status-item danger">{{ stats.offlineDevices }} 离线</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-header">
              <span class="stat-label">集群总数</span>
              <el-icon class="stat-icon"><Connection /></el-icon>
            </div>
            <div class="stat-body">
              <span class="stat-value">{{ stats.totalClusters }}</span>
              <div class="stat-trend positive">
                <el-icon><TrendCharts /></el-icon>
                <span>+1 本月</span>
              </div>
            </div>
            <div class="stat-footer">
              <span class="status-item success">{{ stats.healthyClusters }} 健康</span>
              <span class="status-item warning">{{ stats.warningClusters }} 告警</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-header">
              <span class="stat-label">活动告警</span>
              <el-icon class="stat-icon"><Bell /></el-icon>
            </div>
            <div class="stat-body">
              <span class="stat-value danger">{{ stats.activeAlerts }}</span>
              <div class="stat-trend negative">
                <el-icon><TrendCharts /></el-icon>
                <span>-5 今日</span>
              </div>
            </div>
            <div class="stat-footer">
              <span class="status-item danger">{{ stats.criticalAlerts }} 严重</span>
              <span class="status-item warning">{{ stats.warningAlerts }} 警告</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-header">
              <span class="stat-label">系统可用性</span>
              <el-icon class="stat-icon"><Clock /></el-icon>
            </div>
            <div class="stat-body">
              <span class="stat-value success">{{ stats.availability }}</span>
              <div class="stat-trend positive">
                <el-icon><TrendCharts /></el-icon>
                <span>+0.1% 本周</span>
              </div>
            </div>
            <div class="stat-footer">
              <span class="status-item">运行 {{ stats.upTime }}</span>
            </div>
          </div>
        </div>

        <div class="charts-section">
          <div class="chart-card">
            <div class="card-header">
              <h3 class="card-title">CPU使用率趋势</h3>
              <el-select v-model="timeRange" size="small" class="time-select">
                <el-option label="1小时" value="1h" />
                <el-option label="6小时" value="6h" />
                <el-option label="24小时" value="24h" />
              </el-select>
            </div>
            <div ref="cpuChart" class="chart-container"></div>
          </div>

          <div class="chart-card">
            <div class="card-header">
              <h3 class="card-title">内存使用率趋势</h3>
            </div>
            <div ref="memoryChart" class="chart-container"></div>
          </div>

          <div class="chart-card">
            <div class="card-header">
              <h3 class="card-title">流量统计</h3>
            </div>
            <div ref="trafficChart" class="chart-container"></div>
          </div>

          <div class="chart-card">
            <div class="card-header">
              <h3 class="card-title">设备类型分布</h3>
            </div>
            <div ref="deviceTypeChart" class="chart-container"></div>
          </div>
        </div>

        <div class="bottom-section">
          <div class="alert-card">
            <div class="card-header">
              <h3 class="card-title">最新告警</h3>
              <el-button text size="small" @click="viewAllAlerts">查看全部</el-button>
            </div>
            <div class="alert-list">
              <div 
                v-for="alert in alerts" 
                :key="alert.id" 
                class="alert-item"
                :class="alert.level"
              >
                <div class="alert-indicator"></div>
                <div class="alert-content">
                  <div class="alert-header">
                    <span class="alert-title">{{ alert.title }}</span>
                    <span class="alert-time">{{ alert.time }}</span>
                  </div>
                  <p class="alert-desc">{{ alert.description }}</p>
                  <span class="alert-device">{{ alert.device }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="device-card">
            <div class="card-header">
              <h3 class="card-title">设备状态</h3>
              <el-button text size="small" @click="goToDevices">查看全部</el-button>
            </div>
            <div class="device-list">
              <div 
                v-for="device in devices" 
                :key="device.id" 
                class="device-item"
              >
                <div class="device-status" :class="device.status"></div>
                <div class="device-info">
                  <div class="device-name">{{ device.name }}</div>
                  <div class="device-meta">{{ device.ip_address }} · {{ device.type }}</div>
                </div>
                <div class="device-metrics">
                  <div class="metric">
                    <span class="metric-label">CPU</span>
                    <span class="metric-value">{{ device.cpu }}</span>
                  </div>
                  <div class="metric">
                    <span class="metric-label">内存</span>
                    <span class="metric-value">{{ device.memory }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import Sidebar from '@/components/Sidebar.vue'
import Header from '@/components/Header.vue'
import { Monitor, Connection, Bell, Clock, TrendCharts, Refresh } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const stats = ref({
  totalDevices: 12,
  onlineDevices: 10,
  offlineDevices: 2,
  totalClusters: 3,
  healthyClusters: 2,
  warningClusters: 1,
  activeAlerts: 8,
  criticalAlerts: 2,
  warningAlerts: 6,
  availability: '99.9%',
  upTime: '365天'
})

const timeRange = ref('24h')

const alerts = ref([
  { id: 1, level: 'danger', title: 'CPU使用率过高', description: '设备 lb-01 CPU使用率达到95%', device: 'lb-01', time: '5分钟前' },
  { id: 2, level: 'warning', title: '内存使用率告警', description: '设备 dns-02 内存使用率达到85%', device: 'dns-02', time: '15分钟前' },
  { id: 3, level: 'danger', title: '服务不可用', description: '虚拟服务器 vs-web-01 状态异常', device: 'lb-02', time: '30分钟前' },
  { id: 4, level: 'warning', title: '证书即将过期', description: '证书 www.example.com 还有7天过期', device: 'lb-01', time: '1小时前' },
  { id: 5, level: 'info', title: '配置同步完成', description: '集群 cluster-01 配置同步成功', device: 'cluster-01', time: '2小时前' }
])

const devices = ref([
  { id: 1, name: 'lb-01', ip_address: '192.168.1.101', type: 'BIG-IP', status: 'online', cpu: '45%', memory: '62%' },
  { id: 2, name: 'lb-02', ip_address: '192.168.1.102', type: 'BIG-IP', status: 'online', cpu: '38%', memory: '55%' },
  { id: 3, name: 'dns-01', ip_address: '192.168.1.103', type: 'DNS', status: 'online', cpu: '25%', memory: '40%' },
  { id: 4, name: 'dns-02', ip_address: '192.168.1.104', type: 'DNS', status: 'online', cpu: '85%', memory: '78%' },
  { id: 5, name: 'lb-03', ip_address: '192.168.1.105', type: 'BIG-IP', status: 'offline', cpu: '-', memory: '-' }
])

const cpuChart = ref<HTMLElement | null>(null)
const memoryChart = ref<HTMLElement | null>(null)
const trafficChart = ref<HTMLElement | null>(null)
const deviceTypeChart = ref<HTMLElement | null>(null)

let cpuChartInstance: echarts.ECharts | null = null
let memoryChartInstance: echarts.ECharts | null = null
let trafficChartInstance: echarts.ECharts | null = null
let deviceTypeChartInstance: echarts.ECharts | null = null

const initCharts = () => {
  const hours = ['00:00', '02:00', '04:00', '06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00']
  const cpuData = [45, 42, 38, 35, 40, 55, 62, 58, 65, 60, 52, 48]
  const memoryData = [58, 55, 52, 50, 53, 60, 65, 62, 68, 64, 58, 55]
  const trafficIn = [120, 135, 125, 115, 140, 165, 180, 175, 190, 185, 160, 145]
  const trafficOut = [90, 105, 95, 85, 110, 130, 145, 140, 155, 150, 125, 110]

  if (cpuChart.value) {
    cpuChartInstance = echarts.init(cpuChart.value)
    cpuChartInstance.setOption({
      grid: { top: 20, right: 20, bottom: 30, left: 40 },
      xAxis: { type: 'category', data: hours, axisLine: { lineStyle: { color: '#e2e8f0' } }, axisLabel: { color: '#64748b', fontSize: 11 } },
      yAxis: { type: 'value', max: 100, axisLine: { show: false }, axisTick: { show: false }, splitLine: { lineStyle: { color: '#f1f5f9' } }, axisLabel: { color: '#64748b', fontSize: 11 } },
      series: [{ type: 'line', data: cpuData, smooth: true, areaStyle: { color: 'rgba(30, 64, 175, 0.1)' }, lineStyle: { color: '#1e40af', width: 2 }, itemStyle: { color: '#1e40af' } }]
    })
  }

  if (memoryChart.value) {
    memoryChartInstance = echarts.init(memoryChart.value)
    memoryChartInstance.setOption({
      grid: { top: 20, right: 20, bottom: 30, left: 40 },
      xAxis: { type: 'category', data: hours, axisLine: { lineStyle: { color: '#e2e8f0' } }, axisLabel: { color: '#64748b', fontSize: 11 } },
      yAxis: { type: 'value', max: 100, axisLine: { show: false }, axisTick: { show: false }, splitLine: { lineStyle: { color: '#f1f5f9' } }, axisLabel: { color: '#64748b', fontSize: 11 } },
      series: [{ type: 'line', data: memoryData, smooth: true, areaStyle: { color: 'rgba(22, 163, 74, 0.1)' }, lineStyle: { color: '#16a34a', width: 2 }, itemStyle: { color: '#16a34a' } }]
    })
  }

  if (trafficChart.value) {
    trafficChartInstance = echarts.init(trafficChart.value)
    trafficChartInstance.setOption({
      grid: { top: 20, right: 20, bottom: 30, left: 40 },
      xAxis: { type: 'category', data: hours, axisLine: { lineStyle: { color: '#e2e8f0' } }, axisLabel: { color: '#64748b', fontSize: 11 } },
      yAxis: { type: 'value', axisLine: { show: false }, axisTick: { show: false }, splitLine: { lineStyle: { color: '#f1f5f9' } }, axisLabel: { color: '#64748b', fontSize: 11 } },
      series: [
        { name: '入站流量', type: 'line', data: trafficIn, smooth: true, areaStyle: { color: 'rgba(245, 158, 11, 0.1)' }, lineStyle: { color: '#f59e0b', width: 2 }, itemStyle: { color: '#f59e0b' } },
        { name: '出站流量', type: 'line', data: trafficOut, smooth: true, areaStyle: { color: 'rgba(37, 99, 235, 0.1)' }, lineStyle: { color: '#2563eb', width: 2 }, itemStyle: { color: '#2563eb' } }
      ],
      legend: { bottom: 0, textStyle: { color: '#64748b', fontSize: 11 } }
    })
  }

  if (deviceTypeChart.value) {
    deviceTypeChartInstance = echarts.init(deviceTypeChart.value)
    deviceTypeChartInstance.setOption({
      tooltip: { trigger: 'item' },
      series: [{ type: 'pie', radius: ['50%', '70%'], center: ['50%', '50%'], data: [{ value: 8, name: 'BIG-IP' }, { value: 4, name: 'DNS' }], itemStyle: { borderRadius: 8 }, label: { show: true, color: '#64748b', fontSize: 12 }, labelLine: { show: true } }],
      color: ['#1e40af', '#16a34a']
    })
  }
}

const handleResize = () => {
  cpuChartInstance?.resize()
  memoryChartInstance?.resize()
  trafficChartInstance?.resize()
  deviceTypeChartInstance?.resize()
}

const refreshData = () => {
  console.log('Refresh data')
}

const viewAllAlerts = () => {
  router.push('/monitor')
}

const goToDevices = () => {
  router.push('/devices')
}

onMounted(() => {
  initCharts()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  cpuChartInstance?.dispose()
  memoryChartInstance?.dispose()
  trafficChartInstance?.dispose()
  deviceTypeChartInstance?.dispose()
})
</script>

<style scoped>
.dashboard {
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

.stats-section {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-md);
  margin-bottom: var(--space-xl);
}

.stat-card {
  background: var(--color-white);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  border: 1px solid var(--color-border);
  transition: all var(--transition-normal);
}

.stat-card:hover {
  box-shadow: var(--shadow-md);
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-md);
}

.stat-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  font-weight: 500;
}

.stat-icon {
  font-size: var(--font-size-xl);
  color: var(--color-primary);
}

.stat-body {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: var(--space-md);
}

.stat-value {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: var(--line-height-tight);
}

.stat-value.success {
  color: var(--color-success);
}

.stat-value.danger {
  color: var(--color-danger);
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: 2px;
  font-size: var(--font-size-xs);
  font-weight: 500;
}

.stat-trend.positive {
  color: var(--color-success);
}

.stat-trend.negative {
  color: var(--color-danger);
}

.stat-footer {
  display: flex;
  gap: var(--space-lg);
}

.status-item {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
}

.status-item.success {
  color: var(--color-success);
}

.status-item.danger {
  color: var(--color-danger);
}

.status-item.warning {
  color: var(--color-warning);
}

.charts-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-md);
  margin-bottom: var(--space-xl);
}

.chart-card {
  background: var(--color-white);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  border: 1px solid var(--color-border);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-md);
}

.card-title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.time-select {
  width: auto;
}

.chart-container {
  height: 220px;
}

.bottom-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-md);
}

.alert-card,
.device-card {
  background: var(--color-white);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  border: 1px solid var(--color-border);
}

.alert-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.alert-item {
  display: flex;
  gap: var(--space-sm);
  padding: var(--space-md);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  transition: all var(--transition-fast);
}

.alert-item:hover {
  background: var(--color-surface-raise);
}

.alert-indicator {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  margin-top: 8px;
  flex-shrink: 0;
}

.alert-item.danger .alert-indicator {
  background: var(--color-danger);
  box-shadow: 0 0 8px var(--color-danger);
}

.alert-item.warning .alert-indicator {
  background: var(--color-warning);
  box-shadow: 0 0 8px var(--color-warning);
}

.alert-item.info .alert-indicator {
  background: var(--color-info);
}

.alert-content {
  flex: 1;
  min-width: 0;
}

.alert-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.alert-title {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-primary);
}

.alert-time {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
}

.alert-desc {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.alert-device {
  font-size: var(--font-size-xs);
  color: var(--color-primary);
}

.device-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.device-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-md);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  transition: all var(--transition-fast);
}

.device-item:hover {
  background: var(--color-surface-raise);
}

.device-status {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-text-secondary);
}

.device-status.online {
  background: var(--color-success);
  box-shadow: 0 0 8px var(--color-success);
}

.device-status.offline {
  background: var(--color-danger);
}

.device-info {
  flex: 1;
  min-width: 0;
}

.device-name {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-primary);
}

.device-meta {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
}

.device-metrics {
  display: flex;
  gap: var(--space-lg);
}

.metric {
  text-align: right;
}

.metric-label {
  display: block;
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
}

.metric-value {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-primary);
}

@media (max-width: 1200px) {
  .stats-section {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .charts-section {
    grid-template-columns: 1fr;
  }
  
  .bottom-section {
    grid-template-columns: 1fr;
  }
}
</style>