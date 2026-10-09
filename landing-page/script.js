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
  const autoplayDelay = 2750;
  const lastClone = serviceSlides.at(-1).cloneNode(true);
  const firstClone = serviceSlides[0].cloneNode(true);
  for (const clone of [lastClone, firstClone]) {
    clone.setAttribute('aria-hidden', 'true');
    clone.setAttribute('inert', '');
  }
  serviceSlider.prepend(lastClone);
  serviceSlider.append(firstClone);
  const trackSlides = [lastClone, ...serviceSlides, firstClone];
  let activeIndex = 0;
  let physicalIndex = 1;
  let scrollFrame = 0;
  let settleTimer = 0;
  let autoplayTimer = 0;
  let inView = false;
  let touching = false;

  const slideLeft = (index) => trackSlides[index].offsetLeft - trackSlides[0].offsetLeft;
  const logicalIndex = (index) => (index - 1 + serviceSlides.length) % serviceSlides.length;

  const updateControls = (index) => {
    physicalIndex = index;
    activeIndex = logicalIndex(index);
    servicePosition.textContent = `${String(activeIndex + 1).padStart(2, '0')} / ${String(serviceSlides.length).padStart(2, '0')}`;
    servicePosition.setAttribute('aria-label', `Service ${activeIndex + 1} of ${serviceSlides.length}`);
    serviceProgress.style.width = `${((activeIndex + 1) / serviceSlides.length) * 100}%`;
  };

  const nearestSlide = () => trackSlides.reduce((nearest, slide, index) => {
    const distance = Math.abs(slideLeft(index) - serviceSlider.scrollLeft);
    return distance < nearest.distance ? { index, distance } : nearest;
  }, { index: 0, distance: Infinity }).index;

  const jumpToSlide = (index) => {
    serviceSlider.style.scrollBehavior = 'auto';
    serviceSlider.style.scrollSnapType = 'none';
    serviceSlider.scrollLeft = slideLeft(index);
    serviceSlider.style.scrollSnapType = '';
    serviceSlider.style.scrollBehavior = '';
    updateControls(index);
  };

  const settleLoop = () => {
    const index = nearestSlide();
    if (index === 0) jumpToSlide(serviceSlides.length);
    else if (index === trackSlides.length - 1) jumpToSlide(1);
    else updateControls(index);
  };

  const goToSlide = (direction, announce = false) => {
    if (physicalIndex === 0 || physicalIndex === trackSlides.length - 1) settleLoop();
    const nextIndex = physicalIndex + direction;
    updateControls(nextIndex);
    if (announce) {
      const title = serviceSlides[activeIndex].querySelector('h3').textContent;
      serviceAnnouncement.textContent = `${title}, service ${activeIndex + 1} of ${serviceSlides.length}`;
    }
    serviceSlider.scrollTo({
      left: slideLeft(nextIndex),
      behavior: reducedMotion.matches ? 'auto' : 'smooth',
    });
  };

  const scheduleAutoplay = () => {
    clearTimeout(autoplayTimer);
    const keyboardFocus = section.contains(document.activeElement) && document.activeElement.matches(':focus-visible');
    if (reducedMotion.matches || document.hidden || !inView || touching || keyboardFocus) return;
    autoplayTimer = window.setTimeout(() => {
      goToSlide(1);
      scheduleAutoplay();
    }, autoplayDelay);
  };

  servicePrev.addEventListener('click', () => { goToSlide(-1, true); scheduleAutoplay(); });
  serviceNext.addEventListener('click', () => { goToSlide(1, true); scheduleAutoplay(); });
  serviceSlider.addEventListener('keydown', (event) => {
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    event.preventDefault();
    goToSlide(event.key === 'ArrowRight' ? 1 : -1, true);
    scheduleAutoplay();
  });
  serviceSlider.addEventListener('scroll', () => {
    if (scrollFrame) return;
    scrollFrame = requestAnimationFrame(() => {
      updateControls(nearestSlide());
      scrollFrame = 0;
      scheduleAutoplay();
    });
    if (!('onscrollend' in serviceSlider)) {
      clearTimeout(settleTimer);
      settleTimer = window.setTimeout(settleLoop, 180);
    }
  }, { passive: true });
  serviceSlider.addEventListener('scrollend', settleLoop);
  serviceSlider.addEventListener('pointerdown', () => { touching = true; scheduleAutoplay(); });
  window.addEventListener('pointerup', () => { touching = false; scheduleAutoplay(); });
  section.addEventListener('focusin', scheduleAutoplay);
  section.addEventListener('focusout', () => window.setTimeout(scheduleAutoplay, 0));
  document.addEventListener('visibilitychange', scheduleAutoplay);
  reducedMotion.addEventListener('change', scheduleAutoplay);
  window.addEventListener('resize', () => jumpToSlide(activeIndex + 1));
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(([entry]) => {
      inView = entry.intersectionRatio >= 0.25;
      scheduleAutoplay();
    }, { threshold: 0.25 }).observe(serviceSlider);
  } else {
    inView = true;
    scheduleAutoplay();
  }
  jumpToSlide(1);
}

document.getElementById('year').textContent = new Date().getFullYear();
