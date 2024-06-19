import Vue from 'vue'
import VueRouter from 'vue-router'
import login from '../views/login.vue'
import register from '../views/register.vue'
import layout from '../views/layout.vue'
import topology from '../views/topology.vue'
import testt from '../views/testt.vue'
import exercise from '../views/exercise.vue'

Vue.use(VueRouter)


const  routes= [
   {
      path: '',
      // 重定向
      redirect: '/exercise',
    },
   {
      path:'/exercise',
      name:exercise,
      component:exercise,
   },
   {
      path:'/register',
      name:register,
      component:register,
   },
   {
      path:'/testt',
      name:testt,
      component:testt,
   },
   {
      path:'/layout',
      name:layout,
      component:layout,
      redirect: '/topology',
      children:[
         {
            path:'/topology',
            name:topology,
            component:topology,
         },
      ]
   },

]
const router=new VueRouter({
  mode:'hash',
  routes
})
export default router;


