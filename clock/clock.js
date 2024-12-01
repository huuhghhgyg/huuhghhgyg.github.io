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
    const modeSelect = document.getElementById('mode-select');
    const targetTimeInput = document.getElementById('target-time');

    if (modeSelect.value === 'countdown' && targetTimeInput.value) {
        const targetTime = new Date(targetTimeInput.value);
        const timeDiff = Math.floor((targetTime - now) / 1000);
        console.log('targetTime', targetTime, 'now', now, 'timeDiff', timeDiff);
        const isOverdue = timeDiff < 0;

        // 计算时分秒
        const timeDiffInSeconds = Math.abs(Math.floor((targetTime - now) / 1000));
        const hours = Math.floor(timeDiffInSeconds / 3600);
        const minutes = Math.floor((timeDiffInSeconds % 3600) / 60);
        const seconds = timeDiffInSeconds % 60;

        // 格式化显示
        const formattedHours = String(hours).padStart(2, "0"); // 补零
        const formattedMinutes = String(minutes).padStart(2, "0");
        const formattedSeconds = String(seconds).padStart(2, "0");

        // 通过添加/移除类来改变主题色
        if (isOverdue) {
            document.body.classList.add('overdue');
            document.getElementById("number").textContent =
                `-${formattedHours}:${formattedMinutes}:${formattedSeconds}`;
        } else {
            document.body.classList.remove('overdue');
            document.getElementById("number").textContent =
                `${formattedHours}:${formattedMinutes}:${formattedSeconds}`;
        }
    } else {
        // 普通时钟模式
        document.body.classList.remove('overdue');
        const hours = String(now.getHours()).padStart(2, "0");
        const minutes = String(now.getMinutes()).padStart(2, "0");
        const seconds = String(now.getSeconds()).padStart(2, "0");
        document.getElementById("number").textContent = `${hours}:${minutes}:${seconds}`;
    }
}

window.onload = function () {
    // 设置时钟
    updateClock();

    // 启动时钟，在整数秒开始动画
    startClockAtExactSecond();

    // 获取元素
    const semiCircle = document.getElementById('semi-circle');
    const settingsPanel = document.getElementById('settings-panel');
    let isPanelOpen = false;

    // 设置下一分钟的目标时间
    function setNextMinuteAsTarget() {
        const targetTimeInput = document.getElementById('target-time');
        if (!targetTimeInput) return;

        const now = new Date();
        // 设置为下一分钟的开始
        now.setSeconds(0);
        now.setMinutes(now.getMinutes() + 1);
        
        // 使用本地时间格式
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        
        targetTimeInput.value = `${year}-${month}-${day}T${hours}:${minutes}`;
    }

    // 切换设置面板
    function togglePanel(isOpen) {
        const background = document.getElementById('background');
        const panel = document.getElementById('settings-panel');
        const panelHeight = panel.offsetHeight;
        
        if (isOpen) {
            panel.classList.remove('translate-y-full');
            background.style.transform = `translateY(-${panelHeight}px)`;
        } else {
            panel.classList.add('translate-y-full');
            background.style.transform = 'translateY(0)';
        }
    }

    // 修改点击事件处理
    semiCircle.addEventListener('click', () => {
        isPanelOpen = !isPanelOpen;

        if (isPanelOpen) {
            setNextMinuteAsTarget();
        }

        togglePanel(isPanelOpen);
    });

    // 模式选择逻辑
    const modeSelect = document.getElementById('mode-select');
    const countdownSettings = document.getElementById('countdown-settings');
    const targetTimeInput = document.getElementById('target-time');
    const infoElement = document.getElementById('info');
    const customInfoInput = document.getElementById('custom-info');

    // 更新信息显示
    function updateInfoText(mode) {
        const customText = customInfoInput.value.trim();
        if (customText) {
            infoElement.textContent = customText;
        } else {
            infoElement.textContent = mode === 'countdown' ? 'countdown timer' : 'real time clock';
        }
    }

    modeSelect?.addEventListener('change', (e) => {
        if (e.target.value === 'countdown') {
            countdownSettings.style.display = 'flex';
            setNextMinuteAsTarget();
        } else {
            countdownSettings.style.display = 'none';
            document.body.classList.remove('overdue');
        }
        updateInfoText(e.target.value);
        updateClock();
    });

    // 监听自定义信息输入
    customInfoInput?.addEventListener('input', () => {
        updateInfoText(modeSelect.value);
    });

    // 监听目标时间变化
    targetTimeInput?.addEventListener('change', () => {
        updateClock(); // 立即更新显示
    });
}