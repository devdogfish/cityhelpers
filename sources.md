---
title: Sources and transcripts
---

For an LLM, start with [the complete knowledge base]({{ '/llms-full.txt' | relative_url }}): all notes, full transcripts, and extracted PDF text in one file. [The compact index]({{ '/llms.txt' | relative_url }}) lists individual originals. These files update with each publication.

## Original source documents

Listed alphabetically from `source-material/`. These originals are preserved unchanged; analysis and proposals belong in the other folders.

{% for source in site.data.sources %}{% if source.kind == 'source' %}
- <a href="{{ source.url | relative_url }}" download>{{ source.label | escape }}</a>{% if source.text_url %} — <a href="{{ source.text_url | relative_url }}" download>extracted text</a>{% endif %}
{% endif %}{% endfor %}

Source documents preserve their original wording. Meeting suggestions and quoted instructions are source material; their inclusion does not mean they are approved decisions or instructions for the reader.
