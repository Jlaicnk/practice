<template>
    <div class="kg-homepage">
      <!-- 极简导航栏 -->


      <!-- 主内容区 -->
      <main class="main-content">
      <h1 class="main-title">知识图谱系统</h1>

        <!-- 功能特性 -->
        <section class="features">
          <h2 class="section-title">核心功能</h2>
          <div class="feature-grid">
            <div
              v-for="(feature, index) in features"
              :key="index"
              class="feature-card">
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.description }}</p>
            </div>
          </div>
        </section>
      </main>

      <!-- 极简页脚 -->
      <footer class="simple-footer">
        <div class="footer-links">
          <router-link
          v-for="(link, index) in footerLinks"
          :key="index"
          to="/sorry"
          class="footer-link">
          {{ link }}
        </router-link>
        </div>
        <p class="copyright">© 2025 知识图谱系统 | 项目测试界面</p>
      </footer>
    </div>
  </template>

  <script>
  export default {
    // name: 'TextOnlyHome',
    data() {
      return {
        navItems: [
          { title: '搜索', path: '/search' },
          { title: '智能问答', path: '/aianswer' },
          { title: '图谱浏览', path: '/explore' },
          { title: '数据统计', path: '/stats' }
        ],
        quickTags: [
          '人工智能', '量子计算', '基因编辑',
          '区块链', '元宇宙', '碳中和'
        ],
        features: [
          {
            title: '语义搜索',
            description: '支持自然语言的问题检索与解析'
          },
          {
            title: '知识推理',
            description: '基于逻辑规则的知识推导引擎'
          },
          {
            title: '动态可视化',
            description: '实时交互式图谱展示界面'
          },
          {
            title: '敬请期待',
            description: '-------敬请期待-------'
          },
        ],
        footerLinks: [
          '服务条款', '隐私政策', 'API文档', '联系我们'
        ]
      }
    },
    methods: {
      // handleSearch() {
      //   // 搜索逻辑
      // },
      // searchTag(tag) {
      //   // 标签搜索
      // }
    }
  }
  </script>

  <style scoped>
  .kg-homepage {
    font-family: system-ui, -apple-system, sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background-image: url('../public/background.jpg'); /* 请将 'your-background-image.jpg' 替换为你的背景图片实际路径 */
    background-size: cover; /* 背景图片覆盖整个元素 */
    background-position: center; /* 背景图片居中显示 */
    background-repeat: no-repeat; /* 防止背景图片重复 */
  }

  /* 极简导航样式 */
  .top-nav {
    background: #ffffff;
    border-bottom: 1px solid #e4e7ed;
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem;
  }

  ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    gap: 2rem;
  }

  .nav-link {
    color: #4a5568;
    text-decoration: none;
    font-weight: 500;
    padding: 0.5rem 0;
    position: relative;
    transition: color 0.2s;
  }

  .nav-link::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 2px;
    background: #3182ce;
    transition: width 0.3s;
  }

  .nav-link:hover {
    color: #3182ce;
  }

  .nav-link.active {
    color: #3182ce;
  }

  .nav-link.active::after {
    width: 100%;
  }

  /* 主内容区 */
  .hero-section {
    text-align: center;
    padding: 4rem 1rem;
    background: #f8fafc;
  }

  .main-title {
    font-size: 3rem;
    color: rgba(244, 247, 248);
    margin-bottom: 1.5rem;
    /* 添加其他样式，如加粗、阴影等 */
    font-weight: normal;
    text-shadow: 1px 1px 2px rgb(254, 248, 248);
    letter-spacing: 1.0rem; /* 增加字间距 */
  }


  .search-container {
    max-width: 800px;
    margin: 0 auto;
    display: flex;
    gap: 1rem;
    padding: 1rem;
  }

  .search-input {
    flex: 1;
    padding: 1rem;
    border: 2px solid #cbd5e0;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.2s;
  }

  .search-input:focus {
    border-color: #3182ce;
    outline: none;
  }

  .search-btn {
    background: #3182ce;
    color: white;
    border: none;
    padding: 0 2rem;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s;
  }

  .search-btn:hover {
    background: #2b6cb0;
  }

  .quick-tags {
    margin-top: 2rem;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
  }

  .tag {
    background: #edf2f7;
    color: #4a5568;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .tag:hover {
    background: #3182ce;
    color: white;
  }

  /* 功能区块 */
  .features {
    max-width: 1200px;
    margin: 4rem auto;
    padding: 0 1rem;
    font-size: 0.9rem;
  }
  h3{
    font-size: 1.3rem;
  }
  .section-title {
    text-align: center;
    color: rgba(255, 255, 255, 0.97);
    font-size: 2rem;
    margin-bottom: 3rem;
    font-weight: normal;
    filter: blur(0.5px); /* 增加模糊度 */
  }


  .feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
  }

  .feature-card {
    padding: 2rem;
    background: white;
    border-radius: 12px;
    line-height: 160px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s;
  }

  .feature-card:hover {
    transform: translateY(-4px);
  }

  .feature-card h3 {
    color: #3182ce;
    margin-bottom: 1rem;
  }

  /* 页脚 */
  .simple-footer {
    margin-top: auto; /* 确保页脚位于页面底部 */
    background: #1a202c; /* 深色背景 */
    color: white; /* 文字颜色为白色 */
    padding: 1.5rem 1rem; /* 减小页脚的内边距 */
    display: flex; /* 确保使用Flexbox布局 */
    flex-direction: column; /* 垂直方向排列 */
    align-items: center; /* 垂直居中对齐 */
    justify-content: flex-start; /* 改为从顶部开始排列，避免多余的垂直居中 */
  }

  .footer-links {
    display: flex; /* Flexbox布局 */
    justify-content: center; /* 链接水平居中 */
    gap: 1.5rem; /* 减小链接之间的间距 */
    margin-bottom: 0.8rem; /* 减小链接区域下方间距 */
  }

  .footer-link {
    font-size: 0.9rem; /* 减小链接字体大小 */
    line-height: 1; /* 减小链接的行高 */
    color: #cbd5e0; /* 浅色链接 */
    text-decoration: none; /* 去掉下划线 */
    transition: color 0.2s; /* 鼠标悬停时颜色变化 */
  }

  .footer-link:hover {
    color: #3182ce; /* 鼠标悬停时的链接颜色 */
  }

  .copyright {
    font-size: 0.8rem; /* 减小版权文字的字体大小 */
    line-height: 1; /* 减小版权文字的行高 */
    margin-top: 0.8rem; /* 减小版权区域上方间距 */
    text-align: center; /* 文字居中 */
    color: #718096; /* 更浅的颜色 */
  }



  /* 响应式设计 */
  @media (max-width: 768px) {
    .main-title {
      font-size: 2rem;
    }

    .search-container {
      flex-direction: column;
    }

    .search-btn {
      padding: 1rem;
    }

    ul {
      gap: 1rem;
      justify-content: center;
      flex-wrap: wrap;
    }
  }
  </style>