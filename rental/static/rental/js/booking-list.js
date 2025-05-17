document.addEventListener("DOMContentLoaded", function () {
  // Filter functionality
  const filterBtns = document.querySelectorAll(".filter-btn");
  const bookingCards = document.querySelectorAll(".booking-card");

  filterBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      // Remove active class from all buttons
      filterBtns.forEach((btn) => btn.classList.remove("active"));

      // Add active class to clicked button
      this.classList.add("active");

      const filter = this.getAttribute("data-filter");

      // Show/hide bookings based on filter
      bookingCards.forEach((card) => {
        if (filter === "all" || card.getAttribute("data-status") === filter) {
          card.style.display = "flex";
        } else {
          card.style.display = "none";
        }
      });
    });
  });
});
