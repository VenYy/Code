var myChart = echarts.init(document.getElementById("main"))
var mapData = getData()

// function getData() {
//     var legendData = []
//     var confirmedCut = []
//     var nowConfirmedCut = []
//     return {nowConfirmedCut: nowConfirmedCut, confirmedCut:confirmedCut}
// }

var option = {
    title: {
        text: "今日国内疫情情况",
    },
    tooltip: {
        show: true,
        formatter: "{b}<br />{a}：{c}"
    },
    visualMap: {
        realtime: true,         // 拖拽实时更新
        text: ["High", "Low"],
        inRange: {
            color: ["white", "green", "yellow", "red"]
        }
    },
    series: [{
        name: "当前确诊人数",
        type: "map",
        zoom: 1,
        mapType: "china",
        label: {
            show: true,
            fontSize: 10
        },
        data: mapData.nowConfirmedCut
    }]
}

// 等待图形加载，1s
myChart.showLoading({
      text: 'loading',
      color: '#c23531',
      textColor: '#000',
      maskColor: 'rgba(255, 255, 255, 0.2)',
      zlevel: 0,
    })
setTimeout(() => {
  // setOption前隐藏loading事件
  myChart.hideLoading();
  myChart.setOption(option);
}, 1)