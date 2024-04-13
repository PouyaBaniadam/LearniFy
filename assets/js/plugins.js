// Avoid `console` errors in browsers that lack a console.
(function() {
  var method;
  var noop = function () {};
  var methods = [
    'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
    'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
    'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
    'timeline', 'timelineEnd', 'timeStamp', 'trace', 'warn'
  ];
  var length = methods.length;
  var console = (window.console = window.console || {});

  while (length--) {
    method = methods[length];

    // Only stub undefined methods.
    if (!console[method]) {
      console[method] = noop;
    }
  }
}());

// Place any jQuery/helper plugins in here.

//========= start home slider =========///
var swiper = new Swiper("#homeSlider", {
  spaceBetween: 30,
  centeredSlides: true,
  loop: true,
  autoplay: {
    delay: 5500,
    disableOnInteraction: false,
  },
  effect: "fade",
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
});

///=============end home slider ============/

//========= start new category ==============/
var swiper = new Swiper(".free-mode", {
  slidesPerView: "auto",
  spaceBetween: 10,
  freeMode: true,
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
});
//========= end new category ==============/

//========= start product box ==============/

var swiper = new Swiper("#product-slider", {
  slidesPerView: 5,
  spaceBetween: 10,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    100: {
      slidesPerView: 1,
      spaceBetween: 20,
    },
    576: {
      slidesPerView: 2,
      spaceBetween: 20,
    },
    768: {
      slidesPerView: 2,
      spaceBetween: 20,
    },
    1024: {
      slidesPerView: 3,
      spaceBetween: 20,
    },
    1200: {
      slidesPerView: 4,
      spaceBetween: 20,
    },
  },
});

//========= end product box ==============/

/**
 * image animation with tilt plugin
 */

$('.img-tilt').tilt({
  maxTilt:        10,
  perspective:    1000,   // Transform perspective, the lower the more extreme the tilt gets.
  easing:         "cubic-bezier(0.250, 0.460, 0.450, 0.940)",    // Easing on enter/exit.
  speed:          500,    // Speed of the enter/exit transition.
  transition:     true,   // Set a transition on enter/exit.
  disableAxis:    null,   // What axis should be disabled. Can be X or Y.
  reset:          true,   // If the tilt effect has to be reset on exit.
  glare:          true,  // Enables glare effect
  maxGlare:       0.5      // From 0 - 1.
})


///offer
///offer gallery
var swiper = new Swiper("#offerItemLink", {
  spaceBetween: 10,
  slidesPerView: 4,
  freeMode: true,
  watchSlidesProgress: true,
  allowTouchMove: false,
});
var swiper2 = new Swiper("#offerItem", {
  effect: "fade",
  speed: 1000,
  loop: true,
  autoplay: {
    delay: 5000,
    disableOnInteraction: false,
  },
  spaceBetween: 10,
  thumbs: {
    swiper: swiper,
  },
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
});


//============= sugget moment =============//

var swiperSugget = new Swiper("#suggetMoment", {
  slidesPerView: 1,
  spaceBetween: 30,
  loop: true,
  autoplay: {
    delay: 3000,
    disableOnInteraction: false,
  },
  speed: 500,
  on: {
    init: function () {
      $(".swiper-progress-bar").removeClass("animate");
      $(".swiper-progress-bar").removeClass("active");
      $(".swiper-progress-bar").eq(0).addClass("animate");
      $(".swiper-progress-bar").eq(0).addClass("active");
    },
    slideChangeTransitionStart: function () {
      $(".swiper-progress-bar").removeClass("animate");
      $(".swiper-progress-bar").removeClass("active");
      $(".swiper-progress-bar").eq(0).addClass("active");
    },
    slideChangeTransitionEnd: function () {
      $(".swiper-progress-bar").eq(0).addClass("animate");
    }
  }
});

//============= end sugget moment =============//

//// config floating contact
$('#btncollapzion').Collapzion({
  _child_attribute: [{
    'label': 'پشتیبانی تلفنی',
    'url': 'tel:0930555555555',
    'icon': 'bi bi-telephone'
  },
    {
      'label': 'پشتیبانی تلگرام',
      'url': 'https://tlgrm.me',
      'icon': 'bi bi-telegram'
    },
    {
      'label': 'پشتیبانی واتس آپ',
      'url': 'https://wa.me/444444444',
      'icon': 'bi-whatsapp'
    },

  ],
});

//=========== product gallery ===================//

var proSwiper = new Swiper(".product-gallery-thumb", {
  spaceBetween: 10,
  slidesPerView: 4,
  freeMode: true,
  watchSlidesProgress: true,
  breakpoints: {
    // when window width is >= 320px
    320: {
      slidesPerView: 3,
      spaceBetween: 10
    },
  },
});
var proThumbswiper = new Swiper(".product-gallery", {
  spaceBetween: 10,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  zoom: {
    maxRatio: 3,
    minRation: 1
  },
  thumbs: {
    swiper: proSwiper,
  },
});

//=========== end product gallery ===================//

//========= start new category ==============/
var swiper = new Swiper(".free-mode", {
  slidesPerView: "auto",
  spaceBetween: 10,
  freeMode: true,
});
//========= end new category ==============/


//========= start product box ==============/

var swiper = new Swiper(".product-slider-swiper", {
  slidesPerView: 5,
  spaceBetween: 10,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    100: {
      slidesPerView: 1,
      spaceBetween: 20,
    },
    576: {
      slidesPerView: 2,
      spaceBetween: 20,
    },
    768: {
      slidesPerView: 2,
      spaceBetween: 20,
    },
    1024: {
      slidesPerView: 3,
      spaceBetween: 20,
    },
    1200: {
      slidesPerView: 4,
      spaceBetween: 10,
    },
  },
});

//========= end product box ==============/

$('.img-tilt').tilt({
  maxTilt:        10,
  perspective:    1000,   // Transform perspective, the lower the more extreme the tilt gets.
  easing:         "cubic-bezier(0.250, 0.460, 0.450, 0.940)",    // Easing on enter/exit.
  speed:          500,    // Speed of the enter/exit transition.
  transition:     true,   // Set a transition on enter/exit.
  disableAxis:    null,   // What axis should be disabled. Can be X or Y.
  reset:          true,   // If the tilt effect has to be reset on exit.
  glare:          true,  // Enables glare effect
  maxGlare:       0.5      // From 0 - 1.
})