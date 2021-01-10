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
            type="text">
            <!-- 编辑 -->
          </el-button>
        </span>
      </div>
      <div style="width:100%; height: 300px; margin:-40px 0px -30px 0px" ref="pie_ref"></div>
      <div style="height: 300px;">
        <el-form ref="form" :model="form" label-width="80px">
          <el-form-item label="商品名称">
            <span style="margin-left: 10px;">{{form.name}}</span>
          </el-form-item>
          <!-- <el-form-item label="摆放区域">
            <el-select v-model="form.region" placeholder="请选择活动区域">
              <el-option label="A1" value="A1"></el-option>
              <el-option label="B2" value="B2"></el-option>
            </el-select>
          </el-form-item> -->
          <!-- <el-form-item label="加入时间">
            <el-col :span="11" v-model="form.date1">
              <el-date-picker type="date" placeholder="选择日期" v-model="form.date1" style="width: 100%;"></el-date-picker>
            </el-col>
          </el-form-item> -->
          <!-- <el-form-item label="即时配送">
            <el-switch v-model="form.delivery"></el-switch>
          </el-form-item> -->
          <el-form-item label="商品类别">
            <!-- <el-select v-model="form.type" placeholder="请选择活动区域">
              <el-option label="文具" value="文具"></el-option>
              <el-option label="日用品" value="日用品"></el-option>
              <el-option label="饮料" value="饮料"></el-option>
            </el-select> -->
            <el-badge :value="form.parentId" class="item" type="primary">
              <span style="margin-left: 10px;">{{form.type}}</span>
            </el-badge>
            
          </el-form-item>
          <el-form-item label="介绍">
            <!-- <el-input type="textarea" v-model="form.intro"></el-input> -->
            <span>{{form.intro}}</span>
          </el-form-item>
          <!-- <el-form-item>
            <el-button type="primary" @click="onSubmit">立即创建</el-button>
            <el-button>取消</el-button>
          </el-form-item> -->
        </el-form>
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
            @click="RefreshTime"
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
        pickerTime: null,

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
        form: {
          name: '超级大汉堡',
          // region: 'A1',
          // date1: '2020-01-01 08:00:00',
          // delivery: false,
          parentId: 2,
          type: '速食',
          // resource: '',// 供货商
          intro: '为商品提供给市场，被人们使用和消费，并能满足人们某种需求的任何东西，包括有形的物品、无形的服务、组织、观念或它们的组合。'
        }
      }
    },
    created () {
      this.goodid = this.$route.query.goodid
      console.log(this.goodid)
    },
    mounted() {
      document.getElementById('spanTitle').innerText = this.goodid
      this.GetPieData()
      this.GetGoodDetails()
      // this.GetLineData()
      this.InitCharts()
      window.addEventListener('resize', this.screenAdapter)
      this.screenAdapter()// 初始效果
    },
    methods: {
      RefreshTime() {
        // console.log(this.pickerTime)
        if(this.pickerTime != null) {
          // console.log(this.pickerTime)
          this.startTime=this.pickerTime[0]
          this.endTime=this.pickerTime[1]
        }
        // this.GenerateTimeaxis()
        else this.startTime = ''
        this.GetLineData()
      },
      InitCharts() {
        this.Pie()
        this.Line()
      },
      Pie() {
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
        // this.GetLineData() //先默认查3个月吧
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
      TimeFormat(time) {
        var date_ = new Date(time)
        var year = date_.getFullYear()
        var month = date_.getMonth()+1
        var day = date_.getDate()
        if(month<10) month = "0"+month
        if(day<10) day = "0"+day

        var hours = date_.getHours()
        var mins = date_.getMinutes()
        var secs = date_.getSeconds()
        var msecs = date_.getMilliseconds()
        if(hours<10) hours = "0"+hours
        if(mins<10) mins = "0"+mins
        if(secs<10) secs = "0"+secs
        if(msecs<10) secs = "0"+msecs
        // console.log(year+"/"+month+"/"+day+" "+hours+":"+mins+":"+secs)
        return  year+"/"+month+"/"+day+" "+hours+":"+mins+":"+secs
      },
      async GetGoodDetails() {
        const {data: ret}  = await this.$http.get('/Goods/GoodDetail?good_id=' + this.goodid)
        if(ret.StatusCode == 400) {
          console.log('123456未查到该商品芜湖')
        } else {
          console.log(ret.good)
          // console.log('这部分实际上也可以显示它的供应商等信息，点击跳转那种')

          if(ret.good.name != null)  this.form.name = ret.good.name
          if(ret.good.type != null)  this.form.type = ret.good.parentCat
          if(ret.good.intro != null)  this.form.intro = ret.good.intro
        }
      },
      async GetLineData() {
        if(this.startTime == '') {// 默认查三个月的
          const end = new Date();
          const start = new Date();
          start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
          this.startTime = this.DateFromat(start)
          this.endTime = this.DateFromat(end)
          console.log(this.endTime, this.startTime)// 其实我也可以发送给你精确到秒的
        }
        // this.GenerateTimeaxis()
        // priceIn 进价变化数组
        // priceOut 售价变化数组
        var temp = null
        var len = null
        var ret = await this.$http.post('/PurchaseOrders/GoodPurchasePriceInPeriod', {
          'good_id': this.goodid,
          'start_time': this.startTime,
          'end_time': this.endTime,
        })
        if(ret.status !== 200)
          this.$message.error('Network 获取进价变化失败')
        else {
          // console.log(ret.data.priceList)
          temp = ret.data.priceList
          len = temp.length
          this.priceIn = []
          if(len!=0) {
            this.priceMin = temp[0].price_in
            this.priceMax = temp[0].price_in
          }
          for(var i in temp) {
            // console.log()
            this.priceIn.push([this.TimeFormat(temp[i].finish_time),temp[i].price_in])
            if(temp[i].price_in > this.priceMax) this.priceMax = temp[i].price_in
            if(temp[i].price_in < this.priceMin) this.priceMin = temp[i].price_in
          }

          ret = await this.$http.post('/HistoryOrders/GoodSalePriceInPeriod', {
            'good_id': this.goodid,
            'start_time': this.startTime,
            'end_time': this.endTime,
          })
          if(ret.status !== 200)
            this.$message.error('Network 获取售价变化失败')
          else {
            
            if(len==0 && temp.length!=0) {
              this.priceMin = temp[0].price_in
              this.priceMax = temp[0].price_in
            }
            temp = ret.data.priceList

            // console.log(temp)
            this.priceOut = []
            for(var i in temp) {
              this.priceOut.push([this.TimeFormat(temp[i].datetime),temp[i].price])
              if(temp[i].price > this.priceMax) this.priceMax = temp[i].price
              if(temp[i].price < this.priceMin) this.priceMin = temp[i].price
            }
            // console.log("what",this.priceOut)
            this.priceMax = this.priceMax + this.priceMax / 100.0
            this.priceMin = this.priceMin - this.priceMin / 100.0
            // console.log(this.priceIn,this.priceOut)
            this.UpdataLineChart()// 一个点显示小时，多个显示天
          }
        }
        // 销量数组
      },
      async GetPieData() { 
        var ret  = await this.$http.get('/Stocks/amountOfTheCat?catId=' + this.goodid)
        // var ret = await this.$http.get('/Stocks/amountOfTheCat', {
        //   params: {catId: this.goodid}})
        if(ret.status !== 200)
          this.$message.error('Network 获取商品库存失败')
        else {
          ret = ret.data
          // {value: 335, name: '库存'}
          this.pieData[0] = {value: ret.amount, name: '库存'}
          // console.log(this.pieData[0])
          ret = await this.$http.get('/OnSales/amountOfTheCat?catId=' + this.goodid)
          if(ret.status !== 200)
            this.$message.error('Network 获取商品上架数量失败')
          else {
            ret = ret.data
            // console.log(ret)
            this.pieData[1] = {value: ret.amount, name: '已上架'}
            this.UpdataPieChart()
          }
        }
      },
      UpdataLineChart() {// refresh button
        const newOptions ={
          series: [
            {
              data: this.priceOut
            },
            {
              data: this.priceIn
            }
          ],
          visualMap: {
            min: this.priceMin,
            max: this.priceMax,
          }
        }
        this.lineInstance.setOption(newOptions)
      },
      UpdataPieChart() {
        const newOptions = {
          series: [
            {
              data: this.pieData
            }
          ]
        }
        this.pieInstance.setOption(newOptions)
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
