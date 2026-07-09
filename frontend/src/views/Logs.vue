<template>
  <div class="logs">
    <Sidebar />
    <div class="main-content">
      <Header title="日志分析" />
      <div class="content">
        <div class="content-header">
          <div>
            <h2 class="content-title">日志分析</h2>
            <p class="content-subtitle">查看和分析设备运行日志，快速定位问题</p>
          </div>
        </div>

        <div class="search-bar">
          <div class="search-input-wrapper">
            <el-icon class="search-icon"><Search /></el-icon>
            <el-input 
              v-model="searchQuery" 
              placeholder="搜索日志内容..." 
              class="search-input"
            />
          </div>
          <div class="filter-group">
            <el-select v-model="filterLevel" placeholder="日志级别" class="filter-item">
              <el-option label="全部" value="" />
              <el-option label="ERROR" value="ERROR" />
              <el-option label="WARN" value="WARN" />
              <el-option label="INFO" value="INFO" />
              <el-option label="DEBUG" value="DEBUG" />
            </el-select>
            <el-select v-model="filterDevice" placeholder="设备" class="filter-item">
              <el-option label="全部" value="" />
              <el-option label="lb-01" value="lb-01" />
              <el-option label="lb-02" value="lb-02" />
              <el-option label="dns-01" value="dns-01" />
              <el-option label="dns-02" value="dns-02" />
            </el-select>
            <el-date-picker 
              v-model="dateRange" 
              type="daterange" 
              range-separator="至" 
              start-placeholder="开始日期" 
              end-placeholder="结束日期"
              class="date-filter"
            />
          </div>
          <el-button type="primary" @click="searchLogs">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
        </div>

        <div class="stats-bar">
          <div class="stat-item">
            <span class="stat-count">{{ totalLogs }}</span>
            <span class="stat-label">总日志</span>
          </div>
          <div class="stat-item">
            <span class="stat-count error">{{ errorCount }}</span>
            <span class="stat-label">错误</span>
          </div>
          <div class="stat-item">
            <span class="stat-count warning">{{ warnCount }}</span>
            <span class="stat-label">警告</span>
          </div>
          <div class="stat-item">
            <span class="stat-count info">{{ infoCount }}</span>
            <span class="stat-label">信息</span>
          </div>
        </div>

        <div class="logs-container">
          <div class="logs-sidebar">
            <div class="sidebar-section">
              <h4>日志类型分布</h4>
              <div ref="typeChart" class="chart-mini"></div>
            </div>
            <div class="sidebar-section">
              <h4>设备日志统计</h4>
              <div class="device-stats">
                <div v-for="device in deviceStats" :key="device.name" class="device-stat">
                  <span class="device-name">{{ device.name }}</span>
                  <div class="device-bar">
                    <div class="device-fill" :style="{ width: device.percent + '%' }"></div>
                  </div>
                  <span class="device-count">{{ device.count }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="logs-main">
            <div class="logs-tabs">
              <el-button 
                :class="{ active: activeTab === 'all' }" 
                @click="activeTab = 'all'"
              >全部日志</el-button>
              <el-button 
                :class="{ active: activeTab === 'error' }" 
                type="danger"
                @click="activeTab = 'error'"
              >错误日志</el-button>
              <el-button 
                :class="{ active: activeTab === 'warning' }" 
                type="warning"
                @click="activeTab = 'warning'"
              >警告日志</el-button>
            </div>

            <div class="logs-list">
              <div 
                v-for="log in filteredLogs" 
                :key="log.id" 
                class="log-item"
                :class="log.level"
              >
                <div class="log-indicator"></div>
                <div class="log-content">
                  <div class="log-header">
                    <span class="log-level">{{ log.level }}</span>
                    <span class="log-device">{{ log.device }}</span>
                    <span class="log-time">{{ log.timestamp }}</span>
                  </div>
                  <p class="log-message">{{ log.message }}</p>
                  <div class="log-details">
                    <span class="log-type">{{ log.type }}</span>
                    <span class="log-source">{{ log.source }}</span>
                  </div>
                </div>
              </div>
            </div>

            <el-pagination
              class="logs-pagination"
              :current-page="currentPage"
              :page-size="pageSize"
              :total="totalLogs"
              layout="total, prev, pager, next, jumper"
              @current-change="handlePageChange"
            />
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
import { Search } from '@element-plus/icons-vue'

const searchQuery = ref('')
const filterLevel = ref('')
const filterDevice = ref('')
const dateRange = ref<Date[]>([])
const activeTab = ref('all')
const currentPage = ref(1)
const pageSize = ref(20)

const totalLogs = ref(1258)
const errorCount = ref(45)
const warnCount = ref(128)
const infoCount = ref(1085)

const deviceStats = ref([
  { name: 'lb-01', count: 420, percent: 33 },
  { name: 'lb-02', count: 380, percent: 30 },
  { name: 'dns-01', count: 280, percent: 22 },
  { name: 'dns-02', count: 178, percent: 14 }
])

const logs = ref([
  { id: 1, level: 'ERROR', device: 'lb-01', type: 'SYSTEM', source: '/var/log/ltm', timestamp: '2024-01-15 10:35:22', message: 'Connection timeout on pool member 192.168.2.10:80' },
  { id: 2, level: 'WARN', device: 'lb-01', type: 'SECURITY', source: '/var/log/asm', timestamp: '2024-01-15 10:34:15', message: 'Possible SQL injection attempt detected from IP 10.0.0.5' },
  { id: 3, level: 'INFO', device: 'dns-01', type: 'DNS', source: '/var/log/named', timestamp: '2024-01-15 10:33:40', message: 'Zone transfer completed successfully for example.com' },
  { id: 4, level: 'ERROR', device: 'lb-02', type: 'SYSTEM', source: '/var/log/ltm', timestamp: '2024-01-15 10:32:18', message: 'Virtual server vs-web-01 health check failed' },
  { id: 5, level: 'INFO', device: 'lb-01', type: 'SYSTEM', source: '/var/log/ltm', timestamp: '2024-01-15 10:31:05', message: 'SSL certificate renewed successfully for www.example.com' },
  { id: 6, level: 'WARN', device: 'dns-02', type: 'DNS', source: '/var/log/named', timestamp: '2024-01-15 10:29:33', message: 'High query rate detected, enabling rate limiting' },
  { id: 7, level: 'INFO', device: 'lb-02', type: 'ACCESS', source: '/var/log/apm', timestamp: '2024-01-15 10:28:10', message: 'User admin logged in successfully from IP 192.168.1.50' },
  { id: 8, level: 'DEBUG', device: 'lb-01', type: 'SYSTEM', source: '/var/log/ltm', timestamp: '2024-01-15 10:26:45', message: 'iRule execution completed in 12ms' },
  { id: 9, level: 'WARN', device: 'lb-01', type: 'SYSTEM', source: '/var/log/ltm', timestamp: '2024-01-15 10:25:20', message: 'Memory usage exceeds 80% threshold' },
  { id: 10, level: 'INFO', device: 'dns-01', type: 'DNS', source: '/var/log/named', timestamp: '2024-01-15 10:24:00', message: 'DNS cache cleared' }
])

const filteredLogs = computed(() => {
  if (activeTab.value === 'all') return logs.value
  return logs.value.filter(log => log.level === activeTab.value.toUpperCase())
})

const typeChart = ref<HTMLElement | null>(null)
let typeChartInstance: echarts.ECharts | null = null

const initCharts = () => {
  if (typeChart.value) {
    typeChartInstance = echarts.init(typeChart.value)
    typeChartInstance.setOption({
      tooltip: { trigger: 'item' },
      series: [{ 
        type: 'pie', 
        radius: ['45%', '70%'], 
        center: ['50%', '50%'],
        data: [
          { value: 45, name: 'ERROR' },
          { value: 128, name: 'WARN' },
          { value: 1085, name: 'INFO' }
        ],
        itemStyle: { borderRadius: 6 },
        label: { show: true, color: '#64748b', fontSize: 10 },
        labelLine: { show: true }
      }],
      color: ['#dc2626', '#f59e0b', '#1e40af']
    })
  }
}

const handleResize = () => {
  typeChartInstance?.resize()
}

const searchLogs = () => {
  console.log('Search logs')
}

const handlePageChange = (page: number) => {
  currentPage.value = page
}

onMounted(() => {
  initCharts()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  typeChartInstance?.dispose()
})
</script>

<style scoped>
.logs {
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

.search-bar {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-md);
  background: var(--color-white);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  margin-bottom: var(--space-xl);
}

.search-input-wrapper {
  flex: 1;
  max-width: 400px;
  display: flex;
  align-items: center;
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: var(--space-sm) var(--space-md);
}

.search-icon {
  color: var(--color-text-secondary);
  margin-right: var(--space-sm);
}

.search-input {
  flex: 1;
  border: none;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.filter-item {
  width: 140px;
}

.date-filter {
  width: 280px;
}

.stats-bar {
  display: flex;
  gap: var(--space-md);
  margin-bottom: var(--space-xl);
}

.stat-item {
  flex: 1;
  background: var(--color-white);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  border: 1px solid var(--color-border);
  text-align: center;
}

.stat-count {
  display: block;
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: var(--line-height-tight);
}

.stat-count.error {
  color: var(--color-danger);
}

.stat-count.warning {
  color: var(--color-warning);
}

.stat-count.info {
  color: var(--color-info);
}

.stat-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.logs-container {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: var(--space-md);
}

.logs-sidebar {
  background: var(--color-white);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  border: 1px solid var(--color-border);
}

.sidebar-section {
  margin-bottom: var(--space-xl);
}

.sidebar-section:last-child {
  margin-bottom: 0;
}

.sidebar-section h4 {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--space-md) 0;
}

.chart-mini {
  height: 180px;
}

.device-stats {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.device-stat {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.device-name {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  width: 60px;
}

.device-bar {
  flex: 1;
  height: 6px;
  background: var(--color-surface-raise);
  border-radius: 3px;
  overflow: hidden;
}

.device-fill {
  height: 100%;
  background: var(--color-primary);
  border-radius: 3px;
}

.device-count {
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: var(--color-text-primary);
  width: 40px;
  text-align: right;
}

.logs-main {
  background: var(--color-white);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
}

.logs-tabs {
  display: flex;
  gap: var(--space-xs);
  padding: var(--space-md) var(--space-lg);
  border-bottom: 1px solid var(--color-border);
}

.logs-tabs .el-button {
  font-size: var(--font-size-sm);
  padding: var(--space-sm) var(--space-lg);
}

.logs-tabs .el-button.active {
  background: var(--color-primary);
  color: #fff;
}

.logs-list {
  flex: 1;
  padding: var(--space-md);
  overflow-y: auto;
}

.log-item {
  display: flex;
  gap: var(--space-md);
  padding: var(--space-md);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  margin-bottom: var(--space-sm);
  transition: all var(--transition-fast);
}

.log-item:hover {
  background: var(--color-surface-raise);
}

.log-indicator {
  width: 4px;
  border-radius: 2px;
  flex-shrink: 0;
}

.log-item.ERROR .log-indicator {
  background: var(--color-danger);
}

.log-item.WARN .log-indicator {
  background: var(--color-warning);
}

.log-item.INFO .log-indicator {
  background: var(--color-info);
}

.log-item.DEBUG .log-indicator {
  background: var(--color-text-secondary);
}

.log-content {
  flex: 1;
  min-width: 0;
}

.log-header {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  margin-bottom: var(--space-xs);
}

.log-level {
  font-size: var(--font-size-xs);
  font-weight: 600;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
}

.log-item.ERROR .log-level {
  background: var(--color-danger-light);
  color: var(--color-danger);
}

.log-item.WARN .log-level {
  background: var(--color-warning-light);
  color: var(--color-warning);
}

.log-item.INFO .log-level {
  background: var(--color-info-light);
  color: var(--color-info);
}

.log-item.DEBUG .log-level {
  background: var(--color-surface-raise);
  color: var(--color-text-secondary);
}

.log-device {
  font-size: var(--font-size-xs);
  color: var(--color-primary);
  font-weight: 500;
}

.log-time {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  font-family: monospace;
}

.log-message {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  margin: 0;
  line-height: var(--line-height-body);
}

.log-details {
  display: flex;
  gap: var(--space-md);
  margin-top: var(--space-xs);
}

.log-type,
.log-source {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
}

.logs-pagination {
  padding: var(--space-lg);
  border-top: 1px solid var(--color-border);
}

@media (max-width: 1024px) {
  .logs-container {
    grid-template-columns: 1fr;
  }
  
  .logs-sidebar {
    order: 2;
  }
  
  .logs-main {
    order: 1;
  }
}

@media (max-width: 768px) {
  .search-bar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-input-wrapper {
    max-width: none;
  }
  
  .filter-group {
    flex-wrap: wrap;
  }
  
  .filter-item,
  .date-filter {
    width: calc(50% - 8px);
  }
}
</style>