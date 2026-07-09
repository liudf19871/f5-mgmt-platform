<template>
  <div class="reports">
    <Sidebar />
    <div class="main-content">
      <Header title="报表中心" />
      <div class="content">
        <h1>报表中心</h1>
        <el-tabs v-model="activeTab">
          <el-tab-pane label="流量统计" name="traffic">
            <el-card>流量统计图表</el-card>
          </el-tab-pane>
          <el-tab-pane label="性能趋势" name="performance">
            <el-card>性能趋势图表</el-card>
          </el-tab-pane>
          <el-tab-pane label="可用性报告" name="availability">
            <el-card>可用性报告</el-card>
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

const activeTab = ref('traffic')
</script>

<style scoped>
.reports { display: flex; min-height: 100vh; }
.main-content { flex: 1; display: flex; flex-direction: column; background: #f5f7fa; }
.content { padding: 20px; }
</style>