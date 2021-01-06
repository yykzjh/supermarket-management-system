<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>员工管理</el-breadcrumb-item>
      <el-breadcrumb-item>普通管理员页面</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
      <!--按钮区域-->
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input placeholder="请输入账号" v-model="userName" clearable @clear="searchUser">
            <el-button slot="append" icon="el-icon-search" @click="searchUser"></el-button>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="addDialogVisiable = true">添加用户</el-button>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="downExcel" :loading="downloadLoading">下载表格</el-button>
        </el-col>
      </el-row>
      <!--用户列表区域-->
      <el-table id="example" :data="userList" border stripe>
        <el-table-column type="index"></el-table-column>
        <el-table-column label="姓名" prop="name"></el-table-column>
        <el-table-column label="性别" prop="gender"></el-table-column>
        <el-table-column label="电话" prop="mobile"></el-table-column>
        <el-table-column label="地区" prop="area"></el-table-column>
        <el-table-column label="角色" prop="role_id">
          <template slot-scope="scope">
            <p v-if="scope.row.role_id == 2">管理员</p>
            <p v-if="scope.row.role_id == 1">员工</p>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="primary" icon="el-icon-edit" size="mini" @click="showeditDialog(scope.row.id)"></el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

  <!-- 修改用户密码的对话框 -->
    <el-dialog
      title="修改用户密码"
      :visible.sync="editPassSee"
      width="50%">
      <el-form :model="editForm" :rules="editRules" ref="editFormRef" label-width="70px">
        <el-form-item label="用户名">
          <el-input v-model="editForm.name" disabled></el-input>
        </el-form-item>
        <el-form-item label="用户id">
          <el-input v-model="editForm.id" disabled></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="editForm.password"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editPassSee = false">取消</el-button>
        <el-button type="primary" @click="editUser">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    // 自定义正则表达式验证用户邮箱
    var checkMail = (rule, value, callback) => {
      var regMail = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
      if (regMail.test(value))
        return callback()
      else
        return callback('请输入合法的邮箱')
    }
    var checkMobile = (rule, value, callback) => {
      var regMobile = /^1[0-9]{10}$/;
      if (regMobile.test(value))
        return callback()
      else
        return callback('请输入合法手机号')
    }
    return {
      userList: [],
      downloadLoading: false,
      userName: '',
      editPassSee: false,
      editForm: {},
      editRules: {
        password: [
          {
            required: true,
            message: '请输入密码',
            trigger: 'blur'
          }, {
            min: 6,
            max: 15,
            message: '长度在6到15个字符之间',
            trigger: 'blur'
          }],
      },
    }
  },
  created () {
    this.getUserList()
  },
  methods: {
    // 获得普通管理员及员工名单
    async getUserList() {
      const {data: res1} = await this.$http.get('Users/AllUsers',{
        params:{
          name:"admin"
        }
      })
      const {data: res2} = await this.$http.get('Users/AllUsers', {
        params: {
          name: 'staff'
        }
      })
      this.userList = res1.users.concat(res2.users)
      console.log(this.userList)
    },
    async searchUser() {
      const {data: res} = this.$http.get('/Users/OneUser', {
        params: {
          username: this.searchUser()
        }
      })
      this.userList = res.user
    },
    // 添加新用户
    addDialogVisiable() {},
    // 获得修改对话框中的数据
    async showeditDialog(id) {
      const {data: res} = await this.$http.get('/Users/OneUser', {
        params: { username: id }
      })
      this.editForm = res.user
      this.editForm.password = ''
      // console.log(this.editForm)
      this.editPassSee = true
    },
    // 提交用户修改密码表单
    async editUser() {
      const {data: res} = await this.$http.post('/Users/NewPwd', {
        "username": this.editForm.id, "password": this.editForm.password
      })
      if(res.StatusCode !== 200)
        this.$message.error('修改密码失败')
      else
        this.$message.success('修改密码成功')
    },
    // 下载用户表
    downExcel() {},
  }
}
</script>

<style scoped>

</style>
