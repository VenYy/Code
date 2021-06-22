var myChart = echarts.init(document.getElementById("main"))

var myChartOption = {
    title: {
        text: "今日全国疫情情况",
    },
    tooltip: {
        show: true,
        formatter: "{b}<br />{a}：{c}"
    },

    visualMap: {
        realtime: true,         // 拖拽实时更新
        text: ["High", "Low"],
        inRange: {
            color: ["white", "yellow", "red"]
        }
    },
    series: [{
        name: "当前确诊人数",
        type: "map",
        zoom: 1.2,
        mapType: "china",
        label: {
            show: true,
            fontSize: 10
        },
        data: []
    }]
}
myChart.setOption(myChartOption)