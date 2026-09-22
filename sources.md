---
title: Sources and transcripts
---

[Complete context for LLMs]({{ '/llms-full.txt' | relative_url }}) · [Document index]({{ '/llms.txt' | relative_url }})

## Original source documents

{% for source in site.data.sources %}{% if source.kind == 'source' %}
- <a href="{{ source.url | relative_url }}" download>{{ source.label | escape }}</a>{% if source.text_url %} — <a href="{{ source.text_url | relative_url }}" download>extracted text</a>{% endif %}
{% endif %}{% endfor %}
