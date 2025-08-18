document.addEventListener("DOMContentLoaded", function () {
  const mainImage = document.getElementById("mainPreview");
  const thumbs = document.querySelectorAll(".thumb");
  const leftBtn = document.querySelector(".nav-btn.left");
  const rightBtn = document.querySelector(".nav-btn.right");

  const images = Array.from(thumbs).map(t => t.src);
  let currentIndex = 0;

  function updateMainImage() {
    mainImage.src = images[currentIndex];
    thumbs.forEach((t, i) => {
      t.classList.toggle("active", i === currentIndex);
    });
  }

  thumbs.forEach((thumb, index) => {
    thumb.addEventListener("click", () => {
      currentIndex = index;
      updateMainImage();
    });
  });

  leftBtn.addEventListener("click", () => {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    updateMainImage();
  });

  rightBtn.addEventListener("click", () => {
    currentIndex = (currentIndex + 1) % images.length;
    updateMainImage();
  });

  // Keyboard navigation
  document.addEventListener("keydown", e => {
    if (e.key === "ArrowLeft") leftBtn.click();
    if (e.key === "ArrowRight") rightBtn.click();
  });

  // Touch swipe
  let startX = 0;
  mainImage.addEventListener("touchstart", e => startX = e.changedTouches[0].screenX);
  mainImage.addEventListener("touchend", e => {
    const endX = e.changedTouches[0].screenX;
    if (endX < startX - 50) rightBtn.click();
    else if (endX > startX + 50) leftBtn.click();
  });

  updateMainImage();
});