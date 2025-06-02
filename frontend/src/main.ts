// src/main.ts
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import './assets/styles.css'

// Добавляем типы для компонентов
import type { App as VueApp } from 'vue'

const app = createApp(App) as VueApp
app
 .use(router)
 .use(vuetify)
 .mount('#app')
