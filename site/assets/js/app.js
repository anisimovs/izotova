/* ============================================================
   Интерактив: фильтры по возрасту, лайтбокс обложек,
   появление блоков при скролле, состояние шапки.
   Без зависимостей.
   ============================================================ */
(function () {
  'use strict';

  /* ─────────── 1. Фильтры каталога ─────────── */
  var grid = document.getElementById('grid');
  var emptyNote = document.getElementById('emptyNote');
  var filterBtns = Array.prototype.slice.call(document.querySelectorAll('.filter'));

  if (grid && filterBtns.length) {
    var cards = Array.prototype.slice.call(grid.querySelectorAll('.card'));

    filterBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var wanted = btn.getAttribute('data-filter');

        filterBtns.forEach(function (other) {
          var isActive = other === btn;
          other.classList.toggle('is-active', isActive);
          other.setAttribute('aria-selected', isActive ? 'true' : 'false');
        });

        var shown = 0;
        cards.forEach(function (card) {
          var age = card.getAttribute('data-age');
          var match = wanted === 'all' || age === wanted;
          card.classList.toggle('is-hidden', !match);
          if (match) {
            shown++;
          }
        });

        if (emptyNote) {
          emptyNote.hidden = shown > 0;
        }
      });
    });
  }

  /* ─────────── 2. Лайтбокс обложек ─────────── */
  var lightbox = document.getElementById('lightbox');
  var lightboxImg = lightbox ? lightbox.querySelector('.lightbox-img') : null;

  if (lightbox && lightboxImg) {
    var lastFocused = null;

    var openLightbox = function (card) {
      var img = card.querySelector('.card-media img');
      if (!img) return;

      lightboxImg.src = img.getAttribute('src');
      lightboxImg.alt = img.getAttribute('alt') || '';
      lastFocused = document.activeElement;

      lightbox.hidden = false;
      requestAnimationFrame(function () {
        lightbox.classList.add('is-open');
      });
      document.body.style.overflow = 'hidden';
      var closeBtn = lightbox.querySelector('.lightbox-close');
      if (closeBtn) closeBtn.focus();
    };

    var closeLightbox = function () {
      lightbox.classList.remove('is-open');
      document.body.style.overflow = '';
      var finish = function () {
        lightbox.hidden = true;
        lightboxImg.removeAttribute('src');
      };
      setTimeout(finish, 240);
      if (lastFocused) lastFocused.focus();
    };

    // Клик по обложке открывает просмотр; сама карточка ведёт на покупку,
    // поэтому перехватываем только когда нет модификаторов.
    document.querySelectorAll('.card-media').forEach(function (link) {
      link.addEventListener('click', function (e) {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
        e.preventDefault();
        openLightbox(link.closest('.card'));
      });
    });

    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox || e.target.closest('.lightbox-close')) closeLightbox();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !lightbox.hidden) closeLightbox();
    });
  }

  /* ─────────── 3. Появление блоков при скролле ─────────── */
  var revealables = document.querySelectorAll('.reveal');

  if (!('IntersectionObserver' in window)) {
    revealables.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });

    revealables.forEach(function (el) { io.observe(el); });
  }

  /* ─────────── 4. Тень шапки при скролле ─────────── */
  var topbar = document.querySelector('.topbar');

  if (topbar) {
    var onScroll = function () {
      topbar.classList.toggle('is-stuck', window.scrollY > 8);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }
})();