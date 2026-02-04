/**
 * js_new.js
 * Hospital Website JavaScript
 *
 * Dependencies (use official CDNs):
 * - jQuery: https://code.jquery.com/jquery-3.7.1.min.js
 * - Bootstrap CSS: https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css
 * - Bootstrap JS: https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js
 * - Owl Carousel CSS: https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.3.4/assets/owl.carousel.min.css
 * - Owl Carousel JS: https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.3.4/owl.carousel.min.js
 * - Noto Sans KR: https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap
 */

(function($) {
  'use strict';

  // ==========================================================================
  // Configuration
  // ==========================================================================

  const CONFIG = {
    headerScrollThreshold: 100,
    animationOffset: 100,
    smoothScrollDuration: 800,
    sliderAutoplayTimeout: 5000
  };

  // ==========================================================================
  // 1. Mobile Menu Toggle
  // ==========================================================================

  const MobileMenu = {
    init: function() {
      this.menuToggle = $('.header__menu-toggle');
      this.mobileNav = $('.mobile-nav');
      this.body = $('body');

      this.bindEvents();
    },

    bindEvents: function() {
      const self = this;

      // Toggle menu on button click
      this.menuToggle.on('click', function(e) {
        e.preventDefault();
        self.toggleMenu();
      });

      // Close menu when clicking a link
      this.mobileNav.find('a').on('click', function() {
        self.closeMenu();
      });

      // Close menu on window resize (if resized to desktop)
      $(window).on('resize', function() {
        if ($(window).width() > 991) {
          self.closeMenu();
        }
      });

      // Close menu when clicking outside
      $(document).on('click', function(e) {
        if (!$(e.target).closest('.header__menu-toggle, .mobile-nav').length) {
          self.closeMenu();
        }
      });
    },

    toggleMenu: function() {
      this.menuToggle.toggleClass('active');
      this.mobileNav.toggleClass('active');
      this.body.toggleClass('menu-open');
    },

    closeMenu: function() {
      this.menuToggle.removeClass('active');
      this.mobileNav.removeClass('active');
      this.body.removeClass('menu-open');
    }
  };

  // ==========================================================================
  // 2. Hero Slider (Owl Carousel)
  // ==========================================================================

  const HeroSlider = {
    init: function() {
      this.slider = $('.hero__slider');

      if (this.slider.length && typeof $.fn.owlCarousel !== 'undefined') {
        this.initCarousel();
      }
    },

    initCarousel: function() {
      this.slider.owlCarousel({
        items: 1,
        loop: true,
        autoplay: true,
        autoplayTimeout: CONFIG.sliderAutoplayTimeout,
        autoplayHoverPause: true,
        nav: true,
        navText: [
          '<span aria-label="Previous">&lt;</span>',
          '<span aria-label="Next">&gt;</span>'
        ],
        dots: true,
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        smartSpeed: 500,
        mouseDrag: true,
        touchDrag: true,
        responsive: {
          0: {
            nav: false
          },
          768: {
            nav: true
          }
        }
      });

      // Animate content on slide change
      this.slider.on('changed.owl.carousel', function(event) {
        const currentSlide = $(event.target).find('.owl-item.active');

        // Reset and animate content
        currentSlide.find('.hero__content').css({
          opacity: 0,
          transform: 'translateY(30px)'
        }).animate({
          opacity: 1
        }, {
          duration: 600,
          step: function(now, fx) {
            if (fx.prop === 'opacity') {
              $(this).css('transform', 'translateY(' + (30 - now * 30) + 'px)');
            }
          }
        });
      });
    }
  };

  // ==========================================================================
  // 3. Smooth Scroll
  // ==========================================================================

  const SmoothScroll = {
    init: function() {
      this.bindEvents();
    },

    bindEvents: function() {
      const self = this;

      // Smooth scroll for anchor links
      $('a[href^="#"]').on('click', function(e) {
        const target = $(this.getAttribute('href'));

        if (target.length) {
          e.preventDefault();
          self.scrollTo(target);
        }
      });
    },

    scrollTo: function(target) {
      const headerHeight = $('.header').outerHeight() || 80;
      const targetOffset = target.offset().top - headerHeight;

      $('html, body').animate({
        scrollTop: targetOffset
      }, CONFIG.smoothScrollDuration, 'swing');
    },

    // Public method to scroll to specific element
    scrollToElement: function(selector) {
      const target = $(selector);
      if (target.length) {
        this.scrollTo(target);
      }
    }
  };

  // ==========================================================================
  // 4. Scroll Animations (Fade In on Scroll)
  // ==========================================================================

  const ScrollAnimations = {
    init: function() {
      this.animatedElements = $('.fade-in, .fade-in-left, .fade-in-right');

      if (this.animatedElements.length) {
        this.bindEvents();
        this.checkVisibility();
      }
    },

    bindEvents: function() {
      const self = this;

      // Check visibility on scroll
      $(window).on('scroll', function() {
        self.checkVisibility();
      });

      // Check on window resize
      $(window).on('resize', function() {
        self.checkVisibility();
      });
    },

    checkVisibility: function() {
      const windowHeight = $(window).height();
      const windowTop = $(window).scrollTop();
      const windowBottom = windowTop + windowHeight;

      this.animatedElements.each(function() {
        const element = $(this);
        const elementTop = element.offset().top;
        const elementHeight = element.outerHeight();

        // Check if element is in viewport
        if (elementTop + CONFIG.animationOffset < windowBottom &&
            elementTop + elementHeight > windowTop) {
          // Add delay based on data attribute if present
          const delay = element.data('delay') || 0;

          setTimeout(function() {
            element.addClass('visible');
          }, delay);
        }
      });
    },

    // Reset animations (useful for dynamic content)
    reset: function() {
      this.animatedElements.removeClass('visible');
    }
  };

  // ==========================================================================
  // 5. Header Scroll Behavior (Sticky/Transparent)
  // ==========================================================================

  const HeaderScroll = {
    init: function() {
      this.header = $('.header');
      this.lastScrollTop = 0;

      if (this.header.length) {
        this.bindEvents();
        this.checkScroll();
      }
    },

    bindEvents: function() {
      const self = this;

      $(window).on('scroll', function() {
        self.checkScroll();
      });
    },

    checkScroll: function() {
      const scrollTop = $(window).scrollTop();

      // Add/remove scrolled class based on scroll position
      if (scrollTop > CONFIG.headerScrollThreshold) {
        this.header.removeClass('header--transparent').addClass('header--scrolled');
      } else {
        this.header.removeClass('header--scrolled').addClass('header--transparent');
      }

      // Optional: Hide header on scroll down, show on scroll up
      // Uncomment below code to enable this feature
      /*
      if (scrollTop > this.lastScrollTop && scrollTop > CONFIG.headerScrollThreshold) {
        // Scrolling down
        this.header.addClass('header--hidden');
      } else {
        // Scrolling up
        this.header.removeClass('header--hidden');
      }
      this.lastScrollTop = scrollTop;
      */
    }
  };

  // ==========================================================================
  // Additional Utilities
  // ==========================================================================

  const Utils = {
    // Debounce function for performance optimization
    debounce: function(func, wait) {
      let timeout;
      return function executedFunction(...args) {
        const later = function() {
          clearTimeout(timeout);
          func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    },

    // Throttle function for scroll events
    throttle: function(func, limit) {
      let lastFunc;
      let lastRan;
      return function() {
        const context = this;
        const args = arguments;
        if (!lastRan) {
          func.apply(context, args);
          lastRan = Date.now();
        } else {
          clearTimeout(lastFunc);
          lastFunc = setTimeout(function() {
            if ((Date.now() - lastRan) >= limit) {
              func.apply(context, args);
              lastRan = Date.now();
            }
          }, limit - (Date.now() - lastRan));
        }
      };
    },

    // Check if element is in viewport
    isInViewport: function(element) {
      const rect = element.getBoundingClientRect();
      return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
      );
    },

    // Get URL parameter
    getUrlParam: function(param) {
      const urlParams = new URLSearchParams(window.location.search);
      return urlParams.get(param);
    }
  };

  // ==========================================================================
  // Back to Top Button
  // ==========================================================================

  const BackToTop = {
    init: function() {
      this.createButton();
      this.bindEvents();
    },

    createButton: function() {
      if ($('.back-to-top').length === 0) {
        $('body').append(
          '<button class="back-to-top" aria-label="Back to top" style="' +
          'position: fixed; bottom: 30px; right: 30px; width: 50px; height: 50px; ' +
          'background-color: #2563eb; color: #fff; border: none; border-radius: 50%; ' +
          'cursor: pointer; opacity: 0; visibility: hidden; transition: all 0.3s; ' +
          'display: flex; align-items: center; justify-content: center; z-index: 999; ' +
          'box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);">' +
          '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
          'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
          '<polyline points="18 15 12 9 6 15"></polyline></svg></button>'
        );
      }
      this.button = $('.back-to-top');
    },

    bindEvents: function() {
      const self = this;

      // Show/hide button based on scroll position
      $(window).on('scroll', function() {
        if ($(window).scrollTop() > 300) {
          self.button.css({
            opacity: 1,
            visibility: 'visible'
          });
        } else {
          self.button.css({
            opacity: 0,
            visibility: 'hidden'
          });
        }
      });

      // Scroll to top on click
      this.button.on('click', function() {
        $('html, body').animate({
          scrollTop: 0
        }, CONFIG.smoothScrollDuration);
      });

      // Hover effect
      this.button.on('mouseenter', function() {
        $(this).css('transform', 'translateY(-3px)');
      }).on('mouseleave', function() {
        $(this).css('transform', 'translateY(0)');
      });
    }
  };

  // ==========================================================================
  // Lazy Loading Images
  // ==========================================================================

  const LazyLoad = {
    init: function() {
      // Use native lazy loading if supported
      if ('loading' in HTMLImageElement.prototype) {
        $('img[data-src]').each(function() {
          $(this).attr('src', $(this).data('src'));
          $(this).attr('loading', 'lazy');
        });
      } else {
        // Fallback for older browsers
        this.lazyLoadFallback();
      }
    },

    lazyLoadFallback: function() {
      const lazyImages = $('img[data-src]');

      const loadImage = function() {
        lazyImages.each(function() {
          const img = $(this);
          if (Utils.isInViewport(this)) {
            img.attr('src', img.data('src')).removeAttr('data-src');
          }
        });
      };

      $(window).on('scroll resize', Utils.throttle(loadImage, 200));
      loadImage();
    }
  };

  // ==========================================================================
  // Form Validation (Basic)
  // ==========================================================================

  const FormValidation = {
    init: function() {
      $('form[data-validate]').each(function() {
        const form = $(this);

        form.on('submit', function(e) {
          if (!FormValidation.validateForm(form)) {
            e.preventDefault();
          }
        });
      });
    },

    validateForm: function(form) {
      let isValid = true;

      form.find('[required]').each(function() {
        const input = $(this);
        const value = input.val().trim();

        if (!value) {
          isValid = false;
          input.addClass('is-invalid');
        } else {
          input.removeClass('is-invalid');
        }

        // Email validation
        if (input.attr('type') === 'email' && value) {
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!emailRegex.test(value)) {
            isValid = false;
            input.addClass('is-invalid');
          }
        }

        // Phone validation (Korean format)
        if (input.attr('type') === 'tel' && value) {
          const phoneRegex = /^[0-9]{2,3}-?[0-9]{3,4}-?[0-9]{4}$/;
          if (!phoneRegex.test(value)) {
            isValid = false;
            input.addClass('is-invalid');
          }
        }
      });

      return isValid;
    }
  };

  // ==========================================================================
  // Counter Animation (for statistics)
  // ==========================================================================

  const CounterAnimation = {
    init: function() {
      this.counters = $('[data-counter]');

      if (this.counters.length) {
        this.bindEvents();
      }
    },

    bindEvents: function() {
      const self = this;

      $(window).on('scroll', function() {
        self.counters.each(function() {
          const counter = $(this);
          if (Utils.isInViewport(this) && !counter.hasClass('counted')) {
            self.animateCounter(counter);
          }
        });
      });
    },

    animateCounter: function(counter) {
      counter.addClass('counted');

      const target = parseInt(counter.data('counter'), 10);
      const duration = counter.data('duration') || 2000;
      const increment = target / (duration / 16);

      let current = 0;

      const timer = setInterval(function() {
        current += increment;
        if (current >= target) {
          counter.text(target.toLocaleString());
          clearInterval(timer);
        } else {
          counter.text(Math.floor(current).toLocaleString());
        }
      }, 16);
    }
  };

  // ==========================================================================
  // Initialize All Modules
  // ==========================================================================

  $(document).ready(function() {
    // Initialize all modules
    MobileMenu.init();
    HeroSlider.init();
    SmoothScroll.init();
    ScrollAnimations.init();
    HeaderScroll.init();
    BackToTop.init();
    LazyLoad.init();
    FormValidation.init();
    CounterAnimation.init();

    // Add loaded class to body when page is ready
    $('body').addClass('page-loaded');

    // Log initialization
    console.log('Hospital website scripts initialized successfully.');
  });

  // Re-check animations after all images are loaded
  $(window).on('load', function() {
    ScrollAnimations.checkVisibility();
  });

  // ==========================================================================
  // Expose public API
  // ==========================================================================

  window.HospitalSite = {
    smoothScroll: SmoothScroll,
    scrollAnimations: ScrollAnimations,
    utils: Utils,
    config: CONFIG
  };

})(jQuery);
