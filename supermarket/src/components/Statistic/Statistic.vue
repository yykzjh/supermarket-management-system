<template>
    <div>
        <div>
            <el-switch
                style="float:left; display: block; padding-bottom: 5px;"
                v-model="valueSwitch"
                active-color="#00BFFF"
                inactive-color="#00BFFF"
                active-text="某一天"
                inactive-text="某一段">
            </el-switch>
            <div class="subTimeBlock" v-if="valueSwitch">
                <el-date-picker
                    ref="picker1"
                    v-model="picker1"
                    type="datetime"
                    placeholder="选择日期时间"
                    :picker-options="pickerOptions">
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
                    end-placeholder="结束时间">
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
import axios from 'axios';
  export default {
    data() {
        return {
            valueSwitch: true,
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
            money: []
        }
    },
    mounted() {
        this.getData()
        // this.initChart()
    },
    methods: {
        initChart() {
        },
        async getData() {
            // console.log('search')
            var postData = null
            // var ret = await this.$http.get('/', postData)
            // console.log(ret)
        },
        updateChart() {

        },
    }
  }
</script>