import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupPage from '../views/SignupPage.vue'
import LoginPage from '../views/LoginPage.vue'
import AboutView from '../views/AboutView.vue'
import CreateService from '../views/CreateService.vue'
import EditService from '@/views/EditService.vue'
import AdminDashboard from '@/views/AdminDashboard.vue' 
import CustomerDashboard from '@/views/CustomerDashboard.vue'
import ProfessionalDashboard from '@/views/ProfessionalDashboard.vue' 
//import


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupPage
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: AboutView
  }, 
  {
    path: '/create_service',
    name: 'create_service',
    component: CreateService
  },
  {
    path:'/edit_service/:id',
    name:'edit_service',
    component: EditService
  },
  {
    path: '/admin_dashb',
    name: 'admindashb',
    component: AdminDashboard
  },
  {
    path: '/cust_dashb',
    name: 'customerdashb',
    component: CustomerDashboard
  },
  {
    path: '/profes_dashb',
    name: 'profesdashb',
    component: ProfessionalDashboard
  },
  
  // {
  //   path: '/admin-dashboard',
  //   name: 'admindashboard',
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AdminDashboard.vue')
  // }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
