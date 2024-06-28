import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import request from "@/utils/request";
import 'echarts'

const app = createApp(App)

// 将axios挂载到原型对象上
app.config.globalProperties.$axios = axios;
// 设置axios请求的地址默认是'/api'，后续会通过代理转移
axios.defaults.baseURL = "/api";
// 请求时带上cookie
axios.defaults.withCredentials = true;

// 使用icon
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.config.globalProperties.request = request ;
app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.mount('#app')
