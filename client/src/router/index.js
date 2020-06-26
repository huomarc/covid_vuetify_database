import Vue from 'vue'
import VueRouter from 'vue-router'
import DataTable from '@/components/DataTable'
Vue.use(VueRouter)
export default new VueRouter({
  routes: [
    {
      path: '/',
      name: 'DataTable',
      props: true,
      component: DataTable
    }
  ]
})