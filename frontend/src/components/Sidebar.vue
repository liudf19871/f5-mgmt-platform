<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <div class="logo">
        <div class="logo-icon">
          <el-icon><component :is="icons.Management" /></el-icon>
        </div>
        <span class="logo-text">F5管理平台</span>
      </div>
    </div>
    <nav class="sidebar-nav">
      <el-menu :default-active="activeMenu" router class="sidebar-menu">
        <el-menu-item index="/">
          <el-icon><component :is="icons.HomeFilled" /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/devices">
          <el-icon><component :is="icons.Monitor" /></el-icon>
          <span>设备管理</span>
        </el-menu-item>
        <el-menu-item index="/clusters">
          <el-icon><component :is="icons.Grid" /></el-icon>
          <span>集群管理</span>
        </el-menu-item>
        <el-menu-item index="/monitor">
          <el-icon><component :is="icons.TrendCharts" /></el-icon>
          <span>监控中心</span>
        </el-menu-item>
        <el-menu-item index="/config">
          <el-icon><component :is="icons.Setting" /></el-icon>
          <span>配置管理</span>
        </el-menu-item>
        <el-menu-item index="/logs">
          <el-icon><component :is="icons.Document" /></el-icon>
          <span>日志分析</span>
        </el-menu-item>
        <el-menu-item index="/reports">
          <el-icon><component :is="icons.PieChart" /></el-icon>
          <span>报表中心</span>
        </el-menu-item>
        <el-menu-item index="/batch">
          <el-icon><component :is="icons.MoreFilled" /></el-icon>
          <span>批量操作</span>
        </el-menu-item>
        <el-menu-item index="/users">
          <el-icon><component :is="icons.User" /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
      </el-menu>
    </nav>
    <div class="sidebar-footer">
      <div class="system-status">
        <span class="status-dot online"></span>
        <span class="status-text">系统运行中</span>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  HomeFilled,
  Monitor, 
  Grid, 
  TrendCharts, 
  Setting, 
  Document, 
  PieChart, 
  MoreFilled, 
  User,
  Management
} from '@element-plus/icons-vue'

const route = useRoute()

const icons = {
  HomeFilled,
  Monitor,
  Grid,
  TrendCharts,
  Setting,
  Document,
  PieChart,
  MoreFilled,
  User,
  Management
}

const activeMenu = computed(() => route.path)
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  min-height: 100vh;
  background: var(--color-sidebar-bg);
  color: var(--color-sidebar-text);
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 100;
}

.sidebar-header {
  padding: var(--space-lg);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.logo {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: var(--color-sidebar-active);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: #fff;
}

.logo-text {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: #fff;
}

.sidebar-nav {
  flex: 1;
  padding: var(--space-md);
}

.sidebar-menu {
  background: transparent;
  border-right: none;
}

.sidebar-menu :deep(.el-menu-item) {
  color: var(--color-sidebar-text);
  height: 48px;
  line-height: 48px;
  margin-bottom: var(--space-xs);
  border-radius: var(--radius-md);
  transition: all var(--transition-normal);
}

.sidebar-menu :deep(.el-menu-item:hover) {
  background: var(--color-sidebar-hover);
  color: var(--color-sidebar-text-hover);
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background: var(--color-sidebar-active);
  color: #fff;
}

.sidebar-menu :deep(.el-menu-item.is-active:hover) {
  background: var(--color-primary-hover);
}

.sidebar-menu :deep(.el-menu-item-icon) {
  font-size: var(--font-size-lg);
}

.sidebar-footer {
  padding: var(--space-md) var(--space-lg);
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.system-status {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-text-secondary);
}

.status-dot.online {
  background: var(--color-success);
  box-shadow: 0 0 8px var(--color-success);
}

.status-text {
  font-size: var(--font-size-xs);
  color: var(--color-sidebar-text);
}
</style>