<template>
    <div class="under-development-container">
      <div class="content">
        <h1 class="title">项目该功能正在积极开发中</h1>
        <p class="description">感谢您的支持，我们将在不久的将来推出更多精彩内容！</p>
        <div class="loading-indicator">
          <div class="spinner"></div>
        </div>
        <p class="message">敬请期待！</p>
      </div>
    </div>
  </template>
<style scoped>
.under-development-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f0f0;
  font-family: 'Avenir', 'Helvetica', 'Arial', sans-serif;
}

.content {
  text-align: center;
  padding: 20px;
}

.title {
  font-size: 36px;
  color: #333;
  margin-bottom: 20px;
}

.description {
  font-size: 18px;
  color: #666;
  margin-bottom: 40px;
}

.loading-indicator {
  margin: 20px 0;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #ccc;
  border-top: 5px solid #3498db;
  border-radius: 50%;
  margin: 0 auto;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.message {
  font-size: 24px;
  color: #ff6b6b;
  font-weight: bold;
}
</style>
