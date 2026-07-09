<template>
  <div class="batch">
    <Sidebar />
    <div class="main-content">
      <Header title="批量操作" />
      <div class="content">
        <h1>批量操作</h1>
        <el-card>
          <template #header>批量配置下发</template>
          <el-select v-model="selectedDevices" multiple placeholder="选择设备">
            <el-option label="lb-01" value="1" />
            <el-option label="lb-02" value="2" />
          </el-select>
          <el-button type="primary" style="margin-top: 20px;">执行配置</el-button>
        </el-card>
        <el-card style="margin-top: 20px;">
          <template #header>批量升级</template>
          <el-select v-model="selectedDevices" multiple placeholder="选择设备" />
          <el-button type="primary" style="margin-top: 20px;">执行升级</el-button>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import Header from '@/components/Header.vue'

const selectedDevices = ref<string[]>([])
</script>

<style scoped>
.batch { display: flex; min-height: 100vh; }
.main-content { flex: 1; display: flex; flex-direction: column; background: #f5f7fa; }
.content { padding: 20px; }
</style>