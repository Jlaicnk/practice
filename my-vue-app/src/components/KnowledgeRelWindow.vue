<template>
    <div v-if="visible" class="modal">
      <div class="modal-content">
        <!-- 标题部分 -->
        <h2 class="title">
          {{ nodeData.source + "->" + nodeData.name + "->" + nodeData.target }}
        </h2>

        <!-- 数据展示部分，左右两栏布局 -->
        <div class="custom-grid">
          <!-- 左栏 -->
          <div class="custom-grid-left">
            <el-row class="list-item" gutter="20">
                <el-col :span="4" class="header">category</el-col>
                <el-col :span="20" class="content">{{ categories[sourceNode.category]||"null" }}</el-col>
            </el-row>
            <el-row class="list-item" gutter="20">
                <el-col :span="4" class="header">desc</el-col>
                <el-col :span="20" class="content">{{ sourceNode.desc||"null" }}</el-col>
            </el-row>
          </div>

          <!-- 右栏 -->
          <div class="custom-grid-right">
            <el-row class="list-item" gutter="20">
                <el-col :span="4" class="header">category</el-col>
                <el-col :span="20" class="content">{{ categories[targetNode.category]||"null" }}</el-col>
            </el-row>
            <el-row class="list-item" gutter="20">
                <el-col :span="4" class="header">desc</el-col>
                <el-col :span="20" class="content">{{ targetNode.desc||"null" }}</el-col>
            </el-row>
          </div>
        </div>

        <!-- 关闭按钮 -->
        <button  @click="close">关闭</button>
      </div>
    </div>
  </template>

  <script>
  export default {
    props: {
      nodeData: {
        type: Object, //如果父组件传递的数据类型不是对象，Vue 会发出警告。
        default: () => ({}) //如果父组件没有传递 nodeData，子组件会使用一个空对象 {} 作为默认值。
      },
      sourceNode: {
        type: Object,
        default: () => ({})
     },
     targetNode: {
        type: Object,
        default: () => ({})
     }
    },
    data() {
      return {
        visible: true, // 控制模态框显示
        categories:["章","节","知识点"]
      };
    },
    methods: {
      close() {
        this.visible = false; // 关闭模态框
        this.$emit('close'); // 通知父组件关闭模态框
      }
    },
    created() {
        console.log('nodeData:', this.nodeData);
    },
  };
  </script>

<style scoped>
/* 整体模态框样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  max-width: 600px;
  width: 90%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  color:black;
}

/* 标题样式 */
.title {
  text-align: center;
  font-size: 18px;
  margin: 0;
}

/* 数据展示部分的网格样式 */
.custom-grid {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  color:black;
}

/* 左右两栏样式 */
.custom-grid-left, .custom-grid-right {
  width: calc(50% - 10px);
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 5px;
}

/* 每个数据项的样式 */
.list-item {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

/* 关闭按钮样式 */
button {
  background-color: skyblue;
  color: black;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

</style>
