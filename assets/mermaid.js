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
      code.parentElement.replaceWith(diagram);
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
