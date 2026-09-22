---
title: Sources and transcripts
---

[Complete context for LLMs]({{ '/llms-full.txt' | relative_url }}) · [Document index]({{ '/llms.txt' | relative_url }})

## Original source documents

{% for source in site.data.sources %}{% if source.kind == 'source' %}
- <a href="{{ source.url | relative_url }}" download>{{ source.label | escape }} ({{ source.format }})</a>{% if source.text_url %} · <a href="{{ source.text_url | relative_url }}" download>Same document as text (TXT)</a>{% endif %}{% if source.description %}<br>{{ source.description | escape }}{% endif %}
{% endif %}{% endfor %}
