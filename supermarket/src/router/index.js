import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login'
import Home from '../components/Home'
import Welcome from '../components/Welcome'
import Superinfo from '../components/Staff/Superinfo'
// import Supplier from '../components/Supplier/Supplier'
import Category from '../components/Goods/Category'
import GoodInfo from '../components/Goods/GoodInfo'
import Purchase from '../components/Purchase/Purchase'
import Sales from '../components/Sales/Sales'
import Statistic from '../components/Statistic/Statistic'
import Admininfo from '../components/Staff/Admininfo'
import AddGood from '../components/Goods/AddGood'

import SupplierMap from '../components/Supplier/Map'

Vue.use(VueRouter)

const routes = [
  { path: '/', redirect: '/login' }, // 表示访问登录页面
  { path: '/login', component: Login },
  { path: '/home', component: Home, redirect: '/welcome',
    children: [
      { path: '/welcome', component: Welcome },
      { path: '/superinfo', component: Superinfo },
      { path: '/admininfo', component: Admininfo },
      // { path: '/supplier', component: Supplier },
      { path: '/supplier', component: SupplierMap },
      { path: '/category', component: Category },
      { path: '/addgood', component: AddGood},
      { path: '/goodInfo', component: GoodInfo},
      { path: '/purchase', component: Purchase },
      { path: '/sales', component: Sales },
      { path: '/statistic', component: Statistic}
    ] }
]

const router = new VueRouter({
  routes
})

// 挂载路由守卫导航，得判断有了token才能访问特殊页面
router.beforeEach((to, from, next)=> {
  // to将要访问的路径 from从哪个路径跳转而来 next是一个函数表示放行
  // 1. 访问登录页，直接放行
  if(to.path === '/login') return next();
  // 2. 获取token
  const tokenStr = window.sessionStorage.getItem('token');
  // 3. 如果token不存在，跳转回login页面
  if(!tokenStr) return next('/login');
  // 4. 如果存在，直接放行
  next();
})

export default router


