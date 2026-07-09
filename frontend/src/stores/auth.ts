import { defineStore } from 'pinia'
import { ref } from 'vue'
import request from '@/utils/request'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const username = ref('')
  const role = ref('')

  const login = async (data: { username: string; password: string }) => {
    const response = await request.post('/auth/login', data)
    token.value = response.data.access_token
    localStorage.setItem('token', token.value)
    return response.data
  }

  const logout = () => {
    token.value = ''
    username.value = ''
    role.value = ''
    localStorage.removeItem('token')
  }

  return { token, username, role, login, logout }
})