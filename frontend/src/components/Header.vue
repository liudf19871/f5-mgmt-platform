<template>
  <header class="header">
    <div class="header-left">
      <button class="menu-toggle" @click="toggleMenu" aria-label="切换菜单">
        <el-icon><Menu /></el-icon>
      </button>
      <h1 class="page-title">{{ title }}</h1>
    </div>
    <div class="header-center">
      <div class="search-box">
        <el-icon class="search-icon"><Search /></el-icon>
        <input 
          type="text" 
          class="search-input" 
          placeholder="搜索设备、配置..." 
          v-model="searchQuery"
        />
      </div>
    </div>
    <div class="header-right">
      <button class="header-btn notification-btn" aria-label="通知">
        <el-icon><Bell /></el-icon>
        <span class="badge" v-if="notificationCount > 0">{{ notificationCount }}</span>
      </button>
      <el-dropdown trigger="click" class="user-dropdown">
        <span class="user-info">
          <div class="user-avatar">
            <el-icon><User /></el-icon>
          </div>
          <div class="user-details">
            <span class="user-name">{{ username }}</span>
            <span class="user-role">{{ role }}</span>
          </div>
          <el-icon class="arrow-icon"><ArrowDown /></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="handleProfile">个人中心</el-dropdown-item>
            <el-dropdown-item @click="handleSettings">系统设置</el-dropdown-item>
            <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Menu, User, Bell, Search, ArrowDown } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

defineProps<{
  title: string
}>()

const authStore = useAuthStore()
const router = useRouter()
const username = ref('admin')
const role = ref('管理员')
const searchQuery = ref('')
const notificationCount = ref(3)

const toggleMenu = () => {
  console.log('Toggle menu')
}

const handleProfile = () => {
  console.log('Open profile')
}

const handleSettings = () => {
  console.log('Open settings')
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.header {
  height: var(--header-height);
  background: var(--color-white);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 var(--space-lg);
  position: fixed;
  left: var(--sidebar-width);
  right: 0;
  top: 0;
  z-index: 90;
  box-shadow: var(--shadow-sm);
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.menu-toggle {
  background: none;
  border: none;
  font-size: var(--font-size-xl);
  cursor: pointer;
  padding: var(--space-sm);
  color: var(--color-text-secondary);
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
}

.menu-toggle:hover {
  background: var(--color-surface-raise);
  color: var(--color-text-primary);
}

.page-title {
  margin: 0;
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
  line-height: var(--line-height-tight);
}

.header-center {
  flex: 1;
  max-width: 400px;
  margin: 0 var(--space-xl);
}

.search-box {
  display: flex;
  align-items: center;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-sm) var(--space-md);
  transition: all var(--transition-fast);
}

.search-box:focus-within {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.1);
}

.search-icon {
  color: var(--color-text-secondary);
  font-size: var(--font-size-base);
  margin-right: var(--space-sm);
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
}

.search-input::placeholder {
  color: var(--color-text-secondary);
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.header-btn {
  background: none;
  border: none;
  font-size: var(--font-size-xl);
  cursor: pointer;
  padding: var(--space-sm);
  color: var(--color-text-secondary);
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
  position: relative;
}

.header-btn:hover {
  background: var(--color-surface-raise);
  color: var(--color-text-primary);
}

.badge {
  position: absolute;
  top: 2px;
  right: 2px;
  min-width: 16px;
  height: 16px;
  background: var(--color-danger);
  color: #fff;
  font-size: 10px;
  font-weight: 600;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
}

.user-dropdown {
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.user-info:hover {
  background: var(--color-surface-raise);
}

.user-avatar {
  width: 32px;
  height: 32px;
  background: var(--color-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: var(--font-size-sm);
}

.user-details {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.user-name {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-primary);
}

.user-role {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
}

.arrow-icon {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
}
</style>