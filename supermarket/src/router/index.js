import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login'
import Home from '../components/Home'
import Welcome from '../components/Welcome'
import Superinfo from '../components/Staff/Superinfo'
import Supplier from '../components/Supplier/Supplier'
import Goods from '../components/Goods/Goods'
import Purchase from '../components/Purchase/Purchase'
import Sales from '../components/Sales/Sales'
import Statistic from '../components/Statistic/Statistic'
import Admininfo from '../components/Staff/Admininfo'

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
      { path: '/supplier', component: Supplier },
      { path: '/supplierMap', component: SupplierMap },
      { path: '/goods', component: Goods },
      { path: '/purchase', component: Purchase },
      { path: '/sales', component: Sales },
      { path: '/statistic', component: Statistic}
    ] }
]

const router = new VueRouter({
  routes
})

export default router
