<template>
  <div class="monitor">
    <Sidebar />
    <div class="main-content">
      <Header title="监控中心" />
      <div class="content">
        <div class="content-header">
          <div>
            <h2 class="content-title">监控中心</h2>
            <p class="content-subtitle">实时监控设备性能指标和健康状态</p>
          </div>
          <div class="content-actions">
            <el-select v-model="selectedDevice" placeholder="选择设备" class="device-select">
              <el-option label="全部设备" value="" />
              <el-option v-for="device in deviceList" :key="device.id" :label="device.name" :value="device.id" />
            </el-select>
            <el-select v-model="timeRange" class="time-select">
              <el-option label="1小时" value="1h" />
              <el-option label="6小时" value="6h" />
              <el-option label="24小时" value="24h" />
              <el-option label="7天" value="7d" />
            </el-select>
          </div>
        </div>

        <div class="stats-overview">
          <div class="overview-item">
            <div class="overview-value success">98%</div>
            <div class="overview-label">设备在线率</div>
          </div>
          <div class="overview-item">
            <div class="overview-value">12</div>
            <div class="overview-label">监控设备</div>
          </div>
          <div class="overview-item">
            <div class="overview-value warning">8</div>
            <div class="overview-label">活动告警</div>
          </div>
          <div class="overview-item">
            <div class="overview-value">0</div>
            <div class="overview-label">严重故障</div>
          </div>
        </div>

        <div class="charts-row">
          <div class="chart-panel">
            <div class="panel-header">
              <h3 class="panel-title">CPU使用率</h3>
              <div class="panel-badge" :class="cpuLevel">{{ cpuLevelText }}</div>
            </div>
            <div ref="cpuChart" class="chart-area"></div>
          </div>

          <div class="chart-panel">
            <div class="panel-header">
              <h3 class="panel-title">内存使用率</h3>
              <div class="panel-badge" :class="memoryLevel">{{ memoryLevelText }}</div>
            </div>
            <div ref="memoryChart" class="chart-area"></div>
          </div>

          <div class="chart-panel">
            <div class="panel-header">
              <h3 class="panel-title">磁盘使用率</h3>
              <div class="panel-badge" :class="diskLevel">{{ diskLevelText }}</div>
            </div>
            <div ref="diskChart" class="chart-area"></div>
          </div>

          <div class="chart-panel">
            <div class="panel-header">
              <h3 class="panel-title">网络流量</h3>
            </div>
            <div ref="networkChart" class="chart-area"></div>
          </div>
        </div>

        <div class="bottom-row">
          <div class="alerts-panel">
            <div class="panel-header">
              <h3 class="panel-title">实时告警</h3>
              <el-button text size="small">查看全部</el-button>
            </div>
            <div class="alerts-list">
              <div 
                v-for="alert in alerts" 
                :key="alert.id" 
                class="alert-row"
                :class="alert.level"
              >
                <div class="alert-indicator"></div>
                <div class="alert-content">
                  <div class="alert-header">
                    <span class="alert-title">{{ alert.title }}</span>
                    <span class="alert-time">{{ alert.time }}</span>
                  </div>
                  <p class="alert-desc">{{ alert.description }}</p>
                  <div class="alert-meta">
                    <span class="alert-device">{{ alert.device }}</span>
                    <span class="alert-severity">{{ alert.severity }}</span>
                  </div>
                </div>
                <button class="alert-action">
                  <el-icon><ArrowRight /></el-icon>
                </button>
              </div>
            </div>
          </div>

          <div class="devices-panel">
            <div class="panel-header">
              <h3 class="panel-title">设备状态</h3>
              <div class="status-filter">
                <el-button 
                  :class="{ active: statusFilter === '' }" 
                  size="small" 
                  @click="statusFilter = ''"
                >全部</el-button>
                <el-button 
                  :class="{ active: statusFilter === 'online' }" 
                  size="small" 
                  type="success"
                  @click="statusFilter = 'online'"
                >在线</el-button>
                <el-button 
                  :class="{ active: statusFilter === 'offline' }" 
                  size="small" 
                  type="danger"
                  @click="statusFilter = 'offline'"
                >离线</el-button>
              </div>
            </div>
            <div class="devices-table">
              <div class="table-header">
                <span>设备名称</span>
                <span>IP地址</span>
                <span>CPU</span>
                <span>内存</span>
                <span>状态</span>
              </div>
              <div 
                v-for="device in deviceStatus" 
                :key="device.name" 
                class="table-row"
              >
                <span class="device-name">{{ device.name }}</span>
                <span class="device-ip">{{ device.ip }}</span>
                <div class="metric-cell">
                  <div class="mini-bar">
                    <div class="mini-fill" :style="{ width: device.cpu }"></div>
                  </div>
                  <span>{{ device.cpu }}</span>
                </div>
                <div class="metric-cell">
                  <div class="mini-bar">
                    <div class="mini-fill memory" :style="{ width: device.memory }"></div>
                  </div>
                  <span>{{ device.memory }}</span>
                </div>
                <span class="status-tag" :class="device.status">
                  {{ device.status === 'online' ? '在线' : '离线' }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import Sidebar from '@/components/Sidebar.vue'
import Header from '@/components/Header.vue'
import { ArrowRight } from '@element-plus/icons-vue'

const selectedDevice = ref('')
const timeRange = ref('24h')
const statusFilter = ref('')

const deviceList = ref([
  { id: 1, name: 'lb-01' },
  { id: 2, name: 'lb-02' },
  { id: 3, name: 'dns-01' },
  { id: 4, name: 'dns-02' }
])

const deviceStatus = ref([
  { name: 'lb-01', ip: '192.168.1.101', cpu: '45%', memory: '62%', status: 'online' },
  { name: 'lb-02', ip: '192.168.1.102', cpu: '38%', memory: '55%', status: 'online' },
  { name: 'dns-01', ip: '192.168.1.103', cpu: '25%', memory: '40%', status: 'online' },
  { name: 'dns-02', ip: '192.168.1.104', cpu: '85%', memory: '78%', status: 'online' },
  { name: 'lb-03', ip: '192.168.1.105', cpu: '-', memory: '-', status: 'offline' },
  { name: 'lb-04', ip: '192.168.1.106', cpu: '52%', memory: '68%', status: 'online' }
])

const alerts = ref([
  { id: 1, level: 'danger', title: 'CPU使用率过高', description: '设备 lb-01 CPU使用率达到95%，超过阈值80%', device: 'lb-01', severity: '严重', time: '5分钟前' },
  { id: 2, level: 'warning', title: '内存使用率告警', description: '设备 dns-02 内存使用率达到85%', device: 'dns-02', severity: '警告', time: '15分钟前' },
  { id: 3, level: 'danger', title: '服务不可用', description: '虚拟服务器 vs-web-01 状态异常', device: 'lb-02', severity: '严重', time: '30分钟前' },
  { id: 4, level: 'warning', title: '证书即将过期', description: '证书 www.example.com 还有7天过期', device: 'lb-01', severity: '警告', time: '1小时前' },
  { id: 5, level: 'info', title: '配置同步完成', description: '集群 cluster-01 配置同步成功', device: 'cluster-01', severity: '信息', time: '2小时前' }
])

const cpuLevel = computed(() => 'normal')
const cpuLevelText = computed(() => '正常')
const memoryLevel = computed(() => 'normal')
const memoryLevelText = computed(() => '正常')
const diskLevel = computed(() => 'warning')
const diskLevelText = computed(() => '中等')

const cpuChart = ref<HTMLElement | null>(null)
const memoryChart = ref<HTMLElement | null>(null)
const diskChart = ref<HTMLElement | null>(null)
const networkChart = ref<HTMLElement | null>(null)

let cpuChartInstance: echarts.ECharts | null = null
let memoryChartInstance: echarts.ECharts | null = null
let diskChartInstance: echarts.ECharts | null = null
let networkChartInstance: echarts.ECharts | null = null

const initCharts = () => {
  const hours = ['00:00', '02:00', '04:00', '06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00']
  const cpuData = [45, 42, 38, 35, 40, 55, 62, 58, 65, 60, 52, 48]
  const memoryData = [58, 55, 52, 50, 53, 60, 65, 62, 68, 64, 58, 55]
  const diskData = [72, 73, 73, 74, 74, 75, 75, 76, 76, 77, 77, 78]
  const networkIn = [120, 135, 125, 115, 140, 165, 180, 175, 190, 185, 160, 145]
  const networkOut = [90, 105, 95, 85, 110, 130, 145, 140, 155, 150, 125, 110]

  const baseOption = {
    grid: { top: 10, right: 10, bottom: 25, left: 35 },
    xAxis: { type: 'category', data: hours, axisLine: { show: false }, axisTick: { show: false }, axisLabel: { color: '#64748b', fontSize: 10 } },
    yAxis: { type: 'value', axisLine: { show: false }, axisTick: { show: false }, splitLine: { lineStyle: { color: '#f1f5f9' } }, axisLabel: { color: '#64748b', fontSize: 10 } }
  }

  if (cpuChart.value) {
    cpuChartInstance = echarts.init(cpuChart.value)
    cpuChartInstance.setOption({
      ...baseOption,
      series: [{ type: 'line', data: cpuData, smooth: true, areaStyle: { color: 'rgba(30, 64, 175, 0.08)' }, lineStyle: { color: '#1e40af', width: 2 }, itemStyle: { color: '#1e40af' } }]
    })
  }

  if (memoryChart.value) {
    memoryChartInstance = echarts.init(memoryChart.value)
    memoryChartInstance.setOption({
      ...baseOption,
      series: [{ type: 'line', data: memoryData, smooth: true, areaStyle: { color: 'rgba(22, 163, 74, 0.08)' }, lineStyle: { color: '#16a34a', width: 2 }, itemStyle: { color: '#16a34a' } }]
    })
  }

  if (diskChart.value) {
    diskChartInstance = echarts.init(diskChart.value)
    diskChartInstance.setOption({
      ...baseOption,
      series: [{ type: 'line', data: diskData, smooth: true, areaStyle: { color: 'rgba(245, 158, 11, 0.08)' }, lineStyle: { color: '#f59e0b', width: 2 }, itemStyle: { color: '#f59e0b' } }]
    })
  }

  if (networkChart.value) {
    networkChartInstance = echarts.init(networkChart.value)
    networkChartInstance.setOption({
      ...baseOption,
      series: [
        { type: 'line', data: networkIn, smooth: true, lineStyle: { color: '#1e40af', width: 2 }, itemStyle: { color: '#1e40af' } },
        { type: 'line', data: networkOut, smooth: true, lineStyle: { color: '#16a34a', width: 2 }, itemStyle: { color: '#16a34a' } }
      ]
    })
  }
}

const handleResize = () => {
  cpuChartInstance?.resize()
  memoryChartInstance?.resize()
  diskChartInstance?.resize()
  networkChartInstance?.resize()
}

onMounted(() => {
  initCharts()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  cpuChartInstance?.dispose()
  memoryChartInstance?.dispose()
  diskChartInstance?.dispose()
  networkChartInstance?.dispose()
})
</script>

<style scoped>
.monitor {
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
  gap: var(--space-md);
}

.device-select,
.time-select {
  width: 160px;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-md);
  margin-bottom: var(--space-xl);
}

.overview-item {
  background: var(--color-white);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  border: 1px solid var(--color-border);
  text-align: center;
}

.overview-value {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: var(--line-height-tight);
}

.overview-value.success {
  color: var(--color-success);
}

.overview-value.warning {
  color: var(--color-warning);
}

.overview-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-top: var(--space-xs);
}

.charts-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-md);
  margin-bottom: var(--space-xl);
}

.chart-panel {
  background: var(--color-white);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  border: 1px solid var(--color-border);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-md);
}

.panel-title {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.panel-badge {
  font-size: var(--font-size-xs);
  font-weight: 500;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  background: var(--color-surface-raise);
  color: var(--color-text-secondary);
}

.panel-badge.success {
  background: var(--color-success-light);
  color: var(--color-success);
}

.panel-badge.warning {
  background: var(--color-warning-light);
  color: var(--color-warning);
}

.panel-badge.danger {
  background: var(--color-danger-light);
  color: var(--color-danger);
}

.chart-area {
  height: 180px;
}

.bottom-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-md);
}

.alerts-panel,
.devices-panel {
  background: var(--color-white);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  border: 1px solid var(--color-border);
}

.alerts-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.alert-row {
  display: flex;
  gap: var(--space-md);
  padding: var(--space-md);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  transition: all var(--transition-fast);
}

.alert-row:hover {
  background: var(--color-surface-raise);
}

.alert-indicator {
  width: 4px;
  border-radius: 2px;
  flex-shrink: 0;
}

.alert-row.danger .alert-indicator {
  background: var(--color-danger);
}

.alert-row.warning .alert-indicator {
  background: var(--color-warning);
}

.alert-row.info .alert-indicator {
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

.alert-meta {
  display: flex;
  gap: var(--space-md);
  margin-top: var(--space-xs);
}

.alert-device {
  font-size: var(--font-size-xs);
  color: var(--color-primary);
}

.alert-severity {
  font-size: var(--font-size-xs);
  font-weight: 500;
  padding: 1px 6px;
  border-radius: var(--radius-sm);
}

.alert-row.danger .alert-severity {
  background: var(--color-danger-light);
  color: var(--color-danger);
}

.alert-row.warning .alert-severity {
  background: var(--color-warning-light);
  color: var(--color-warning);
}

.alert-row.info .alert-severity {
  background: var(--color-info-light);
  color: var(--color-info);
}

.alert-action {
  background: none;
  border: none;
  padding: var(--space-sm);
  border-radius: var(--radius-sm);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.alert-action:hover {
  background: var(--color-surface-raise);
  color: var(--color-primary);
}

.status-filter {
  display: flex;
  gap: var(--space-xs);
}

.status-filter .el-button.active {
  background: var(--color-primary);
  color: #fff;
}

.devices-table {
  margin-top: var(--space-md);
}

.table-header {
  display: grid;
  grid-template-columns: 1fr 1fr 0.8fr 0.8fr 0.6fr;
  padding: var(--space-sm) var(--space-md);
  background: var(--color-surface);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: var(--color-text-secondary);
}

.table-row {
  display: grid;
  grid-template-columns: 1fr 1fr 0.8fr 0.8fr 0.6fr;
  padding: var(--space-sm) var(--space-md);
  border-bottom: 1px solid var(--color-border);
  align-items: center;
  transition: background var(--transition-fast);
}

.table-row:hover {
  background: var(--color-surface);
}

.device-name {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-primary);
}

.device-ip {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  font-family: monospace;
}

.metric-cell {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.mini-bar {
  flex: 1;
  height: 4px;
  background: var(--color-surface-raise);
  border-radius: 2px;
  overflow: hidden;
}

.mini-fill {
  height: 100%;
  background: var(--color-primary);
  border-radius: 2px;
}

.mini-fill.memory {
  background: var(--color-success);
}

.status-tag {
  font-size: var(--font-size-xs);
  font-weight: 500;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  text-align: center;
}

.status-tag.online {
  background: var(--color-success-light);
  color: var(--color-success);
}

.status-tag.offline {
  background: var(--color-danger-light);
  color: var(--color-danger);
}

@media (max-width: 1200px) {
  .charts-row {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .bottom-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-overview {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .charts-row {
    grid-template-columns: 1fr;
  }
  
  .table-header,
  .table-row {
    grid-template-columns: 1fr 1fr;
  }
}
</style>