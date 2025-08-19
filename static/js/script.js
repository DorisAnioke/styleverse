document.addEventListener("DOMContentLoaded", () => {

  // === Hero Slider (Flash Sale / Main Hero) ===
  const slider = document.querySelector("#heroSlider");
  if (slider) {
    const slides = slider.querySelectorAll(".slide");
    const prevBtn = slider.querySelector(".slider-btn.prev");
    const nextBtn = slider.querySelector(".slider-btn.next");
    let currentSlide = 0;

    function showSlide(index) {
      slides.forEach((slide, i) => {
        slide.classList.remove("active");
        if (i === index) slide.classList.add("active");
      });
    }

    function moveSlide(step) {
      currentSlide = (currentSlide + step + slides.length) % slides.length;
      showSlide(currentSlide);
    }

    if (prevBtn && nextBtn && slides.length > 0) {
      prevBtn.addEventListener("click", () => moveSlide(-1));
      nextBtn.addEventListener("click", () => moveSlide(1));
    }

    // Auto-slide every 5 seconds
    if (slides.length > 0) setInterval(() => moveSlide(1), 5000);

    // Show first slide
    if (slides.length > 0) showSlide(currentSlide);

    // Swipe support for mobile
    let startX = 0;
    slider.addEventListener("touchstart", e => {
      startX = e.touches[0].clientX;
    }, { passive: true });

    slider.addEventListener("touchend", e => {
      const diff = e.changedTouches[0].clientX - startX;
      if (Math.abs(diff) > 50) {
        if (diff < 0) moveSlide(1);
        else moveSlide(-1);
      }
    });
  }

  // === Product Image Preview + Swipe ===
  const mainImage = document.getElementById("mainPreview");
  const thumbnails = document.querySelectorAll(".thumbnails img");
  const prevThumbBtn = document.querySelector(".nav-btn.left");
  const nextThumbBtn = document.querySelector(".nav-btn.right");
  let currentIndex = 0;
  let startXThumb = 0;

  if (mainImage && thumbnails.length > 0) {
    thumbnails[0].classList.add("active-thumb");
    mainImage.src = thumbnails[0].src;

    function changeImage(index) {
      thumbnails.forEach(t => t.classList.remove("active-thumb"));
      thumbnails[index].classList.add("active-thumb");
      mainImage.src = thumbnails[index].src;
      currentIndex = index;
    }

    thumbnails.forEach((thumb, index) => {
      thumb.addEventListener("click", () => changeImage(index));
    });

    if (prevThumbBtn) {
      prevThumbBtn.addEventListener("click", () => {
        currentIndex = (currentIndex - 1 + thumbnails.length) % thumbnails.length;
        changeImage(currentIndex);
      });
    }

    if (nextThumbBtn) {
      nextThumbBtn.addEventListener("click", () => {
        currentIndex = (currentIndex + 1) % thumbnails.length;
        changeImage(currentIndex);
      });
    }

    mainImage.addEventListener("touchstart", e => {
      startXThumb = e.touches[0].clientX;
    }, { passive: true });

    mainImage.addEventListener("touchend", e => {
      const diff = e.changedTouches[0].clientX - startXThumb;
      if (Math.abs(diff) > 50) {
        if (diff < 0) currentIndex = (currentIndex + 1) % thumbnails.length;
        else currentIndex = (currentIndex - 1 + thumbnails.length) % thumbnails.length;
        changeImage(currentIndex);
      }
    });
  }

  // === Quantity Input Control ===
  const quantityInput = document.querySelector('input[name="quantity"]');
  if (quantityInput) {
    quantityInput.addEventListener("input", () => {
      let val = parseInt(quantityInput.value);
      if (isNaN(val) || val < 1) quantityInput.value = 1;
    });
  }

  // === Mobile Menu Toggle ===
  const menuToggle = document.querySelector(".menu-toggle");
  const navMenu = document.querySelector(".nav-links");
  if (menuToggle && navMenu) {
    menuToggle.addEventListener("click", () => {
      navMenu.classList.toggle("show");
    });
  }

  // === Search Form Toggle ===
  const searchBtn = document.querySelector(".search-btn");
  const searchForm = document.querySelector(".search-form");
  if (searchBtn && searchForm) {
    searchBtn.addEventListener("click", () => {
      searchForm.classList.toggle("visible");
    });
  }

  // === Add to Cart Alert ===
  const addToCartBtn = document.querySelector(".add-to-cart-btn");
  if (addToCartBtn) {
    addToCartBtn.addEventListener("click", () => {
      alert("🛒 Item added to cart!");
    });
  }

  // === Wishlist Toggle ===
  const wishlistBtns = document.querySelectorAll(".wishlist-btn");
  wishlistBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      btn.classList.toggle("active");
      const added = btn.classList.contains("active");
      alert(added ? "❤️ Added to wishlist!" : "💔 Removed from wishlist.");
    });
  });

  // === Review Form Toggle (Order History Page) ===
  const reviewToggles = document.querySelectorAll(".toggle-review-form");
  reviewToggles.forEach(btn => {
    btn.addEventListener("click", () => {
      const form = btn.nextElementSibling;
      if (form) form.classList.toggle("visible");
    });
  });

});