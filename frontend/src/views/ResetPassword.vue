<template>
  <div class="flex flex-col">
    <section>
      <div class="container mx-auto px-8 py-4 max-w-6xl">
        <nav class="text-1xl text-gray-600">
          <router-link to="/" class="hover:underline">主页</router-link>
          <span class="mx-2">></span>
          <span class="text-gray-900">重置密码</span>
        </nav>
      </div>
    </section>
    <section>
      <div class="container mx-auto px-8">
        <div class="min-h-[600px] flex items-center justify-center">
          <div class="bg-white p-6 sm:p-8 rounded-lg shadow-md w-full max-w-md">
            <div v-if="errorMessage" class="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">{{ errorMessage }}</div>
            <div v-if="successMessage" class="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">{{ successMessage }}</div>
            <h2 class="text-2xl font-bold text-center mb-6">重置密码</h2>
            <form @submit.prevent="handleReset">
              <div class="mb-4">
                <input
                  type="email"
                  v-model="email"
                  class="w-full p-3 border rounded-lg focus:outline-none focus:border-blue-500"
                  placeholder="请输入注册邮箱"
                />
              </div>
              <div class="mb-4">
                <input
                  type="text"
                  v-model="code"
                  class="w-full p-3 border rounded-lg focus:outline-none focus:border-blue-500"
                  placeholder="请输入验证码"
                />
              </div>
              <div class="mb-6">
                <input
                  type="password"
                  v-model="newPassword"
                  class="w-full p-3 border rounded-lg focus:outline-none focus:border-blue-500"
                  placeholder="请输入新的密码"
                />
              </div>
              <div class="mb-6">
                <input
                  type="password"
                  v-model="confirmPassword"
                  class="w-full p-3 border rounded-lg focus:outline-none focus:border-blue-500"
                  placeholder="再次输入新的密码"
                />
              </div>
              <button type="submit" :disabled="loading" class="w-full py-3 text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:bg-gray-300">
                {{ loading ? '重置中...' : '确认重置' }}
              </button>
            </form>
            <div class="mt-4 text-center text-sm text-gray-600">
              还没有验证码？
              <router-link to="/forgot-password" class="text-blue-600">去获取</router-link>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const email = ref('')
const code = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const loading = ref(false)
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const handleReset = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (!email.value || !emailRegex.test(email.value)) {
    errorMessage.value = '请输入有效的邮箱地址'
    return
  }
  if (!code.value || code.value.length !== 6) {
    errorMessage.value = '请输入6位验证码'
    return
  }
  if (!newPassword.value || newPassword.value.length < 6) {
    errorMessage.value = '新密码至少6位'
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value = '两次输入的密码不一致'
    return
  }

  loading.value = true
  const result = await authStore.resetPassword({ email: email.value, code: code.value, newPassword: newPassword.value })
  loading.value = false

  if (result.success) {
    successMessage.value = result.message
    setTimeout(() => {
      router.push('/login')
    }, 1500)
  } else {
    errorMessage.value = result.message
  }
}
</script>
