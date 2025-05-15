<template>
  <el-container style="height: 100vh;">
    <el-container>
      <el-container>
        <Nav />
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </el-container>
</template>

<script>
import Nav from '../components/nav.vue'
export default {
  components: {
    Nav
  }
}
</script>

<style scoped>
/* 布局样式 */
.el-container {
  display: flex;
  flex-direction: column;
  padding: 0; /* 设置内边距为0 */
}

.el-header, .el-footer {
  background-color: #409EFF;
  color: #333;
  text-align: center;
  line-height: 50px;
  padding: 0; /* 设置内边距为0 */
}

.el-aside {
  background-color: #545c64;
  color: #333;
  text-align: center;
  line-height: 200px;
  padding: 0; /* 设置内边距为0 */
}

.el-main {
  background-color: #e9eef3;
  color: #333;
  text-align: center;
  /* line-height: 160px; */
  padding: 0; /* 设置内边距为0 */
}

body > .el-container {
  margin: 0;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
  padding: 0; /* 设置内边距为0 */
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
  padding: 0; /* 设置内边距为0 */
}
</style>
