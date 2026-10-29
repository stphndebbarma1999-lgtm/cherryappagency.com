/* Cherry App Agency: mobile menu toggle and the diamond-to-USD converter.
   All page content works without this file. */
(function () {
  'use strict';

  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.hidden = false;
    var setOpen = function (open) {
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      nav.classList.toggle('is-open', open);
    };
    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        toggle.focus();
      }
    });
    window.matchMedia('(min-width: 1080px)').addEventListener('change', function (mq) {
      if (mq.matches) setOpen(false);
    });
  }

  // Keep the floating WhatsApp button out of the way while the page hero,
  // which carries the main calls to action, is visible.
  var floatBtn = document.querySelector('.wa-float');
  var hero = document.querySelector('.hero, .page-hero');
  if (floatBtn && hero && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      floatBtn.classList.toggle('is-hidden', entries[0].isIntersecting);
    }).observe(hero);
  }

  var form = document.getElementById('diamond-converter');
  if (form) {
    var input = form.querySelector('input');
    var result = document.getElementById('converter-result');
    var DIAMONDS_PER_USD = 10000;
    var HOST_MINIMUM_USD = 10;
    var usd = new Intl.NumberFormat('en-US', {
      style: 'currency', currency: 'USD', minimumFractionDigits: 2, maximumFractionDigits: 4
    });
    var count = new Intl.NumberFormat('en-US');

    var show = function (message, isError) {
      result.innerHTML = '';
      var p = document.createElement('p');
      if (isError) p.className = 'converter-error';
      p.innerHTML = message;
      result.appendChild(p);
      input.setAttribute('aria-invalid', isError ? 'true' : 'false');
    };

    var convert = function () {
      var raw = input.value.replace(/[\s,]/g, '');
      if (raw === '') {
        show('Enter a number of diamonds to see the USD equivalent.', false);
        return;
      }
      if (!/^\d+$/.test(raw)) {
        show('Please enter a whole number of diamonds using digits only, for example 250000. Negative numbers and decimals are not accepted.', true);
        return;
      }
      if (raw.length > 15) {
        show('That number is too large to convert reliably. Please enter 15 digits or fewer.', true);
        return;
      }
      var diamonds = Number(raw);
      var dollars = diamonds / DIAMONDS_PER_USD;
      var minimumText = dollars >= HOST_MINIMUM_USD
        ? 'This is at or above the stated $10 host minimum withdrawal.'
        : 'This is below the stated $10 host minimum withdrawal (100,000 diamonds).';
      show(count.format(diamonds) + ' diamonds &asymp; <strong>' + usd.format(dollars) + '</strong><br>' +
        'Conversion estimate at 10,000 diamonds = $1. ' + minimumText +
        ' This is not an approved payout amount.', false);
    };

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      convert();
    });
    input.addEventListener('input', convert);
  }
})();
