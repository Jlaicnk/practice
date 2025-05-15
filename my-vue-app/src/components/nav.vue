<template>
  <nav class="top-nav">
  <ul>
    <li v-if="!isActiveHome">
        <router-link
          to="/Home"
          class="nav-link"
          active-class="active"
        >
          返回首页
        </router-link>
      </li>
    <li>
      <router-link to="/search" class="nav-link" active-class="active">搜索</router-link>
    </li>
    <li>
      <router-link to="/aianswer" class="nav-link" active-class="active">问答</router-link>
    </li>
    <li>
      <router-link to="/recommend" class="nav-link" active-class="active">推荐</router-link>
    </li>
    <li>
      <router-link to="/user-management" class="nav-link" active-class="active">用户管理</router-link>
    </li>
    <li>
      <router-link to="/login" class="nav-link" active-class="active">登录</router-link>
    </li>
  </ul>
  </nav>
</template>

<script>
export default {
  computed: {
    isActiveHome() {
      return this.$route.path === '/Home';
    }
  }
}
</script>

<style scoped>
    body {
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f4f4f9;
    }

    header {
        background-color: #13b7db;
        position: sticky;
        top: 0;
        z-index: 1000; /* 确保导航固定在顶部 */
    }

    .top-nav {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding: 10px 20px;
        background-color:#1a202c;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 添加阴影，提升层次感 */
    }

    /* 导航栏列表样式 */
    .top-nav ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        display: flex;
    }

    .top-nav ul li {
        margin: 0 10px;
    }

    /* 导航链接样式 */
    .top-nav ul li a {
        text-decoration: none;
        color: white; /* 默认字体颜色 */
        font-size: 18px;
        font-weight: 500; /* 字体加粗，提升可读性 */
        padding: 10px 20px; /* 内间距稍大一些 */
        display: block;
        transition: color 0.3s ease, background-color 0.3s ease; /* 添加平滑过渡 */
    }

    /* 鼠标悬停效果 */
    .top-nav ul li a:hover {
        color:rgb(132, 186, 244); /* 悬停时字体颜色变化 */
        background-color: rgba(255, 255, 255, 0.1); /* 背景稍微变浅 */
        text-decoration: none; /* 取消下划线 */
    }

    /* 选中的样式 */
    .top-nav ul li a.active {
        color: #007BFF; /* 激活状态字体颜色 */
        border-bottom: 2px solid #007BFF; /* 底部下划线 */
    }
</style>