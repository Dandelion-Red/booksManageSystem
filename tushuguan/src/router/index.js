import Vue from 'vue'
import Router from 'vue-router'
import VueResource from 'vue-resource'
import iView from 'iview'
import 'iView/dist/styles/iview.css'
import VueQuillEditor from 'vue-quill-editor'
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
import HelloWorld from '../components/HelloWorld'
import Index from '../components/Index'
import Manager from '../components/Manager'
import RecordManage from '../components/RecordManage'
import UserManage from '../components/UserManage'
// import MyRecord from '../components/MyRecord'
// import SearchBook from '../components/SearchBook'
// import Reader from '../components/Reader'
import BookManage from '../components/BookManage'

Vue.use(Router)
Vue.use(VueResource)
Vue.use(iView)
// Vue.use(VueQuillEditor,{default global options})
Vue.use(VueQuillEditor)

// 定义各种路径跳转
export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/index',
      component: Index
    },
    {
      path: '/recordManage',
      component: RecordManage
    },
    {
      path: '/userManage',
      component: UserManage
    },
    // {
    //   path: '/myRecord',
    //   component: MyRecord
    // },
    // {
    //   path: '/searchBook',
    //   component: SearchBook
    // },
    // {
    //   path: '/reader',
    //   component: Reader
    // },
    {
      path: '/bookManage',
      component: BookManage
    },
    {
      path: '/manager',
      component: Manager
    }
  ]
})
