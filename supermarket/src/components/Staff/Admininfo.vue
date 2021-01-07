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
          <el-input placeholder="请输入账号" v-model="userName" clearable @clear="getUserList">
            <el-button slot="append" icon="el-icon-search" @click="searchUser"></el-button>
          </el-input>
        </el-col>
        <el-col :span="3">
          <el-button class="gutter" type="primary" @click="addUserSee = true">添加用户</el-button>
        </el-col>
        <el-col :span="3">
          <el-button class="gutter" type="primary" @click="downExcel" :loading="downloadLoading">下载表格</el-button>
        </el-col>
      </el-row>
      <!--用户列表区域-->
      <el-table id="example" :data="userList.slice((pagenum-1)*pagesize, pagenum*pagesize)" border stripe>
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
            <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteUser(scope.row.id)"></el-button>
          </template>
        </el-table-column>
      </el-table>

      <!--分页区域-->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pagenum"
        :page-sizes="[1, 2, 5, 10]"
        :page-size="pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total">
      </el-pagination>
    </el-card>

  <!-- 修改用户密码的对话框 -->
    <el-dialog
      title="修改用户密码"
      :visible.sync="editPassSee"
      width="50%" @close="cancelEdit">
      <el-form :model="editForm" :rules="editFormRules" ref="editFormRef" label-width="70px">
        <el-form-item label="用户名">
          <el-input v-model="editForm.name" disabled></el-input>
        </el-form-item>
        <el-form-item label="用户id">
          <el-input v-model="editForm.id" disabled></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="editForm.password"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editPassSee = false">取消</el-button>
        <el-button type="primary" @click="editUser">确定</el-button>
      </span>
    </el-dialog>
  <!--增加新用户的对话框, 此部分关于表单验证有点问题-->
    <el-dialog
      title="增加新用户"
      :visible.sync="addUserSee"
      width="50%" @close="cancelAdd">
      <el-form :model="addUserForm" :rules="editFormRules" ref="addUserFormRef" label-width="90px">
        <el-form-item label="用户id">
          <el-input v-model="addUserForm.username"></el-input>
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="addUserForm.name"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="addUserForm.password"></el-input>
        </el-form-item>
        <el-form-item label="联系方式" prop="mobile">
          <el-input v-model="addUserForm.mobile"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-radio v-model="addUserForm.gender" label="男">男</el-radio>
          <el-radio v-model="addUserForm.gender" label="女">女</el-radio>
        </el-form-item>
        <el-form-item label="生日" >
          <el-date-picker value-format="yyyy-MM-dd" v-model="addUserForm.birthday" type="date" placeholder="请选择日期" />
        </el-form-item>
        <el-form-item label="地区">
          <el-cascader
            v-model="addUserForm.area"
            :options="citydata"
            :props="{ expandTrigger: 'hover',value:'value',label:'label',children:'children' }"
          ></el-cascader>
        </el-form-item>
        <el-form-item label="薪资">
          <el-input v-model="addUserForm.salary"></el-input>
        </el-form-item>
        <el-form-item label="权限">
          <el-radio v-model="addUserForm.role_id" label=1>员工</el-radio>
          <el-radio v-model="addUserForm.role_id" label=2>管理员</el-radio>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addUserSee = false">取消</el-button>
        <el-button type="primary" @click="addUser">确定</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
  import citydata from '../../vender/citydata'
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
      addUserSee: false,
      citydata,
      pagesize: 3,
      pagenum: 1,
      total: 0,
      addUserForm: {
        "username": '', "password": '', "name": '', "gender": '', "birthday": '',
        "mobile": '', "area": '', "salary": 0, "role_id": 1
      },
      editForm: {},
      editFormRules: {
        id: [
          { required: true, message: '请输入用户id', trigger: 'blur'}],
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 10, message: '长度在3到10个字符之间', trigger: 'blur' }],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 15, message: '长度在6到15个字符之间', trigger: 'blur' }],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { validator: checkMail, trigger: 'blur' }],
        mobile: [
          { required: true, message: '请输入手机号', trigger: 'blur' },
          { validator: checkMobile, trigger: 'blur' }]
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
      this.total = this.userList.length
      // console.log(this.userList)
    },
    async searchUser() {
      const {data: res} = await this.$http.get('/Users/OneUser', {
        params: {
          username: this.userName
        }
      })
      this.userList = []
      this.userList[0] = res.user
      if(this.userList[0].role_id == 3) // 超级管理员不显示
        this.userList = []
      // console.log(this.userList)
    },
    // 添加新用户
    async addUser() {
      // console.log(this.addUserForm)
      this.$refs.addUserFormRef.validate(async valid => {
        if(!valid){
          this.$message.error("表单填写有误，请填写必填项")
          return ;
        }
        else {
          // 将地区数组转化为字符串
          this.addUserForm.area = this.addUserForm.area.toString()
          this.addUserForm.salary = parseInt(this.addUserForm.salary)
          this.addUserForm.role_id = parseInt(this.addUserForm.role_id)
          console.log(this.addUserForm)
          const {data: res } = await this.$http.post('Users/NewUser', this.addUserForm)
          if(res.StatusCode !== 200)
            this.$message.error('添加用户失败')
          else {
            this.$message.success('添加用户成功')
            this.getUserList()
            this.addUserSee = false
            this.addUserForm = {}
          }
        }
      })
    },
    // 取消添加新用户
    cancelAdd() {
      this.$refs.addUserFormRef.resetFields();
      this.addUserForm = {}
    },
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
    // 取消添加新用户
    cancelEdit() {
      this.$refs.editFormRef.resetFields();
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
    // 删除用户
    async deleteUser(id){
      const res = await this.$confirm('此操作将永久删除该用户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).catch(err => {
        return err
      })

      if (res !== 'confirm') return this.$message.info('取消删除')
      else {
        const { data: mess } = await this.$http.get('Users/RestUser',
          { params: { username: id }})
        if (mess.StatusCode !== 200) return this.$message.error('删除用户失败')
        else {
          this.$message.success('删除用户成功')
          this.getUserList()
        }
      }
    },
    // 分页的大小变化
    handleSizeChange(newSize) {
      this.pagesize = newSize;
    },
    // 分页的页面变化
    handleCurrentChange(newCurr){
      this.pagenum = newCurr
    },
    // 下载用户表
    downExcel () {
      this.downloadLoading = true
      import("../../vender/Export2Excel").then(excel => {
        const tHeader = [
          "姓名", "性别", "电话", "地区", "角色"
        ]
        const filterVal = [
          "name", "gender", "mobile", "area", "role_id"
        ]
        const data = this.formatJson(filterVal)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: "员工信息表"
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal) {
      return this.userList.map(v =>
        filterVal.map(j => {
          if(j === "role_id"){
            // console.log(v[j])
            return v[j] == 1 ? "员工" : "管理员";
          }else {
            return v[j];
          }
        })
      );
    },
  }
}
</script>

<style scoped>

</style>
