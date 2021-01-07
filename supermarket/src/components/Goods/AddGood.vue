<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>商品管理</el-breadcrumb-item>
      <el-breadcrumb-item>添加商品</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card>
      <el-alert title="请添加商品信息" type="info" center show-icon :closable="false"></el-alert>
      <!--步骤条区域-->
      <el-steps :space="200" :active="activeIndex - 0" finish-status="success" align-center>
        <el-step title="基本信息"></el-step>
        <el-step title="商品参数"></el-step>
        <el-step title="商品属性"></el-step>
        <el-step title="商品图片"></el-step>
        <el-step title="商品内容"></el-step>
        <el-step title="完成"></el-step>
      </el-steps>
      <!--tab栏区域-->
      <el-form :model="addForm" :rules="addFormRules" ref="ruleFormRef"
               label-position="top" label-width="100px" class="demo-ruleForm">
        <el-tabs v-model="activeIndex" :tab-position="'left'" :before-leave="beforeTabLeave">
          <el-tab-pane label="基本信息" name="0">
            <el-form-item label="商品名称" prop="">
              <el-input v-model="addForm.goods_name"></el-input>
            </el-form-item>
            <el-form-item label="商品价格" prop="">
              <el-input v-model="addForm.goods_price"></el-input>
            </el-form-item>
            <el-form-item label="商品重量" prop="">
              <el-input v-model="addForm.goods_weight"></el-input>
            </el-form-item>
            <el-form-item label="商品数量" prop="">
              <el-input v-model="addForm.goods_number"></el-input>
            </el-form-item>
            <el-form-item label="商品种类">
              <el-cascader
                v-model="addForm.goods_cat" width="50px"
                :options="cateList"
                :props="{ expandTrigger: 'hover',value:'cat_id',label:'cat_name',children:'children' }">
              </el-cascader>
            </el-form-item>
          </el-tab-pane>
          <el-tab-pane label="商品参数" name="1">商品参数</el-tab-pane>
          <el-tab-pane label="商品属性" name="2">商品属性</el-tab-pane>
          <el-tab-pane label="商品图片" name="3">
            <!-- action表示图片要上传到的API地址-->
            <el-upload
              action="http://127.0.0.1:8888/api/private/v1/upload"
              :on-preview="handlePreview"
              :on-remove="handleRemove"
              list-type="picture" :headers="headerObj" :on-success="handleSuccess">
              <el-button size="small" type="primary">点击上传</el-button>
              <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
            </el-upload>
          </el-tab-pane>

          <el-tab-pane label="商品内容" name="4">商品内容</el-tab-pane>
        </el-tabs>
      </el-form>

    </el-card>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        addForm: {
          goods_name: '',
          goods_cat: [],
          goods_price: 0,
          goods_number: 0,
          goods_weight: 0,
          goods_introduction: '',
          pics: [],
          attrs: ''
        },
        choseValue: [],
        activeIndex: 0,
        addFormRules: {
        },
        cateList: [],
        headerObj: { // 图片上传组件的header请求头
          Authorization: window.sessionStorage.getItem('token')
        },
        pics: [],
        previewPath: '',
      }
    },
    created () {
      this.getCateList()
    },
    methods: {
      async getCateList() {
        const { data: res } = await this.$http.get('categories')
        if(res.meta.status !== 200)
          return this.$message.error('获取商品分类失败')
        else
          this.cateList = res.data
        console.log(this.cateList)
      },
      beforeTabLeave(activeName, oldActiveName) {
        if(oldActiveName === '0' && this.addForm.goods_cat.length !== 3){
          this.$message.error('请先完成上一步')
          return false
        }
      },
      handlePreview(file) { // 预览图片
        // console.log(file) // 可以看到图片的url
        this.previewPath = file.response.data.url
      },
      handleRemove(file) { // 点击移除图片的动作
        // console.log(file)
        // 1. 获取将要删除文件的临时路径
        const filePath = file.response.data.tmp_path
        // 2. 从pics数组中，找到图片对应的索引值
        const i = this.addForm.pics.findIndex(x => x.pic === filePath)
        // 3. 删除这个图片
        this.addForm.pics.splice(i, 1)
        // console.log(this.addForm)
      },
      handleSuccess(response) { // 监听图片上传成功
        // 1. 拼接得到一个图片信息对象
        const picInfo = { pic: response.data.tmp_path }
        // 2. 将图片信息对象push到pics数组中
        this.addForm.pics.push(picInfo)
        console.log(this.addForm)
      }
    }
  }
</script>

<style lang="less" scoped>

</style>
