import { createRouter, createWebHashHistory } from "vue-router";
import Layout from "../components/Layout.vue";

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/', // 添加路径
      redirect: '/Home',
      component: Layout,
      children: [
        { path: 'Home', component: () => import("../views/HomePage.vue") }, // 默认子路由
        { path: 'test', component: () => import("../views/TestView.vue") },
        { path: 'search', component: () => import("../views/KnowledgeGraphView.vue") },
        { path: 'aianswer', component: () => import("../views/KnowledgeAiAnswerView.vue") },
        { path: 'sorry', component: () => import("../views/sorry.vue") },
        { path: 'login', component: () => import("../views/AuthView.vue") },
        { path: 'logout', component: () => import("../views/LogoutView.vue") },
        { path: 'API', component: () => import("../views/API.vue") },
        { path: 'recommend', component: () => import("../views/Recommend.vue") },
      ],
    },
  ],
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('access_token');

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next('/login');
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
