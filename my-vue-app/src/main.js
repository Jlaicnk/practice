import { createApp } from "vue";
import './style.css'
import App from "./App.vue";
import router from "./router";
import store from './store'

import axios from "axios";
import { message } from "ant-design-vue";
import { handleError } from "../src/error/handleError";
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import './assets/fonts/iconfonts/iconfont'
// 全局配置
axios.defaults.baseURL = axios.defaults.baseURL = 'http://localhost:8000'; //设置axios的默认请求基础URL
message.config({ duration: 2, top: "50px", maxCount: 3 });  //对ant-design-vue的message组件进行全局配置。

const app = createApp(App)
app.mixin(handleError)
app.use(store)
app.use(ElementPlus)
app.use(router).mount("#app");

