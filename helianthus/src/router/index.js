import Vue from 'vue'
import Router from 'vue-router'

import Home from '@/components/Home'
import SocialSecurity from '@/components/SocialSecurity'
import UserManage from '@/components/UserManage'
import AddBlog from '@/components/AddBlog'
import About from '@/components/About'
import BlogList from '@/components/BlogList'
import UploadData from '@/components/UploadData'
import Manage from '@/components/Manage'
import Login from '@/components/User/Login'
import Register from '@/components/User/Register'
import ROOT from '@/components/User/ROOT'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {path: '/', name: 'Home', component: Home},  // 主页
    {path: '/socialsecurity', name: 'SocialSecurity', component: SocialSecurity},  // 个人社保信息
    {path: '/usermanage', name: 'UserManage', component: UserManage},
    {path: '/addblog', name: 'AddBlog', component: AddBlog},   // 添加blog
    {path: '/manage', name: 'Manage', component: Manage},   // 风控模型管理
    {path: '/about', name: 'About', component: About},   // 关于
    {path: '/bloglist', name: 'BlogList', component: BlogList},  // 显示blog信息
    {path: '/uploaddata', name: 'UploadData', component: UploadData},   // 上传工资表
    {path: '/user/login', name: 'Login', component: Login},   // 登录
    {path: '/user/register', name: 'Register', component: Register},   // 注册
    {path: '/user/root', name: 'ROOT', component: ROOT},   // 个人信息
  ]
})
