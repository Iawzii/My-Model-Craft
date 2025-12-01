import { defineStore } from 'pinia'
import { modelsApi } from '@/api'

export const useModelsStore = defineStore('models', {
  state: () => ({
    models: []
  }),
  actions: {
    async fetchRecentModels(limit = 12) {
      const { data } = await modelsApi.listRecent({ limit })
      this.models = data
      return this.models
    },
    async searchModels(params) {
      const res = await modelsApi.search(params)
      return res.data
    },
    async fetchModelById(id) {
      const { data } = await modelsApi.getById(id)
      return data
    },
    async fetchAuthorModels(authorId, limit = 4) {
      if (!authorId) return []
      const { data } = await modelsApi.listRecent({ authorId, limit })
      return data
    }
  }
})
