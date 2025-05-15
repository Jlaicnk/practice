<template>
  <div class="auth-container">
    <div class="tabs">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        @click="isLogin = tab.isLogin"
        :class="{ 'active-tab': isLogin === tab.isLogin }"
      >
        {{ tab.label }}
      </button>
    </div>

    <form @submit.prevent="handleSubmit" class="compact-form">
      <!-- 用户名 -->
      <input
        v-model="formData.username"
        type="text"
        placeholder="用户名"
        class="form-input"
        required
      />

      <!-- 电子邮箱 -->
      <input
        v-if="!isLogin"
        v-model="formData.email"
        type="email"
        placeholder="电子邮箱"
        class="form-input"
        required
      />

      <!-- 密码 -->
      <input
        v-model="formData.password"
        type="password"
        :placeholder="isLogin ? '密码' : '设置密码（至少8位）'"
        class="form-input"
        required
        minlength="8"
      />

      <!-- 确认密码（注册时显示） -->
      <input
        v-if="!isLogin"
        v-model="formData.confirmPassword"
        type="password"
        placeholder="确认密码"
        class="form-input"
        required
      />

      <!-- 手机号码 -->
      <input
        v-if="!isLogin"
        v-model="formData.phonenumber"
        type="text"
        placeholder="手机号码"
        class="form-input"
        required
        pattern="^\d{11}$"
        title="请输入有效的11位手机号码"
      />

      <!-- 文件上传（注册时显示） -->
      <input
        v-if="!isLogin"
        type="file"
        @change="handleFileUpload"
        accept="image/*"
        class="form-input"
      />

      <!-- 提交按钮 -->
      <button type="submit" class="submit-btn">
        {{ isLogin ? '立即登录' : '注册账号' }}
      </button>
    </form>

    <!-- 错误提示 -->
    <div v-if="errorMsg" class="error-tip">
      ⚠️ {{ errorMsg }}
    </div>
        <!-- 成功提示 -->
    <div v-if="successMsg" class="success-tip">
      ✅ {{ successMsg }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import FrontendService from '../api/config'
import { useRouter } from 'vue-router'

// 状态变量
const isLogin = ref(true)
const errorMsg = ref('')
const successMsg = ref('') // 新增成功提示变量
const router = useRouter()

// 选项卡
const tabs = [
  { id: 1, label: '登录', isLogin: true },
  { id: 2, label: '注册', isLogin: false }
]

// 表单数据
const formData = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  phonenumber: '', // 增加手机号码字段
  avatar: null
})

// 处理文件上传
const handleFileUpload = (event) => {
  formData.avatar = event.target.files[0]
}

// 表单验证
const validateForm = () => {
  // 清空错误提示
  errorMsg.value = ''

  // 校验两次密码是否一致（仅注册时）
  if (!isLogin.value && formData.password !== formData.confirmPassword) {
    errorMsg.value = '两次密码输入不一致'
    return false
  }

  // 校验手机号格式（仅注册时）
  if (!isLogin.value && !/^\d{11}$/.test(formData.phonenumber)) {
    errorMsg.value = '请输入有效的11位手机号码'
    return false
  }

  return true
}

// 提交表单
const handleSubmit = async () => {
  if (!validateForm()) return

  try {
    const url = isLogin.value ? 'User/login/' : 'User/register/'
    const config = {}

    const formDataToSend = new FormData()
    formDataToSend.append('username', formData.username)
    formDataToSend.append('password', formData.password)

    if (!isLogin.value) {
      formDataToSend.append('email', formData.email)
      formDataToSend.append('confirmPassword', formData.confirmPassword)
      formDataToSend.append('phonenumber', formData.phonenumber)
      if (formData.avatar) {
        formDataToSend.append('avatar', formData.avatar)
      }
    }

    const response = await FrontendService.post(url, formDataToSend, config)
    console.log(response.data)

    //--测试代码--
    // 处理成功响应
    if (!isLogin.value && response.status === 201) {
      // 注册成功
      successMsg.value = '注册成功！'
      // 清空表单
      formData.username = ''
      formData.email = ''
      formData.password = ''
      formData.confirmPassword = ''
      formData.phonenumber = ''
      formData.avatar = null

      // 存储 access_token 和 refresh_token
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)

      setTimeout(() => {
        successMsg.value = ''
        // 将 isLogin 设置为 true
       isLogin.value = true
        router.push('/login') // 假设登录页面路径为 '/login'
      }, 3000)
    } else if (isLogin.value && response.status === 200) {
      // 登录成功
      successMsg.value = '登录成功！'
      formData.username = ''
      formData.password = ''

      // 存储 access_token 和 refresh_token
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)
      
      // 可选：跳转到首页
      setTimeout(() => {
        successMsg.value = ''
        router.push('/') // 假设首页路径为 '/'
      }, 3000)
    } else {
      errorMsg.value = '操作失败，请检查输入信息。'
    }
    //--测试代码--
    // 处理成功逻辑
  } catch (error) {
    console.error('Error in request:', error)
    // 捕获后端返回的错误 JSON
    if (error.response && error.response.data) {
      // 提取后端返回的错误信息
      const backendErrors = error.response.data
      let errorMessage = ''

      // 遍历后端返回的错误对象，拼接错误信息
      for (const key in backendErrors) {
        if (backendErrors.hasOwnProperty(key)) {
          const fieldErrors = backendErrors[key]
          fieldErrors.forEach((message) => {
            errorMessage += `${key}: ${message}\n`
          })
        }
      }

      // 设置 errorMsg
      errorMsg.value = errorMessage
    } else {
      // 如果后端没有返回错误 JSON，则显示默认错误信息
      errorMsg.value = '操作失败，请检查输入信息。'
    }
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

.tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
}

.tabs button {
  flex: 1;
  padding: 10px 0;
  border: none;
  background: none;
  font-size: 15px;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 6px;
}

.active-tab {
  background: #f0f5ff !important;
  color: #2a60eb !important;
  font-weight: 500;
}

.compact-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.form-input {
  padding: 10px 14px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-input:focus {
  border-color: #2a60eb;
  outline: none;
  box-shadow: 0 0 0 2px rgba(42,96,235,0.1);
}

.submit-btn {
  margin-top: 8px;
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

.error-tip {
  margin-top: 12px;
  padding: 8px;
  background: #fee;
  border-radius: 6px;
  color: #e44;
  font-size: 13px;
  text-align: center;
}
</style>
