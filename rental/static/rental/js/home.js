document.addEventListener("DOMContentLoaded", function () {
  // Initialize main swiper
  var mainSwiper = new Swiper(".mainSwiper", {
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
    },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
  });

  // Initialize thumb swiper
  var thumbSwiper = new Swiper(".thumbSwiper", {
    slidesPerView: 3,
    spaceBetween: 10,
    watchSlidesProgress: true,
  });

  // Link the two swipers
  mainSwiper.controller.control = thumbSwiper;
  thumbSwiper.controller.control = mainSwiper;

  // Click on thumb to navigate
  const thumbItems = document.querySelectorAll(".thumb-item");
  thumbItems.forEach((item, index) => {
    item.addEventListener("click", () => {
      mainSwiper.slideTo(index + 1);
    });
  });
});
