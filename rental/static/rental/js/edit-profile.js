document.addEventListener("DOMContentLoaded", function () {
  // Profile picture preview
  const profilePicInput = document.getElementById("id_profile_picture");
  const profilePicPreview = document.getElementById("profile-pic-preview");
  const profilePicIcon = document.getElementById("profile-pic-icon");

  if (profilePicInput) {
    profilePicInput.addEventListener("change", function () {
      if (this.files && this.files[0]) {
        const reader = new FileReader();

        reader.onload = function (e) {
          profilePicPreview.src = e.target.result;
          profilePicPreview.style.display = "block";
          if (profilePicIcon) {
            profilePicIcon.style.display = "none";
          }
        };

        reader.readAsDataURL(this.files[0]);
      }
    });
  }
});
