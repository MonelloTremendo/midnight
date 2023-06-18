import { Vue, createApp } from 'vue';
import App from './App.vue';
import './registerServiceWorker';
import router from './router';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.js';
import 'bootstrap-icons/font/bootstrap-icons.css';

// import { library } from 'fontawesome-svg-core';
// import { FontAwesomeIcon } from 'vue-fontawesome';
// import { faUserSecret } from 'free-solid-svg-icons';

// library.add(faUserSecret);

// Vue.component('font-awesome-icon', FontAwesomeIcon)

createApp(App)
    .use(router)
    .mount('#app');
