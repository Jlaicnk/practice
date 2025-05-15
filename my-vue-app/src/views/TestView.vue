<template>
    <div class="site-main">
      <el-form-item>
        <el-button type="primary" @click="getNum()">获取随机数</el-button>
        <el-input type='text' style="width: 200px;" placeholder="随机数" v-model="num"></el-input>
        <el-input-number v-model="numNo" :min="1" :max="5" />
      </el-form-item>
    </div>
  </template>

  <script>
  import  searchApi  from '../api/search'

  export default {

    data() {
      return {
        num: '',
        numNo: 1,
      }
    },
    methods: {
        // 生成随机数
        getNum() {
          searchApi.getRandomNumber(this.numNo)
            .then(response => {
                console.log("view响应数据：" , response);
                this.num = response; // 将返回的随机数赋值给 num
            })
            .catch(error => {
                console.error("获取随机数错误:", error); // 处理可能的错误
            });
        }
    }
  }

  </script>

  <style scoped>
  .site-main {
    background: #fff;
    padding: 24px;
    height: 100vh;
    width: 100%;
  }
  </style>