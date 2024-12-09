(function() {
    // 检查是否已经初始化
    if (window.tocInitialized) {
        // console.log("TOC already initialized");
        return;
    }

    // 标记为已初始化
    window.tocInitialized = true;
    // console.log("toc.html loaded");

    document.addEventListener("DOMContentLoaded", function() {
        const tocLinks = document.querySelectorAll(".md\\:block .toc-nav .nav-link");
        const headers = Array.from(tocLinks).map(link => document.querySelector(decodeURI(link.getAttribute("href"))));
        const indicator = document.querySelector(".md\\:block .indicator");
        const offset = 100;
        
        if (tocLinks.length === 0) return;

        function updateActiveLink() {
            let index = headers.findIndex(header => header.getBoundingClientRect().top > offset);
            if (index === -1) {
                index = headers.length - 1;
            } else if (index > 0) {
                index -= 1;
            }
            
            tocLinks.forEach(link => link.classList.remove("active"));
            const activeLink = tocLinks[index];
            activeLink.classList.add("active");
            
            if (indicator) {
                indicator.style.opacity = "1";
                indicator.style.setProperty("--indicator-top", `${activeLink.offsetTop}px`);
                indicator.style.setProperty("--indicator-height", `${activeLink.offsetHeight}px`);
                indicator.style.setProperty("--indicator-left", `${activeLink.offsetLeft}px`);
                indicator.style.setProperty("--indicator-width", `${activeLink.offsetWidth}px`);
            }
        }

        window.addEventListener("scroll", updateActiveLink);
        tocLinks.forEach(link => {
            link.addEventListener("click", function(event) {
                event.preventDefault();
                const targetId = decodeURI(this.getAttribute("href").substring(1));
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: "smooth", block: "start" });
                    history.pushState(null, null, `#${targetId}`);
                    setTimeout(updateActiveLink, 100);
                }
            });
        });

        updateActiveLink();
    });
})();