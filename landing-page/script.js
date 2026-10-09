const menuButton = document.querySelector('.menu-toggle');
const menu = document.querySelector('.primary-nav');

menuButton?.addEventListener('click', () => {
  const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!isOpen));
  menuButton.setAttribute('aria-label', isOpen ? 'Open menu' : 'Close menu');
  menu.classList.toggle('is-open', !isOpen);
});

menu?.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Open menu');
    menu.classList.remove('is-open');
  });
});

const siteHeader = document.querySelector('.site-header');
if (siteHeader) {
  let previousScrollY = window.scrollY;
  let scrollFrame = 0;

  const updateHeader = () => {
    const currentScrollY = Math.max(0, window.scrollY);
    const keyboardFocus = siteHeader.contains(document.activeElement) && document.activeElement.matches(':focus-visible');
    if (currentScrollY === 0 || currentScrollY < previousScrollY || keyboardFocus || menu?.classList.contains('is-open')) {
      siteHeader.classList.remove('is-hidden');
    } else if (currentScrollY > siteHeader.offsetHeight && currentScrollY > previousScrollY) {
      siteHeader.classList.add('is-hidden');
    }
    previousScrollY = currentScrollY;
    scrollFrame = 0;
  };

  window.addEventListener('scroll', () => {
    if (!scrollFrame) scrollFrame = requestAnimationFrame(updateHeader);
  }, { passive: true });
  siteHeader.addEventListener('focusin', () => siteHeader.classList.remove('is-hidden'));
}

const serviceSlider = document.getElementById('service-slider');

if (serviceSlider && window.Splide) {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const carousel = new Splide(serviceSlider, {
    type: 'loop',
    perPage: 1,
    drag: true,
    arrows: true,
    pagination: false,
    keyboard: 'focused',
    autoplay: 'pause',
    interval: 2750,
    pauseOnHover: false,
    pauseOnFocus: true,
    speed: 450,
  });
  carousel.mount();

  const autoplay = carousel.Components.Autoplay;
  let inView = false;
  const updateAutoplay = () => {
    const keyboardFocus = serviceSlider.contains(document.activeElement) && document.activeElement.matches(':focus-visible');
    if (inView && !document.hidden && !reducedMotion.matches && !keyboardFocus) autoplay.play();
    else autoplay.pause();
  };

  carousel.on('drag', () => autoplay.pause());
  carousel.on('dragged', updateAutoplay);
  document.addEventListener('visibilitychange', updateAutoplay);
  reducedMotion.addEventListener('change', updateAutoplay);
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(([entry]) => {
      inView = entry.intersectionRatio >= 0.25;
      updateAutoplay();
    }, { threshold: 0.25 }).observe(serviceSlider);
  } else {
    inView = true;
    updateAutoplay();
  }
}

document.getElementById('year').textContent = new Date().getFullYear();
