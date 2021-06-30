// 展示当前时间
function showTime() {
    $.ajax({
        url: "api/showTime",
        type: "post",
        timeout: 10000, //超时时间设置为10秒；
        success: function (data) {
            $(".time").html(data)
        },
        error: function (xhr, type, errorThrown) {
        }
    });
}

function screen_info() {
    $.ajax({
        url: "api/screen_info",
        type: "post",
        success: function (d) {
            // jQuery eq() 方法 选取指定索引号的html元素
            $(".info .num h1").eq(0).text(d["nowConfirmed"])
            $(".info .num h1").eq(1).text(d["confirmed"])
            $(".info .num h1").eq(2).text(d["suspected"])
            $(".info .num h1").eq(3).text(d["dead"])
        }, error: function () {
            alert("ajax请求加载失败")
        }
    })
}

function showMap() {
    $.ajax({
        url: "api/showMap",
        type: "post",
        success: function (d) {
            console.log(d)
            mapOption.series[0].name = "当前确诊人数"
            mapOption.series[0].data = d[0].data
            mapChart.setOption(mapOption)
            $(".ul1>li").mousedown(function () {
                var char = "当前确诊人数"
                var data = d[0].data

                function myfun() {
                    mapOption.series[0].name = char
                    mapOption.series[0].data = data
                    return mapChart.setOption(mapOption)
                }

                // 点击后切换类名，实现css效果
                $(this).addClass("active").siblings("li").removeClass("active")
                var index = $(this).index();
                if (index === 0) {
                    myfun()
                } else {
                    char = "累计确诊人数"
                    data = d[1].data
                    myfun()
                }
            })
        }, error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status)
            alert(XMLHttpRequest.readyState)
            alert(textStatus)
        }
    })
}

function leftTop() {
    $.ajax({
        url: "api/leftTop",
        type: "post",
        success: function (d) {
            console.log(d.dateId)
            leftTopOption.xAxis.data = d.dateId
            leftTopOption.series[0].data = d.confirmedIncr
            leftTopOption.series[1].data = d.curedIncr
            leftTopOption.series[2].data = d.deadIncr
            leftTopChart.setOption(leftTopOption)
        }, error: function (r) {
            alert(r.status)
        }
    })
}

function leftBottom() {
    $.ajax({
        url: "api/leftBottom",
        type: "post",
        success: function (d) {
            console.log(d.dateId)
            leftBottomOption.xAxis.data = d.dateId
            leftBottomOption.series[0].data = d.confirmedCount
            leftBottomOption.series[1].data = d.curedCount
            leftBottomOption.series[2].data = d.deadCount
            leftBottomChart.setOption(leftBottomOption)
        }, error: function (r) {
            alert(r.status)
        }
    })
}


showTime()
screen_info()
// showMap()
// leftTop()
// leftBottom()
// 十分钟更新一次
setInterval(showTime, 1000)
setInterval(screen_info, 1000 * 60 * 10)
// setInterval(showMap, 1000 * 60 * 10)
// setInterval(leftTop, 1000 * 60 * 10)
// setInterval(leftBottom, 1000 * 60 * 10)