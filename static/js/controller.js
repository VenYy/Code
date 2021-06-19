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
            alert(d)
        },error: function () {
            alert("ajax:地图加载失败")
        }
    })
}

screen_info()
// showMap()
