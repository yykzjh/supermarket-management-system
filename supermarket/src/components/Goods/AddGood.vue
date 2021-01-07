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
      <el-steps :space="300" :active="activeIndex - 0" finish-status="success" align-center>
        <el-step title="基本信息"></el-step>
        <el-step title="商品描述"></el-step>
        <el-step title="商品图片"></el-step>
        <el-step title="完成"></el-step>
      </el-steps>
      <!--tab栏区域-->
      <el-form :model="addForm" :rules="addFormRules" ref="ruleFormRef"
               label-position="top" label-width="100px" class="demo-ruleForm">
        <el-tabs v-model="activeIndex" :tab-position="'left'" :before-leave="beforeTabLeave">
          <el-tab-pane label="基本信息" name="0">
            <el-form-item label="商品名称" prop="">
              <el-input v-model="addForm.name"></el-input>
            </el-form-item>
            <el-form-item label="商品种类">
              <el-cascader
                v-model="addForm.parent" width="50px"
                :options="cateList" @change="handleChange"
                :props="{ expandTrigger: 'hover', checkStrictly: true, value:'id',label:'name',children:'children' }">
              </el-cascader>
            </el-form-item>
          </el-tab-pane>

          <el-tab-pane label="商品图片" name="1">
            <!-- action表示图片要上传到的API地址-->
            <el-upload
              action="http://127.0.0.1:5000/Goods/NewGood"
              :on-preview="handlePreview"
              :on-remove="handleRemove" :headers="headerObj"
              list-type="picture" :on-success="handleSuccess">
              <el-button size="small" type="primary">点击上传</el-button>
              <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
            </el-upload>
          </el-tab-pane>

          <el-tab-pane label="商品描述" name="2">
            <!--富文本编辑器-->
            <quill-editor v-model="addForm.intro"></quill-editor>
            <el-button type="primary" @click="addGood">添加商品</el-button>
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
      handlePreview(file) { // 预览图片
        // console.log(file) // 可以看到图片的url
        this.previewPath = file.response.data.url
      },
      handleRemove(file) { // 点击移除图片的动作
        // console.log(file)
        this.addForm.icon = ''
      },
      handleSuccess(response) { // 监听图片上传成功
        // 1. 拼接得到一个图片信息对象
        this.addForm.icon = response.data.tmp_path
        // 2. 将图片信息对象push到pics数组中
        console.log(this.addForm)
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
      addGood() {
        this.console(this.addForm)
      }
    }
  }
</script>

<style lang="less" scoped>

</style>
