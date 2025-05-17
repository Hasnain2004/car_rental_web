document.addEventListener("DOMContentLoaded", function () {
  // Mobile menu toggle
  const menuTrigger = document.querySelector(".menu-trigger");
  const mainNav = document.querySelector(".main-nav");

  if (menuTrigger) {
    menuTrigger.addEventListener("click", function () {
      mainNav.classList.toggle("active");
    });
  }

  // Close mobile menu when clicking outside
  document.addEventListener("click", function (event) {
    if (
      mainNav &&
      mainNav.classList.contains("active") &&
      !mainNav.contains(event.target) &&
      event.target !== menuTrigger
    ) {
      mainNav.classList.remove("active");
    }
  });

  // Message dismissal
  const closeButtons = document.querySelectorAll(".close-message");

  closeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const message = this.parentElement;
      message.style.opacity = "0";
      setTimeout(() => {
        message.style.display = "none";
      }, 300);
    });
  });

  // Auto dismiss messages after 5 seconds
  const messages = document.querySelectorAll(".message");

  if (messages.length) {
    setTimeout(() => {
      messages.forEach((message) => {
        message.style.opacity = "0";
        setTimeout(() => {
          message.style.display = "none";
        }, 300);
      });
    }, 5000);
  }
});
