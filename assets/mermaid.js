// Jekyll emits code fences as plain code; enhance Mermaid fences after rendering.
const blocks = [...document.querySelectorAll('pre > code.language-mermaid, .language-mermaid pre > code')];

if (blocks.length) {
  try {
    const { default: mermaid } = await import('https://cdn.jsdelivr.net/npm/mermaid@11.12.0/dist/mermaid.esm.min.mjs');
    mermaid.initialize({
      startOnLoad: false,
      securityLevel: 'strict',
      fontFamily: 'Arial, Helvetica, sans-serif',
      flowchart: { useMaxWidth: false },
    });
    for (const [index, code] of blocks.entries()) {
      const { svg } = await mermaid.render(`notes-diagram-${index}`, code.textContent);
      const diagram = document.createElement('div');
      diagram.className = 'mermaid';
      diagram.tabIndex = 0;
      diagram.setAttribute('role', 'region');
      diagram.setAttribute('aria-label', 'Diagram (scroll to explore)');
      diagram.innerHTML = svg;
      const viewer = document.createElement('section');
      viewer.className = 'diagram-viewer';
      const toolbar = document.createElement('div');
      toolbar.className = 'diagram-toolbar';
      toolbar.setAttribute('aria-label', 'Diagram zoom controls');
      const percent = document.createElement('output');
      percent.setAttribute('aria-label', 'Zoom level');
      const drawing = diagram.querySelector('svg');
      const bounds = drawing.viewBox.baseVal;
      const width = bounds.width;
      const height = bounds.height;
      let scale = 1;
      let gestureStart = null;
      function zoom(next, x = diagram.clientWidth / 2, y = diagram.clientHeight / 2) {
        next = Math.min(4, Math.max(0.02, next));
        const ratio = next / scale;
        const left = (diagram.scrollLeft + x) * ratio - x;
        const top = (diagram.scrollTop + y) * ratio - y;
        scale = next;
        drawing.style.width = `${width * scale}px`;
        drawing.style.height = `${height * scale}px`;
        diagram.scrollLeft = left;
        diagram.scrollTop = top;
        percent.textContent = `${Math.round(scale * 100)}%`;
      }
      function fit() {
        zoom(Math.min(diagram.clientWidth / width, diagram.clientHeight / height));
        diagram.scrollTo(0, 0);
      }
      for (const [label, action] of [
        ['Zoom in', () => zoom(scale * 1.25)],
        ['Zoom out', () => zoom(scale / 1.25)],
        ['Fit to screen', fit],
        ['Reset', () => { zoom(1); diagram.scrollTo(0, 0); }],
      ]) {
        const button = document.createElement('button');
        button.type = 'button';
        button.textContent = label;
        button.addEventListener('click', action);
        toolbar.append(button);
      }
      const fullscreen = document.createElement('button');
      fullscreen.type = 'button';
      fullscreen.textContent = 'Fullscreen';
      fullscreen.addEventListener('click', async () => {
        if (document.fullscreenElement === viewer) {
          await document.exitFullscreen();
        } else if (viewer.requestFullscreen && document.fullscreenEnabled) {
          await viewer.requestFullscreen();
        } else {
          viewer.classList.toggle('diagram-expanded');
          fullscreen.textContent = viewer.classList.contains('diagram-expanded') ? 'Exit fullscreen' : 'Fullscreen';
          fit();
        }
      });
      document.addEventListener('fullscreenchange', () => {
        fullscreen.textContent = document.fullscreenElement === viewer ? 'Exit fullscreen' : 'Fullscreen';
        fit();
      });
      document.addEventListener('keydown', event => {
        if (event.key === 'Escape' && viewer.classList.contains('diagram-expanded')) {
          viewer.classList.remove('diagram-expanded');
          fullscreen.textContent = 'Fullscreen';
          fit();
        }
      });
      toolbar.append(fullscreen, percent);
      const hint = document.createElement('span');
      hint.textContent = 'Pinch to zoom · Scroll to pan';
      hint.className = 'diagram-hint';
      toolbar.append(hint);
      diagram.setAttribute('aria-label', 'Diagram: pinch to zoom, scroll to pan');
      diagram.addEventListener('wheel', event => {
        if (!event.ctrlKey) return;
        event.preventDefault();
        if (gestureStart !== null) return;
        const rect = diagram.getBoundingClientRect();
        const delta = event.deltaY * (event.deltaMode === 1 ? 16 : event.deltaMode === 2 ? diagram.clientHeight : 1);
        zoom(scale * Math.exp(-delta * 0.01), event.clientX - rect.left, event.clientY - rect.top);
      }, { passive: false });
      // Safari exposes trackpad pinch as gesture events instead of Ctrl+wheel.
      diagram.addEventListener('gesturestart', event => {
        event.preventDefault();
        gestureStart = scale;
      }, { passive: false });
      diagram.addEventListener('gesturechange', event => {
        event.preventDefault();
        if (gestureStart === null) return;
        const rect = diagram.getBoundingClientRect();
        zoom(gestureStart * event.scale, event.clientX - rect.left, event.clientY - rect.top);
      }, { passive: false });
      diagram.addEventListener('gestureend', event => {
        event.preventDefault();
        gestureStart = null;
      }, { passive: false });
      viewer.append(toolbar, diagram);
      code.parentElement.replaceWith(viewer);
      fit();
    }
  } catch (error) {
    console.error('Could not render Mermaid diagram:', error);
    const message = document.createElement('p');
    message.setAttribute('role', 'status');
    message.textContent = 'The diagram could not load. Its source is shown below; reload to try again.';
    const remaining = blocks.find(code => code.isConnected);
    remaining?.parentElement.before(message);
  }
}
