<template>
  <div
    class="bg-white rounded shadow cursor-pointer hover:shadow-lg transition flex flex-col h-full"
    @click="emit('click', modelId)"
  >
    <img :src="model.thumbnailUrl || fallbackThumbnail" alt="thumbnail" class="w-full h-40 sm:h-48 lg:h-56 object-cover rounded-t">
    <div class="p-4">
      <h3 class="font-semibold text-lg mb-1">{{ model.title }}</h3>
      <p class="text-gray-600 text-sm mb-2">{{ (model.description || '').slice(0, 50) }}...</p>
      <p class="text-sm text-gray-500">作者: {{ model.authorName || model.author?.username || '匿名创作者' }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  model: {
    type: Object,
    required: true
  }
})
const emit = defineEmits(['click'])

const fallbackThumbnail = 'https://images.unsplash.com/photo-1489515217757-5fd1be406fef?auto=format&fit=crop&w=600&q=80'

const modelId = computed(() => props.model.id)
</script>
