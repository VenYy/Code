function checkTime(i) {
    if (i<10){
        i="0" + i;
    }
      return i;
}
function startTime() {
    var today = new Date()
    var yyyy = today.getFullYear()
    var MM = today.getMonth() + 1
    var dd = today.getDate()
    var hh = today.getHours()
    var mm = today.getMinutes()
    var ss = today.getSeconds()

    // 如果分钟或小时的值小于10，则在其值前加0，比如如果时间是下午3点20分9秒的话，则显示15：20：09
    MM=checkTime(MM);
    dd=checkTime(dd);
    mm=checkTime(mm);
    ss=checkTime(ss);

    var day; //用于保存星期（getDay()方法得到星期编号）
    if (today.getDay() == 0)   day   =   "星期日 "
    if (today.getDay() == 1)   day   =   "星期一 "
    if (today.getDay() == 2)   day   =   "星期二 "
    if (today.getDay() == 3)   day   =   "星期三 "
    if (today.getDay() == 4)   day   =   "星期四 "
    if (today.getDay() == 5)   day   =   "星期五 "
    if (today.getDay() == 6)   day   =   "星期六 "

    var str = "数据更新时间：<br />" + yyyy + "-" + MM + "-" + dd + " " + hh + ":" + mm + ":" + ss + " " + day

    document.getElementById("currentTime").innerHTML = str
}
setInterval(startTime, 1000)

