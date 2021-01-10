<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>订单管理</el-breadcrumb-item>
      <el-breadcrumb-item>销售订单管理</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row>
      <el-col :span="11">
        <el-card class="grid-content">
          <div id="newEcharts" class="grid-content" style="width:500px;height:400px;padding-top:40px"></div>
        </el-card>
      </el-col>
      <el-col :span="12" style="margin-left: 15px">
        <el-card class="grid-content">
          <el-table
            border height="400px" :data="scollPrice">
            <el-table-column prop="time" label="订单生成时间"></el-table-column>
            <el-table-column prop="total" label="订单总额"></el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>


    <el-card style="margin-top: 15px">
      <el-table :data="ordersList" :span-method="spanMethod" border stripe style="width: 100%">
        <el-table-column prop="datetime" label="时间"></el-table-column>
        <el-table-column prop="good_name" label="名称"></el-table-column>
        <el-table-column prop="price" label="价格"></el-table-column>
        <el-table-column prop="amount" label="数量"></el-table-column>
      </el-table>
    </el-card>
  </div>

</template>

<script>
export default {

  data() {
    return {
      ordersList: [],
      rowUnit: [],//2 1 1 1
      testID: [0,-1,1,2,3],
      tableIndex: 0, // table的下标
      UnitIndex: 0, // rowUnit的下标
      scollPrice: [],
      dataset: { source: [
        ]},
    }
  },
  created () {
    this.getImgList()
    this.getOrdersList()
    this.play()
  },
  methods: {
    createImg() {
      let that = this
      // console.log(this.dataset)
      const myChart = this.$echarts.init(document.getElementById('newEcharts'))
      setTimeout(function () {
        const option = {
          legend: {},
          tooltip: {
            trigger: 'axis',//触发类型，'axis'为坐标系触发
            showContent: false//是否显示提示框浮层
          },
          dataset: that.dataset,
          xAxis: {type: 'category'},
          yAxis: {gridIndex: 0},//y轴所在的grid的索引
          grid: {top: '55%'},
          series: [
            //smooth:是否平滑曲线显示，若是boolean属性，表示开启平滑处理，若是number类型(取直范围0到1)
            //则表示平滑程度，越小表示越接近折线段
            //seriesLayoutBy:'row'表示dataset中每一行是一个维度(dimension)
            {type: 'line', smooth: true, seriesLayoutBy: 'row'},
            {type: 'line', smooth: true, seriesLayoutBy: 'row'},
            {type: 'line', smooth: true, seriesLayoutBy: 'row'},
            {type: 'line', smooth: true, seriesLayoutBy: 'row'},
            {
              type: 'pie',
              id: 'pie',  //组件ID
              radius: '30%',  //饼图的半径
              //center:饼圆的中心(圆心)坐标，第一项是横坐标，第二项是纵坐标
              //设置成百分比时第一项是相对于容器宽度，第二项是相对于容器高度。
              center: ['50%', '25%'],
              label: {
                formatter: '{b}: {@2012} ({d}%)'
              },
              encode: {
                itemName: 'product',
                value: '2012',
                tooltip: '2012'
              }
            }
          ]
        };

        myChart.on('updateAxisPointer', function (event) {
          var xAxisInfo = event.axesInfo[0];
          if (xAxisInfo) {
            var dimension = xAxisInfo.value + 1;
            myChart.setOption({
              series: {
                id: 'pie',
                label: {
                  formatter: '{b}: {@[' + dimension + ']} ({d}%)'
                },
                encode: {
                  value: dimension,
                  tooltip: dimension    //表示维度在tooltip(提示框组件)中显示
                }
              }
            });
          }
        });

        myChart.setOption(option);
      });
    },
    async getOrdersList() {
      const {data: res} = await this.$http.get('/HistoryOrders/AllHistoryOrders')
      if(res === {})
        return this.$message.error('获取订单信息失败')
      else{
        let that = this
        Object.keys(res.orders).forEach(function(key){
          // console.log(key,res.orders[key]);
          let tempAmount = res.orders[key].amount.split("  ")
          let tempName = res.orders[key].good_name.split("  ")
          let tempPrice = res.orders[key].price.split("  ")
          that.rowUnit.push(tempAmount.length)
          // console.log(that.rowUnit)

          let totalMoney = 0

          for(let i=0; i<tempAmount.length; i++){
            let tempObj = { amount: 0, datetime: '', good_name: '', price: 0 }
            tempObj.amount = parseFloat(tempAmount[i])
            tempObj.good_name = tempName[i]
            tempObj.price = parseFloat(tempPrice[i])
            totalMoney += tempObj.amount * tempObj.price
            tempObj.datetime = res.orders[key].datetime.split(" ")[0]
            that.ordersList.push(tempObj)
          }
          let tempObj2 = {time: res.orders[key].datetime.split(" ")[0], total: totalMoney}
          that.scollPrice.push(tempObj2)
        });
        // console.log(that.ordersList)
        // console.log(that.scollPrice)
        // console.log(that.rowUnit)
      }
    },
    // 播放销售订单
    play() {
      setInterval(this.change, 2000);//每两秒执行一次插入删除操作
    },
    spanMethod({ row, column, rowIndex, columnIndex }){
      if(columnIndex === 0){
<<<<<<< HEAD
        if(rowIndex === this.tableIndex){ //每次相等table的游标都下移rowUnit单位
          this.tableIndex += this.rowUnit[this.UnitIndex]
          return {
            rowspan: this.rowUnit[this.UnitIndex++], // 每次unit下标加一
            colspan: 1
          };
        }else {
          return {
            rowspan: 1,
            colspan: 1
=======
        if (this.testID[rowIndex] >=  0) {
            return {
              rowspan: this.rowUnit[this.testID[rowIndex]],
              colspan: 1
            };
          } else {
            return {
              rowspan: 0,
              colspan: 0
            }
>>>>>>> ef30876c57a234966cc030f30838a23b02b0886a
          }
      }
    },
    change() {
      this.scollPrice.push(this.scollPrice[0]);//把第一条数据插入数组最有一条
      this.scollPrice.shift();//删除数组中第一条数据
    },
    async getImgList() {
      const {data: res} = await this.$http.get('/HistoryOrders/TopCatsSaleCount')
      if(res === {})
        this.$message.error('获取图表信息为空')
      else {
        let temp = []
        temp[0] = 'sales'
        for(let i=0; i<6; i++){
          temp.push(parseInt(res.data[0].data[i].start_time.split('-')[1]).toString())
        }
        this.dataset.source.push(temp)
        // console.log(this.dataset)

        for(let i=0; i<res.data.length; i++){
          temp = []
          temp.push(res.data[i].name)
          for(let j=0; j<6; j++){
            temp.push(res.data[i].data[j].count)
          }
        this.dataset.source.push(temp)
        }
        this.createImg()
      }
    }

  },

}
</script>

<style scoped>

</style>
