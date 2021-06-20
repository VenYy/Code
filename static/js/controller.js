// 展示当前时间
function showTime() {
    $.ajax({
        url: "/showTime",
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
        url: "/screen_info",
        type: "post",
        success: function (d) {
            // jQuery eq() 方法 选取指定索引号的html元素
            $(".info .num h1").eq(0).text(d["nowConfirmed"])
            $(".info .num h1").eq(1).text(d["confirmed"])
            $(".info .num h1").eq(2).text(d["suspected"])
            $(".info .num h1").eq(3).text(d["dead"])
        },error: function () {
            alert("ajax请求加载失败")
        }
    })
}

function showMap() {
    $.ajax({
        url: "/showMap",
        type: "post",
        success: function (d) {
            myChartOption.series[0].data = d.data
            myChart.setOption(myChartOption)
        },error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status)
            alert(XMLHttpRequest.readyState)
            alert(textStatus)
        }
    })
}

showTime()
screen_info()
showMap()
setInterval(showTime, 1000)