const col3SwiperSlider = new Swiper(".col3-swiper-slider", {
  spaceBetween: 20,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    992: {
      slidesPerView: 3,
    },
    576: {
      slidesPerView: 2,
    },
    0: {
      slidesPerView: 1,
    },
  },
});

const col4SwiperSlider = new Swiper(".col4-swiper-slider", {
  spaceBetween: 20,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    992: {
      slidesPerView: 4,
    },
    768: {
      slidesPerView: 3,
    },
    480: {
      slidesPerView: 2,
    },
    0: {
      slidesPerView: 1,
    },
  },
});

const autoSwiperSlider = new Swiper(".auto-swiper-slider", {
  slidesPerView: "auto",
  spaceBetween: 30,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
});

const cardSwiperSlider = new Swiper(".card-swiper-slider", {
  effect: "cards",
  grabCursor: true,
  autoplay: {
    delay: 3000,
  },
  cardsEffect: {
    rotate: 50,
    slideShadows: false,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
});

const players = document.querySelectorAll(".js-player");

if (players) {
  Array.from(players).map(
    (p) =>
      new Plyr(p, {
        // options
      })
  );
}

const scrollToTopBtn = document.getElementById("scrollToTopBtn");

if (scrollToTopBtn) {
  scrollToTopBtn.addEventListener("click", function (event) {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  });
}
