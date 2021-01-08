<!--单页面组件-->
<template>
  <div class="login_container">
    <div class="login_box">
      <!-- 头像区-->
      <div class="avatar_box">
        <img src="../assets/logo.png" alt="logo">
      </div>
      <!--登录表单区 v-model是双向绑定对象 :model是单向绑定对象-->
      <el-form ref="loginFormRef" :model="loginForm" :rules="loginFormRules" label-width="0px" class="login_form">
        <!--用户名-->
        <el-form-item prop="username">
          <el-input v-model="loginForm.username" prefix-icon="iconfont icon-user">
          </el-input>
        </el-form-item>
        <!--密码-->
        <el-form-item prop="password">
          <el-input v-model="loginForm.password" prefix-icon="iconfont icon-3702mima" type="password"></el-input>
        </el-form-item>
        <!--按钮区-->
        <el-form-item class="btns">
          <el-button type="primary" @click="login">登录</el-button>
          <el-button type="info" @click="resetLoginForm">重置</el-button>
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
        loginForm: {
          username: '2017040380',
          password: '123456'
        },
        // 表单的验证规则对象
        // 首先在表单外部声明rules 而后再将每一个规则赋给具体的元素，例如第一个输入文本框，给它赋值一个prop
        loginFormRules: {
          // 验证用户名是否合法
          username: [
            { required: true, message: '请输入登录用户名', trigger: 'blur' },
            { min: 3, max: 10, message: '长度在 3 到 10 个字符', trigger: 'blur' }
          ],
          // 验证密码是否合法
          password: [
            { required: true, message: '请输入登录密码', trigger: 'blur' },
            { min: 6, max: 15, message: '长度在 6 到 15 个字符', trigger: 'blur' }
          ]
        }
      }
    },
    methods: {
      resetLoginForm () {
        console.log(this); // this指向当前组件的实例对象，也就是ref绑定的那个
        // this.$refs.loginFormRef 表示表单的引用对象
        this.$refs.loginFormRef.resetFields();
      },
      login () {
        // 表单登录前的预验证，拿到表单的引用对象，调用validate函数进行预校验
        /*
        this.$refs.loginFormRef.validate(
          function (valid) {
            console.log(valid);
          }
        )
        */
        // 匿名内部类方式
        // 返回promise对象的话，可使用async await等简化操作
        this.$refs.loginFormRef.validate(async valid => {
          const {data: res}  = await this.$http.post('/Users/Login', this.loginForm);
          console.log(res)
          // console.log(res);
          if (res.StatusCode === 200){
            this.$message.success('登陆成功')
            window.sessionStorage.setItem('token', res.token);
            window.sessionStorage.setItem('role_id', res.role_id);
            this.$router.push('/home');
          }
          else
            return this.$message.error('登录失败')
          // 1.将登陆成功之后的token，保存到客户端的sessionStorage中
          // 1.1 项目中除了登录之外其他的API接口，必须在登陆之后才能访问
          // 1.2 token只应在当前网站打开期间生效，所以将token保存在sessionStorage中
          // 2 通过编程式导航跳转到后台主页，路由地址是 /home

        })
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
    height: 300px;
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
