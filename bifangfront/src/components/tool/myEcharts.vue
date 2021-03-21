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
export default {
  name: 'Echarts',
  methods:{
	  myEcharts(){
		  // 基于准备好的dom，初始化echarts实例
		  var myChart = this.$echarts.init(this.$refs['main']);

		  // 指定图表的配置项和数据
		  var option = {
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
                },
                yAxis: {
                    type: 'category',
                    data: ['A组件', 'B组件', 'C组件', 'D组件', 'E组件']
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
                        data: [32, 12, 9, 11, 37]
                    }
                ]
            };

		  // 使用刚指定的配置项和数据显示图表。
		  myChart.setOption(option);
	 },
     myEcharts1(){
		  // 基于准备好的dom，初始化echarts实例
		  var myChart1 = this.$echarts.init(this.$refs['main1']);

		  // 指定图表的配置项和数据
		  var option1 = {
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
                        name: '发布单失败比例',
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
                            position: 'center'
                        },
                        emphasis: {
                            label: {
                                show: true,
                                fontSize: '40',
                                fontWeight: 'bold'
                            }
                        },
                        labelLine: {
                            show: false
                        },
                        data: [
                            {value: 1048, name: 'A组件'},
                            {value: 735, name: 'B组件'},
                            {value: 580, name: 'C组件'}
                        ]
                    }
                ]
            };

		  // 使用刚指定的配置项和数据显示图表。
          myChart1.setOption(option1);
	 }
  },
  mounted() {
  	this.myEcharts();
    this.myEcharts1();
  }
}
</script>