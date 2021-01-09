<template>
  <div>
    <!--面包屑导航-->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>商品管理</el-breadcrumb-item>
      <el-breadcrumb-item>商品信息</el-breadcrumb-item>
    </el-breadcrumb>
    <!--商品列表-->

    <el-card class="box-card">
      <el-row :gutter="30">
        <el-col>
          <el-button class="gutter" type="primary" @click="addCateSee = true">添加分类</el-button>
          <el-button class="gutter" type="primary" @click="addGood">添加商品</el-button>
        </el-col>
      </el-row>

      <el-table id="example" :data="goodList" border stripe>
        <el-table-column type="expand">
          <template slot-scope="scope">
            <el-row :class="['bdbottom', i1===0 ? 'bdtop': '', 'vcenter']" v-for="(item1, i1) in scope.row.children" :key="item1.id">
              <!--渲染一级商品分类-->
              <el-col :span="5">
                <el-tag :closable="item1.children.length == 0 ? true: false" @close="deleteCat(item1.id)">{{item1.name}}</el-tag>
                <i class="el-icon-caret-right"></i>
              </el-col>
              <el-col :span="19">
                <!--渲染二级商品分类-->
                <el-row :class="[i2 === 0 ? '' : 'bdtop', 'vcenter']" v-for="(item2, i2) in item1.children" :key="item2.id">
                  <el-col :span="6">
                    <el-tag type="success" :closable="item2.children.length == 0 ? true: false" @close="deleteCat(item2.id)">{{item2.name}}</el-tag>
                    <i class="el-icon-caret-right"></i>
                  </el-col>
                  <el-col :span="18">
                    <el-tag @click="jumpToInfo(item3.id)" type="warning" v-for="(item3, i3) in item2.children" :key="item3.id" closable @close="deleteGood(item3.id)">
                      {{item3.name}}</el-tag>
                  </el-col>
                </el-row>
              </el-col>
            </el-row>
          </template>
        </el-table-column>
        <el-table-column label="商品分类" prop="name"></el-table-column>
        <el-table-column label="下含分类" prop="children.length"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="warning" icon="el-icon-setting" size="mini" @click="openSaleDialog(scope.row.id)">销售情况</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!--添加分类对话框-->
    <el-dialog title="增加商品分类" :visible.sync="addCateSee" width="50%" @close="closeCatDialog">
      <el-form :model="tempForm" ref="tempFormRef" label-width="90px">
        <el-form-item label="父级分类">
          <el-cascader
            v-model="tempForm.choseValue"
            :options="goodList"
            :props="{ expandTrigger: 'hover', checkStrictly: true, value:'id',label:'name',children:'children' }"
           ></el-cascader>
        </el-form-item>

        <el-form-item v-for="(domain, index) in tempForm.domains" :label="index === 0 ?  '添加分类':''" :key="domain.key"
                      >
          <el-input v-model="domain.value"  style="width: 60%;"></el-input>
          <el-button @click="removeDomain(domain)" style="margin-left: 10px" icon="el-icon-delete" type="warning" size="mini"></el-button>
        </el-form-item>
        <el-button type="text" @click="addDomain" style="left: 50px;" :disabled="this.tempForm.domains.length + this.tempForm.choseValue.length >= 3 ? true : false">＋ 添加子分类</el-button>
      </el-form>
      <span slot="footer" class="dialog-footer">
          <el-button @click="addCateSee = false">取消</el-button>
          <el-button type="primary" @click="AddCate">确定</el-button>
      </span>
    </el-dialog>
    <!--展示销售情况的对话框-->
    <el-dialog title="销售情况" :visible.sync="saleSee" width="50%" @open="openImg" @close="closeImg">
      <div id="newEcharts" style="width:500px;height:400px;padding-top:40px"></div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="saleSee = false">取 消</el-button>
        <el-button type="primary" @click="saleSee = false">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      goodList: [],
      totalNum: 0,
      addCateSee: false,
      saleSee: false,
      saleSeeid: 0,
      dataset: {source:[
          ['product', '2012', '2013', '2014', '2015'],
        ]},
      tempForm: { // 提交增加分类表单前的预操作
        choseValue: [],
        domains: [{ value: '', key:  1}],
      },
      addCateForm: {
        pid: 0,
        plevel: 0,
        name_list: [],
      },
      columns: [{ label: '分类名称', prop: 'name' },
        { label: '分类级别', prop: 'level', type:'template', template: 'detail'}],
    }
  },
  created () {
    this.getGoodsList()
  },
  methods: {
    async getGoodsList() {
      const {data: res} = await this.$http.get('/Goods/AllCatDetails')
      if(Object.keys(res).length == 0)
        this.$message.error('获取商品信息失败')
      else
        this.goodList = res.results
      this.totalNum = this.goodList.length
      this.setDisable(1, this.goodList, 2)
      console.log(this.goodList)
    },
    jumpToInfo(goodid) {
      this.$router.push('/goodInfo?goodid=' + goodid)
    },
    // 增加分类选框
    addDomain() {
      this.tempForm.domains.push({ value: '', key: Date.now() })
    },
    // 移除分类选框
    removeDomain(item) {
      var index = this.tempForm.domains.indexOf(item)
      if(index !== 0)
        this.tempForm.domains.splice(index, 1)
    },
    closeCatDialog() {
      this.$refs.tempFormRef.resetFields()
      this.tempForm.choseValue = []
      this.tempForm.domains = [{ value: '', key:  1}]
    },
    // 设置第四级分类，即商品不可选中
    setDisable (count, data, maxNum) {
      if (count > maxNum) {
        data.forEach(v => {
          v.disabled = true // 超过设定的最大级数,给这一集的数据添加disabled属性
        })
      } else {
        data.forEach(v => {
          v.count = count // 设置最外层数据的初始count

          if (v.children && v.children.length) {
            v.count++
            this.setDisable(v.count, v.children, maxNum) // 子级循环时把这一层数据的count传入
          }
        })
      }
    },
    async AddCate() {
      if(this.tempForm.domains[0].value === ''){
        this.$message.error('请填写必填项')
        return;
      }
      else{
        // console.log(this.tempForm)
        var len = this.tempForm.choseValue.length
        if(len === 0)
          this.addCateForm.pid = 0
        else
          this.addCateForm.pid = this.tempForm.choseValue[len-1]
        this.addCateForm.plevel = len
        for(let i=0; i<this.tempForm.domains.length; i++)
          this.addCateForm.name_list.push(this.tempForm.domains[i].value)
        // console.log(this.addCateForm)
        const {data: res} = await this.$http.post('/Goods/NewCats', this.addCateForm)
        if(res.StatusCode !== 200) {
          this.$message.error('增加商品分类失败')
          console.log(this.addCateForm)
        }
        else {
          this.$message.success('增加商品分类成功')
          this.addCateSee = false
          this.getGoodsList()
          this.tempForm.domains = [{ value: '', key:  1}],
          this.addCateForm.name_list = []
        }
      }
    },
    // 添加商品，跳转至添加商品页面
    addGood(){
      this.$router.push('/addgood')
    },
    // 删除没有子分类的类别
    async deleteCat(id){
      // console.log(id)
      const {data: res} = await this.$http.get('Goods/DeleteCat', {
        params: {catId: id}
      })
      if(res.StatusCode !== 200)
        return this.$message.error('删除分类失败')
      else{
        this.$message.success('删除分类成功')
        this.call(this.goodList, id)
        // this.getGoodsList()
      }
    },
    // 删除商品
    async deleteGood(id){
      const {data: res} = await this.$http.get('Goods/DeleteGood', {
        params: {good_id: id}
      })
      if(res.StatusCode !== 200)
        return this.$message.error('删除商品失败')
      else{
        this.$message.success('删除商品成功')
        this.call(this.goodList, id)
      }
    },
    // 递归删除children
    call(arr, tag){
      for(var i = arr.length; i>0; i--){
        if(arr[i-1].id == tag) {
          arr.splice(i - 1, 1)
        }
        else{
          if(arr[i-1].children){
            this.call(arr[i-1].children, tag)
          }
        }
      }
    },
    // 打开图片，得到展示的id值
    openSaleDialog(id) {
      this.saleSeeid = id
      this.saleSee = true
    },
    // 打开图片
    async openImg(){
      console.log(this.saleSeeid)
      const {data: res} = await this.$http.get('/Statistic/NextCatsProfits?catId=' + this.saleSeeid)
      if(res.StatusCode !== 200)
        return this.$message.error('获取销售数据失败')
      else{
        for(let i=0; i<res.data.length; i++){
          let temp = []
          temp.push(res.data[i].name, res.data[i].day_profit, res.data[i].month_profit, res.data[i].year_profit)
          this.dataset.source.push(temp)
        }
        console.log(this.dataset)
      }
      this.$nextTick(() => {
        //  执行echarts方法
        this.initEcharts()
      })
    },
    initEcharts() {
      const myChart = this.$echarts.init(document.getElementById('newEcharts'))
      var option = {
        legend: {},
        tooltip: {},
        dataset: this.dataset,
        series: [{
          name: "日利润",
          type: 'pie',
          radius: 60,
          center: ['45%', '30%']
        }, {
          name: "月利润",
          type: 'pie',
          radius: 60,
          center: ['25%', '75%'],
          encode: {
            itemName: 'product',
            value: '2013'
          }
        }, {
            name: "年利润",
            type: 'pie',
            radius: 60,
            center: ['75%', '75%'],
            encode: {
              itemName: 'product',
              value: '2014'
            }
        }]
      }
      myChart.setOption(option)
    },
    closeImg() {
      this.dataset =  {source:[
        ['product', '2012', '2013', '2014', '2015'],
      ]}
    }

  }
}
</script>

<style lang="less" scoped>
  .el-tag {
    margin: 7px;
  }
  .bdtop {
    border-top: 1px solid #eee;
  }
  .bdbottom {
    border-bottom: 1px solid #eee;
  }
  .vcenter {
    display: flex;
    align-items: center;
  }
</style>
