<!-- 
  商家地理位置分布
 -->
<template>
  <div class="chart-container" @dblclick="returnChinaMap">
    <div>
      <el-dropdown style="padding-right: 5px">
        <span class="el-dropdown-link">
            切换<i class="el-icon-caret-bottom el-icon--right"></i>
        </span>
        <el-dropdown-menu slot="dropdown">
            <el-dropdown-item class="clearfix" @click.native="ChangeCondition(false)">供应商分布</el-dropdown-item>
            <el-dropdown-item class="clearfix" @click.native="ChangeCondition(true)">按供货筛选</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <el-button icon="el-icon-plus" circle @click="ChangeAddState(true)"></el-button>
    </div>

    <div class="chart-chart" ref="map_ref" v-show="!valueSwitch"></div>

    <div v-show="valueSwitch" style="padding-top: 5px">
      <el-card class="box-card">
        <!--按钮区域-->
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input placeholder="请输入名称或电话或商品编号" v-model="inputCondition" clearable>
              <el-button slot="append" icon="el-icon-search"></el-button>
            </el-input>
          </el-col>

          <!-- <el-col :span="3"> -->
            <!-- <el-button class="gutter" type="primary" @click="addUserSee = true">添加供应商</el-button> -->
          <!-- </el-col> -->
          <el-col :span="3">
            <el-button icon="el-icon-download" circle></el-button>
            <!-- <el-button class="gutter" type="primary" @click="downExcel" :loading="downloadLoading">下载表格</el-button> -->
          </el-col>
        </el-row>
        <!--供应商列表-->
        <el-table>
          <el-table-column type="index"></el-table-column>
          <el-table-column label="名称" prop="name"></el-table-column>
          <el-table-column label="电话" prop="mobile"></el-table-column>
          <el-table-column label="地区" prop="area"></el-table-column>
          <el-table-column label="供应项目" prop="provide"></el-table-column>
          <el-table-column label="可执行操作">
            <template>
              <el-button type="primary" icon="el-icon-edit" size="mini"></el-button>
              <el-button type="danger" icon="el-icon-delete" size="mini" ></el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
    <el-dialog title="新增供货商" :visible.sync="addSupplierSee" width="50%" @close="ChangeAddState(false)">
      <el-form :model="addSupplierForm" :rules="editSupplierRules" :label-width="formLabelWidth">
        <el-form-item label="供货商名称" prop="name">
          <el-input v-model="addSupplierForm.name" autocomplete="off" clearable></el-input>
        </el-form-item>
        <el-form-item label="联系电话" prop="mobile">
          <el-input v-model="addSupplierForm.mobile" autocomplete="off" clearable></el-input>
        </el-form-item>
        <el-form-item label="合约起始日期" prop="sign_start">
          <!-- style="float:left" -->
          <el-date-picker value-format="yyyy-MM-dd" v-model="addSupplierForm.sign_start" type="date" placeholder="请选择日期"/>
          <!-- style="width:180px;" -->
        </el-form-item>
        <el-form-item label="合约截止日期" prop="sign_end">
          <el-date-picker value-format="yyyy-MM-dd" v-model="addSupplierForm.sign_end" type="date" placeholder="请选择日期"/>
        </el-form-item>
        <el-form-item label="供应商地址" prop="address">
          <el-cascader class="width" placeholder="北京市 / 朝阳区" v-model="addSupplierForm.address" :options="cityData" :props="{ expandTrigger: 'hover',value:'value',label:'label',children:'children' }" clearable></el-cascader>
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="AddSupplier">确定</el-button>
      </span>
    </el-dialog>

    <el-drawer :title="drawerTitle" :visible.sync="drawer" >
      <!-- <el-collapse :v-model="activeName" accordion class="el-collapse-map">
        <el-collapse-item title="" :name=1>
        </el-collapse-item>
        <el-collapse-item title="" :name=2>
        </el-collapse-item>
        <el-collapse-item title="" :name=3>
        </el-collapse-item>
        <el-collapse-item title="" :name=4>
        </el-collapse-item>
      </el-collapse> -->
    </el-drawer>
  </div>
</template>


<script>
import '../../assets/css/charts.css'
// 导入省份中文拼音map
import {getProvinceMapInfo} from '@/vender/map_utils'
import cityData from '@/vender/citydata'
// 局部引用
import axios from 'axios'
export default {
  data() {
    var checkMobile = (rule, value, callback) => {
      var regMobile = /^1\d{10}$/;// \d是现代正则表达式的简写[0-9]
      var regTelephone = /^\d{7}(?:\d{1})?$/ ;// 固定电话的区号为一般为4位，少数为3位（如北京，上海等）号码一般为7位或8位
      if (regMobile.test(value) || regTelephone.test(value))
        return callback()
      else
        return callback('请输入合法座机号或手机号')
    }
    return {
      valueSwitch: false,
      chartInstance: null,
      // 省份矢量数据缓存
      mapData: [],
      // 当前地图等级 1省 2市
      nowPosition: null,
      // numSupplier: [],
      timesMax: 20,
      timesData: [
        {name:'北京', value: 15},
        {name:'江苏', value: 4}
      ],
      drawer: false,
      activeName: 1,
      drawerTitle: null,

      // 多条件查询供应商增删改
      addSupplierSee: false,
      inputCondition: '',

      // 新增供货商表单
      addSupplierForm: {
        name: '',
        mobile: '',
        // province: '',
        // city: '',
        address: '北京市 / 朝阳区',
        sign_start: '',
        sign_end: '',
      },
      formLabelWidth: '120px',
      cityData,
      editSupplierRules: {
        name: [
          { required: true, message: '请输入供应商名称', trigger: 'blur' }],
        mobile: [
          { required: true, message: '请输入联系方式', trigger: 'blur' },
          { validator: checkMobile, trigger: 'blur' }],
        sign_start: [
          // blur失去焦点，change数据改变
          { required: true, message: '请输入合约开始日期', trigger: 'blur'}],
        sign_end: [
          { required: true, message: '请输入合约截止日期', trigger: 'blur'}],
        address: [
          { type: 'array', required: true, message: '请选择地址', trigger: 'change'}], 
      },
    }
  },
  mounted() {
    this.initChart()
    // this.getData()
    window.addEventListener('resize', this.screenAdapter)
    this.screenAdapter()// 初始效果
  },
  methods: {
    async initChart() {
      this.chartInstance = this.$echarts.init(this.$refs.map_ref)
      const ChinaJson = await axios.get('http://localhost:8080/static/map/China.json')
      // console.log(ChinaJson)
      this.$echarts.registerMap('China',ChinaJson.data)

      const initOption = {
        animation: true,
        title: {
          text:'供应商分布',
          left: 20,
          top: 20
        },
        geo: {
          type: 'map',
          map: 'China',
          top: '5%',
          bottom: '5%',
          itemStyle: {
            // areaColor: 'green'
          },
          roam: true,// 拖动缩放 太偏需要返回中心点
          label: {
            show: true
          },
          // center: []
        },
        series: [
          {
            data: this.timesData,
            geoIndex: 0,// 关联series和geo0
            type: 'map'
          }
        ],
        tooltip: {// 没有series不显示
            trigger: 'item',
            showDelay: 0,
            transitionDuration: 0.2,
            formatter: function (params) {
              // console.log(params)
              return params.name + Number(isNaN(params.value)?0:params.value)
            }
        },
        visualMap: {
            bottom: 40,
            min: 0,
            max: this.timesMax,
            inRange: {
                color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
            },
            text: ['High', 'Low'],// 文本，默认为数值文本
            calculable: true// 滑块
        },
      }
      this.chartInstance.setOption(initOption)
      this.nowPosition = 1
      // **************地图点击事件**************
      // 点击进入某省
      this.chartInstance.on('click', async (arg)=>{
        // 判断当前是否是China 可进入下一级查询
        if (this.nowPosition != 1) {
          // 具体某个省直接显示该省下所有供应商
          // console.log(arg.name)
          this.SuppliersDrawer(arg.name)
          return
        }
        this.nowPosition = 2
        // console.log(arg)
        // 中文省份对应拼音 map
        const provinceIfo = getProvinceMapInfo(arg.name)
        // console.log(provinceIfo)
        if (!this.mapData[provinceIfo.key]) {
          // alert(12345)
          const regionJson = await axios.get('http://localhost:8080/'+provinceIfo.path)
          // console.log(regionJson)
          this.mapData[provinceIfo.key] = regionJson.data
          // 注册一次 string就可用
          this.$echarts.registerMap(provinceIfo.key, regionJson.data)
        }
        const newOption = {
          title: {
            text: arg.name+'供应商分布',
            subtext: '双击返回大地图'
          },
          geo: {
            map: provinceIfo.key
          },
        }
        this.chartInstance.setOption(newOption)
      })
      // 监听双击dbclick返回China
    },
    returnChinaMap() {
      const returnOption = {
        title: {
          text:'供应商分布',
          subtext: ''
        },
        geo: {
          map: 'China',
          // center: []
        }
      }
      this.chartInstance.setOption(returnOption)
      this.nowPosition = 1
    },
    getData() {
      // 基于前端vue环境 http://localhost:8080/static/map/China.json
      // Promise对象await解析 async
      
      // jQuery ajax获取地图矢量数据 ../../assets/json/China.json
      // $.get('../../assets/json/China.json',function(ChinaJson){
      //   console.log(ChinaJson)
      //   this.mapData=ChinaJson
      // })

      // axios.defaults.baseURL = 'http://127.0.0.1:5000'
      // this.$http.get('src/assets/json/China.json').then(function(res){
      //     console.log(res);
      // });

    },
    // 更新图表
    updateChart() {

      const newOption = {}
      this.chartInstance.setOption(newOption)
    },
    screenAdapter() {
      const titleFontSize = this.$refs.map_ref.offsetWidth / 100 * 2.5
      // alert('size: '+titleFontSize)
      const adaptOption = {
        title: {
          textStyle: {
            fontSize: titleFontSize
          }
        }
      }
      this.chartInstance.setOption(adaptOption)
      this.chartInstance.resize()
    },
    SuppliersDrawer(cityName) {
      console.log(cityName)
      this.drawer = true
      this.drawerTitle = cityName
    },
    ChangeCondition(state) {
      this.valueSwitch = state
      // console.log(state)
    },
    ChangeAddState(state) {
      this.addSupplierSee = state
      // alert(this.addSupplierSee)
    },
    AddSupplier() {
      // 添加成功关闭对话窗口
      // this.ChangeAddState(false)
      alert(12)
      alert(this.addSupplierForm.address)
    }
  }
}
</script>