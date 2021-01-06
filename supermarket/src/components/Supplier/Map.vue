<!-- 
  商家地理位置分布
 -->
<template>
  <div class="chart-container" @dblclick="returnChinaMap">
    <div class="chart-chart" ref="map_ref"></div>
  </div>
</template>


<script>
import '../../assets/css/charts.css'
// 导入省份中文拼音map
import {getProvinceMapInfo} from '@/vender/map_utils'
// 局部引用
import axios from 'axios'
export default {
  data() {
    return {
      chartInstance: null,
      // 省份矢量数据缓存
      mapData: [],
      // 当前地图等级 1省 2市
      nowPosition: null
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
            areaColor: 'green'
          }
        }
      }
      this.chartInstance.setOption(initOption)
      this.nowPosition = 1
      // **************地图点击事件**************
      // 点击进入某省
      this.chartInstance.on('click', async (arg)=>{
        // 判断当前是否是China 可进入下一级查询
        if (this.nowPosition != 1) return
        this.nowPosition = 2
        // console.log(arg)
        // 中文省份对应拼音 map
        const provinceIfo = getProvinceMapInfo(arg.name)
        // console.log(provinceIfo)
        if (!this.mapData[provinceIfo.key]) {
          alert(12345)
          const regionJson = await axios.get('http://localhost:8080/'+provinceIfo.path)
          // console.log(regionJson)
          this.mapData[provinceIfo.key] = regionJson.data
          // 注册一次 string就可用
          this.$echarts.registerMap(provinceIfo.key, regionJson.data)
        }
        const newOption = {
          geo: {
            map: provinceIfo.key
          }
        }
        this.chartInstance.setOption(newOption)
      })
      // 监听双击dbclick返回China
    },
    returnChinaMap() {
      const returnOption = {
        geo: {
          map: 'China'
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
    }
  }
}
</script>