<template>
    <div class="form-container" >
      <el-form class="form-left" :model="form" label-width="80px">
        <div class="form-row">
          <el-form-item label="节点1">
            <el-input v-model="form.e1"></el-input>
          </el-form-item>
          <el-form-item label="关系">
            <el-input v-model="form.rel"></el-input>
          </el-form-item>
          <el-form-item label="节点2">
            <el-input v-model="form.e2"></el-input>
          </el-form-item>
        </div>
        <div class="form-row">
          <el-form-item label="最小步长">
            <el-input v-model="form.min"></el-input>
          </el-form-item>
          <el-form-item label="最大步长">
            <el-input v-model="form.max"></el-input>
          </el-form-item>
          <el-form-item label="节点数">
            <el-input v-model="form.limit"></el-input>
          </el-form-item>
        </div>
      </el-form>
      <div class="form-right">
        <el-form-item>
          <el-button type="primary" @click="submitForm">查询</el-button>
        </el-form-item>
      </div>
    </div>
  </template>


  <script>
  import  searchApi  from '../api/search'
  import  userApi  from '../api/user'

  export default {
    data() {
      return {
        form: {
          e1: '',
          rel: '',
          e2: '',
          min: '',
          max: '',
          limit: ''
        },
        performance:null
      };
    },
    mounted() {
        // 在组件挂载时添加事件监听器
        document.addEventListener('keydown', this.handleKeyDown);
        console.log("事件监听器已添加");
      },
    beforeDestroy() {
      // 在组件销毁前移除事件监听器
      document.removeEventListener('keydown', this.handleKeyDown);
      console.log("事件监听器已移除");
    },
    methods: {
      submitForm() {
        const currentUserId = userApi.getCurrentUserId();
        console.log("currentUserId",currentUserId);
        // 发送Get和POST请求
        Promise.all
        ([searchApi.getSearchForm(this.form),
        userApi.getUserPreferences(currentUserId)])
        .then(([response1, response2]) => {
            console.log("后端返回图谱数据：", response1);
            console.log("后端返回图谱数据：", response2);
          // 处理响应，更新图表数据
          this.$emit('update-data', {currentUserId, response1, response2 });
        });
      },
      handleKeyDown(event) {
        console.log("按键按下", event.key);
        if (event.key === 'Enter') {
          this.submitForm();
        }
      }
    }
  };
  </script>

<style>
.form-container {
  display: flex;
  justify-content: space-between;
  border: 1px solid skyblue;
  padding: 20px;
}
.form-left {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}
.form-row {
  display: flex;
  justify-content: space-around;
}
.form-right {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100px;
}
</style>
