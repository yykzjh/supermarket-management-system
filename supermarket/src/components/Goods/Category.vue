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
                <el-tag>{{item1.name}}</el-tag>
                <i class="el-icon-caret-right"></i>
              </el-col>
              <el-col :span="19">
                <!--渲染二级商品分类-->
                <el-row :class="[i2 === 0 ? '' : 'bdtop', 'vcenter']" v-for="(item2, i2) in item1.children" :key="item2.id">
                  <el-col :span="6">
                    <el-tag type="success">{{item2.name}}</el-tag>
                    <i class="el-icon-caret-right"></i>
                  </el-col>
                  <el-col :span="18">
                    <el-tag @click="jumpToInfo(item3.id)" type="warning" v-for="(item3, i3) in item2.children" :key="i3.id">
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
            <el-button type="warning" icon="el-icon-setting" size="mini">还没想好</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!--添加分类对话框-->
    <el-dialog title="增加商品分类" :visible.sync="addCateSee" width="50%">
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
        <el-button type="text" @click="addDomain" style="left: 50px;">＋ 添加同级分类</el-button>
      </el-form>
      <span slot="footer" class="dialog-footer">
          <el-button @click="addCateSee = false">取消</el-button>
          <el-button type="primary" @click="AddCate">确定</el-button>
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
    changeHandle(){
      console.log(this.choseValue)
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
        this.addCateForm.pid = this.tempForm.choseValue[len-1]
        this.addCateForm.plevel = len
        for(let i=0; i<this.tempForm.domains.length; i++)
          this.addCateForm.name_list.push(this.tempForm.domains[i].value)
        // console.log(this.addCateForm)
        const {data: res} = await this.$http.post('/Goods/NewCats', this.addCateForm)
        if(res.StatusCode !== 200)
          this.$message.error('增加商品分类失败')
        else {
          this.$message.success('增加商品分类成功')
          this.addCateSee = false
          this.getGoodsList()
        }
      }
    },
    // 添加商品，跳转至添加商品页面
    addGood(){
      this.$router.push('/addgood')
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
