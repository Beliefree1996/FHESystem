<template>
  <div :class="className" :style="{height:height,width:width}"/>
</template>

<script>
  import echarts from 'echarts'

  require('echarts/theme/macarons') // echarts theme

  export default {
    props: {
      className: {
        type: String,
        default: 'chart'
      },
      width: {
        type: String,
        default: '100%'
      },
      height: {
        type: String,
        default: '350px'
      },
      autoResize: {
        type: Boolean,
        default: true
      },
      chartData: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        isLogin: false,
        chart: null
      }
    },
    watch: {
      chartData: {
        deep: true,
        handler(val) {
          this.setOptions(val)
        }
      }
    },
    mounted() {
      this.$nextTick(() => {
        this.initChart()
      })
    },
    beforeDestroy() {
      if (!this.chart) {
        return
      }
      this.chart.dispose()
      this.chart = null
    },
    methods: {
      initChart() {
        this.chart = echarts.init(this.$el, 'macarons')
        this.setOptions(this.chartData)
      },
      setOptions({wageData, taxData, xAxisData} = {}) {
        // const wage = this.wageArr
        console.log(this.wageArr)
        this.chart.setOption({
          xAxis: {
            data: xAxisData,
            boundaryGap: false,
            axisTick: {
              show: false
            }
          },
          grid: {
            left: 10,
            right: 30,
            bottom: 20,
            top: 30,
            containLabel: true
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'cross'
            },
            padding: [5, 10]
          },
          yAxis: {
            axisTick: {
              show: false
            }
          },
          legend: {
            data: ['公积金月缴额', '社保缴费基数']
          },
          series: [{
            name: '公积金月缴额', itemStyle: {
              normal: {
                color: '#FF005A',
                lineStyle: {
                  color: '#FF005A',
                  width: 2
                }
              }
            },
            smooth: true,
            type: 'line',
            data: wageData,
            animationDuration: 2800,
            animationEasing: 'cubicInOut'
          },
            {
              name: '社保缴费基数',
              smooth: true,
              type: 'line',
              itemStyle: {
                normal: {
                  color: '#3888fa',
                  lineStyle: {
                    color: '#3888fa',
                    width: 2
                  },
                  areaStyle: {
                    color: '#f3f8ff'
                  }
                }
              },
              data: taxData,
              animationDuration: 2800,
              animationEasing: 'quadraticOut'
            }]
        })
      }
    },
    created() {
      this.$axios.get('apis/user/getstatus?aa=60&kk=6')
        .then(response => {
          if (response.data.status === 1) {
            this.$router.push({path: '/user/login'})
          }
          else if (response.data.status === 2){

          }
          else {
            this.isLogin = true
          }
        })
    }
  }
</script>
