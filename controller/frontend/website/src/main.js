// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import axios from 'axios'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import * as echarts from 'echarts'
import './assets/css/base.css'

Vue.prototype.$fetch = async function(url, method = 'GET', body) {
  const baseURL = 'http://127.0.0.1:4523/m1/4228670-0-default/';
const requestOptions = {
   method: method.toUpperCase(),
   headers: {
   'Content-Type': 'application/json'
   },
   body: method.toUpperCase() === 'POST' ? JSON.stringify(body) : undefined
  };
 
  const response = await fetch(baseURL + url, requestOptions);
  const data = await response.json();
  
   if (response.ok) {
   return data;
   } else {
   throw new Error(data.message || '请求失败');
   }
  };
axios.defaults.baseURL='http://219.242.112.215:8000/';
Vue.prototype.$echarts = echarts;
Vue.config.productionTip = false;
Vue.prototype.$axios = axios;

Vue.use(ElementUI)
Vue.use(echarts)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
