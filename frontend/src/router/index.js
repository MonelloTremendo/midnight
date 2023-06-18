'use strict';

import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    { path: '/exploits', name: 'exploits', component: () => import('../views/ExploitsView.vue') },
    { path: '/exploits/:id', name: 'exploit', component: () => import('../views/ExploitDetailsView.vue') },
    { path: '/plots', name: 'plots', component: () => import('../views/PlotsView.vue') },
    { path: '/settings', name: 'settings', component: () => import('../views/SettingsView.vue') },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
