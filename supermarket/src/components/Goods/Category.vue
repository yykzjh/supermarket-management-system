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
      <el-row>
        <el-col>
          <el-button class="gutter" type="primary" @click="addCateSee = true">添加分类</el-button>
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
    <el-dialog
      title="修改用户密码"
      :visible.sync="addCateSee"
      width="50%">
      <el-form :model="addCateForm" :rules="addCateFormRules" ref="addCateFormRef" label-width="90px">
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="addCateForm.name"></el-input>
        </el-form-item>
        <el-form-item label="父级分类" >
          <el-input v-model="addCateForm.parent"></el-input>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      goodList: [],
      totalNum: 0,
      choseValue: [],
      addCateSee: false,
      addCateForm: {
        name: '',
        level: 0,
        parent: 1,
      },
      columns: [{ label: '分类名称', prop: 'name' },
        { label: '分类级别', prop: 'level', type:'template', template: 'detail'}],
      addCateFormRules:{
        name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }] },
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
      console.log(this.goodList)
    },
    jumpToInfo(goodid) {
      this.$router.push('/goodInfo?goodid=' + goodid)
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
