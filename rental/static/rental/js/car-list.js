document.addEventListener("DOMContentLoaded", function () {
  // Filter functionality
  const filterBtns = document.querySelectorAll(".filter-btn");
  const carItems = document.querySelectorAll(".car-item");

  filterBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      // Remove active class from all buttons
      filterBtns.forEach((btn) => btn.classList.remove("active"));

      // Add active class to clicked button
      this.classList.add("active");

      const filter = this.getAttribute("data-filter");

      // Show/hide cars based on filter
      carItems.forEach((item) => {
        if (filter === "all" || item.getAttribute("data-category") === filter) {
          item.style.display = "block";
        } else {
          item.style.display = "none";
        }
      });
    });
  });
});
