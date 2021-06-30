var mapChart = echarts.init(document.getElementById("main"));
var mapOption = {
    title: {
        text: "国内疫情地图",
        subtext: "现存确诊,数据每十分钟更新一次",
        x: "5%",
        y: "5%",
        textStyle: {
            color: "white"
        }
    },
    tooltip: {
        show: true,
        // formatter: "{b}<br />{a}：{c}",
        formatter: function (item) {
          var temp = item.value;
          var name = item.name
          var res = temp[2];
          return name + "<br />" + "现存确诊：" + res
        },
        trigger: "item",
    },
    //
    // visualMap: {
    //     type: "continuous",
    //     calculable: false,
    //     realtime: true,         // 拖拽实时更新
    //     text: ["High", "Low"],
    //     inRange: {
    //         color: ["white", "yellow", "red"]
    //     },
    //     textStyle: {
    //         color: "white"
    //     }
    // },
    geo: {
        map: "chinaMap",
        roam: false,
        zoom: 1.2,
        scaleLimit: {
            min: 0.5,
            max: 3
        },
        itemStyle: {
            normal: {
                borderColor: 'rgba(147, 235, 248, 1)',
                borderWidth: 2,
                areaColor: {
                    type: 'radial',
                    x: 0.5,
                    y: 0.5,
                    r: 0.8,
                    colorStops: [{
                        offset: 0,
                        color: 'rgba(175,238,238, 0)' // 0% 处的颜色
                    }, {
                        offset: 1,
                        color: 'rgba(   47,79,79, .2)' // 100% 处的颜色
                    }],
                    globalCoord: false // 缺省为 false
                },
                shadowColor: 'rgba(128, 217, 248, 1)',
                shadowOffsetX: -2,
                shadowOffsetY: 2,
                shadowBlur: 10
            },
            emphasis: {
                areaColor: '#389BB7',
                borderWidth: 0
            }
        },
        label: {
            show: true,
            formatter: ""
        }
    },
    series: [
        {
            type: "effectScatter",
            coordinateSystem: 'geo',
            legendHoverLink: true,
            effectType: "ripple",
            rippleEffect: {
                period: 2,
                scale: 3
            },
            data: [],
            symbolSize: 8,
            // symbolSize: function (item) {
            //     return item[2] / 150
            // },
            label: {
                show: true,
                color: "white",
                formatter: "{b}",
                position: "left",
                distance: 10
            },
            itemStyle: {
                color: function (item) {
                    var value = item.value
                    value = value[2]
                    if (value === 0) {
                        return "white"
                    } else if (value < 10) {
                        return "#FDD835"
                    } else if (value < 50) {
                        return "#FF8F00"
                    } else if (value < 200) {
                        return "#D84315"
                    } else if (value >= 200) {
                        return "#C62828"
                    }
                }
            }
        }
    ]
}
mapChart.showLoading({
    text: 'loading',
    color: '#c23531',
    textColor: 'red',
    maskColor: 'rgba(255, 255, 255, 0.2)',
    zlevel: 0,
});
setTimeout(() => {
    // setOption前隐藏loading事件
    mapChart.hideLoading();
    mapChart.setOption(mapOption);
}, 1000);

function loadData(url) {
    var json = null;
    $.ajax({
        'async': false,
        'global': false,
        'url': url,
        'dataType': "json",
        'success': function (data) {
            json = data;
        }
    });
    return json;
};
// 注册地图
var geoJson = loadData("static/js/china.json")
echarts.registerMap("chinaMap", geoJson)
var mapData = {
    '新疆维吾尔自治区': [84.9023, 42.148],
    '西藏自治区': [87.8695, 31.6846],
    '内蒙古自治区': [111.671, 40.8183],
    '青海省': [95.2402, 35.4199],
    '四川省': [101.9199, 30.1904],
    '黑龙江省': [126.1445, 48.7156],
    '甘肃省': [99.7129, 38.166],
    '云南省': [101.0652, 25.1807],
    '广西壮族自治区': [107.7813, 23.6426],
    '湖南省': [111.5332, 27.3779],
    '陕西省': [109.5996, 35.7396],
    '广东省': [113.4668, 22.8076],
    '吉林省': [125.7746, 43.5938],
    '河北省': [115.4004, 39.4688],
    '湖北省': [112.2363, 31.1572],
    '贵州省': [106.6113, 26.9385],
    '山东省': [118.7402, 36.4307],
    '江西省': [116.0156, 27.29],
    '河南省': [113.0668, 33.8818],
    '辽宁省': [122.0438, 41.0889],
    '山西省': [112.4121, 37.6611],
    '安徽省': [117.2461, 32.0361],
    '福建省': [118.3008, 25.9277],
    '浙江省': [120.498, 29.0918],
    '江苏省': [118.8586, 32.915],
    '重庆市': [107.7539, 30.1904],
    '宁夏回族自治区': [105.9961, 37.3096],
    '海南省': [109.9512, 19.2041],
    '台湾': [120.0254, 23.5986],
    '北京市': [116.4551, 40.2539],
    '天津市': [117.4219, 39.4189],
    '上海市': [121.4648, 31.2891],
    '香港': [114.1178, 22.3242],
    '澳门': [111.5547, 22.1484]
}
console.log(mapData)


var convertData = function (data) {
    var res = []
    for (var i = 0; i < data.length; i++) {
        var geoCoord = mapData[data[i].name]
        // console.log(geoCoord)
        if (geoCoord) {
            res.push({
                name: data[i].name,
                value: geoCoord.concat(data[i].value)
            })
        }
    }
    console.log(res)
    return res
}

function showMap() {
    $.ajax({
        url: "api/showMap",
        type: "post",
        success: function (d) {
            console.log(d)
            // var data = d[0].data
            console.log(d[0].data)
            mapOption.series[0].name = "当前确诊人数"
            mapOption.series[0].data = convertData(d[0].data)
            mapChart.setOption(mapOption)
        }, error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status)
            alert(XMLHttpRequest.readyState)
            alert(textStatus)
        }
    })
}

showMap()
setInterval(showMap, 1000 * 60)