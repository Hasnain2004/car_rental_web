document.addEventListener("DOMContentLoaded", function () {
  // Thumbnail click functionality
  const thumbnails = document.querySelectorAll(".thumbnail");
  const mainImage = document.querySelector(".main-image img");

  thumbnails.forEach((thumbnail) => {
    thumbnail.addEventListener("click", function () {
      // Remove active class from all thumbnails
      thumbnails.forEach((t) => t.classList.remove("active"));

      // Add active class to clicked thumbnail
      this.classList.add("active");

      // Update main image (in a real scenario, you would change the src)
      // For now, we just have the same image
      mainImage.src = this.querySelector("img").src;
    });
  });
});
