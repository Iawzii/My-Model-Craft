<template>
  <div class="w-64 bg-white border border-gray-100 rounded-2xl shadow-2xl p-4 text-left">
    <p class="text-sm font-semibold text-gray-700 mb-3">{{ title }}</p>
    <div v-if="loading" class="text-sm text-gray-500 py-6 text-center">加载中...</div>
    <div v-else-if="!users.length" class="text-sm text-gray-400 py-6 text-center">{{ emptyText }}</div>
    <ul v-else class="space-y-3 max-h-64 overflow-y-auto pr-1">
      <li v-for="user in users" :key="user.id" class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-indigo-500 text-white font-semibold flex items-center justify-center overflow-hidden">
          <span v-if="!user.avatarUrl">{{ getInitial(user.username) }}</span>
          <img v-else :src="user.avatarUrl" :alt="user.username" class="w-full h-full object-cover" />
        </div>
        <div>
          <p class="text-sm font-medium text-gray-900">{{ user.username }}</p>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: ''
  },
  users: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  emptyText: {
    type: String,
    default: '暂无数据'
  }
})

const getInitial = (name) => {
  if (!name) return 'U'
  return name.charAt(0).toUpperCase()
}
</script>
