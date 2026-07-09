<template>
  <div class="users">
    <Sidebar />
    <div class="main-content">
      <Header title="用户管理" />
      <div class="content">
        <div class="content-header">
          <div>
            <h2 class="content-title">用户管理</h2>
            <p class="content-subtitle">管理系统用户和角色权限</p>
          </div>
          <div class="content-actions">
            <el-button type="primary" @click="showAddDialog = true">
              <el-icon><Plus /></el-icon>
              创建用户
            </el-button>
          </div>
        </div>

        <div class="stats-cards">
          <div class="stat-card">
            <div class="stat-icon users-icon">
              <el-icon><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ totalUsers }}</div>
              <div class="stat-label">总用户数</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon admin-icon">
              <el-icon><UserFilled /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ adminCount }}</div>
              <div class="stat-label">管理员</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon operator-icon">
              <el-icon><Monitor /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ operatorCount }}</div>
              <div class="stat-label">运维人员</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon viewer-icon">
              <el-icon><View /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ viewerCount }}</div>
              <div class="stat-label">只读用户</div>
            </div>
          </div>
        </div>

        <div class="users-table-container">
          <div class="table-header-row">
            <el-input 
              v-model="searchQuery" 
              placeholder="搜索用户名或邮箱" 
              class="search-input"
              prefix-icon="Search"
            />
            <el-select v-model="filterRole" placeholder="角色筛选" class="role-filter">
              <el-option label="全部" value="" />
              <el-option label="管理员" value="admin" />
              <el-option label="运维人员" value="operator" />
              <el-option label="只读用户" value="viewer" />
            </el-select>
          </div>

          <div class="users-table">
            <div class="table-head">
              <div class="table-cell"><el-checkbox v-model="selectAll" @change="handleSelectAll" /></div>
              <div class="table-cell">用户名</div>
              <div class="table-cell">邮箱</div>
              <div class="table-cell">角色</div>
              <div class="table-cell">状态</div>
              <div class="table-cell">最后登录</div>
              <div class="table-cell">操作</div>
            </div>
            <div 
              v-for="user in users" 
              :key="user.id" 
              class="table-row"
              :class="{ selected: selectedUsers.includes(user.id) }"
            >
              <div class="table-cell">
                <el-checkbox v-model="selectedUsers" :value="user.id" />
              </div>
              <div class="table-cell user-name">
                <div class="user-avatar-small">{{ user.username.charAt(0).toUpperCase() }}</div>
                <span>{{ user.username }}</span>
              </div>
              <div class="table-cell">{{ user.email }}</div>
              <div class="table-cell">
                <span class="role-tag" :class="user.role">{{ getRoleLabel(user.role) }}</span>
              </div>
              <div class="table-cell">
                <span class="status-tag" :class="user.status">{{ user.status === 'active' ? '启用' : '禁用' }}</span>
              </div>
              <div class="table-cell">{{ user.last_login || '未登录' }}</div>
              <div class="table-cell">
                <div class="action-buttons">
                  <button class="action-btn" @click="editUser(user)" title="编辑">
                    <el-icon><Edit /></el-icon>
                  </button>
                  <button 
                    class="action-btn" 
                    :class="{ danger: user.status === 'active' }"
                    @click="toggleStatus(user)"
                    :title="user.status === 'active' ? '禁用' : '启用'"
                  >
                    <el-icon><component :is="user.status === 'active' ? Lock : Unlock" /></el-icon>
                  </button>
                  <button class="action-btn danger" @click="deleteUser(user.id)" title="删除">
                    <el-icon><Delete /></el-icon>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="table-footer">
            <span>已选择 {{ selectedUsers.length }} 项</span>
            <el-button 
              v-if="selectedUsers.length > 0" 
              type="danger" 
              size="small"
              @click="batchDelete"
            >批量删除</el-button>
            <el-pagination
              :current-page="currentPage"
              :page-size="pageSize"
              :total="totalUsers"
              layout="total, prev, pager, next, jumper"
              @current-change="handlePageChange"
            />
          </div>
        </div>

        <el-dialog v-model="showAddDialog" :title="isEdit ? '编辑用户' : '创建用户'" width="500px" class="user-dialog">
          <el-form :model="form" label-width="100px" class="user-form">
            <el-form-item label="用户名" required>
              <el-input v-model="form.username" placeholder="请输入用户名" />
            </el-form-item>
            <el-form-item label="邮箱" required>
              <el-input v-model="form.email" placeholder="请输入邮箱" />
            </el-form-item>
            <el-form-item label="密码" :required="!isEdit">
              <el-input v-model="form.password" type="password" :placeholder="isEdit ? '留空则不修改' : '请输入密码'" />
            </el-form-item>
            <el-form-item label="角色" required>
              <el-select v-model="form.role">
                <el-option label="管理员" value="admin" />
                <el-option label="运维人员" value="operator" />
                <el-option label="只读用户" value="viewer" />
              </el-select>
            </el-form-item>
            <el-form-item label="状态">
              <el-switch v-model="form.status" :active-value="'active'" :inactive-value="'disabled'" />
            </el-form-item>
          </el-form>
          <template #footer>
            <el-button @click="showAddDialog = false">取消</el-button>
            <el-button type="primary" @click="handleSave">{{ isEdit ? '保存修改' : '创建用户' }}</el-button>
          </template>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import Header from '@/components/Header.vue'
import { Plus, User, UserFilled, Monitor, View, Edit, Delete, Lock, Unlock } from '@element-plus/icons-vue'

const searchQuery = ref('')
const filterRole = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const showAddDialog = ref(false)
const isEdit = ref(false)
const selectAll = ref(false)
const selectedUsers = ref<number[]>([])

const users = ref([
  { id: 1, username: 'admin', email: 'admin@example.com', role: 'admin', status: 'active', last_login: '2024-01-15 10:30:00' },
  { id: 2, username: 'operator', email: 'operator@example.com', role: 'operator', status: 'active', last_login: '2024-01-15 09:15:00' },
  { id: 3, username: 'viewer', email: 'viewer@example.com', role: 'viewer', status: 'active', last_login: '2024-01-14 16:45:00' },
  { id: 4, username: 'john', email: 'john@example.com', role: 'operator', status: 'active', last_login: '2024-01-15 08:00:00' },
  { id: 5, username: 'jane', email: 'jane@example.com', role: 'viewer', status: 'disabled', last_login: '2024-01-10 14:30:00' },
  { id: 6, username: 'bob', email: 'bob@example.com', role: 'operator', status: 'active', last_login: '2024-01-15 11:00:00' }
])

const form = reactive({
  id: 0,
  username: '',
  email: '',
  password: '',
  role: 'operator',
  status: 'active'
})

const totalUsers = computed(() => users.value.length)
const adminCount = computed(() => users.value.filter(u => u.role === 'admin').length)
const operatorCount = computed(() => users.value.filter(u => u.role === 'operator').length)
const viewerCount = computed(() => users.value.filter(u => u.role === 'viewer').length)

const getRoleLabel = (role: string) => {
  const labels: Record<string, string> = {
    admin: '管理员',
    operator: '运维人员',
    viewer: '只读用户'
  }
  return labels[role] || role
}

const handleSelectAll = (val: boolean) => {
  selectedUsers.value = val ? users.value.map(u => u.id) : []
}

const handleSave = () => {
  if (isEdit.value) {
    const index = users.value.findIndex(u => u.id === form.id)
    if (index !== -1) {
      users.value[index] = { ...users.value[index], ...form }
    }
  } else {
    users.value.push({
      ...form,
      id: Date.now(),
      last_login: ''
    })
  }
  showAddDialog.value = false
  resetForm()
}

const resetForm = () => {
  Object.assign(form, {
    id: 0,
    username: '',
    email: '',
    password: '',
    role: 'operator',
    status: 'active'
  })
  isEdit.value = false
}

const editUser = (user: any) => {
  Object.assign(form, user)
  isEdit.value = true
  showAddDialog.value = true
}

const toggleStatus = (user: any) => {
  user.status = user.status === 'active' ? 'disabled' : 'active'
}

const deleteUser = (id: number) => {
  users.value = users.value.filter(u => u.id !== id)
}

const batchDelete = () => {
  users.value = users.value.filter(u => !selectedUsers.value.includes(u.id))
  selectedUsers.value = []
  selectAll.value = false
}

const handlePageChange = (page: number) => {
  currentPage.value = page
}
</script>

<style scoped>
.users {
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

.stats-cards {
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
  display: flex;
  align-items: center;
  gap: var(--space-md);
  transition: all var(--transition-normal);
}

.stat-card:hover {
  box-shadow: var(--shadow-md);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-xl);
}

.users-icon {
  background: var(--color-info-light);
  color: var(--color-info);
}

.admin-icon {
  background: var(--color-danger-light);
  color: var(--color-danger);
}

.operator-icon {
  background: var(--color-warning-light);
  color: var(--color-warning);
}

.viewer-icon {
  background: var(--color-success-light);
  color: var(--color-success);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: var(--line-height-tight);
}

.stat-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-top: 2px;
}

.users-table-container {
  background: var(--color-white);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  overflow: hidden;
}

.table-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-md) var(--space-lg);
  border-bottom: 1px solid var(--color-border);
  gap: var(--space-md);
}

.search-input {
  flex: 1;
  max-width: 300px;
}

.role-filter {
  width: 150px;
}

.users-table {
  max-height: 400px;
  overflow-y: auto;
}

.table-head {
  display: grid;
  grid-template-columns: 40px 1fr 1fr 100px 80px 140px 120px;
  padding: var(--space-md) var(--space-lg);
  background: var(--color-surface);
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: var(--color-text-secondary);
  position: sticky;
  top: 0;
  z-index: 10;
}

.table-row {
  display: grid;
  grid-template-columns: 40px 1fr 1fr 100px 80px 140px 120px;
  padding: var(--space-md) var(--space-lg);
  border-bottom: 1px solid var(--color-border);
  align-items: center;
  transition: background var(--transition-fast);
}

.table-row:hover {
  background: var(--color-surface);
}

.table-row.selected {
  background: var(--color-info-light);
}

.table-cell {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
}

.user-name {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.user-avatar-small {
  width: 32px;
  height: 32px;
  background: var(--color-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: var(--font-size-sm);
  font-weight: 600;
}

.role-tag {
  font-size: var(--font-size-xs);
  font-weight: 500;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
}

.role-tag.admin {
  background: var(--color-danger-light);
  color: var(--color-danger);
}

.role-tag.operator {
  background: var(--color-warning-light);
  color: var(--color-warning);
}

.role-tag.viewer {
  background: var(--color-success-light);
  color: var(--color-success);
}

.status-tag {
  font-size: var(--font-size-xs);
  font-weight: 500;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
}

.status-tag.active {
  background: var(--color-success-light);
  color: var(--color-success);
}

.status-tag.disabled {
  background: var(--color-surface-raise);
  color: var(--color-text-secondary);
}

.action-buttons {
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

.table-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-md) var(--space-lg);
  border-top: 1px solid var(--color-border);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.user-dialog :deep(.el-dialog__header) {
  border-bottom: 1px solid var(--color-border);
  padding: var(--space-lg);
}

.user-dialog :deep(.el-dialog__title) {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
}

.user-dialog :deep(.el-dialog__body) {
  padding: var(--space-lg);
}

.user-dialog :deep(.el-dialog__footer) {
  border-top: 1px solid var(--color-border);
  padding: var(--space-lg);
}

.user-form {
  max-height: 400px;
  overflow-y: auto;
}

@media (max-width: 1024px) {
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .table-head,
  .table-row {
    grid-template-columns: 40px 1fr 1fr;
  }
}

@media (max-width: 768px) {
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .table-header-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-input {
    max-width: none;
  }
  
  .role-filter {
    width: 100%;
  }
}
</style>