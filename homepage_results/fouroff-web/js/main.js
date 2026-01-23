$(document).ready(function() {
  $('.testimonial-carousel').slick({
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 4000,
    pauseOnHover: true,
    responsive: [
      {
        breakpoint: 992,
        settings: {
          slidesToShow: 2
        }
      },
      {
        breakpoint: 576,
        settings: {
          slidesToShow: 1
        }
      }
    ]
  });

  $(window).scroll(function() {
    if ($(this).scrollTop() > 50) {
      $('.navbar').addClass('scrolled');
    } else {
      $('.navbar').removeClass('scrolled');
    }
  });

  $('a[href^="#"]').on('click', function(e) {
    var target = $(this.getAttribute('href'));
    if (target.length) {
      e.preventDefault();
      $('html, body').animate({
        scrollTop: target.offset().top - 80
      }, 600);
    }
  });

  $('.navbar-nav .dropdown').hover(
    function() {
      if ($(window).width() > 991) {
        $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeIn(200);
      }
    },
    function() {
      if ($(window).width() > 991) {
        $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeOut(200);
      }
    }
  );

  $('.navbar-toggler').on('click', function() {
    setTimeout(function() {
      if ($('.navbar-collapse').hasClass('show')) {
        $('.mobile-menu-cta').slideDown();
      } else {
        $('.mobile-menu-cta').slideUp();
      }
    }, 10);
  });

  $(document).on('click', function(e) {
    if (!$(e.target).closest('.navbar').length) {
      $('.navbar-collapse').collapse('hide');
      $('.mobile-menu-cta').slideUp();
    }
  });

  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        $(entry.target).addClass('animate-in');
      }
    });
  }, { threshold: 0.1 });

  $('.feature-card, .why-card, .target-card, .problem-item, .solution-item').each(function() {
    observer.observe(this);
  });

  if (window.location.hash) {
    var hash = window.location.hash;
    setTimeout(function() {
      $('html, body').animate({
        scrollTop: $(hash).offset().top - 150
      }, 600);
    }, 100);
  }

  $('.feature-nav a').on('click', function(e) {
    e.preventDefault();
    var target = $($(this).attr('href'));
    if (target.length) {
      $('html, body').animate({
        scrollTop: target.offset().top - 150
      }, 600);
    }
    $('.feature-nav a').removeClass('active');
    $(this).addClass('active');
  });

  $(window).on('scroll', function() {
    var scrollPos = $(window).scrollTop();
    $('.feature-section').each(function() {
      var top = $(this).offset().top - 200;
      var bottom = top + $(this).outerHeight();
      var id = $(this).attr('id');
      if (scrollPos >= top && scrollPos < bottom) {
        $('.feature-nav a').removeClass('active');
        $('.feature-nav a[href="#' + id + '"]').addClass('active');
      }
    });
  });
});
