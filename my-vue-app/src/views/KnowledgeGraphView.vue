<template>
  <div>
    <!-- 引入表单组件，并监听其update-data事件以更新数据 -->
    <FormComponent @update-data="updateData" />
    <!-- 定义一个div作为echarts图表的容器，设置高度为800px -->
    <div id="main" style="height: 800px;"></div>
    <!-- 根据visible的值决定是否显示知识窗口组件，并传递nodeData给它，同时监听close事件以关闭模态框 -->
    <KnowledgeNodeWindow v-if="visible&& windowStyle === 'style1'" :nodeData="selectedNode"  :entity_dict="entity_dict" :user_id="user_id" @close="closeModal" />
    <KnowledgeRelWindow v-if="visible&& windowStyle === 'style2'" :nodeData="selectedNode" :sourceNode="sourceNode"
     :targetNode="targetNode" @close="closeModal" />
  </div>
</template>

<script>
// 导入组件
import FormComponent from '../components/FormComponent.vue';
import KnowledgeNodeWindow from '../components/KnowledgeNodeWindow.vue'
import KnowledgeRelWindow from '../components/KnowledgeRelWindow.vue'
// 引入echarts库
import * as echarts from 'echarts';

export default {
  components: {
    FormComponent,
    KnowledgeNodeWindow,
    KnowledgeRelWindow
  },
  data() {
    return {
      chart: null, // 存储echarts实例
      chartData: null, // 存储图表数据
      visible: false, // 控制模态框的显示与隐藏
      windowStyle: 'style1', // 默认显示第一个样式的知识窗口
      selectedNode: null, // 存储点击的节点数据
      sourceNode:null,
      targetNode:null,
      entity_dict:null,
      user_preferences:null,
      user_id:0
    };
  },
  mounted() {
    // 在组件挂载后初始化图表
    this.initChart();
  },

  methods: {
    // 初始化图表的方法
    initChart() {
      // 通过echarts.init方法创建图表实例，并绑定到id为'main'的div上
      this.chart = echarts.init(document.getElementById('main'));
    },

    // 更新数据的方法，接收来自FormComponent的数据
    updateData(data) {
      // 如果接收到的数据是字符串类型，则将其解析为JSON对象
      if (typeof data === 'string') {
        this.chartData = JSON.parse(data);
      } else {
        this.chartData = data;
      }
      // 输出数据类型到控制台
      console.log(typeof(data));
      // 输出解析后的图表数据到控制台
      console.log("updateData：",this.chartData);
      // 调用renderChart方法渲染图表
      this.renderChart();
    },

    // 渲染图表的方法
    renderChart() {
      // 如果没有图表数据则直接返回
      if (!this.chartData) return;

      // 定义图表的类别
      const categories = [{ name: "章" }, { name: "节" }, { name: "知识点" }];
      //解构两个回应

      // 解构图表数据中的data和links
      this.user_id = this.chartData.currentUserId;
      console.log("currentUserId",this.user_id);
      const {data, links ,entity_dict} = JSON.parse(this.chartData.response1);
      console.log("图表data数据：",data);
      console.log("图表links数据：",links);
      console.log("图表entity_dict数据：",entity_dict);
      this.entity_dict = entity_dict;
      const {preferences} = this.chartData.response2;
      this.user_preferences = preferences
      console.log("///////////////////:",this.user_preferences);
      this.endictInit();
      // 输出数据类型到控制台
      // console.log("------------------------",this.chartData);


      // 定义图表的配置项
      const option = {
        // 图表的标题部分
        title: {
            text: '知识图谱搜索结果' // 标题文本内容
        },
        // 提示框的设置
        tooltip: {
            // 设置提示框的内容格式，这里显示的是节点的描述信息
            formatter: function (x) {
                return x.data.des; // 鼠标悬停时显示的数据格式
            },
        },
        // 工具箱的设置
        toolbox: {
            show: true, // 显示工具箱
            feature: {
                mark: { show: true }, // 显示标记工具
                restore: { show: true }, // 显示还原工具
                saveAsImage: { show: true } // 显示保存为图片的工具
            }
        },
        // 图例的设置
        legend: [{
            // 图例的数据来源于分类名称
            data: categories.map(a => a.name)
        }],
        // 系列的设置
        series: [{
            type: 'graph', // 类型:关系图
            layout: 'force', // 图的布局，类型为力导图
            roam: true, // 是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移,可以设置成 'scale' 或者 'move'。设置成 true 为都开启
            edgeSymbol: ['circle', 'arrow'], // 边两端的符号， ['circle', 'arrow'] 表示开头为圆点，结尾为箭头
            edgeSymbolSize: [2, 10], // 边两端符号的大小
            edgeLabel: {
                normal: {
                    // 边标签的文字样式
                    textStyle: {
                        fontSize: 20
                    }
                }
            },
            force: {
                repulsion: 2500, // 节点之间的斥力大小
                edgeLength: [10, 50], // 边的长度
                layoutAnimation: true // 是否显示布局动画
            },
            draggable: true, // 节点是否可被拖拽
            lineStyle: {
                normal: {
                    width: 2, // 边的宽度
                    color: '#4b565b', // 边的颜色
                }
            },
            edgeLabel: {
                normal: {
                    show: false, // 默认情况下不显示边标签
                    textStyle: {
                      fontSize: 20 // 边标签的文字大小
                    },
                },
            },
            label: {
                normal: {
                    show: true, // 默认情况下显示节点标签
                    textStyle: {} // 节点标签的文字样式
                },
                emphasis: {
                  show: true, // 鼠标悬停时显示标签
                  position: 'right', // 标签位置
                  textStyle: {
                      color: '#333' // 标签文字颜色
                  }
                }
            },
            emphasis: {
                focus: 'adjacent', // 只显示与当前节点相邻的节点和边
                lineStyle: {
                    width: 4, // 突出显示连接线
                    color: '#333' // 突出显示连接线的颜色
                },
                edgeLabel: {
                      show: true, // 鼠标悬停时显示边标签
                      formatter: function (x) {
                          return x.data.name; // 边标签显示关系名称
                      }
                    },
            },
            // 数据部分
            data: data, // 节点数据
            links: links, // 定义节点之间的关系
            categories: categories, // 给类别赋值
        }],
        // 监听图表的点击事件，当点击节点时，显示知识窗口
        // click: (x) => {
        //   // 检查点击的元素是否有data属性
        //   if (x.data) {
        //     // 将点击的节点数据存储到selectedNode
        //     this.selectedNode = x.data;
        //     console.log(this.selectedNode); // 输出选中的节点数据
        //     this.visible = true; // 显示知识窗口
        //   }
        // }
      };
      // 将图表配置项设置到echarts实例中
      this.chart.setOption(option);

      // 监听图表的点击事件
      this.chart.on("click", (x) => {
        // 检查点击的元素是否有data属性
        if (x.dataType === 'node' && x.data) {
          // 将点击的节点数据存储到selectedNode
          this.selectedNode = x.data;
          this.windowStyle = "style1";
          // console.log("++++++++++++++++++++++",x);
          // console.log(this.selectedNode); // 输出选中的节点数据
          this.visible = true; // 显示知识窗口
        }
        else if (x.dataType === 'edge' && x.data){
          this.selectedNode = x.data;
          const sourceNodeName = x.data.source;
          this.sourceNode = data.find(node => node.name === sourceNodeName);
          const targetNodeName = x.data.target;
          this.targetNode = data.find(node => node.name === targetNodeName);
          this.windowStyle = "style2";
          // console.log(this.selectedNode); // 输出选中的节点数据
          this.visible = true; // 显示知识窗口
        }
      });
    },
    endictInit(){
      Object.values(this.user_preferences).forEach(value => {
        console.log(value); // 输出值
        this.entity_dict[value] = true;
      });
      console.log(this.entity_dict);
    },
    // 关闭模态框的方法
    closeModal() {
        this.visible = false; // 设置visible为false以隐藏知识窗口
    },
  },
};
</script>
