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

const serviceSlider = document.getElementById('service-slider');
const serviceSlides = [...(serviceSlider?.querySelectorAll('.service-slide') ?? [])];
const servicePrev = document.getElementById('service-prev');
const serviceNext = document.getElementById('service-next');
const servicePosition = document.getElementById('service-position');
const serviceProgress = document.getElementById('service-progress-fill');
const serviceAnnouncement = document.getElementById('service-announcement');

if (serviceSlider && serviceSlides.length && servicePrev && serviceNext) {
  const section = serviceSlider.closest('.services');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const autoplayDelay = 5500;
  let activeIndex = 0;
  let scrollFrame = 0;
  let autoplayTimer = 0;
  let inView = false;
  let hovered = false;
  let touching = false;

  const updateControls = (index) => {
    activeIndex = index;
    servicePrev.disabled = index === 0;
    serviceNext.disabled = index === serviceSlides.length - 1;
    servicePosition.textContent = `${String(index + 1).padStart(2, '0')} / ${String(serviceSlides.length).padStart(2, '0')}`;
    servicePosition.setAttribute('aria-label', `Service ${index + 1} of ${serviceSlides.length}`);
    serviceProgress.style.width = `${((index + 1) / serviceSlides.length) * 100}%`;
  };

  const nearestSlide = () => serviceSlides.reduce((nearest, slide, index) => {
    const distance = Math.abs(slide.offsetLeft - serviceSlides[0].offsetLeft - serviceSlider.scrollLeft);
    return distance < nearest.distance ? { index, distance } : nearest;
  }, { index: 0, distance: Infinity }).index;

  const goToSlide = (index, announce = false) => {
    const nextIndex = Math.max(0, Math.min(serviceSlides.length - 1, index));
    updateControls(nextIndex);
    if (announce) {
      const title = serviceSlides[nextIndex].querySelector('h3').textContent;
      serviceAnnouncement.textContent = `${title}, service ${nextIndex + 1} of ${serviceSlides.length}`;
    }
    serviceSlider.scrollTo({
      left: serviceSlides[nextIndex].offsetLeft - serviceSlides[0].offsetLeft,
      behavior: reducedMotion.matches ? 'auto' : 'smooth',
    });
  };

  const scheduleAutoplay = () => {
    clearTimeout(autoplayTimer);
    const keyboardFocus = section.contains(document.activeElement) && document.activeElement.matches(':focus-visible');
    if (reducedMotion.matches || document.hidden || !inView || hovered || touching || keyboardFocus) return;
    autoplayTimer = window.setTimeout(() => {
      goToSlide((activeIndex + 1) % serviceSlides.length);
      scheduleAutoplay();
    }, autoplayDelay);
  };

  servicePrev.addEventListener('click', () => { goToSlide(activeIndex - 1, true); scheduleAutoplay(); });
  serviceNext.addEventListener('click', () => { goToSlide(activeIndex + 1, true); scheduleAutoplay(); });
  serviceSlider.addEventListener('scroll', () => {
    if (scrollFrame) return;
    scrollFrame = requestAnimationFrame(() => {
      updateControls(nearestSlide());
      scrollFrame = 0;
      scheduleAutoplay();
    });
  }, { passive: true });
  serviceSlider.addEventListener('mouseenter', () => { hovered = true; scheduleAutoplay(); });
  serviceSlider.addEventListener('mouseleave', () => { hovered = false; scheduleAutoplay(); });
  serviceSlider.addEventListener('pointerdown', () => { touching = true; scheduleAutoplay(); });
  window.addEventListener('pointerup', () => { touching = false; scheduleAutoplay(); });
  section.addEventListener('focusin', scheduleAutoplay);
  section.addEventListener('focusout', () => window.setTimeout(scheduleAutoplay, 0));
  document.addEventListener('visibilitychange', scheduleAutoplay);
  reducedMotion.addEventListener('change', scheduleAutoplay);
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(([entry]) => {
      inView = entry.intersectionRatio >= 0.25;
      scheduleAutoplay();
    }, { threshold: 0.25 }).observe(serviceSlider);
  } else {
    inView = true;
    scheduleAutoplay();
  }
  updateControls(0);
}

document.getElementById('year').textContent = new Date().getFullYear();
