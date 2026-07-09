<template>
  <div class="config">
    <Sidebar />
    <div class="main-content">
      <Header title="配置管理" />
      <div class="content">
        <h1>配置管理</h1>
        <el-tabs v-model="activeTab">
          <el-tab-pane label="虚拟服务器" name="vs">
            <el-button type="primary">创建虚拟服务器</el-button>
          </el-tab-pane>
          <el-tab-pane label="池" name="pools">
            <el-button type="primary">创建池</el-button>
          </el-tab-pane>
          <el-tab-pane label="证书" name="certificates">
            <el-button type="primary">上传证书</el-button>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import Header from '@/components/Header.vue'

const activeTab = ref('vs')
</script>

<style scoped>
.config { display: flex; min-height: 100vh; }
.main-content { flex: 1; display: flex; flex-direction: column; background: #f5f7fa; }
.content { padding: 20px; }
</style>