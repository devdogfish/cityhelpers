// Without JavaScript all navigation remains visible.
const toggle = document.querySelector('.nav-toggle');
const sidebar = toggle?.closest('aside');
if (toggle && sidebar) {
  const mobile = matchMedia('(max-width: 760px)');
  const setExpanded = expanded => {
    toggle.setAttribute('aria-expanded', String(expanded));
    sidebar.classList.toggle('is-collapsed', !expanded);
  };
  toggle.hidden = false;
  setExpanded(!mobile.matches);
  toggle.addEventListener('click', () => setExpanded(toggle.getAttribute('aria-expanded') !== 'true'));
  mobile.addEventListener('change', () => setExpanded(!mobile.matches));
}
