<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>订单管理</el-breadcrumb-item>
      <el-breadcrumb-item>进货订单管理</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-cascader
            placeholder="选择查看分类订单"
            v-model="catId"
            :options="goodList"
            :props="{ expandTrigger: 'hover', checkStrictly: true, value:'id',label:'name',children:'children' }"
            @change="getBuyListById"
          ></el-cascader>
        </el-col>
      </el-row>
      <el-table :data="buyList" border stripe>
        <el-table-column type="index"></el-table-column>
        <el-table-column prop="good_name" label="名称"></el-table-column>
        <el-table-column prop="supplier_name" label="供应商" ></el-table-column>
        <el-table-column prop="price_in" label="进价"></el-table-column>
        <el-table-column prop="amount" label="数量"></el-table-column>
        <el-table-column prop="if_shelf" label="上架状态">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.if_shelf == true">已上架</el-tag>
            <el-tag v-if="scope.row.if_shelf == false" type="danger">未上架</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="if_finish" label="完成状态">
          <template slot-scope="scope">
            <el-switch disabled v-model="value1" v-if="scope.row.if_finish"></el-switch>
            <el-switch v-model="scope.row.if_finished" v-if="!scope.row.if_finish"
                       @change="changeState(scope.row.good_id, scope.row.supplier_id, scope.row.buildtime)"></el-switch>
          </template>
        </el-table-column>

      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      value1: true,
      buyList: [],
      goodList: [],
      value: [],
      catId: [],
    }
  },
  created() {
    this.getBuyList()
    this.getGoodsList()
  },
  methods: {
    async getBuyList() {
      const {data: res} = await this.$http.get('/PurchaseOrders/AllPurchaseOrders')
      this.buyList = res.purchaseOrders
      if(this.buyList === [])
        return this.$message.error('订单为空')
      else
        console.log(this.buyList)
    },
    async getGoodsList() {
      const {data: res} = await this.$http.get('/Goods/AllCatDetails')
      if(Object.keys(res).length == 0)
        this.$message.error('获取商品信息失败')
      else
        this.goodList = res.results
      // console.log(this.goodList)
    },
    async getBuyListById(){
      const {data: res} = await this.$http.get(
        '/PurchaseOrders/CatPurchaseOrders?catId=' + this.catId[this.catId.length-1])
      this.buyList = res.orders
    },
    async changeState(goodid, supplierid, buildtime){
      // console.log(goodid, supplierid)
      var d = new Date(buildtime);
      var resDate = d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate() + ' '
        + (d.getHours()-8) + ':' + d.getMinutes() + ':' + d.getSeconds();
      // console.log(resDate)
      const {data: res} = await this.$http.post('/PurchaseOrders/StatusToFinish', {
        "good_id": goodid,
        "supplier_id": supplierid,
        "build_time": resDate
      })
      if(res.StatusCode === 200) {
        this.$message.success('订单状态更新成功')
        this.getBuyList()
      }
    }
  }
}
</script>

<style scoped>

</style>
