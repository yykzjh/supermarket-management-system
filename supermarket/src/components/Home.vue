<template>
  <el-container class="home-container">
    <!--头部区域-->
    <!-- <el-header >
      
    </el-header> -->
    <!--页面主题区域-->
    <el-container>
      <!--侧边栏-->
      <el-aside :width="isCollapse ? '64px': '200px'">
        <div class="toggle-button" @click="toggleMenu"> | | | </div>
        <!--侧边栏菜单区域-->
        <el-menu
          background-color="#333744" text-color="#fff" active-text-color="#ffd04b"
          :collapse="isCollapse" :collapse-transition="false"
          :router="true" :default-active="activePath"
        >
          <el-submenu index="1">
            <template slot="title">
              <i :class="menuList[0].icon"></i>
              <span>{{menuList[0].name}}</span>
            </template>
            <el-menu-item-group>
              <template slot="title"></template>
              <el-menu-item :index="menuList[0].children[0].path">
                <template slot="title">
                  <i class="el-icon-menu"></i>
                  <span>{{menuList[0].children[0].name}}</span>
                </template>
              </el-menu-item>
              <el-menu-item :index="menuList[0].children[1].path" :disabled="roleSee">
                <template slot="title">
                  <i class="el-icon-menu"></i>
                  <span>{{menuList[0].children[1].name}}</span>
                </template>
              </el-menu-item>
            </el-menu-item-group>
          </el-submenu>

          <el-menu-item :index="menuList[1].path" :disabled="roleSee">
            <template slot="title">
              <i :class="menuList[1].icon"></i>
              <span>{{menuList[1].name}}</span>
            </template>
          </el-menu-item>

          <el-menu-item :index="item.path" v-for="(item, index) in menuList" v-if="index > 1" :key="item.id" @click="saveNavStatus(item.path)">
            <i :class="item.icon"></i>
            <span slot="title">{{item.name}}</span>
          </el-menu-item>

          <el-menu-item>
            <div>
              <img src="../assets/market.jpeg" alt="logo" class="imgg1">
              <span>超市管理系统</span>
            </div>
            <div>
              <img src="../assets/avater.gif" alt="avater" class="imgg2">
              <el-button type="info" @click="logout">退出</el-button>
            </div>
          </el-menu-item>

        </el-menu>

      </el-aside>
      <!--右侧主体-->
      <el-main>
        <!-- 路由占位符-->
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      menuList: [
        { id: 1, name: '员工信息', path: '/staff', icon: 'el-icon-user', children: [
            { id: 2, name: '超级管理员', path: '/superinfo', icon: 'el-icon-menu' },
            { id: 3, name: '普通管理员', path: '/admininfo', icon: 'el-icon-menu' },
          ] },
        { id: 2, name: '供应商信息', path: '/supplier', icon: 'el-icon-chat-line-round'},
        { id: 3, name: '商品信息', path: '/category', icon: 'el-icon-box' },
        { id: 4, name: '进货订单信息', path: '/purchase', icon: 'el-icon-truck' },
        { id: 5, name: '销售订单信息', path: '/sales', icon: 'el-icon-tickets' },
        { id: 6, name: '财务报表', path: '/statistic', icon: 'el-icon-data-line'},
      ],
      isCollapse: false,
      activePath: '',
      roleSee: true, // 根据用户角色得到用户可访问的菜单
    }
  },
  created () {
    this.getRoleId()
  },
  methods: {
    logout () {
      window.sessionStorage.clear()
      this.$router.push('/login')
    },
    toggleMenu () {
      this.isCollapse = !this.isCollapse
    },
    // 保存链接的激活状态，把route放到session中，设置跳转卡高亮
    saveNavStatus(activePath) {
      window.sessionStorage.setItem('activePath', activePath)
      this.activePath = activePath
    },
    getRoleId() { // 通过获得session中的role_id来动态加载侧边栏
      var id = window.sessionStorage.getItem('role_id')
      if(id == 3)
        this.roleSee = false
    }
  }
}
</script>

<style lang="less" scoped>
   .home-container {
     height: 100%;
   }
   .imgg1 {
     height: 40px;
     width: 40px;
     margin-left: 10px;
     border-radius: 50%;
   }
   .imgg2 {
     height: 40px;
     width: 40px;
     margin-right: 10px;
   }
  .el-header {
    background-color: #373d41;
    display: flex;
    justify-content: space-between;
    padding-left: 0;
    align-items: center;
    color: white;
    font-size: 20px;
    > div {
      display: flex;
      align-items: center;
      span {
        margin-left: 15px;
      }
    }
  }
  .el-aside {
    background-color: #333744;
    .el-menu {
      border-right: none;
    }
  }
  .el-main {
    background-color: #EAEDF1;
  }
  .iconfont {
    margin-right: 10px;
  }
  .toggle-button {
    background-color: #333744;
    font-size: 10px;
    line-height: 24px;
    color: white;
    text-align: center;
    cursor: pointer;
  }
</style>
