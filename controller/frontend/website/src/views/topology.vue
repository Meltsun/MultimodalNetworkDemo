<template>
  <div class="layout">
    <div class="Header">
      <span style="font-size: 30px; color: #fff; font-weight: bold; margin-left: 20px;background-color: #003377; ">
      多模态网络系统</span>
      <div class="custom-divider"></div>
    </div>
    <div class="container">
      <div>
      <div class="charts-container">
        <div class="chart-container">
          <div class="chart">
          <i class="el-icon-set-up" style="font-size:16px; color: #0044BB;margin-left: 10px;margin-top:10px;"></i>
          <span style="font-size:16px; color: #0044BB;">网络拓扑展示:</span>
        <div id="chartsBox">
        </div>
          </div>
        </div>
      <div class="danxuan">
        <div class="tabel">
          <div class="tabel1-container">
            <div>
              <el-button  icon="el-icon-document" style="font-size:7px; background-color: white; border-radius:90%; 
              color:#0044BB; margin-left: 5px;margin-top: 5px;" circle >
              </el-button>
              <span style="font-size:15px; color: #0044BB;">场景一</span>
            </div>
            <div class="tabel1">
              <div class="tabel11">
                <span style="font-size:15px; color: #0044BB;margin-left: 5px;">视频一:</span>
              </div>
              <div class="an1">
                <el-radio v-model="radio" label="1">ENCC</el-radio>
              </div>
            </div>
            <div class="tabel2">
              <div class="tabel12">
                <span style="font-size:15px; color: #0044BB;margin-left: 5px;">视频二:</span>
              </div>
              <div class="an2">
                <el-radio v-model="radio" label="2">QUIC</el-radio>
                <el-radio v-model="radio" label="3">WebRTC</el-radio>
                <el-radio v-model="radio" label="4">BBR</el-radio>
              </div>
            </div>
            <el-row>
              <el-button :plain="true"  @click=" handleSubmit" style="font-size:15px; width: 110px;height:35px;
               background-color:#003377; color:#fff; border-radius:8px;margin-left:120px;margin-top: 3px;">协议部署</el-button>
            </el-row>
        </div>
      <div class="tabel2-container">
          <div>
            <el-button  icon="el-icon-document" style="font-size:7px; background-color: white; border-radius:80%; 
            color:#0044BB; margin-left: 5px;margin-top: 5px;" circle >
            </el-button>
            <span style="font-size:15px; color:#0044BB;">场景二</span>
            </div>
            <div class="tabel3">
            <div class="tabel21">
              <span style="font-size:15px; color: #0044BB;margin-left: 5px;margin-top: 5px;">视频一:</span>
            </div>
            <div class="an3">
              <el-radio v-model="radio" label="5">ENCC</el-radio>
            </div>
          </div>
          <div class="tabel4">
            <div class="tabel22">
              <span style="font-size:15px; color: #0044BB;margin-left: 5px;">视频二:</span>
            </div>
            <div class="an4">
              <el-radio v-model="radio" label="6">QUIC</el-radio>
              <el-radio v-model="radio" label="7">WebRTC</el-radio>
              <el-radio v-model="radio" label="8">BBR</el-radio>
            </div>
          </div>
          <el-row>
        <el-button :plain="true" @click="handleSubmit" style="font-size:15px; width: 110px;height:35px; 
        background-color:#003377; color:#fff; border-radius:8px;margin-left:120px;margin-top: 3px;">协议部署</el-button>
      </el-row>
        </div>
        </div>
      </div>
      </div>
      <div class="danxuan-container">
        <div>
          <el-button  icon="el-icon-document" style="font-size:10px; background-color: gold; border-radius:80%;
          margin-left:20px;margin-top:10px;" circle ></el-button>
          <span style="font-size:15px; color: #000;font-weight: bold;">状态展示</span>
        </div>
        <div class="newcharts">
          <div id="charts1" class="canvas"></div>
          <div id="charts2" class="canvas"></div>
        </div>
      </div>
    </div>
      <div class="tabel-container">
      <div class="toggle-buttons">
        <div class="toggle">
        <el-button  icon="el-icon-document" style="font-size:15px; background-color: gold; border-radius:80%;" circle >
        </el-button>
        <span style="font-size:18px; color: #000;font-weight: bold;">百万级链接调控</span>
        </div>
        <div class="buttons">
        <el-row>
          <el-button @click="increaseBackgroundFlow"  icon="el-icon-document" style="font-size:18px; width: 170px;height:55px;
            background-color:#003377; color:#fff; border-radius:8px;">加大活跃流</el-button>
          <el-button @click="decreaseBackgroundFlow" icon="el-icon-document" style="font-size:18px; width: 170px;height:55px;
            background-color:#003377; color:#fff; margin-left:60px; border-radius:8px;">缩小活跃流</el-button>
        </el-row>
        </div>
      </div>
      <div class="tabs-container">
        <div>
        <el-button  icon="el-icon-document" style="font-size:15px; background-color: gold; border-radius:80%;margin-left:20px;
        margin-top:20px;" circle ></el-button>
        <span style="font-size:18px; color: #000;font-weight: bold;">数据展示</span>
        </div>
        <div class="tab">
          <el-tabs v-model="activeTab" @tab-click="handleTabClick">
          <el-tab-pane label="百万级链接信息" name="background"></el-tab-pane>
          <el-tab-pane label="测试结果分析" name="protocols"></el-tab-pane>
          <el-tab-pane label="历史数据" name="historyProtocols"></el-tab-pane>
          </el-tabs>
        </div>
  <div class="tab-container">
    <div v-if="activeTab === 'background'" class="table-container">
      <div class="table-wrapper1">
    <el-table show-summary border  :data="backgroundTableData" stripe>
      <!-- "查看背景流"标签对应的表格列 -->
      <el-table-column prop="communication_terminal1" label="通信端1">
      </el-table-column>
      <el-table-column prop="communication_terminal2" label="通信端2">
      </el-table-column>
      <el-table-column prop="active_connections" label="活跃连接数">
      </el-table-column>
      <el-table-column prop="sleep_connections" label="休眠连接数">
      </el-table-column>
      <el-table-column prop="total_connections" label="总连接数">
      </el-table-column>
    </el-table>
    </div>
    </div>
    <div v-if="activeTab === 'protocols'" class="table-container">
      <div class="table-wrapper2">
      <el-table class="custom-table" border show-summary:false :data="protocolsTableData"  stripe>
      <!-- "展示各协议组合标签"标签对应的表格列 -->
      <el-table-column prop="state" label="阶段" width="75">
      <template slot-scope="scope">
        <div class="state"> {{ scope.row.state}}</div>
      </template>
    </el-table-column>
    <el-table-column prop="create_time" label="时间" width="88">
      <template slot-scope="scope">
        <div class="create_time">{{ scope.row.create_time}}</div>
      </template>
    </el-table-column>
    <el-table-column prop="protocol" label="协议" width="86">
      <template slot-scope="scope">
        <div class="custom-protocol">{{ scope.row.protocol}}</div>
      </template>
    </el-table-column>
    <el-table-column label="像素" width="87">
      <template slot-scope="scope">
        <div class="custom-protocol2">{{ scope.row.resolution_width}} × {{scope.row.resolution_height}}</div>
      </template>
    </el-table-column>
    <el-table-column prop="congestion_rate" label="卡顿率(%)" width="109">
      <template slot-scope="scope">
        <div class="custom-protocol3">{{ scope.row.congestion_rate }}
          <span v-if="parseInt(scope.row.congestion_rate_compare) > 0" 
            :style="{ color: 'blue' , 'font-weight': 'bold' }">
            (相比 {{ scope.row.protocol}}降低:{{ scope.row.congestion_rate_compare }})
          </span>
        </div>
      </template>
    </el-table-column>
    <el-table-column prop="tail_delay" label="尾时延(s)" width="109">
      <template slot-scope="scope">
        <div class="custom-protocol3">
          {{ scope.row.tail_delay }}
          <span v-if="parseInt(scope.row.tail_delay_compare) > 0" 
            :style="{ color:'blue', 'font-weight': 'bold' }">
            (相比 {{ scope.row.protocol}}降低:{{ scope.row.tail_delay_compare }})
          </span>
        </div>
      </template>
    </el-table-column>
    </el-table>
  </div>
    </div>
  <div v-if="activeTab === 'historyProtocols'" class="table-container">
    <div class="table-wrapper3">
      <el-table class="custom-table"  border :data="historyTableData" stripe>
      <!-- "展示各协议组合标签"标签对应的表格列 -->
      <el-table-column prop="state" label="阶段" width="75">
      <template slot-scope="scope">
        <div class="state"> {{ scope.row.state}}</div>
      </template>
    </el-table-column>
    <el-table-column prop="create_time" label="时间" width="88">
      <template slot-scope="scope">
        <div class="create_time">{{ scope.row.create_time}}</div>
      </template>
    </el-table-column>
      <el-table-column prop="protocol" label="协议" width="86">
      <template slot-scope="scope">
        <div class="custom-protocol">{{ scope.row.protocol}}</div>
      </template>
    </el-table-column>
    <el-table-column label="像素" width="87">
      <template slot-scope="scope">
        <div class="custom-protocol2"> {{ scope.row.resolution_width}} × {{scope.row.resolution_height}}</div>
    </template>
    </el-table-column>
    <el-table-column prop="congestion_rate" label="卡顿率(%)" width="109">
    </el-table-column>
    <el-table-column prop="tail_delay" label="尾时延(s)" width="109">
    </el-table-column>
    </el-table>
    </div>
  </div>
  </div>
 </div>
</div>
</div>
</div>
</template>
  
  <script>
  import * as echarts from 'echarts';
  import Host from "@/assets/img/host.png"
  import Server from "@/assets/img/server.png"
  import Switch from "@/assets/img/switch.png"
  export default {
    data() {
    return {
      myChart:null,
      nodes: [], // 从后端获取的节点数据
      links: [], // 从后端获取的链接数据
      tableData: [
      { selected: ''},
    ],
      radio: '', // 场景一的视频一单选项选择值
      activeTab: 'protocols', // 设置默认活动标签
      backgroundTableData: [], // "查看背景流"标签的表格数据
      protocolsTableData: [], // "展示各协议组合标签"标签的表格数据
      historyTableData: [],
      tooltipContent: '',
      linkIds: [],
      timer: null, // 用于自动数据获取的计时器
    };
  },
  mounted() {
    this.fetchData();
    this.startAutoRefresh();
    this.fetchTableDataAndDrawChart();
  },
  beforeDestroy() {
    this.stopAutoRefresh();
  },
  methods:{
    fetchData() {
    this.$fetch('topology')
      .then(data => {
        console.log(data);
        this.nodes = data.nodes;
        this.links = data.links.map(link => ({
        id:link.id,
        source: link.from,
        target: link.to,
    }));
        console.log(this.nodes);
        console.log(this.links);
        this.initChart(); // 调用初始化方法绘制关系图
      })
      .catch(error => {
        console.error('Error:', error);
      });
  },
    startAutoRefresh() {
      this.timer = setInterval(() => {
        this.fetchHighDelayLinkData();
      }, 10000); // 每10秒刷新一次
    },
    stopAutoRefresh() {
      clearInterval(this.timer);
    },
    fetchHighDelayLinkData() {
      this.$fetch('high-delay-link')
        .then(data => {
          console.log(data);
          const newLinkIds = data.map(item => item.link_id);//.topology
          console.log(newLinkIds);
          if (this.linkIds.toString() !== newLinkIds.toString()) {
            this.linkIds = newLinkIds;
            this.updateChart();
          }
        })
        .catch(error => {
          console.error('错误:', error);
        });
    },
    readNodes(type) {
        if (type == 'switch') {
          return 'image://' + Switch; 
        } else if(type == 'host'){
          return 'image://' + Host;
        }
        else {
          return 'image://' + Server;
        }
      },
    initChart() {
        const chartDom = document.getElementById('chartsBox');
        this.myChart = echarts.init(chartDom);//const
        const option = {
          grid: {
            left: '5%',    // 绘图区域距离容器左边的距离
            top: '10%',     // 绘图区域距离容器上边的距离
            right: '5%',   // 绘图区域距离容器右边的距离
            bottom: '10%',  // 绘图区域距离容器下边的距离
            containLabel: true  // 包含坐标轴标签的内容，默认为 false
        },
          tooltip: {
            show:true,
            enterable: true, // 设置为可进入状态
            triggerOn: "click", 
            confine: true, // 是否将 tooltip 框限制在图表的区域内
            backgroundColor: '#EEF1F7',
            borderColor: '#EEF1F7',
            borderWidth: 1,
            textStyle: {
              width: 160,
              height: 250,
              lineHeight: 24,
              color: '#003377',
              fontSize: '14',
              fontFamily: 'SourceHanSansCN-Normal'
            },
          formatter: () => {
             return this.tooltipContent; // 返回节点信息作为工具提示内容
            },
        },
          series: [
            {
              type: 'graph',
              data: this.nodes.map((node) => {
              const { x, y } = this.calculateCoordinatesById(node.id);
              return {
                ...node,
                symbolSize:35,
                symbol: this.readNodes(node.type),
                 x, 
                 y, 
                 label: {
                  show: true,
                  position: 'bottom',
                  formatter: (params) => {
                  const { labelContent, nodename } = this.calculatelabelContentById(node.id);
                 return  `${nodename} ${labelContent}`;
                },
                   color: '#000',
                   fontSize: 12,
              },
              }
            }),
            links: this.links.map((link) => {
            const linkId = link.id;
            const lineStyle = {
                color: this.linkIds.includes(linkId) ? 'red' : '#1b3c89',
                width: this.linkIds.includes(linkId) ?3 : 1,
              };
            return {
              ...link,
              lineStyle,
            };
              }),
            },
          ],
        };
      this.myChart.setOption(option);//this
      this.myChart.on('click', (params) => {
      const bulletPoint = '● '; // 小圆点
      if (params.dataType === 'node') {
        const dataIndex = params.dataIndex;
        const node = this.nodes[dataIndex];
        const id = node.id;
        const type = node.type;
      if (type === 'switch') {
        // 发送请求获取交换机节点信息
        this.$fetch(`node/${id}`)
          .then((nodeInfo) => {
            // 根据节点信息执行其他操作
            console.log(nodeInfo);
            this.tooltipContent =  `
              ${bulletPoint} ID:    ${id}<br>
              ${bulletPoint} Name:  ${nodeInfo.name}<br>
              ${bulletPoint} Type:  ${nodeInfo.type}<br>
              ${bulletPoint} IP:    ${nodeInfo.ip}
            `
          })
          .catch((error) => {
            console.error('Error:', error);
          });
      } else if (type === 'host') {
        this.$fetch(`node/${id}`)
          .then((nodeInfo) => {
            this.tooltipContent = `
            ${bulletPoint} Name: ${nodeInfo.name}<br>
            ${bulletPoint} IP: ${nodeInfo.ip}`;
          })
          .catch((error) => {
            console.error('Error:', error);
          });
      }
    } else if (params.dataType === 'edge') {
      const dataIndex = params.dataIndex;
      const link = this.links[dataIndex];
      const id = link.id;
      console.log(id);
      // 发送请求获取链接信息
      this.$fetch(`link/${id}`)
        .then((linkInfo) => {
          const linkInfo1=linkInfo[0];  //！！！改
          const linkInfo2=linkInfo[1];  //！！！改
          console.log(linkInfo)
          const minDelay = Math.min(linkInfo1.delay, linkInfo2.delay);
          const minLost = Math.min(linkInfo1.lost, linkInfo2.lost);
          const sumRate = linkInfo1.rate + linkInfo2.rate;
          const minDelay2 = minDelay.toFixed(3);
          const minLost2 = minLost.toFixed(3);
          const sumRate2 = sumRate.toFixed(3);
          if (linkInfo1) {
            this.tooltipContent = 
            `${bulletPoint} link_id:${linkInfo1.link_id}<br>
            ${bulletPoint}  rate: ${sumRate2}<br>
            ${bulletPoint}  delay: ${minDelay2}ms<br>
            ${bulletPoint}  lost:${minLost2}
            `;
          }
        })
        .catch((error) => {
          console.error('Error:', error);
        });
      }
   });
  },
    updateChart() {
      const option = {
        series: [
          {
            links: this.links.map((link) => {
              const linkId = link.id;
              const lineStyle = {
                color: this.linkIds.includes(linkId) ? 'red' : '#1b3c89',
                width: this.linkIds.includes(linkId) ? 3 : 1,
              };
              return {
                ...link,
                lineStyle,
              };
            }),
          },
        ],
      };
      this.myChart.setOption(option); // 使用 setOption 方法更新图表
    },
    calculateCoordinatesById(nodeId) {
    let x, y;
    switch (nodeId) {
      case 176:
        x=-450;
        y= 450;
        break;
      case 182:
        x = -200;
        y = 300;
        break;
      case 184:
        x = 150;
        y = 300;
        break;
      case 178:
        x = 450;
        y = 450;
        break;
      case 188:
        x = 150;
        y = 600;
        break;
      case 186:
        x = -200;
        y = 600;
        break;
      case 170:
        x = -600;
        y = 600;
        break;
      case 180:
        x =600;
        y = 600;
        break;
      case 172:
        x = -480;
        y =250;
        break;
      case 162:
        x = -250;
        y = 100;
        break;
      case 164:
        x = 180;
        y = 100;
        break;
      case 174:
        x = 480;
        y = 250;
        break;
      case 166:
        x = -270;
        y =750;
        break;
      case 168:
        x =180;
        y =750;
        break;
      default:
        x =0;
        y =0;
        break;
    }
    return { x, y };
    },
    calculatelabelContentById(nodeId) {
    let labelContent,nodename;
    switch (nodeId) {
      case 176:
      labelContent='175/176';
      nodename='西安';
        break;
      case 182:
      labelContent='10.162.162.1';
      nodename='北京';
        break;
      case 184:
      labelContent='10.164.164.1';
      nodename='南京';
        break;
      case 178:
      labelContent='10.174.174.1';
      nodename='上海';
        break;
      case 188:
      labelContent='10.168.168.1';
      nodename='深圳';
        break;
      case 186:
      labelContent='10.166.166.1';
      nodename='重庆';
        break;
      case 170:
      labelContent='10.170.170.2';
      nodename='';
        break;
      case 180:
      labelContent='10.180.180.2';
      nodename='';
        break;
      case 172:
      labelContent='10.172.172.2';
      nodename='';
        break;
      case 162:
      labelContent='10.162.162.2';
      nodename='';
        break;
      case 164:
      labelContent='10.164.164.2';
      nodename='';
        break;
      case 174:
      labelContent='10.174.174.2';
      nodename='';
        break;
      case 166:
      labelContent='10.166.166.2';
      nodename='';
        break;
      case 168:
      labelContent='10.168.168.2';
      nodename='';
        break;
      default:
      labelContent='';
        break;
    }
    return{
      labelContent,
      nodename
    }
    },
    increaseBackgroundFlow() {
     this.$fetch('StartFileReq')
        .then(data => {
        console.log(data);
        this.backgroundTableData = data;
      })
        .catch(error => {
          console.error(error);
        });
    },
    decreaseBackgroundFlow(){
      this.$fetch('StopFileReq')
        .then(data => {
        console.log(data);
        this.backgroundTableData = data;
      })
        .catch(error => {
          console.error(error);
        });
    },
    handleTabClick(tab) {
      this.timer = setInterval(() => {
        this.fetchbackgroundTableData();
      }, 10000); // 每10秒刷新一次
      const tabName = tab.name;
      if (tabName === 'background') {
        this.fetchbackgroundTableData();
      } else if (tabName === 'protocols') {
        this.fetchTableDataAndDrawChart();
        }else if (tabName === 'historyProtocols') {
        this.fetchHistoryTableData();
        }
    },
    fetchHistoryTableData(){
      this.$fetch('NetworkPerformance/history')
          .then(data => {
          console.log(data);
          this.historyTableData = data.data;
        })
    },
    fetchTableDataAndDrawChart() {
      this.$fetch(`NetworkPerformance/latest`)
      .then(data => {
        console.log(data);
        const newData = data.data;
        this.protocolsTableData = newData;
        // 从protocolsTableData中获取最新的延迟数据
        const protocolsData = {
            encc: null,
            quic: null,
            bbr: null,
            webrtc: null,
            'encc2':null,
            'quic2': null,
            'bbr2': null,
            'webrtc2': null,
          };
          const colorMap = {
            encc: '#99BBFF',
            quic: '#FF8888',
            bbr: '#CCBBFF',
            webrtc: '#AAFFEE',
            'encc2': '#99BBFF',
            'quic2': '#FF8888',
            'bbr2': '#CCBBFF',
            'webrtc2': '#AAFFEE',
          };
          newData.forEach(item => {
          const protocolKey = item.state === '场景一' ? item.protocol : item.protocol + '2';
              if (protocolsData.hasOwnProperty(protocolKey)) {
                protocolsData[protocolKey] = item;
              }
            });
          const xAxisData = Object.keys(protocolsData); // X轴标签
          const yAxisData1 = xAxisData.map(protocol => ({
            value: protocolsData[protocol] ? protocolsData[protocol].tail_delay : null,
            itemStyle: {
              color: colorMap[protocol],
            },
          }));
          const yAxisData2 = xAxisData.map(protocol => ({
            value: protocolsData[protocol] ? protocolsData[protocol].congestion_rate : null,
            itemStyle: {
              color: colorMap[protocol],
            },
            }));
            // 创建图表实例
            const chart1 = echarts.init(document.getElementById('charts1'));
            const chart2 = echarts.init(document.getElementById('charts2'));
            const chart1Options = {
              title: {
                text: '尾延迟对比图',
                textStyle: {
                  fontSize: 15, // 标题字体大小
                  fontWeight: 'bold', // 标题字体粗细
                  fontFamily: 'Arial, sans-serif', // 标题字体
                },
                padding:[10,0,0,10],
              },
              legend: {
                data: ['场景一', '场景二']
              },
              tooltip: {},
              grid: {
                left: '8%',
                top:'15%',
                right: '7%',
                bottom: '6%',
                containLabel: true
              },
              xAxis: {
                type: 'category',
                data: xAxisData,
                name:'协议类型',
                nameLocation: 'center', // 将 x 轴标题居中显示
                nameGap:25, // 设置 x 轴标题与刻度之间的间距
                axisLine: {
                  lineStyle: {
                    color: 'gray',
                  },
                },
                axisTick: {
                  lineStyle: {
                    color: 'gray',
                  },
                },
                axisTick: {
                  show: false, // 不显示 X 轴刻度线
                },
                axisLabel: {
                  interval: 0, // 强制显示所有刻度
                },
              },
              yAxis: {
                min: 0,      // 纵坐标最小值
                max: 5,   // 纵坐标最大值
                interval: 1,  // 刻度间隔
                name:'尾时延  /s',
                nameLocation: 'center', // 将 x 轴标题居中显示
                nameGap:42, // 设置 x 轴标题与刻度之间的间距
                rotate: -90, // 旋转Y轴标题
                axisLine: {
                  show: false, // 不显示 Y 轴轴线
                },
                axisTick: {
                  show: false, // 不显示 Y 轴刻度线
                },
                type: 'value',
                splitLine: {
                  lineStyle: {
                    color: '#DDDDDD', // 设置背景刻度对准线的颜色
                  },
                },
                axisLabel: {
                  margin: 12, // 刻度值与坐标轴的距离
              },
              },
              series: [
                {
                  name: '延迟',
                  type: 'bar',
                  data: yAxisData1,
                  barWidth: '80%',
                  itemStyle: {
                    borderWidth: 0.5,
                    color: '#73c0de',
                  }
                },
              ],
            };
            const chart2Options = {
              title: {
                text: '卡顿率对比图',
                textStyle: {
                  fontSize: 15, // 标题字体大小
                  fontWeight: 'bold', // 标题字体粗细
                  fontFamily: 'Arial, sans-serif', // 标题字体
                },
                padding:[10,0,0,10],
              },
              legend: {
                data: ['场景一', '场景二']
              },
              tooltip: {},
              grid: {
                left: '8%',
                top:'15%',
                right: '7%',
                bottom: '6%',
                containLabel: true
              },
              xAxis: {
                type: 'category',
                data: xAxisData,
                name:'协议类型',
                nameLocation: 'center', // 将 x 轴标题居中显示
                nameGap:25, // 设置 x 轴标题与刻度之间的间距
                axisLine: {
                  lineStyle: {
                    color: 'gray',
                  },
                },
                axisTick: {
                  lineStyle: {
                    color: 'gray',
                  },
                },
                axisTick: {
                  show: false, // 不显示 X 轴刻度线
                },
                axisLabel: {
                  interval: 0, // 强制显示所有刻度
                },
              },
              yAxis: {
                min: 0,      // 纵坐标最小值
                max: 10,   // 纵坐标最大值
                interval: 2,  // 刻度间隔
                name:'卡顿率  /%',
                nameLocation: 'center', // 将 x 轴标题居中显示
                nameGap:35, // 设置 x 轴标题与刻度之间的间距
                rotate: -90, // 旋转Y轴标题
                axisLine: {
                  show: false, // 不显示 Y 轴轴线
                },
                axisTick: {
                  show: false, // 不显示 Y 轴刻度线
                },
                type: 'value',
                splitLine: {
                  lineStyle: {
                    color: '#DDDDDD', // 设置背景刻度对准线的颜色
                  },
                },
                axisLabel: {
                  margin: 12, // 刻度值与坐标轴的距离
              },
              },
              series: [
                {
                  name: '卡顿率',
                  type: 'bar',
                  data: yAxisData2,
                  barWidth: '80%',
                  itemStyle: {
                    borderWidth: 0.7,
                    color: '#73c0de',
                  }
                },
              ],
            };
              // 设置选项并渲染图表
              console.log(chart1);
              chart1.setOption(chart1Options);
              console.log(chart2);
              chart2.setOption(chart2Options);
          })
        },
    fetchbackgroundTableData(){
      this.$fetch('test/condition')
        .then(data => {
        //console.log(data);
        this.backgroundTableData = data.data;
        //this.backgroundTableData = data.backgroundTableData;   //!!!
        })
    },
    handleSubmit() {
      this.timer = setInterval(() => {
        this.fetchTableDataAndDrawChart();
      }, 10000); // 每10秒刷新一次
      const selectedpath = [];
      const selectedprotocol = [];
      selectedprotocol.push(
      this.radio === '1' ? 'reno' :
      this.radio === '4' ? 'bbr' :
      this.radio ===' 5' ? 'reno' :
      this.radio === '8' ? 'bbr' :
      ''
    ); // 具体单选项
    const selectedProtocol=selectedprotocol[0];
    console.log(selectedProtocol);
    console.log(typeof selectedProtocol);
    // 获取选中的值
    selectedpath.push(
      this.radio === '1' ? '1' :
      this.radio === '2' ? '1' :
      this.radio === '3' ? '1' :
      this.radio === '4' ? '1' :
      this.radio === '5' ? '2' :
      this.radio === '6' ? '2' :
      this.radio === '7' ? '2' :
      this.radio === '8' ? '2' :
      ''
    );
    const selectedPath=selectedpath[0];
    console.log(selectedPath);
    this.$fetch('test/condition')
          .then(data => {
          console.log(data);
        })
      if(selectedpath == 1){
        this.$fetch(`SinglePath`)
          .then(data => {
            console.log(data);
            if (data){
              this.$message({message:"协议部署成功",type:"success"});
            }
        })
      }else{
        this.$fetch(`multipath`)
          .then(data => {
            console.log(data);
            if (data){
                this.$message({message:"协议部署成功",type:"success"});
              }
        })
      }
      if(selectedprotocol == 1 || selectedprotocol == 4 || selectedprotocol == 5 || selectedprotocol == 8){
        this.$fetch(`congestion/${selectedprotocol}`)
          .then((data) => {
          console.log(data);
        })
      }
    this.fetchTableDataAndDrawChart();
   }
  }
}
  </script>

<style scpoed>
.Header{
  width: 100%;
  background-color: #003377; /* 设置分割线的背景颜色为蓝色 */
}
.charts-container{
  display: flex;
  justify-content: flex-start;
  background-color: #ffffff;
  width:1070px;
  height: 395px;
  margin-top:5px;
  padding-bottom: 10px;
  border: 1px solid #adb0b6;
  border-left:none;
  border-top-right-radius: 6px;    /* 右上角 */
  border-bottom-right-radius: 6px; /* 右下角 */
}
.chart-container{
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left:20px;
  margin-top:10px;
  margin-bottom: 10px;
  background-color: #c4f1e8;
  height: 380px;
  width: 640px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
}
.tabel{
  flex: 1;
  margin-top: 20px;
  margin-left: 20px;
  display: flex;
  flex-direction: column;
}
.tabel1-container{
  width:375px;
  height:195px;
  margin-right: 20px;
  margin-top: -15px;
  background-color: #CCEEFF;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
}
.tabel1{
  width:345px;
  height:50px;
  background-color: #fffffe;
  margin-top:-10px;
  margin-left: 15px;
  border-radius:8px;
}
.tabel11{
  margin-top:15px;
  margin-left:35px;
}
.tabel12{
  margin-top: 20px;
  margin-left:35px;
}
.tabel2{
  width:345px;
  height:53px;
  background-color: #fffffe;
  margin-top:-13px;
  margin-left: 15px;
  border-radius:8px;
}
.an2,
.an4{
  margin-left: 120px;
  margin-top: -20px;
}
.an1,
.an3{
  margin-left:120px;
  margin-top: -13px;
}
.tabel2-container{
  margin-right: 20px;
  margin-top: 5px;
  width:375px;
  height:195px;
  background-color: #dee9ff;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
}
.tabel3{
  width:345px;
  height:50px;
  background-color: #fffffe;
  margin-top:-10px;
  margin-left: 15px;
  border-radius:8px;
}
.tabel4{
  width:345px;
  height:53px;
  background-color: #fffffe;
  margin-top:7px;
  margin-left: 15px;
  border-radius:8px;
}
.tabel21{
  margin-top: 16px;
  margin-left:35px;
}
.tabel22{
  margin-top: 8px;
  margin-left:35px;
}
#chartsBox{
 width:600px;
 height:320px;
 background-color: #ffffff;
 margin-top: 10px;
 margin-left: 10px;
 padding-bottom: 10px;
 border-radius: 40px;
}
.toggle-buttons{
  width:593px;
  height:190px;
  background-color: #ffffff;
  margin-top: 10px;
  margin-left:10px;
  border-radius:8px;
  border: 1px solid #e0e3ea;
}
.toggle{
  margin-left:20px;
  padding-top: 20px;
}
.buttons{
  margin-top: 30px;
  margin-left:80px;
}
.danxuan-container{
  padding-left: 0;
  margin-top: 5px;
  background-color: #ffffff;
  width: 1070px;
  height: 345px;
  border: 1px solid #eceef0;
  border-left:none;
  border-top-right-radius: 6px;    /* 右上角 */
  border-bottom-right-radius: 6px; /* 右下角 */
}
.newcharts{
  display: flex;
  justify-content: flex-start;
  width:990px;
  height:290px;
  margin-left: 50px;
  margin-top: 2px;
  background-color: #FFFFE0;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
}
#charts1{
  flex:1;
  display: flex;
  flex-direction: column;
  width:460px;
  height:260px;
  background-color: #ffffff;
  margin-left: 25px;
  margin-top:10px;
  padding-bottom: 10px;
}
#charts2{
  flex:1;
  display: flex;
  flex-direction: column;
  width:460px;
  height:260px;
  background-color: #ffffff;
  margin-left: 10px;
  margin-right: 25px;
  margin-top:10px;
  padding-bottom: 10px;
}
.tabs-container{
  width:593px;
  background-color: #ffffff;
  margin-left:10px;
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  border-radius:8px;
  border: 1px solid #e0e3ea;
  overflow:auto;
}
.tab{
  margin-left: 10px;
  margin-right: 10px;
  margin-top: 10px;
}
.tab-container{
  margin-left: 10px;
  margin-right: 10px;
  margin-bottom: 5px;
  margin-top: 2px;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
}
.table-container {
  height: 415px;
  overflow: auto;
  position: relative;
}
.table-wrapper1,
.table-wrapper2,
.table-wrapper3{
  height: 100%;
  overflow: auto;
}
.custom-protocol{
  font-size:14px;
}
.custom-protocol2{
  font-size:12px;
}
.custom-protocol3{
  font-size:12px;
}
.create_time{
  font-size:12px;
}
.el-table {
  margin-bottom: 10px;
}
.container {
  display: flex; /* 使用 flexbox 布局 */
}
.bulletClass{
  color:#7fa8e6;
}
</style>