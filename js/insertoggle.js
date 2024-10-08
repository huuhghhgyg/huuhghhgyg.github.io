(() => {
  // <stdin>
  (function() {
    const toggleButtons = document.querySelectorAll(".toggle-button:not(#search-btn)");
    function hideAllExcept(targetElement) {
      document.querySelectorAll(".hidden").forEach((element) => {
        if (element !== targetElement) {
          element.classList.add("close");
          element.classList.remove("open");
        }
      });
    }
    function toggleElement(targetElement) {
      const isHidden = targetElement.classList.contains("close");
      hideAllExcept(targetElement);
      targetElement.classList.toggle("close", !isHidden);
      targetElement.classList.toggle("open", isHidden);
    }
    toggleButtons.forEach((button) => {
      button.addEventListener("click", function() {
        const targetIds = this.getAttribute("data-target").split(" ");
        targetIds.forEach((targetId) => {
          const targetElement = document.getElementById(targetId);
          if (targetElement) {
            toggleElement(targetElement);
          }
        });
      });
    });
    document.addEventListener("click", function(event) {
      const targetElements = Array.from(document.querySelectorAll(".open"));
      const clickedOutsideAllTargets = targetElements.every((element) => {
        return !element.contains(event.target) && !event.target.closest(".toggle-button");
      });
      if (clickedOutsideAllTargets) {
        targetElements.forEach((element) => {
          element.classList.remove("open");
          element.classList.add("close");
        });
      }
    });
  })();
})();
