// src/App.vue
<template>
 <div id="app">
 <router-view />
 </div>
</template>

<script setup lang="ts">
import { defineAsyncComponent } from 'vue'

// Использование defineAsyncComponent для корректной типизации
const Home = defineAsyncComponent(() => import('./views/Home.vue'))
const EquipmentList = defineAsyncComponent(() => import('./views/EquipmentList.vue'))
</script>

<style>
#app {
 font-family: Avenir, Helvetica, Arial, sans-serif;
 -webkit-font-smoothing: antialiased;
 -moz-osx-font-smoothing: grayscale;
 text-align: center;
 color: #2c3e50;
}
</style>
