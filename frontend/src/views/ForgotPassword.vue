<template>
  <div class="flex flex-col">
    <section>
      <div class="container mx-auto px-8 py-4 max-w-6xl">
        <nav class="text-1xl text-gray-600">
          <router-link to="/" class="hover:underline">主页</router-link>
          <span class="mx-2">></span>
          <span class="text-gray-900">找回密码</span>
        </nav>
      </div>
    </section>
    <section>
      <div class="container mx-auto px-8">
        <div class="min-h-[600px] flex items-center justify-center">
          <div class="bg-white p-6 sm:p-8 rounded-lg shadow-md w-full max-w-md">
            <div v-if="errorMessage" class="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">{{ errorMessage }}</div>
            <div v-if="successMessage" class="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">{{ successMessage }}</div>
            <h2 class="text-2xl font-bold text-center mb-6">找回密码</h2>
            <p class="text-sm text-gray-600 mb-4">输入注册邮箱，我们会发送验证码到该邮箱。</p>
            <form @submit.prevent="handleSend">
              <div class="mb-4">
                <input
                  type="email"
                  v-model="email"
                  class="w-full p-3 border rounded-lg focus:outline-none focus:border-blue-500"
                  placeholder="请输入注册邮箱"
                />
              </div>
              <button type="submit" :disabled="loading" class="w-full py-3 text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:bg-gray-300">
                {{ loading ? '发送中...' : '发送验证码' }}
              </button>
            </form>
            <div class="mt-4 text-center text-sm text-gray-600">
              已经收到验证码？
              <router-link to="/reset-password" class="text-blue-600">前往重置</router-link>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const email = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const loading = ref(false)
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const handleSend = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (!email.value || !emailRegex.test(email.value)) {
    errorMessage.value = '请输入有效的邮箱地址'
    return
  }

  loading.value = true
  const result = await authStore.forgotPassword(email.value)
  loading.value = false
  if (result.success) {
    successMessage.value = result.message
  } else {
    errorMessage.value = result.message
  }
}
</script>
