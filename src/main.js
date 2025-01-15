import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

const app = createApp(App);

//守卫
router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn');
  if (to.path === '/goods-list' && !isLoggedIn) {
    next('/login');
  } else {
    next();
  }
});

app.use(router);
app.mount('#app');
