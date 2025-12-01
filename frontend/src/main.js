import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from '@/stores/auth'
import './assets/tailwind.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)

const authStore = useAuthStore(pinia)
if (authStore.token) {
	authStore.fetchCurrentUser().catch(() => {})
}

app.use(router)
app.mount('#app')
