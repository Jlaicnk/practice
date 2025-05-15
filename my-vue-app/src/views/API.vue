<template>
  <section class="recommendation-section">
    <h2 class="section-title">精选推荐</h2>
    <div class="recommendation-list">
      <div
        v-for="item in recommendations"
        :key="item.id"
        class="recommendation-item"
        @click="handleItemClick(item)"
      >
        <div class="item-content">
          <h3 class="item-title">{{ item.title }}</h3>
          <div class="category-tag">{{ item.category }}</div>
          <p class="item-desc">{{ item.description }}</p>
          <div class="item-meta">
            <span class="views">
              <i class="fas fa-eye"></i>
              {{ item.views.toLocaleString() }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref,onMounted } from 'vue'
import userApi from '../api/user'

// 模拟8条数据
const recommendations = ref([
  {
    id: 1,
    title: 'Vue3 高级技巧',
    description: '深入探讨Vue3的组合式API和性能优化，掌握Vue3的最新特性，打造更加健壮的应用，助你成为Vue3专家！',
    category: '前端开发',
    views: 2543,
  },
  {
    id: 2,
    title: 'TypeScript 入门指南',
    description: '从零开始学习TypeScript核心概念',
    category: '编程基础',
    views: 1896,
  },
  {
    id: 3,
    title: 'Node.js 实践指南',
    description: '构建高性能后端服务的最佳实践',
    category: '后端开发',
    views: 3245,
  },
  {
    id: 4,
    title: 'React 18 新特性',
    description: '探索React最新版本的核心更新',
    category: '前端开发',
    views: 1987,
  },
  {
    id: 5,
    title: 'Python 数据分析',
    description: '使用Python进行大数据处理与分析',
    category: '数据科学',
    views: 4321,
  },
  {
    id: 6,
    title: 'UI/UX 设计原则',
    description: '现代Web设计的基本原则与实践',
    category: '设计',
    views: 2876,
  },
  {
    id: 7,
    title: '云原生架构',
    description: '构建可扩展的云原生应用架构',
    category: '云计算',
    views: 3765,
  },
  {
    id: 8,
    title: '机器学习基础',
    description: '机器学习入门与实践指南',
    category: '人工智能',
    views: 4123,
  }
])

// 保持原有点击处理逻辑
const handleItemClick = (item) => {
  console.log('Clicked item:', item)
}

// 定义获取用户推荐的异步函数
const getUserRecommend = async () => {
  const user_id = userApi.getCurrentUserId();
  const response = await userApi.getUserRecommend(user_id);
  recommendations.value = response.recommendItems // 更新推荐数据
  console.log(response.recommendItems);
}

// 组件挂载后调用获取用户推荐的函数
onMounted(() => {
  getUserRecommend()
})

</script>

<style scoped>
/* 基础样式 */
.recommendation-section {
  max-width: 1440px;
  margin: 0 auto;
}

.section-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: #2c3e50;
  margin: -1rem;
  text-align: center;
  position: relative;
  padding: 40px;
}

/* 网格布局 */
.recommendation-list {
  display: grid;
  gap: 2rem;
  grid-template-columns: repeat(4, minmax(240px, 1fr));
  grid-auto-rows: minmax(360px, auto);
}

@media (max-width: 1200px) {
  .recommendation-list {
    grid-template-columns: repeat(2, minmax(300px, 1fr));
  }
}

@media (max-width: 768px) {
  .recommendation-list {
    grid-template-columns: 1fr;
  }
}

/* 卡片设计 */
.recommendation-item {
  background: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  display: flex;
  flex-direction: column;
}

.recommendation-item:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1);
}

/* 内容区域 */
.item-content {
  padding: 1.5rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.item-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.75rem;
  line-height: 1.3;
}

.item-desc {
  font-size: 0.9rem;
  color: #7f8c8d;
  line-height: 1.5;
  flex: 1;
  margin-bottom: 1rem;
  display: -webkit-box;  /* 针对 WebKit 浏览器 */
  display: box;          /* 标准属性（备用） */
  -webkit-line-clamp: 3; /* 针对 WebKit 浏览器 */
  line-clamp: 3;         /* 标准属性（未来支持兼容性） */
  -o-text-overflow: ellipsis; /* Opera 浏览器前缀 */
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 1rem;
}
/* 分类标签 */
.category-tag {
  font-size: 0.9rem; /* 设置分类标签的字体大小 */
  padding: 0.05rem 0.5rem; /* 进一步减少上下padding */
  border-radius: 2px; /* 减小边框圆角 */
  margin-bottom: 0.5rem;
  display: inline-block; /* 确保标签只占据所需的高度 */
}

/* 元信息 */
.item-meta {
  margin-top: auto;
  display: flex;
  align-items: center;
  font-size: 0.85rem;
  color: #95a5a6;
}

.fa-eye {
  margin-right: 6px;
  font-size: 0.9rem;
  color: #bdc3c7;
}

/* 交互增强 */
.recommendation-item:hover .item-title {
  color: #3498db;
}
</style>
