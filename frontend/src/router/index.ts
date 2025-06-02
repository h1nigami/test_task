// src/router/index.ts
import { createRouter, createWebHistory} from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import Home from '@/views/Home.vue'
import EquipmentList from '@/views/EquipmentList.vue'
import type { DefineComponent } from 'vue'

type Component = DefineComponent<{},{},any>

const routes: RouteRecordRaw[] = [
    {
        path: '/',
        name: 'Home',
        component: Home as Component
    },
    {
        path: '/equipment',
        name: 'EquipmentList',
        component: EquipmentList as Component
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
