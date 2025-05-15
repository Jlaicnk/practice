<template>
  <div v-if="visible" class="modal">
    <div class="modal-content">
      <div class="favorite-container">
        <svg class="icon" :class="{favorited: isFavorited}" aria-hidden="true" @click="toggleFavorite">
          <use :xlink:href="isFavorited ? '#icon-yishoucang' : '#icon-shoucang1'"></use>
        </svg>
        <span class="favorite-text" @click="toggleFavorite">点击{{isFavorited ? '取消' : '收藏'}}</span>
      </div>
      <h2 class="title">{{ nodeData.name }}</h2>
      <div class="custom-list">
        <el-row class="list-item" gutter="20">
          <el-col :span="4" class="header">标签</el-col>
          <el-col :span="20" class="content">{{ categories[nodeData.category] || "null" }}</el-col>
        </el-row>

        <el-row class="list-item" gutter="20">
          <el-col :span="4" class="header">描述</el-col>
          <el-col :span="20" class="content">{{ nodeData.desc || "null" }}</el-col>
        </el-row>
      </div>
      <button @click="close">关闭</button>
    </div>
  </div>
</template>

<script>
import userApi from '../api/user'

export default {
  props: {
    nodeData: {
      type: Object,
      default: () => ({}) // 如果父组件没有传递 nodeData，默认为空对象 {}。
    },
    entity_dict: {
      type: Object,
      default: () => ({}) // 如果父组件没有传递 entity_dict，默认为空对象 {}。
    },
    user_id: {
      type: Number, // 指定为 Number 类型
      default: 0,   // 默认值为 0
    }
  },
  data() {
    return {
      visible: true, // 控制模态框显示
      categories: ['章', '节', '知识点'],
      isFavorited: this.entity_dict[this.nodeData.name] || false, // 收藏状态，初始化为未收藏
      user_preferences: null,
    };
  },
  methods: {
    close() {
      this.visible = false; // 关闭模态框
      this.$emit('close'); // 通知父组件关闭模态框
      console.log("entity_dict:", this.entity_dict);
    },
    toggleFavorite() {
      // 切换收藏状态
      this.isFavorited = !this.isFavorited;
      this.entity_dict[this.nodeData.name] = this.isFavorited;
      // 模拟后端交互（例如发送请求）
      console.log(`收藏状态已更新：${this.isFavorited}`);
      this.user_preferences = this.preInit();
      userApi.alterUserPreferences(this.user_id, this.user_preferences);
      console.log("收藏组件返回用户偏好信息：", this.user_preferences);
      // 通知父组件收藏状态已改变
      this.$emit('favorite', this.nodeData, this.isFavorited);
    },
    preInit() {
      return Object.keys(this.entity_dict).filter(key => this.entity_dict[key] === true);
    },
  }
};
</script>

<style scoped>
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
  color: black;
}

/* 收藏图标样式 */
.icon {
  margin-top: 0;
  cursor: pointer;
  font-size: 20px;
}

.favorited {
  color: red; /* 已收藏时图标颜色 */
}

/* 收藏文字样式 */
.favorite-text {
  margin-left: 10px;
  font-size: 14px;
  cursor: pointer;
}

.favorite-container {
  display: flex;
  align-items: center;
  justify-content: right; /* 使收藏图标和文字居中 */
}

/* 标题样式 */
.title {
  text-align: center;
  font-size: 18px;
  margin: 0;
}

.custom-list {
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 5px;
}

.list-item {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.header {
  padding: 10px;
  color: black;
  text-align: center;
}

.content {
  padding: 10px;
  color: black;
}

button {
  background-color: skyblue;
  color: black;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}
</style>
