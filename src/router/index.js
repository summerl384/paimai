import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from '../views/UserLogin.vue';
import UserRegister from '../views/UserRegister.vue';
import GoodsList from '../views/GoodsList.vue';
import AdminDashboard from '../views/AdminDashboard.vue';
import AuctionDetail from '../views/AuctionDetail.vue';
import AuctionResult from '../views/AuctionResult.vue';
import UserM from '../views/UserM.vue';

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: UserLogin },
  { path: '/register', component: UserRegister },
  { path: '/goods-list', component: GoodsList },
  { path: '/admin-dashboard', component: AdminDashboard },
  { path: '/auction-detail/:id', component: AuctionDetail, props: true },
  { path: '/auction-result/:id', component: AuctionResult, props: true },
  { path: '/user-profile', component: UserM, meta: { requiresAuth: true } }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isLoggedIn) {
      next({ path: '/login' });
    } else {
      next();
    }
  } else {
    next();
  }
});


export default router;