// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Global from './components/util/Global'
// import locale from 'element-ui/lib/locale/lang/zh-CN'
import moment from 'moment'

Vue.filter('dateFormat', function (dateStr, pattern = 'YYYY-MM-DD HH:mm:ss') {
  return moment(dateStr).format(pattern)
})
// import Moment from 'moment'
// Vue.prototype.moment = Moment
Vue.prototype.GLOBAL = Global
Vue.config.productionTip = false
Vue.http.options.emulateJSON = true
// 设置请求头部content-type:application/x-www-form-urlencoded
// Vue.http.options.emulateJSON = true
// Vue.http.options.emulateHTTP = true
// Vue.http.options.xhr = { withCredentials: true }

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: {App}
})
