<template>
  <div class="Echarts">
      <a-card-grid  style="width:50%;height:250px;padding:0">
          <div ref="main" style="width:330px;height:250px"></div>
      </a-card-grid>
      <a-card-grid style="width:50%;height:250px;padding:0">
          <div ref="main1" style="width:330px;height:250px"></div>
      </a-card-grid>
  </div>
</template>

<script>
import API from '@/service'

// 指定图表的配置项和数据
const releaseTop5Option = {
    title: {
        //top:"bottom",
        subtext: '发布单统计图',
        left: 'center',
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {            // Use axis to trigger tooltip
            type: 'shadow'        // 'shadow' as default; can also be 'line' or 'shadow'
        }
    },
    // legend: {
    //     left: 'right',
    //     data: ['发布单量']
    // },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'value'
    }
};
const faiedTop5Option = {
    title: {
        //top:"bottom",
        left: 'center',
        subtext: '发布单失败统计'
    },
    tooltip: {
        trigger: 'item'
    },
    legend: {
        top: '5%',
        left: 'center',
        top:"bottom"
    },
    series: [
        {
            name: '发布单失败数量',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
            },
            label: {
                show: false,
            },
            labelLine: {
                show: false
            },
            data: []
        }
    ]
};

export default {
  name: 'Echarts',
  created(){
      this.fetchReleaseTop5()
      this.fetchReleaseFailedTop5()
  },
  methods:{
	  releaseTop5Chart(option){
		  // 基于准备好的dom，初始化echarts实例
		  var top5Chart = this.$echarts.init(this.$refs['main']);
          Object.assign(releaseTop5Option,option)
		  // 使用刚指定的配置项和数据显示图表。
		  top5Chart.setOption(releaseTop5Option);
	 },
     failedTop5Chart(){
		  // 基于准备好的dom，初始化echarts实例
		  var failedChart = this.$echarts.init(this.$refs['main1']);
		  // 使用刚指定的配置项和数据显示图表。
          failedChart.setOption(faiedTop5Option);
	 },
     fetchReleaseTop5(){
        API.ReleaseTop5().then((res)=>{
            let result = res.data
            if(res.status == 200 && result.code == 0){
                console.log(result)
                this.releaseTop5Chart({
                    yAxis: {
                        type: 'category',
                        data: result.data.app_name.reverse()
                    },
                    series: [
                        {
                            name: '发布单量',
                            type: 'bar',
                            label: {
                                show: true
                            },
                            emphasis: {
                                focus: 'series'
                            },
                            data: result.data.release_count.reverse()
                        }
                    ]
                });
            }
        })
      },
      fetchReleaseFailedTop5(){
        API.ReleaseFailedTop5().then((res)=>{
            let result = res.data
            if(res.status == 200 && result.code == 0){
                let series_data = []
                result.data["app_name"].forEach((item,index)=>{
                    series_data.push({
                        value:result.data["release_count"][index],
                        name:String(item)
                    })
                })
                faiedTop5Option.series[0].data = series_data
                this.failedTop5Chart()
            }
        })
      }
  }
}
</script>