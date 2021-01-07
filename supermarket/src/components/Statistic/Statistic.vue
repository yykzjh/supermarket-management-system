<template>
    <div class="chart-container">
        <div>
            <el-switch
                style="float:left; display: block; padding-bottom: 5px;"
                v-model="valueSwitch"
                active-color="#2f4554"
                inactive-color="#2f4554"
                active-text="某一天"
                inactive-text="某一段">
            </el-switch>
            <div class="subTimeBlock" v-if="valueSwitch">
                <el-date-picker
                    ref="picker1"
                    v-model="picker1"
                    type="date"
                    placeholder="选择日期时间"
                    :picker-options="pickerOptions"
                    value-format="yyyy-MM-dd">
                </el-date-picker>
            </div>
            <div class="subTimeBlock" v-if="!valueSwitch">
                <el-date-picker
                    ref="picker2"
                    v-model="picker2"
                    type="datetimerange"
                    :picker-options="pickerOptionsRange"
                    range-separator="至"
                    start-placeholder="开始时间"
                    end-placeholder="结束时间"
                    value-format="yyyy-MM-dd HH:mm:ss">
                </el-date-picker>
            </div>
            <el-button icon="el-icon-search" circle @click="getData"></el-button>
        </div>
            
        <div class="chart-container">
            <div class="chart-chart" ref="statistic_ref"></div>
        </div>
    </div>
</template>

<script>
import '../../assets/css/charts.css'
  export default {
    data() {
        return {
            valueSwitch: false,
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
            pickerOptions: {
                shortcuts: [{
                    text: '今天',
                    onClick(picker) {
                        picker.$emit('pick', new Date());
                    }
                },
                {
                    text: '昨天',
                    onClick(picker) {
                        const date = new Date();
                        date.setTime(date.getTime() - 3600 * 1000 * 24);
                        picker.$emit('pick', date);
                    }
                },
                {
                    text: '一周前',
                    onClick(picker) {
                        const date = new Date();
                        date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
                        picker.$emit('pick', date);
                    }
                }]
            },
            picker2: '',
            picker1: '',

            // echarts
            xAxisData: [],
            moneyIn: [],
            moneyOut: [],
            money: [],
            chartInstance: null,
            moneyMax: 0
        }
    },
    mounted() {
        this.dummyData()
        this.initChart()
    },
    methods: {
        initChart() {
            // this.dummyData()
            this.chartInstance = this.$echarts.init(this.$refs.statistic_ref)
            var emphasisStyle = {
                itemStyle: {
                    barBorderWidth: 1,
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowOffsetY: 0,
                    shadowColor: 'rgba(0,0,0,0.5)'
                }
            }
            const initOption = {
                backgroundColor: '#eee',
                legend: {
                    data: ['收入', '支出'],
                    left: 10
                },
                // brush: {
                //     toolbox: ['rect', 'polygon', 'lineX', 'lineY', 'keep', 'clear'],
                //     xAxisIndex: 0
                // },
                toolbox: {
                    feature: {
                        magicType: {
                            type: ['stack', 'tiled']
                        },
                        dataView: {}
                    }
                },
                tooltip: {},
                xAxis: {
                    data: this.xAxisData,
                    name: 'X Axis',
                    axisLine: {onZero: true},
                    splitLine: {show: false},
                    splitArea: {show: false}
                },
                yAxis: {
                    inverse: false,
                    splitArea: {show: false}
                },
                grid: {
                    left: 100
                },
                visualMap: {
                    type: 'continuous',
                    dimension: 1,
                    text: ['High', 'Low'],
                    inverse: true,
                    itemHeight: 200,
                    calculable: true,
                    min: -this.moneyMax,
                    max: this.moneyMax,
                    top: 60,
                    left: 10,
                    inRange: {
                        colorLightness: [0.4, 0.8]
                    },
                    outOfRange: {
                        color: '#bbb'
                    },
                    controller: {
                        inRange: {
                            color: '#2f4554'
                        }
                    }
                },
                series: [
                    {
                        name: '支出',
                        type: 'bar',
                        stack: 'one',
                        emphasis: emphasisStyle,
                        data: this.moneyOut
                    },{
                        name: '收入',
                        type: 'bar',
                        stack: 'one',
                        emphasis: emphasisStyle,
                        data: this.moneyIn
                    },
                ]
            }
            this.chartInstance.setOption(initOption)
        },
        async getData() {
            this.cleanContainer()
            var startTime = null
            var endTime = null
            // "picker"+String(this.valueSwitch?1:0)
            if(this.valueSwitch) {// 某一天
                // console.log(this.picker1)
                startTime=this.picker1+" 00:00:00"
                endTime=this.picker1+" 23:59:59"
            } else {// 某一时间段
                // console.log(this.picker2)
                startTime=this.picker2[0]
                endTime=this.picker2[1]
            } 
            // console.log(startTime)
            // console.log(endTime)
    
            var postData = {'startTime':startTime,'endTime':endTime,'catId':1,'unit':'day','timeLength':15}
            var ret = await this.$http.post('/PurchaseOrders/ExpenditureOfDivideTime', postData)
            var jsonData = ret.data.results
            console.log(jsonData.length)
            this.moneyMax = 0
            for (var i = 0; i < jsonData.length; i++) {
                // console.log(i,jsonData[i].startTime)
                this.xAxisData.push(i);//jsonData[i].startTime
                this.moneyIn.push(jsonData[i].expenditure);
                this.moneyOut.push(-jsonData[i].expenditure);
                if(jsonData[i].expenditure > this.moneyMax) {
                    this.moneyMax = jsonData[i].expenditure
                }
            }
            this.initChart()
        },
        updateChart() {

        },
        screenAdapter() {
            // alert('size: '+titleFontSize)
            const adaptOption = {
            }
            this.chartInstance.setOption(adaptOption)
            this.chartInstance.resize()
        },
        dummyData() {
            for (var i = 0; i < 10; i++) {
                this.xAxisData.push('Dy' + i);
                this.moneyIn.push((Math.random() * 2).toFixed(2));
                this.moneyOut.push(-Math.random().toFixed(2));
            }
            this.moneyMax = 6
        },
        cleanContainer() {
            // 1: arr.splice(0,arr.length)
            // 2: arr = []
            this.xAxisData.length = 0
            this.moneyIn.length = 0
            this.moneyOut.length = 0
            this.moneyMax = 0
        }
    }
  }
</script>