<template>
    <div class="chart-container">
        <div>
            <!-- <el-switch
                style="float:left; display: block; padding-bottom: 5px;"
                v-model="valueSwitch"
                active-color="#2f4554"
                inactive-color="#2f4554"
                active-text="某一天"
                inactive-text="某一段">
            </el-switch> -->
            <el-dropdown>
                <span class="el-dropdown-link">
                    切换<i class="el-icon-caret-bottom el-icon--right"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item class="clearfix" @click.native="ChangeTimer(false)">某一时间段</el-dropdown-item>
                    <el-dropdown-item class="clearfix" @click.native="ChangeTimer(true)">某一天</el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
            <!-- <div > -->
                <el-date-picker
                    v-if="valueSwitch"
                    ref="picker1"
                    v-model="picker1"
                    type="date"
                    placeholder="选择日期时间"
                    :picker-options="pickerOptions"
                    value-format="yyyy-MM-dd">
                </el-date-picker>
            <!-- </div> -->
            <!-- <div class="subTimeBlock" > -->
                <el-date-picker
                    v-if="!valueSwitch"
                    ref="picker2"
                    v-model="picker2"
                    type="datetimerange"
                    :picker-options="pickerOptionsRange"
                    range-separator="至"
                    start-placeholder="开始时间"
                    end-placeholder="结束时间"
                    value-format="yyyy-MM-dd HH:mm:ss">
                </el-date-picker>
            <!-- </div> -->
            <el-select v-model="valueSelect" placeholder="默认图表单位为天" style="padding-right:5px">
                <el-option
                    v-for="item in optionsSelector"
                    :key="item.valueSelect"
                    :label="item.label"
                    :value="item.valueSelect">
                </el-option>
            </el-select>
            <el-button icon="el-icon-search" circle @click="getData"></el-button>
        </div>
        <!-- <span class="demonstration">调整步长</span> -->
        <el-slider v-model="valueAddLength" :min=1 :max=20 show-stops style="width: 50% color:'#2f4554'"> </el-slider>
        <div class="chart-container">
            <div style="height:400px" ref="statistic_ref"></div>
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
            //Selector
            optionsSelector: [{
                valueSelect: 'year',
                label: '年'
            }, {
                valueSelect: 'month',
                label: '月'
            }, {
                valueSelect: 'day',
                label: '日'
            }, {
                valueSelect: 'hour',
                label: '小时'
            }],
            valueSelect: '',
            valueAddLength: 2,// 后端间隔步长

            // echarts
            xAxisData: [],
            moneyIn: [],
            moneyOut: [],
            money: [],
            chartInstance: null,
            moneyMax: 0,
            unit: null
        }
    },
    mounted() {
        this.dummyData()
        this.initChart()
        window.addEventListener('resize', this.screenAdapter)
        this.screenAdapter()// 初始效果
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
                    data: ['收入', '支出', '收益'],
                    left: 10,
                    bottom: 2
                },
                // brush: {
                //     toolbox: ['rect', 'polygon', 'lineX', 'lineY', 'keep', 'clear'],
                //     xAxisIndex: 0
                // },
                toolbox: {
                    right: 10,
                    bottom: 2,
                    feature: {
                        // magicType: {
                        //     type: ['stack', 'tiled']
                        // },
                        dataView: {
                            lang: ['数据视图', '关闭', '刷新']
                        },
                        saveAsImage: {},
                        restore: {}, // 重置
                        dataZoom: {}, // 区域缩放
                        magicType: {
                            type: ['line']
                        } // 动态切换图表类型
                    }
                },
                tooltip: {
                    trigger: 'item',//'axis'
                    formatter: function(arg){
                        // console.log(arg)
                        return arg.seriesName + ': ' + arg.value
                    }
                },
                xAxis: {
                    data: this.xAxisData,
                    name: 'Day',
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
                    text: ['Max', 'Min'],
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
                    },{
                        name: '收益',
                        type: 'line',
                        data: this.money,
                        lineStyle: {
                            color: '#2f4554'
                        }
                    }
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

            // console.log(this.valueSelect)

            if(this.valueSelect == '')  this.unit = 'day'
            else  this.unit = this.valueSelect

            var postData = {'startTime':startTime,'endTime':endTime,'catId':1,'unit':this.unit,'timeLength':this.valueAddLength}
            var ret = await this.$http.post('/PurchaseOrders/ExpenditureOfDivideTime', postData)
            // 需要写获取失败的判断
            var jsonData = ret.data.results
            console.log(jsonData.length)
            this.moneyMax = 0
            for (var i = 0; i < jsonData.length; i++) {
                // console.log(i,jsonData[i].startTime)
                this.xAxisData.push(i);//jsonData[i].startTime
                this.moneyIn.push(jsonData[i].expenditure)
                this.moneyOut.push(-jsonData[i].expenditure)
                this.money.push(this.moneyIn[i] + this.moneyOut[i])
                if(jsonData[i].expenditure > this.moneyMax) {
                    this.moneyMax = jsonData[i].expenditure
                }
            }
            console.log(this.moneyIn)
            this.updateChart()
        },
        updateChart() { 
            const newOption = {
                xAxis: {
                    data: this.xAxisData,
                    name: this.unit,
                },
                visualMap: {
                    min: -this.moneyMax,
                    max: this.moneyMax,
                },
                series: [
                    {
                        name: '支出',
                        data: this.moneyOut
                    },{
                        name: '收入',
                        data: this.moneyIn
                    },{
                        name: '收益',
                        data: this.money
                    },
                ]
            }
            this.chartInstance.setOption(newOption)
        },
        screenAdapter() {
            // alert('size: '+titleFontSize)
            // const adaptOption = {

            // }
            // this.chartInstance.setOption(adaptOption)
            this.chartInstance.resize()
        },
        dummyData() {
            for (var i = 0; i < 10; i++) {
                this.xAxisData.push('Dy' + i)
                this.moneyIn.push(parseFloat((Math.random() * 2).toFixed(2)))
                this.moneyOut.push(parseFloat(-Math.random().toFixed(2)))
                this.money.push(this.moneyIn[i] + this.moneyOut[i])
                // console.log(this.moneyIn[i])
            }
            this.moneyMax = 6
        },
        cleanContainer() {
            // 1: arr.splice(0,arr.length)
            // 2: arr = []
            this.xAxisData.length = 0
            this.moneyIn.length = 0
            this.moneyOut.length = 0
            this.money.length = 0
            this.moneyMax = 0
        },
        ChangeTimer(state) {
            // alert(state)
            this.valueSwitch = state
        }
    }
  }
</script>