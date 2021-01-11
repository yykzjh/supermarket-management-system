<template>
  <div>
    <el-alert
      title="请填写必要信息及上传用户照片"
      type="warning"
      closable center style="width: 70%; margin: auto">
    </el-alert>
    <el-card style="margin: auto; width: 70%; margin-top: 15px">
      <el-steps :space="300" :active="activeIndex - 0" finish-status="success" align-center>
        <el-step title="基本信息"></el-step>
        <el-step title="个人照片"></el-step>
        <el-step title="完成"></el-step>
      </el-steps>
      <el-form :model="registerForm" :rules="registerFormRules" ref="registerFormRef"
               label-position="top" label-width="100px">
        <el-tabs v-model="activeIndex" :tab-position="'left'">
          <el-tab-pane label="基本信息" name="0">
            <el-form-item prop="username" label="工号">
              <el-input v-model="registerForm.username"></el-input>
            </el-form-item>
            <el-form-item prop="name" label="姓名">
              <el-input v-model="registerForm.name"></el-input>
            </el-form-item>
            <el-form-item prop="password" label="密码">
              <el-input v-model="registerForm.password"></el-input>
            </el-form-item>
            <el-form-item prop="mobile" label="联系方式">
              <el-input v-model="registerForm.mobile"></el-input>
            </el-form-item>
            <el-row>
              <el-col :span="8"><div class="grid-content">
                <el-form-item prop="gender" label="性别">
                  <el-select v-model="registerForm.gender" placeholder="请选择">
                    <el-option v-for="item in [{value: '男', label: '男'}, {value: '女', label: '女'}]"
                               :key="item.value"
                               :label="item.label"
                               :value="item.value">
                    </el-option>
                  </el-select>
                </el-form-item>
              </div></el-col>

              <el-col :span="8"><div class="grid-content">
                <el-form-item label="地区">
                  <el-cascader
                    v-model="registerForm.area"
                    :options="citydata"
                    :props="{ expandTrigger: 'hover',value:'value',label:'label',children:'children' }"
                  ></el-cascader>
                </el-form-item>
              </div></el-col>

              <el-col :span="8"><div class="grid-content">
                <el-form-item label="生日" >
                  <el-date-picker value-format="yyyy-MM-dd HH:mm:ss" v-model="registerForm.birthday" type="date" placeholder="请选择日期" />
                </el-form-item>
              </div></el-col>
            </el-row>
          </el-tab-pane>

          <el-tab-pane label="个人照片" name="1">
            <div class="user-icon">
              <video width="320" height="240" ref="videoDom" id="video" preload autoplay loop muted></video>
              <canvas width="320" height="240" ref="canvasDOM"></canvas>
            </div>
            <div>{{loding}}</div>
            <el-button class="primary" @click="initTracker">开启摄像头</el-button>

            <el-button type="success" @click="registerUser">开始注册</el-button>
          </el-tab-pane>
        </el-tabs>
      </el-form>
    </el-card>
  </div>
</template>

<script>
  import citydata from '../vender/citydata'
  require('tracking/build/tracking-min.js')
  require('tracking/build/data/face-min.js')
  export default {
    name: 'testTracking',
    data() {
      var checkMobile = (rule, value, callback) => {
        var regMobile = /^1[0-9]{10}$/;
        if (regMobile.test(value))
          return callback()
        else
          return callback('请输入合法手机号')
      }
      return {
        registerForm: {
          "name": '',
          "face": '',
          "username": '',
          "password": '',
          "gender": '',
          "birthday": '2000-06-22 00:00:00',
          "mobile": '',
          "area": '',
          "role_id": 1,
          "salary": 5000,
        },
        citydata,
        activeIndex: 0,
        registerFormRules: {
          username: [{required: true, message: '请输入商品名称', trigger: 'blur'}],
          name: [{required: true, message: '请输入商品名称', trigger: 'blur'}],
          password: [{required: true, message: '请输入商品名称', trigger: 'blur'},
            { min: 6, max: 15, message: '长度在 6 到 15 个字符', trigger: 'blur' }],
          mobile: [
            { required: true, message: '请输入手机号', trigger: 'blur' },
            { validator: checkMobile, trigger: 'blur' }]
        },
        count: 0,
        isdetected: '请您保持脸部在画面中央',
        loding: ''
      }
    },
    methods: {
      async registerUser() {
        console.log(this.registerForm)
        this.registerForm.area = this.registerForm.area.toString()
        const {data : res} = await this.$http.post('/Users/Register', this.registerForm)
        if(res.StatusCode === 200) {
          this.$message.success('注册成功')
          this.$router.replace({path: '/login'})
        }
        else{
          this.$message.error(res.msg)
        }

      },
      initTracker(){
        // alert('进来了')
        // alert(navigator.mediaDevices)
        // 启用摄像头,这一个是原生调用摄像头的功能,不写的话有时候谷歌浏览器调用摄像头会失败
        navigator.mediaDevices
          .getUserMedia({video: true,audio: true})
          .then(this.getMediaStreamSuccess)
          .catch(this.getMediaStreamError)

        this.context  = this.canvas.getContext('2d')

        // 初始化tracking参数
        this.tracker = new tracking.ObjectTracker("face");
        this.tracker.setInitialScale(4);
        this.tracker.setStepSize(2);
        this.tracker.setEdgesDensity(0.1);
        this.tracker.on("track", event => {
          this.onTracked(event);
        });

        // tracking启用摄像头,这里我选择调用原生的摄像头
        // tracking.track(this.video, this.tracker, { camera: true });

        // 如果是读取视频，可以用trackerTask.stop trackerTask.run来暂停、开始视频
        this.trackerTask = tracking.track(this.video, this.tracker);
      },
      // 监听中
      onTracked(event){
        // 判断终止条件, stop是异步的，不返回的话，还会一直截图
        if (this.count >= 21) {
          this.onStopTracking();
          return;
        }

        // 画框框
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        event.data.forEach(rect => {
          this.context.lineWidth = 1;
          this.context.strokeStyle = "#a64ceb";
          //'#a64ceb';
          this.context.strokeRect(rect.x, rect.y, rect.width, rect.height);
          this.context.font = "11px Helvetica";
          this.context.fillStyle = "#fff";
          // 截图

          if (event.data.length > 0 && this.count <= 20) {
            if (this.count < 0) {
              this.count = 0
            }
            this.count += 1
            if (this.count > 20) {
              this.isdetected = '已检测到人脸，正在识别'
              this.getPhoto()
            }
          } else {
            this.count -= 1
            if (this.count < 0){
              this.isdetected = '请您保持脸部在画面中央'
            }
          }


        });
        // 视频中心展示文字
        this.context.fillText(this.isdetected, 100,30);
      },
      // 停止监听
      onStopTracking() {
        this.trackerTask.stop();
        this.video.pause();
        // 关闭摄像头
        this.video.srcObject = null
        window.stream.getTracks().forEach(track => track.stop())

      },
      // 获取人脸照片
      getPhoto(){
        this.isdetected = ''
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        let video = document.getElementById('video')
        this.context.drawImage(video, 0,0, this.canvas.width, this.canvas.height)
        let dataUrl = this.canvas.toDataURL('image/jpeg', 1);
        this.imgbase64 = dataUrl.replace(/^data:image\/\w+;base64,/, "");
        // 开始人脸识别
        this.postFace()

      },
      // 人脸验证
      postFace(){
        this.loding = '正在识别中,请稍后................'
        this.registerForm.face = this.imgbase64
        this.imgbase64 = ''
        this.loding = ''
      },
      // 视频流启动
      getMediaStreamSuccess(stream) {
        window.stream = stream
        this.video.srcObject = stream
      },
      // 视频媒体流失败
      getMediaStreamError(error) {
        alert('视频媒体流获取错误' + error)
      },
    },
    mounted() {
      this.video = this.$refs.videoDom
      this.canvas = this.$refs.canvasDOM
    },
    destroyed() {

    }
  }
</script>
