<!--单页面组件-->
<template>
  <div class="login_container">
    <div class="login_box">
      <!-- 头像区-->
      <div class="avatar_box">
        <img src="../assets/logo.png" alt="logo">
      </div>
      <el-form label-width="0px" class="login_form">
        <div>
          <div class="user-icon">
            <video width="320" height="240" ref="videoDom" id="video" preload autoplay loop muted></video>
            <canvas width="320" height="240" ref="canvasDOM"></canvas>
          </div>
          <el-button @click="initTracker" style="margin: auto; display: flex; margin-bottom: 15px">人脸识别登录</el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
  require('tracking/build/tracking-min.js')
  require('tracking/build/data/face-min.js')
  // 嘴巴等特征,后期可添加
  // require('tracking/build/data/mouth-min.js')
  // require('tracking/build/data/eye-min.js')
  //var objects = new tracking.ObjectTracker(['face', 'eye', 'mouth']);
  // require('tracking/examples/assets/stats.min.js')

  export default {
    name: 'testTracking',
    data() {
      return {
        // 记录拍照到了几次
        count: 0,
        isdetected: '请您保持脸部在画面中央',
        loding: ''
      }
    },
    methods: {
      // 初始化racker
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
      async postFace(){
        this.loding = '正在识别中,请稍后................'
        const {data: res} = await this.$http.post('/Users/FaceLogin',{
          "face": this.imgbase64
        })
        console.log(res)
        if(res.StatusCode === 200){
          this.$message.success('登陆成功')
          window.sessionStorage.setItem('token', res.token);
          window.sessionStorage.setItem('role_id', res.role_id);
          this.$router.push('/home');
        }
        else {
          this.$message.error('登录失败' + res.msg)
        }
        // this.loding = ''
        // if(res.StatusCode !== 200){
        //   this.$message.error('失败')
        // }else {
        //   this.$message.success('成功')
        // }
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

<style scoped>
  .user-icon {
    position: relative;
    margin: 0 auto;
    margin-top: 10px;
    width: 360px;
    height: 360px;
  }
  .button {
    width: 90vw;
    height: 50px;
    line-height: 50px;
    margin: 0 auto;
    background-color: skyblue;
    color: white;
    text-align: center;
    border-radius: 5px;
    font-size: 16px;
  }
  video, canvas {
    position: absolute;
  }
  .login_container{
    background-color: #2b4b6b;
    height: 100%;
  }
  .login_box {
    width: 600px;
    height: 550px;
    background-color: #fff;
    border-radius: 3px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
  }
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
  }
  img {
    height: 100%;
    width: 100%;
    border-radius: 50%;
    background-color: #eee;
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
