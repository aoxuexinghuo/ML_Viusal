import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import request from "@/utils/request"
import 'echarts'
import mermaid from 'mermaid'

const app = createApp(App)

app.config.globalProperties.$axios = axios;
axios.defaults.baseURL = "/api";
axios.defaults.withCredentials = true;

// 使用icon
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.config.globalProperties.request = request ;
app.use(createPinia())
app.use(router)
app.use(ElementPlus)

// 配置 mermaid
mermaid.initialize({
    startOnLoad: true,
    theme: 'default'
});

app.mount('#app')
