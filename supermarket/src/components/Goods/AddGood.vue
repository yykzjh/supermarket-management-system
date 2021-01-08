<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item :to="{ path: '/category' }">商品管理</el-breadcrumb-item>
      <el-breadcrumb-item>添加商品</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card>
      <el-alert title="请添加商品信息" type="info" center show-icon :closable="false"></el-alert>
      <!--步骤条区域-->
      <el-steps :space="300" :active="activeIndex - 0" finish-status="success" align-center>
        <el-step title="基本信息"></el-step>
        <el-step title="商品图片"></el-step>
        <el-step title="商品描述"></el-step>
        <el-step title="完成"></el-step>
      </el-steps>
      <!--tab栏区域-->
      <el-form :model="addForm" :rules="addFormRules" ref="addFormRef"
               label-position="top" label-width="100px" class="demo-ruleForm">
        <el-tabs v-model="activeIndex" :tab-position="'left'" :before-leave="beforeTabLeave">
          <el-tab-pane label="基本信息" name="0">
            <el-form-item label="商品名称" prop="name">
              <el-input v-model="addForm.name"></el-input>
            </el-form-item>
            <el-form-item label="商品种类" prop="parent">
              <el-cascader
                v-model="addForm.parent" width="50px"
                :options="cateList" @change="handleChange"
                :props="{ expandTrigger: 'hover', checkStrictly: true, value:'id',label:'name',children:'children' }">
              </el-cascader>
            </el-form-item>
          </el-tab-pane>

          <el-tab-pane label="商品图片" name="1">
            <!-- action表示图片要上传到的API地址-->
            <input type="file" name="icon" accept="image/gif,image/jpeg,image/jpg,image/png" @change="changeImage($event)" ref="avatarInput">
          </el-tab-pane>

          <el-tab-pane label="商品描述" name="2">
            <!--富文本编辑器-->
            <quill-editor v-model="addForm.intro"></quill-editor>
            <el-button type="primary" @click="addGood" style="margin-top: 15px">添加商品</el-button>
          </el-tab-pane>
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
          name: '',
          parent: [],
          intro: '',
          icon: '',
        },
        choseValue: [],
        activeIndex: 0,
        addFormRules: {
          name: [{required: true, message: '请输入商品名称', trigger: 'blur'}],
          parent: [{required: true, message: '请选择商品种类', trigger: 'blur'}]
        },
        headerObj: { // 图片上传组件的header请求头
          Authorization: window.sessionStorage.getItem('token')
        },
        cateList: [],
        pics: [],
        previewPath: '',
      }
    },
    created () {
      this.getCateList()
    },
    methods: {
      async getCateList() {
        const { data: res } = await this.$http.get('/Goods/AllCatDetails')
        if(Object.keys(res).length == 0)
          this.$message.error('获取商品信息失败')
        else{
          this.cateList = res.results
          this.setDisable(1, this.cateList, 3)
        }
        //console.log(this.cateList)
      },
      beforeTabLeave(activeName, oldActiveName) {
        if(oldActiveName === '0' && this.addForm.parent.length !== 3){
          this.$message.error('请先完成上一步')
          return false
        }
      },
      // 设置只能选中三级分类添加商品
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
      // 设置只能选中三级分类
      handleChange(){
        if(this.addForm.parent.length !== 3)
          this.addForm.parent = []
      },
      // 修改商品图片的事件
      changeImage(e){
        var file = e.target.files[0]
        var reader = new FileReader()
        var that = this
        reader.readAsDataURL(file)
        reader.onload = function (e) {
          that.addForm.icon = this.result
        }
      },
      // 添加商品
      addGood() {
        console.log(this.addForm)
        this.$refs.addFormRef.validate( async valid => {
          if(!valid)
            return this.$message.error('请填写所添加商品的必需信息')
          else{
            var form = { name: '', parent: [], intro: '', icon: ''}
            form.name = this.addForm.name
            form.parent = this.addForm.parent[this.addForm.parent.length-1]
            form.intro = this.addForm.intro
            form.icon = this.addForm.icon
            console.log(form)
            const {data: res} = await this.$http.post('/Goods/NewGood', form)
            if(res.StatusCode !== 200)
              return this.$message.error('增加商品信息失败')
            else
              this.$message.success('增加商品信息成功')
          }
        })
      },
    }
  }
</script>

<style lang="less" scoped>

</style>
