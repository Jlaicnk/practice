<template>
    <div class="auth-container">
      <button @click="logout" class="submit-btn">
        注销账号
      </button>
    </div>
  </template>

  <script setup>
  import { ref } from 'vue'
  // import FrontendService from '../services/FrontendService'
  import router from '../router'

  const logout = async () => {
    try {
      const refresh_token = localStorage.getItem('refresh_token')
      if (!refresh_token) {
        throw new Error('Refresh token not found')
      }

      const response = await FrontendService.post('User/logout/', { refresh: refresh_token })
      console.log(response.data)

      // 注销成功后的逻辑
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      alert('注销成功！')

      // 重定向到登录页面
      router.push('/login')
    } catch (error) {
      console.error(error)
      alert('注销失败，请重试。')
    }
  }
  </script>

  <style scoped>
  .auth-container {
    width: 360px;
    margin: 40px auto;
    padding: 24px;
    background: #fcfcfd;
    border-radius: 12px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
  }

  .submit-btn {
    padding: 12px;
    background: #2a60eb;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    cursor: pointer;
    transition: background 0.2s;
  }

  .submit-btn:hover {
    background: #1a4ac7;
  }
  </style>
