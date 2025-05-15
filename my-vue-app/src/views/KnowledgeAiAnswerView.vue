<template>
  <div class="container">
    <h1>🔍 问答</h1>
    <div class="input-section">
      <input
        v-model="question"
        @keyup.enter="submitQuestion"
        placeholder="输入您的问题，例如：变量是什么？"
        :disabled="isLoading"
      >
      <button @click="submitQuestion" :disabled="isLoading">
        <span v-if="isLoading" class="loading"></span>
        {{ isLoading ? '思考中...' : '开始提问' }}
      </button>
    </div>

    <div class="thinking-process" v-if="steps.length > 0">
      <h3 style="color: var(--primary-color); margin-bottom: 1rem;">推理过程 🧠</h3>
      <div v-for="(step, index) in steps" :key="index" class="step">
        {{ step }}
      </div>
    </div>

    <div class="answer" v-if="answer">
      <h3 style="color: var(--primary-color); margin-bottom: 1rem;">最终答案 ✅</h3>
      <p style="line-height: 1.6;">{{ answer }}</p>
    </div>
  </div>
</template>


<script>
import searchApi from '../api/search'
export default {
    data() {
        return {
            question: '',
            response: null,
            thinkingSteps: [],
            cypher: '',
            graph_data: [],
            rag_data: [],
            answer: '',
            steps: [],
            isLoading: false
        }
    },
    methods: {
        async getQuestion() {
            try {
                this.thinkingSteps = []; // 清空之前的推理步骤
                this.steps = []; // 清空之前的步骤数组

                this.steps.push("🔍 开始解析用户问题...");
                this.thinkingSteps.push(this.steps[this.steps.length - 1]);
                await new Promise(resolve => setTimeout(resolve, 800));

                const response = await searchApi.getAiAnswer(this.question);
                console.log("后端返回数据：", response);

                this.steps.push(`✨ 转换为Cypher语言：\n${response.cypher}`);
                this.cypher = response.cypher;
                this.thinkingSteps.push(this.steps[this.steps.length - 1]);
                await new Promise(resolve => setTimeout(resolve, 800));

                this.steps.push("🌐 连接知识图谱...");
                this.thinkingSteps.push(this.steps[this.steps.length - 1]);
                await new Promise(resolve => setTimeout(resolve, 800));

                const graphDataSteps = [
                    "📅 搜索到的相关节点：", // 提示文本
                    ...response.graph_data
                    .filter(node => node.name || node.desc)
                    .map((node,index) => `${index+1}、${node.name || ''}  ${node.desc || ''}`) // 每个节点的描述内容
                  ].join('\n'); // 使用换行符拼接
                this.steps.push(graphDataSteps);
                this.graph_data = response.graph_data;
                this.thinkingSteps.push(this.steps[this.steps.length - 1]);
                await new Promise(resolve => setTimeout(resolve, 800));

                const ragDataSteps = [
                  "🪐 与文字数据库进行词向量匹配：",
                  ...response.rag_data.map((node,index) => `${index+1}、${node || '无描述'}`)
                ].join('\n');
                this.steps.push(ragDataSteps);
                this.rag_data = response.rag_data;
                console.log("ragdata：", this.rag_data);
                this.thinkingSteps.push(this.steps[this.steps.length - 1]);
                await new Promise(resolve => setTimeout(resolve, 800));

                this.steps.push("🧮 整合多源数据验证");
                this.thinkingSteps.push(this.steps[this.steps.length - 1]);
                await new Promise(resolve => setTimeout(resolve, 800));

                this.steps.push("✅ 生成最终结论");
                this.answer = response.qa_answer;
                console.log("steps:", this.steps);
                this.thinkingSteps.push(this.steps[this.steps.length - 1]);
                await new Promise(resolve => setTimeout(resolve, 800));
            } catch (error) {
                console.error("获取AI问答结果错误:", error); // 处理可能的错误
                this.isLoading = false; // 确保在发生错误时关闭加载状态
            }
        },
        async submitQuestion() {
            if (!this.question.trim() || this.isLoading) return;
            this.answer = '';
            this.isLoading = true;
            await this.getQuestion();
            this.isLoading = false;
        }
    }
}
</script>

<style scoped>
/* 移除 :root 定义，因为它不会生效在 scoped 样式中 */
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

h1 {
  text-align: center;
  color: #1a1a1a;
  margin-bottom: 2rem;
  font-weight: 600;
  font-size: 2.2rem;
}

.input-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  position: relative;
}

input {
  flex: 1;
  padding: 1rem 1.5rem;
  border: 2px solid #e0e0e0;
  border-radius: 2rem;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: var(--card-bg);
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 4px rgba(23,100,255,0.1);
}

button {
  padding: 0.8rem 2rem;
  background: var(--gradient);
  color: white; /* 修改为白色以匹配背景 */
  border: none;
  border-radius: 2rem;
  cursor: pointer;
  font-weight: 500;
  transition: transform 0.2s, opacity 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

button:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.thinking-process {
  background: var(--card-bg);
  border-radius: 1rem;
  padding: 1.5rem;
  margin: 1.5rem 0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  border: 1px solid rgba(0,0,0,0.05);
}

.answer {
  background: var(--card-bg);
  border-radius: 1rem;
  padding: 1.5rem;
  margin: 1.5rem 0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  animation: fadeIn 0.5s ease;
}

.step {
  padding: 0.8rem;
  margin: 0.5rem 0;
  background: rgba(23,100,255,0.05);
  border-radius: 0.5rem;
  color: #1a1a1a;
  animation: slideIn 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  white-space: pre-wrap; /* 确保换行符生效 */
  text-align: left;
}

.step::before {
  content: "•";
  color: var(--primary-color);
  font-weight: bold;
  font-size: 1.2rem;
}

.loading {
  width: 1.5rem;
  height: 1.5rem;
  border: 3px solid rgba(255,255,255,0.2);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
  from { opacity: 0; transform: translateX(20px); }
  to { opacity: 1; transform: translateX(0); }
}

@media (max-width: 768px) {
  .container {
    padding: 1rem;
  }

  input {
    padding: 0.8rem 1.2rem;
  }

  button {
    padding: 0.8rem 1.5rem;
  }
}
  pre {
    white-space: pre-wrap; /* 确保换行符生效 */
  }
</style>

<style>
/* 全局样式定义 :root 变量 */
:root {
  --primary-color: #1764FF;
  --gradient: linear-gradient(135deg, #1764FF 0%, #4285F4 100%);
  --bg-color: #FAFCFF;
  --card-bg: #ffffff;
}

body {
  background: var(--bg-color);
  min-height: 100vh;
}
</style>