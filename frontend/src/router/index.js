'use strict';

import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
    { path: '/', name: 'dashboard', component: () => import('../views/DashboardView.vue') },
    { path: '/exploits', name: 'exploits', component: () => import('../views/ExploitsView.vue') },
    { path: '/exploits/:id/edit', name: 'exploit-edit', component: () => import('../views/ExploitEditView.vue') },
    { path: '/exploits/:id/stats', name: 'exploit-stats', component: () => import('../views/ExploitStatsView.vue') },
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router
