<!-- 
  商家地理位置分布
 -->
<template>
  <div class="chart-container">
    <div>
      <el-breadcrumb separator="/" style="margin:0 0 0px 0;float:left;padding:13px;">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>供应商</el-breadcrumb-item>
      </el-breadcrumb>
      <el-dropdown style="padding-right: 5px">
        <span class="el-dropdown-link">
            切换<i class="el-icon-caret-bottom el-icon--right"></i>
        </span>
        <el-dropdown-menu slot="dropdown">
            <el-dropdown-item
              class="clearfix"
              @click.native="ChangeCondition(false)">供应商分布
            </el-dropdown-item>
            <el-dropdown-item
              class="clearfix"
              @click.native="ChangeCondition(true)">按供货筛选
            </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <el-button icon="el-icon-plus" circle @click="ChangeAddState(true)"></el-button>
    </div>

    <div class="chart-chart" ref="map_ref" v-show="!valueSwitch" @dblclick="returnChinaMap"></div>

    <div v-show="valueSwitch" style="padding-top: 5px">
      <el-card class="box-card">
        <!--按钮区域-->
        <el-row :gutter="20">
          <el-col :span="10">
            <el-input
              placeholder="请输入名称或电话关键字查询"
              v-model="inputCondition"
              clearable>
              <el-button
                slot="append"
                icon="el-icon-search"
                @click="ScreenSupplier">
              </el-button>
            </el-input>
          </el-col>

          <!-- <el-col :span="3"> -->
            <!-- <el-button class="gutter" type="primary" @click="addUserSee = true">添加供应商</el-button> -->
          <!-- </el-col> -->
          <el-col :span="3">
            <el-button
              icon="el-icon-download"
              circle
              @click="downExcel"
              :loading="downloadLoading">
            </el-button>
            <!-- <el-button class="gutter" type="primary" @click="downExcel" :loading="downloadLoading">下载表格</el-button> -->
          </el-col>
        </el-row>
        <!--供应商列表-->
        <el-table
          :data="supplierList.slice((pageNum-1)*pageSize, pageNum*pageSize)"
          stripe>
          <el-table-column type="index"></el-table-column>
          <el-table-column label="名称" prop="name">
            <template slot-scope="scope">
              <el-input
                v-show="scope.row.isEdit"
                v-model="scope.row.name">
              </el-input>
              <span
                v-show="!scope.row.isEdit">
                {{scope.row.name}}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="联系方式" prop="mobile">
            <template slot-scope="scope">
              <el-input
                v-show="scope.row.isEdit"
                v-model="scope.row.mobile">
              </el-input>
              <span
                v-show="!scope.row.isEdit">
                {{scope.row.mobile}}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="地区" prop="area">
            <template slot-scope="scope">
              <span>
                <!-- v-show="!scope.row.isEdit" -->
                <!-- 不隐藏当参考 -->
                {{scope.row.area}}
              </span>
              <el-cascader class="width"
                v-show="scope.row.isEdit"
                v-model="scope.row.area"
                :options="cityData"
                :props="{ expandTrigger: 'hover',value:'value',label:'label',children:'children' }">
              </el-cascader>
            </template>
          </el-table-column>
          <el-table-column label="合作起始日期" prop="sign_start">
            <template slot-scope="scope">
              <el-date-picker
                value-format="yyyy-MM-dd"
                v-show="scope.row.isEdit"
                v-model="scope.row.sign_start"
                type="date"/>
              <span
                v-show="!scope.row.isEdit">
                {{scope.row.sign_start}}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="截止日期" prop="sign_end">
            <template slot-scope="scope">
              <el-date-picker
                value-format="yyyy-MM-dd"
                v-show="scope.row.isEdit"
                v-model="scope.row.sign_end"
                type="date"/>
              <span
                v-show="!scope.row.isEdit">
                {{scope.row.sign_end}}
              </span>
            </template>
          </el-table-column>
          <!-- <el-table-column label="供应项目" prop="provide"></el-table-column> -->
          <el-table-column label="可执行操作">
            <template slot-scope="scope">
              <el-button type="close" icon="el-icon-close" size="mini" @click="CancleEdit(scope.row)" v-show="scope.row.isEdit"></el-button>
              <el-button type="success" icon="el-icon-check" size="mini" @click="SaveChange(scope.row)" v-show="scope.row.isEdit"></el-button>
              <el-button type="primary" icon="el-icon-edit" size="mini" @click="ShowEditDialog(scope.row)" v-show="!scope.row.isEdit"></el-button>
              <!-- <el-button disabled type="primary" icon="el-icon-edit" size="mini" @click="ShowEditDialog(scope.row)" v-show="!scope.row.isEdit"></el-button> -->
              <el-button type="danger" icon="el-icon-delete" size="mini" @click="DeleteSupplier(scope.row.id)" v-show="!scope.row.isEdit"></el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pageNum"
          :page-sizes="[1, 2, 5, 10]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pageTotal">
        </el-pagination>
      </el-card>
    </div>
    <el-dialog
      title="新增供货商"
      :visible.sync="addSupplierSee"
      width="50%"
      @close="ChangeAddState(false)">
      <el-form
        :model="addSupplierForm"
        :rules="editSupplierRules"
        :label-width="formLabelWidth">
        <el-form-item label="供货商名称" prop="name">
          <el-input v-model="addSupplierForm.name" autocomplete="off" clearable></el-input>
        </el-form-item>
        <el-form-item label="联系电话" prop="mobile">
          <el-input v-model="addSupplierForm.mobile" autocomplete="off" clearable></el-input>
        </el-form-item>
        <el-form-item label="合约起始日期" prop="sign_start">
          <!-- style="float:left" -->
          <el-date-picker
            value-format="yyyy-MM-dd"
            v-model="addSupplierForm.sign_start"
            type="date"
            placeholder="请选择日期"/>
          <!-- style="width:180px;" -->
        </el-form-item>
        <el-form-item label="合约截止日期" prop="sign_end">
          <el-date-picker
            value-format="yyyy-MM-dd"
            v-model="addSupplierForm.sign_end"
            type="date"
            placeholder="请选择日期"/>
        </el-form-item>
        <el-form-item label="供应商地址" prop="address">
          <el-cascader
            class="width"
            placeholder="北京市 / 朝阳区"
            v-model="addSupplierForm.address"
            :options="cityData"
            :props="{ expandTrigger: 'hover',value:'value',label:'label',children:'children' }"
            clearable>
          </el-cascader>
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
        <!-- <el-popconfirm
          confirm-button-text='好的'
          icon="el-icon-info"
          icon-color="red"
          title="请检查信息填写是否正确"
          v-show="verifyCorrect">
          <el-button type="primary" @click="AddSupplier" v-show="false"></el-button>
        </el-popconfirm> -->
        <!-- confirm-button-text='好的' -->
        <el-popconfirm
          icon="el-icon-info"
          icon-color="blue"
          :title=verifyCorrect>
        <!-- slot="reference" 很重要 没有连按钮都不显示 -->
          <el-button type="primary" slot="reference" @click="AddSupplier">确定</el-button>
        </el-popconfirm>
        <!-- <el-button type="primary" @click="AddSupplier">确定</el-button> -->
      </span>
    </el-dialog>

    <el-drawer
      :title="drawerTitle"
      :visible.sync="drawer"
      size="50%">
      <el-table
        :data="regionSupplierList.slice((pageNum-1)*pageSize, pageNum*pageSize)"
        stripe>
          <el-table-column type="index"></el-table-column>
          <el-table-column label="名称" prop="name">
            <template slot-scope="scope">
              <el-input
                v-show="scope.row.isEdit"
                v-model="scope.row.name">
              </el-input>
              <span
                v-show="!scope.row.isEdit">
                {{scope.row.name}}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="联系方式" prop="mobile">
            <template slot-scope="scope">
              <el-input
                v-show="scope.row.isEdit"
                v-model="scope.row.mobile">
              </el-input>
              <span
                v-show="!scope.row.isEdit">
                {{scope.row.mobile}}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="地区" prop="area">
            <template slot-scope="scope">
              <span>
                <!-- v-show="!scope.row.isEdit" -->
                <!-- 不隐藏当参考 -->
                {{scope.row.area}}
              </span>
              <el-cascader class="width"
                v-show="scope.row.isEdit"
                v-model="scope.row.area"
                :options="cityData"
                :props="{ expandTrigger: 'hover',value:'value',label:'label',children:'children' }">
              </el-cascader>
            </template>
          </el-table-column>
          <el-table-column label="合作起始日期" prop="sign_start">
            <template slot-scope="scope">
              <el-date-picker
                value-format="yyyy-MM-dd"
                v-show="scope.row.isEdit"
                v-model="scope.row.sign_start"
                type="date"/>
              <span
                v-show="!scope.row.isEdit">
                {{scope.row.sign_start}}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="截止日期" prop="sign_end">
            <template slot-scope="scope">
              <el-date-picker
                value-format="yyyy-MM-dd"
                v-show="scope.row.isEdit"
                v-model="scope.row.sign_end"
                type="date"/>
              <span
                v-show="!scope.row.isEdit">
                {{scope.row.sign_end}}
              </span>
            </template>
          </el-table-column>
          <!-- <el-table-column label="供应项目" prop="provide"></el-table-column> -->
          <el-table-column label="可执行操作">
            <template slot-scope="scope">
              <el-button type="close" icon="el-icon-close" size="mini" @click="CancleEdit(scope.row)" v-show="scope.row.isEdit"></el-button>
              <el-button type="success" icon="el-icon-check" size="mini" @click="SaveChange(scope.row)" v-show="scope.row.isEdit"></el-button>
              <el-button type="primary" icon="el-icon-edit" size="mini" @click="ShowEditDialog(scope.row)" v-show="!scope.row.isEdit"></el-button>
              <!-- <el-button disabled type="primary" icon="el-icon-edit" size="mini" @click="ShowEditDialog(scope.row)" v-show="!scope.row.isEdit"></el-button> -->
              <el-button type="danger" icon="el-icon-delete" size="mini" @click="DeleteSupplier(scope.row.id)" v-show="!scope.row.isEdit"></el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pageNum"
          :page-sizes="[1, 2, 5, 10]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pageTotal">
        </el-pagination>
    </el-drawer>
  </div>
</template>


<script>
import '../../assets/css/charts.css'
// 导入省份中文拼音map
import {getProvinceMapInfo} from '@/vender/map_utils'
// import {Excel} from "@/vender/Export2Excel"
import cityData from '@/vender/citydata'
// 局部引用
import axios from 'axios'
export default {
  data() {
    var checkMobile = (rule, value, callback) => {
      var regMobile = /^1\d{10}$/;// \d是现代正则表达式的简写[0-9]
      var regTelephone = /^\d{7}(?:\d{1})?$/ ;// 固定电话的区号为一般为4位，少数为3位（如北京，上海等）号码一般为7位或8位
      // console.log(12345678)
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
      nowPlace: null,
      // numSupplier: [],
      timesMax: 20,
      timesData: {
        "中国":[
          { "name": "北京", "value": 15 },
          { "name": "河北", "value": 8 }
        ],
        "北京":[
            { "name": "朝阳区", "value": 4 },
            { "name": "昌平区", "value": 11 }
        ],
        "河北":[
            { "name": "张家口市", "value": 2 },
            { "name": "唐山市", "value": 6 }
        ]
      },
      suplliersIncity: {
        "昌平区": [
          {id: 101, name: '我们做得很好',  mobile: '12345678', area: '上海 普陀区 金沙江路 1518 弄', sign_start: '2020-01-08', sign_end: '2050-01-08'},
          {id: 102,  name: '液氮供不完大公司', mobile: '04511432', area: '北京 朝阳区', sign_start: '2019-12-12', sign_end: '2077-01-01'}
        ]
      },
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
        address: '北京 / 朝阳区',
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
          { required: true, message: '请输入合约开始日期', trigger: 'blur'},
          { required: true, message: '请输入合约开始日期', trigger: 'change'}],
        sign_end: [
          { required: true, message: '请输入合约截止日期', trigger: 'blur'},
          { required: true, message: '请输入合约截止日期', trigger: 'change'}],
        address: [
          { type: 'array', required: true, message: '请选择地址', trigger: 'change'}], 
      },
      verifyCorrect: '',// 验证信息&弹出提示

      // 供应商列表
      supplierList: [],
      regionSupplierList: [],
      citysTemp: null,// 暂存place Json{name, value}
      pageSize: 5,
      pageNum: 1,
      pageTotal: 0,
      downloadLoading: false,
      initUpdateVal: '',
      nowEdit: -1,
      editTemp: null
    }
  },
  mounted() {
    this.initChart()
    this.getGlobalData()// timesData
    this.AllSupplier()
    window.addEventListener('resize', this.screenAdapter)
    this.screenAdapter()// 初始效果
  },
  methods: {
    async initChart() {
      // console.log('chart',this.timesData["中国"])
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
            data: this.timesData["中国"],
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
      this.nowPlace = '中国'
      // **************地图点击事件**************
      // 点击进入某省
      this.chartInstance.on('click', async (arg)=>{
        // 判断当前是否是China1 可进入下一级查询
        if (this.nowPosition != 1) {
          // 具体某个省直接显示该省下所有供应商
          // console.log(arg.name)
          this.SuppliersDrawer(arg.name)
          return
        }
        this.nowPosition = 2
        this.nowPlace = arg.name
        // 中文省份对应拼音 map
        const provinceIfo = getProvinceMapInfo(arg.name)
        // console.log(arg.name)
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
            subtext: '双击空白区域返回大地图'
          },
          geo: {
            map: provinceIfo.key,
            zoom: 1.2
          },
          series: [
            {
              data: this.timesData[arg.name],
              // geoIndex: 0,// 关联series和geo0
              // type: 'map'
            }
          ],
        }
        // console.log(arg.name,provinceIfo.key)
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
          zoom: 1
          // center: []
        },
        series: [
          {
            data: this.timesData["中国"],
            // geoIndex: 0,// 关联series和geo0
            // type: 'map'
          }
        ],
      }
      this.chartInstance.setOption(returnOption)
      this.nowPosition = 1
    },
    async getGlobalData() {
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
      // console.log(this.timesData)
      var ret = await this.$http.get('/Suppliers/StatisticInfo')
      if(ret.status !== 200)
        this.$message.error('Network 获取供应商数量分布失败')
      else {
        ret = ret.data
        this.timesData = ret.data
        // console.log(this.timesData["中国"])
        this.updateChart('中国')
      }
    },
    UpdateCitysValue(ops, place) {
      for (var i in this.citysTemp) {
        if(this.citysTemp[i]['name'] == place){
          this.citysTemp[i]['value'] = this.citysTemp[i]['value'] + ops
          break
        }
      }
    },
    getPlaceData(province, city, op) {
      this.citysTemp = null
      var ops = null
      console.log(province, city)
      if(op == 'add') {
        ops = 1
        this.citysTemp = this.timesData['中国']
        this.UpdateCitysValue(ops, province)

        this.citysTemp = this.timesData[province]
        this.UpdateCitysValue(ops, city)
        
      } else if(op == 'delete') {
        ops = -1
        this.citysTemp = this.timesData['中国']
        this.UpdateCitysValue(ops, province)

        this.citysTemp = this.timesData[province]
        this.UpdateCitysValue(ops, city)
      }
      // console.log(this.nowPlace)
      this.updateChart(this.nowPlace)
    },
    // 更新当前地理位置图表
    updateChart(place) {
      console.log(this.timesData[place])
      const newOption = {
        series: [
          {
            data: this.timesData[place]
          }
        ],
      }
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
    async SuppliersDrawer(cityName) {
      // console.log(cityName)
      // console.log(this.nowPlace, cityName)
      var ret = await this.$http.get('/Suppliers/SearchByPosition?province=' + this.nowPlace+"&city="+cityName)
      console.log(ret)
      if(ret.status != 200) console.log('Network 获取该城市供应商列表失败')
      else {
        var listTemp = ret.data.suppliers
        this.ListTemp2SuppliersList(listTemp, 2)
      }
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
    InitSupplier() {
      this.addSupplierForm.name = ''
      this.addSupplierForm.mobile= ''
      this.addSupplierForm.address= '北京 / 朝阳区'
      this.addSupplierForm.sign_start= ''
      this.addSupplierForm.sign_end= ''
    },
    async AddSupplier() {
      var regMobile = /^1\d{10}$/;
      var regTelephone = /^\d{7}(?:\d{1})?$/;
      // alert(this.verifyCorrect)
      // alert(this.addSupplierForm.address)
      var place = null
      // var addressTemp =
      // 切分地址为省0、市1
      if(typeof(this.addSupplierForm.address) == "string") {
        place = (this.addSupplierForm.address).split('/');
        for(var i = 0; i < place.length; i++) {
          place[i] = place[i].trim()
        }
        // console.log(place)
      } else {
        place = this.addSupplierForm.address
      }
      // console.log(place)
      const province = place[0]
      const city = place[1]
      // 检查填写数据是否合理
      if(this.addSupplierForm.name=='' || 
        this.addSupplierForm.sign_start=='' || 
        this.addSupplierForm.end_start=='' ||
        (!(regMobile.test(this.addSupplierForm.mobile) || regTelephone.test(this.addSupplierForm.mobile))) ) {
        this.verifyCorrect = '信息填写不合理，请检查一波'
        return
      }
      // console.log('content: ',this.addSupplierForm.name,this.addSupplierForm.sign_start,this.addSupplierForm.sign_end,this.addSupplierForm.mobile)

      // this.verifyCorrect = false //需要看一下不显示了但是是不是真的变成了false：不显示就是false

      var ret = await this.$http.post('/Suppliers/NewSupplier', {
        'name': this.addSupplierForm.name,
        'mobile': this.addSupplierForm.mobile,
        'sign_start': this.addSupplierForm.sign_start,
        'sign_end': this.addSupplierForm.sign_end,
        'province': province,
        'city': city
      })
      ret = ret.data
      // console.log(ret)
      if(ret.StatusCode !== 200) {// !== 同时检测它们的类型是否不相同
        this.verifyCorrect = ret.msg
      }
      else {
        this.verifyCorrect = '添加供应商成功'
        this.$message.success('添加供应商成功')
        // 添加成功关闭对话窗口
        this.ChangeAddState(false)

        this.getPlaceData(province, city, 'add')

        var tempCopy = {}
        Object.assign(tempCopy, {
          'id': ret.id,// 供应商id
          'name': this.addSupplierForm.name,
          'mobile': this.addSupplierForm.mobile,
          'sign_start': this.addSupplierForm.sign_start,
          'sign_end': this.addSupplierForm.sign_end,
          'province': province,
          'city': city,
          'area': province + city,
          'isEdit': false
        })
        // console.log('length1',this.supplierList.length)
        // 新增供货商 更新列表
        this.supplierList.push(tempCopy)
        // console.log('length2',this.supplierList.length)
        // console.log(this.supplierList)
        // 清空addSupplierForm信息
        this.InitSupplier()
      }
    },
    ListTemp2SuppliersList(listTemp, level) {
      this.pageTotal = listTemp.length
      var time
      for (var i in listTemp) {
        time = new Date(listTemp[i]['sign_start'])
        listTemp[i]['sign_start'] = time.getFullYear()+'-'+(time.getMonth()+1<10?'0'+(time.getMonth()+1):(time.getMonth()+1))+'-'+(time.getDate()<10?'0'+time.getDate():time.getDate())
        time = new Date(listTemp[i]['sign_end'])
        listTemp[i]['sign_end'] = time.getFullYear()+'-'+(time.getMonth()+1<10?'0'+(time.getMonth()+1):(time.getMonth()+1))+'-'+(time.getDate()<10?'0'+time.getDate():time.getDate())
        listTemp[i]['area'] = listTemp[i]['province'] + listTemp[i]['city']
        listTemp[i]['isEdit'] = false
      }
      if(level == 1) this.supplierList = listTemp
      else if(level == 2) this.regionSupplierList = listTemp
    },
    async AllSupplier() {
      var ret = await this.$http.get('/Suppliers/SuppliersInfo')
      // this.supplierList = [
      //   {
      //     id: 101,
      //     name: '我们做得很好',
      //     mobile: '12345678',
      //     area: '上海 普陀区 金沙江路 1518 弄',
      //     sign_start: '2020-01-08',
      //     sign_end: '2050-01-08',
      //     isEdit: false
      //   },{
      //     id: 102,
      //     name: '液氮供不完大公司',
      //     mobile: '04511432',
      //     area: '北京 朝阳区',
      //     sign_start: '2019-12-12',
      //     sign_end: '2077-01-01',
      //     isEdit: false
      //   }
      // ]
      // console.log(this.supplierList)
      var listTemp = ret.data.suppliers
      this.ListTemp2SuppliersList(listTemp, 1)
      // this.supplierList = ret.data.suppliers
      // this.pageTotal = this.supplierList.length
      // var time
      // for (var i in this.supplierList) {
      //   time = new Date(this.supplierList[i]['sign_start'])
      //   this.supplierList[i]['sign_start'] = time.getFullYear()+'-'+(time.getMonth()+1<10?'0'+(time.getMonth()+1):(time.getMonth()+1))+'-'+(time.getDate()<10?'0'+time.getDate():time.getDate())
      //   time = new Date(this.supplierList[i]['sign_end'])
      //   this.supplierList[i]['sign_end'] = time.getFullYear()+'-'+(time.getMonth()+1<10?'0'+(time.getMonth()+1):(time.getMonth()+1))+'-'+(time.getDate()<10?'0'+time.getDate():time.getDate())
      //   this.supplierList[i]['area'] = this.supplierList[i]['province'] + this.supplierList[i]['city']
      //   this.supplierList[i]['isEdit'] = false
      // }
      // console.log(this.supplierList)
    },
    async ScreenSupplier() {// 根据输入的条件筛选供应商
    if(this.inputCondition=='') return
      var ret = await this.$http.get('/Suppliers/SeachByNameOrMobile?text=' + this.inputCondition)
      var listTemp = ret.data.suppliers
      this.ListTemp2SuppliersList(listTemp, 1)
      console.log(this.supplierList)
    },
    async SaveChange(row) {// line-110
      // console.log(typeof(row.area),row.area)
      var province = null
      var city = null
      // console.log(typeof(row.area),row.area)// object用户选了 string没变过
      if(typeof(row.area) != "string") {// 重新设定地址object
        province = row.area[0]
        city = row.area[1]
        row.area = province + city
      }
      // 保存修改上传
      const ret = await this.$confirm('此操作将修改该供货商信息, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).catch(err => {
        return err
      })

      if (ret !== 'confirm') {
        this.CancleEdit(row)
        return this.$message.info('取消修改')
      }
      else {
        const { data: mess } = await this.$http.post('Suppliers/ModifySupplier',{
          'id': row.id,
          'name': row.name,
          'mobile': row.mobile,
          'province': province,
          'city': city,
          'sign_start': row.sign_start,
          'sign_end': row.sign_end
        })
        if (mess.StatusCode !== 200) return this.$message.error(mess.msg)
        else {
          // console.log(mess)
          // 更新row 重新渲染
          row.isEdit = false
          this.nowEdit = -1
          this.$message.success('修改供货商信息成功')
        }
      }
    },
    CancleEdit(row) {
      // console.log(row.id)
      if(this.editTemp.id != row.id)
        console.log('Bug正在编辑行副本和当前行id不一致')
      // 取消不修改供应商信息
      // this.ShowEditDialog(row)
      // 根据副本恢复修改前信息
      Object.assign(row,this.editTemp)
      this.nowEdit = -1//当前没有正在编辑行
      row.isEdit = false
      // ****************************************************筛选的话 id怎么排?
      // for (var i in this.supplierList) {
      //   console.log(this.supplierList[i]['id'], this.supplierList[i]['id'] == row.id)
      //   if(this.supplierList[i]['id'] == row.id){
      //     row.name = this.supplierList[i].name
      //     row.mobile = this.supplierList[i].mobile
      //     row.area = this.supplierList[i].area //province city
      //     row.sign_start = this.supplierList[i].sign_start
      //     row.sign_end = this.supplierList[i].sign_end
      //     break
      //   }
      // }
    },
    ShowEditDialog(row) {
      console.log('Show',row.id)
      if(this.nowEdit >=0 ) {
        alert('有正在编辑的条目')
        return
      }
      // 以防cancel修改 来个副本
      this.editTemp = {}
      Object.assign(this.editTemp,row)

      // console.log(row)
      // console.log(this.editTemp)
      this.nowEdit = row.id
      row.isEdit = true
    },
    DeteleSupplierFromList(id) {
      for (var i in this.supplierList) {
        if(this.supplierList[i]['id'] == id){
          this.getPlaceData(this.supplierList[i]['province'], this.supplierList[i]['city'], 'delete') // 还需判断0
          this.supplierList.splice(i,1);
          return true
        }
      }
      alert('根据id没能找到该供货商')
      return false
    },
    async DeleteSupplier(id) {
      console.log('deleteID',id)
      // this.DeteleSupplierFromList(id)

      const ret = await this.$confirm('此操作将永久删除该供货商, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).catch(err => {
        return err
      })

      if (ret !== 'confirm') return this.$message.info('取消删除')
      else {
        const { data: mess } = await this.$http.get('Suppliers/DeleteSupplier',{
          params: {
            id: id
          }
        })
        console.log(id, mess)
        if (mess.StatusCode !== 200) return this.$message.error('删除供货商失败')
        else {
          if(this.DeteleSupplierFromList(id)) this.$message.success('删除供货商成功')
        }
      }
    },
    handleSizeChange(newSize) {
      this.pageSize = newSize;
    },
    // 分页的页面变化
    handleCurrentChange(newCurr){
      this.pageNum = newCurr
    },
    // 下载供应商表
    // table筛选
    downExcel () {
      this.downloadLoading = true
      import("../../vender/Export2Excel").then(excel => {
        const tHeader = [
          "名称", "联系方式", "省", "市", "合作起始日期", "截止日期"
        ]
        const filterVal = [
          "name", "mobile", "province", "city", "sign_start", "sign_end"
        ]
        const data = this.formatJson(filterVal)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: "供应商信息表"
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal) {
      return this.supplierList.map(v =>
        filterVal.map(j => {
          return v[j];
        })
      )
    },
  }
}
</script>