<template>
  <div>
    <el-card
      class="box-card"
      style="width:40%; float:left"
      id="card1">
      <div slot="header" class="clearfix">
        <span id="spanTitle"></span>
        <span>
          <el-button
            style="float: right; padding: 3px 0"
            type="text">编辑
          </el-button>
        </span>
      </div>
      <div style="width:100%; height: 300px; margin:-40px 0px -30px 0px" ref="pie_ref"></div>
      <div style="background-color:red; height: 300px;">
        
      </div>
    </el-card>
    <el-card
      class="box-card"
      style="width:59%">
      <div slot="header" style="text-align:center">
        <span>
          <el-date-picker
            ref="pickerTime"
            v-model="pickerTime"
            type="daterange"
            :picker-options="pickerOptionsRange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            value-format="yyyy-MM-dd">
          </el-date-picker>
          <el-button
            type="refresh"
            icon="el-icon-refresh"
            circle
            @click="UpdataLineChart"
            style="margin-left: 5px">
          </el-button>
        </span>
      </div>
      <div style="width:100%; height:510px;" ref="line_ref" id="line"></div>
    </el-card>
  </div>
</template>

<script>
  // import ecStat from 'echarts-stat'
  export default {
    data() {
      return {
        goodid: 0,
        pickerOptionsRange: {
          shortcuts: [{
            text: '最近一周',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', [start, end]);
            }
          }, 
          {
            text: '最近一个月',
            onClick(picker) {
                const end = new Date();
                const start = new Date();
                start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
                picker.$emit('pick', [start, end]);
            }
          }, 
          {
            text: '最近三个月',
            onClick(picker) {
                const end = new Date();
                const start = new Date();
                start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
                picker.$emit('pick', [start, end]);
            }
          }]
        },
        pickerTime: '',

        // pie图表数据
        pieInstance: null,
        lineInstance: null,
        pieData: [
          {value: 335, name: '库存'},
          {value: 310, name: '已上架'},
        ],
        // line图表数据
        startTime: '',
        endTime: null,
        timeData: null,

        goosUnit: '件',// 商品单价单位
        valueMax: 500,// 价格最大值
        priceMin: 0,
        priceMax: 1,// 价格最大值
        priceIn: [
    [ '2017-03-01',1 ],
    [ '2017-06-01', 0.5 ],
    [ '2017-07-02', 0.5 ],
    [ '2017-12-01',1 ],
    [ '2018-01-01', 0.5 ],
    [ '2018-02-02', 0.5 ],
    [ '2018-03-01',1 ],
    [ '2018-06-01', 0.5 ],
    [ '2018-07-02', 0.5 ],
],// 进价变化数组
        priceOut: [
    [ '2017-03-01',1 ],
    [ '2017-06-01', 0.5 ],
    [ '2017-07-02', 0.5 ],
    [ '2017-12-01',1 ],
    [ '2018-01-01', 0.5 ],
    [ '2018-02-02', 0.5 ],
    [ '2018-03-01',1 ],
    [ '2018-06-01', 0.5 ],
    [ '2018-07-02', 0.5 ],
],// 售价变化数组
      }
    },
    created () {
      this.goodid = this.$route.query.goodid
      console.log(this.goodid)
    },
    mounted() {
      document.getElementById('spanTitle').innerText = this.goodid
      this.InitCharts()
      window.addEventListener('resize', this.screenAdapter)
      this.screenAdapter()// 初始效果
    },
    methods: {
      RefreshTime() {
        // console.log(this.pickerTime)
        this.startTime=this.pickerTime[0]
        this.endTime=this.pickerTime[1]
        // this.GenerateTimeaxis()
        
      },
      InitCharts() {
        this.Pie()
        this.Line()
      },
      Pie() {
        this.GetPieData()
        this.pieInstance = this.$echarts.init(this.$refs.pie_ref)
        const initOption = {
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            right: 10,
            bottom: 50,
            data: ['库存', '已上架']
          },
          series: [
            {
              name: '商品余量',
              type: 'pie',
              radius: ['50%', '70%'],
              avoidLabelOverlap: false,
              label: {
                  show: false,
                  position: 'center'
              },
              emphasis: {
                  label: {
                      show: true,
                      fontSize: '30',
                      fontWeight: 'bold'
                  }
              },
              labelLine: {
                  show: false
              },
              data: this.pieData
            }
          ],
          // <img src="" class="image">
          graphic: [
            {
              type: 'image',
              id: 'logo',
              right: 'center',
              top: 'center',
              z: -10,
              bounding: 'raw',
              style: {
                image: 'https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png',
                width: 150,
                height: 150,
                opacity: 1,
              }
            }
          ]
        }
        this.pieInstance.setOption(initOption)
      },
      Line() {
        this.GetLineData()
        this.lineInstance = this.$echarts.init(this.$refs.line_ref)

        // var regressionIn = ecStat.regression('polynomial', this.priceIn, 3);
        // regressionIn.points.sort(function(a, b) {
        //     return a[0] - b[0];
        // });
        // var regressionOut = ecStat.regression('polynomial', this.priceOut, 3);
        // regressionOut.points.sort(function(a, b) {
        //     return a[0] - b[0];
        // });

        const initOption = {
          title: {
            text: '价格变动情况',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'cross'
            }
          },
          // legend: {
          //     data: ['售价', '进价'],
          //     left: 10
          // },
          toolbox: {
            top: 0,
            feature: {
              dataZoom: {
                yAxisIndex: 'none'
              },
              // restore: {},
              saveAsImage: {}
            }
          },
          axisPointer: {
            link: {xAxisIndex: 'all'}
          },
          dataZoom: [
            {
              show: true,
              realtime: true,
              start: 0,
              end: 100,
              xAxisIndex: [0, 1]
            },
            {
              type: 'inside',
              realtime: true,
              start: 0,
              end: 100,
              xAxisIndex: [0, 1]
            }
          ],
          grid: [{
            left: 50,
            right: 50,
            height: '35%'
          }, {
            left: 50,
            right: 50,
            top: '47%',
            height: '35%'
          }],
          xAxis: [
            {
                type: 'time',
                boundaryGap: false,
                axisLine: {onZero: true},
            },
            {
                gridIndex: 1,
                type: 'time',
                boundaryGap: false,
                axisLine: {onZero: true},
                position: 'top',
                show: false
            }
          ],
          yAxis: [
            {
              name: '售价(元/s)',
              type: 'value',
              // max: 500
            },
            {
              gridIndex: 1,
              name: '进价（元/s）',
              type: 'value',
              inverse: true
            }
          ],
          series: [
            {
              name: '售价',
              type: 'line',
              symbolSize: 8,
              smooth: true,
              // hoverAnimation: false,
              data: this.priceOut
            },
            {
              name: '进价',
              type: 'line',
              xAxisIndex: 1,
              yAxisIndex: 1,
              symbolSize: 8,
              smooth: true,
              // hoverAnimation: false,
              data: this.priceIn
            }
          ],
          visualMap: {
            // orient: 'horizontal',
            right: 0,
            bottom: 30,
            min: this.priceMin,
            max: this.priceMax,
            calculable: true,// 滑块
            inRange: {
              color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
              // color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
            },
            // pieces: [{
            //   gt: 0.4,
            //   lte: 0.5,
            //   color: '#096'
            // }, {
            //   gt: 0.5,
            //   lte: 0.6,
            //   color: '#ffde33'
            // }, {
            //   gt: 0.6,
            //   lte: 0.7,
            //   color: '#ff9933'
            // }, {
            //   gt: 0.7,
            //   lte: 0.8,
            //   color: '#cc0033'
            // }, {
            //   gt: 0.8,
            //   lte: 0.9,
            //   color: '#660099'
            // }, {
            //   gt: 0.9,
            //   color: '#7e0023'
            // }],
            // outOfRange: {
            //   color: '#999'
            // }
          }
        }
        this.lineInstance.setOption(initOption)
      },
      getDiffDate(start, end) {
        var startTime = this.getDate(start);
        var endTime = this.getDate(end);
        var dateArr = [];
        var year = null
        var month = null
        var day = null
        while ((endTime.getTime() - startTime.getTime()) > 0) {
            year = startTime.getFullYear();
            month = (startTime.getMonth()+1<10?'0'+(startTime.getMonth()+1):(startTime.getMonth()+1))
            day = startTime.getDate()<10?'0'+startTime.getDate():startTime.getDate();
            dateArr.push(year + "-" + month + "-" + day);
            startTime.setDate(startTime.getDate() + 1);
        }
        return dateArr;
      },
      getDate (datestr) {
        var temp = datestr.split("-");
        // 0年 1月 2日
        if (temp[1] === '01') {
            temp[0] = parseInt(temp[0],10) - 1;// 指定基数10
            temp[1] = '12';
        } else {
            temp[1] = parseInt(temp[1],10) - 1;
        }
        //new Date()的月份入参实际都是当前值-1
        var date = new Date(temp[0], temp[1], temp[2]);
        return date;
      },
      GenerateTimeaxis() {
        // 单位是天
        // input: start end
        // out: [date1, date2, ]
        this.timeData = this.getDiffDate(this.startTime, this.endTime)
        // console.log(this.timeData)
      },
      DateFromat(time) {
        return time.getFullYear()+'-'+
        (time.getMonth()+1<10?'0'+(time.getMonth()+1):(time.getMonth()+1))+'-'+
        (time.getDate()<10?'0'+time.getDate():time.getDate())
      },
      GetLineData() {
        if(this.startTime == '') {
          const end = new Date();
          const start = new Date();
          start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
          this.startTime = this.DateFromat(start)
          this.endTime = this.DateFromat(end)
          console.log(this.endTime, this.startTime)
        }
        this.GenerateTimeaxis()
        // priceIn 进价变化数组
        // priceOut 售价变化数组
        var i = 0
        const len = this.timeData.length

        // 销量数组
      },
      GetPieData() {

      },
      UpdataLineChart() {
        this.RefreshTime()

      },
      screenAdapter() {
        this.pieInstance.resize()
        this.lineInstance.resize()
        // console.log(window.innerHeight)
        // document.getElementById('card1').style.height = window.innerHeight + "px"
        // document.getElementById('line').style.height = window.innerHeight + "px"
      },
    }
  }
</script>

<style scoped>

</style>
