function startClockAtExactSecond() {
    const hourHand = document.getElementById("hour-hand");
    const minuteHand = document.getElementById("minute-hand");

    // 获取当前的毫秒数
    const now = new Date();
    const milliseconds = now.getMilliseconds();

    // 计算到下一个整数秒的剩余时间
    const delay = 1000 - milliseconds;

    // 延迟到下一个整数秒后添加动画类
    setTimeout(() => {
        // 添加动画类，使指针开始旋转
        hourHand.classList.add("animate");
        minuteHand.classList.add("animate");

        // 每秒更新一次时间文本
        updateClock(); // 立即调用一次，避免延迟一秒才显示
        setInterval(updateClock, 1000);
    }, delay);
}

// 更新时间文本的函数
function updateClock() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");
    const seconds = String(now.getSeconds()).padStart(2, "0");
    document.getElementById(
        "number"
    ).textContent = `${hours}:${minutes}:${seconds}`;
}

window.onload = function () {
    // 设置时钟
    updateClock();

    // 启动时钟，在整数秒开始动画
    startClockAtExactSecond();
}