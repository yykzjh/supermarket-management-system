<!--单页面组件-->
<template>
  <div class="login_container">
    <div class="login_box">
      <!-- 头像区-->
      <div class="avatar_box">
        <img src="../assets/logo.png" alt="logo">
      </div>
      <!--登录表单区 v-model是双向绑定对象 :model是单向绑定对象-->
      <el-form ref="registerFormRef" :model="registerForm" :rules="registerFormRules" label-width="0px" class="login_form">
        <!--用户名-->
        <el-form-item prop="username">
          <el-input v-model="registerForm.username" prefix-icon="iconfont icon-user">
          </el-input>
        </el-form-item>
        <!--密码-->
        <el-form-item prop="password">
          <el-input v-model="registerForm.password" prefix-icon="iconfont icon-3702mima" type="password"></el-input>
        </el-form-item>

        <el-form-item prop="password" >
          <el-input v-model="repassword" prefix-icon="iconfont icon-3702mima" type="password" placeholder="请再次输入密码"></el-input>
        </el-form-item>

        <el-form-item prop="face">
          <el-button type="text">上传个人图片</el-button>
          <el-upload   action="#" ref="upload" list-type="picture" :http-request="httpRequest">
          <i class="el-icon-plus"></i>
          </el-upload>
        </el-form-item>
        <!--按钮区-->
        <el-form-item class="btns">
          <el-button type="warning" @click="registerUser">注册</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        // 登录表单的数据绑定对象
        registerForm: {
          "username": '',
          "password": '',
          "name": '',
          "gender": '',
          "birthday": "2020-11-11 00:00:00",
          "mobile": '',
          "salary": 2000,
          "area": '',
          "role_id": 2,
          "face": ''
        },
        repassword: '',
        // 表单的验证规则对象
        // 首先在表单外部声明rules 而后再将每一个规则赋给具体的元素，例如第一个输入文本框，给它赋值一个prop
        registerFormRules: {
          // 验证用户名是否合法
          username: [
            { required: true, message: '请输入注册用户名', trigger: 'blur' },
          ],
          // 验证密码是否合法
          password: [
            { required: true, message: '请输入注册密码', trigger: 'blur' },
          ],
          face: [
            { required: true, message: '请输入登录密码', trigger: 'blur' },
          ]
        }
      }
    },
    methods: {
      httpRequest(data) {
        let _this = this  // 这里要转一下是因为在下面的function里 this的指向发生了变化
        let rd = new FileReader()
        let file = data.file
        rd.readAsDataURL(file)
        rd.onloadend = function(e) {
          _this.registerForm.face = this.result
        }
      },
      async registerUser() {
        this.registerForm.face = this.registerForm.face.replace(/data:image\/.*;base64,/,'')
        if(this.registerForm.password !== this.repassword)
          this.$message.error('两次输入密码不一致，请重新输入')
        // console.log(this.registerForm)
        const {data : res} = await this.$http.post('/Users/Register', this.registerForm)
        if(res.StatusCode !== 200) {
          this.$message.error('注册失败')
          console.log(res)
        }
        else
          this.$message.success('请求成功')
      }
    }
  }
</script>

<!--scoped表示当前样式只在当前模板内生效-->
<style lang="less" scoped>
  .login_container{
    background-color: #2b4b6b;
    height: 100%;
  }
  .login_box {
    width: 450px;
    height: 500px;
    background-color: #fff;
    border-radius: 3px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);

    .avatar_box {
      height: 130px;
      width: 130px;
      border-radius: 50%;
      padding: 10px;
      box-shadow: 0 0 10px #ddd;
      position: absolute;
      left: 50%;
      transform: translate(-50%, -50%);
      background-color: #fff;
      img {
        height: 100%;
        width: 100%;
        border-radius: 50%;
        background-color: #eee;
      }
    }
  }
  .login_form {
    position: absolute;
    bottom: 0;
    width: 100%;
    padding: 0 20px;
    box-sizing: border-box;
  }
  .btns {
    display: flex;
    justify-content: flex-end;
  }
</style>
