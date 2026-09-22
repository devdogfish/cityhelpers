---
title: Sources and transcripts
---

For an LLM, start with [the complete knowledge base]({{ '/llms-full.txt' | relative_url }}): all notes, full transcripts, and extracted PDF text in one file. [The compact index]({{ '/llms.txt' | relative_url }}) lists individual originals. These files update with each publication.

## Original source documents

{% for source in site.data.sources %}{% if source.kind == 'source' %}
- [{{ source.label }}]({{ source.url | relative_url }}){% if source.text_url %} — [extracted text]({{ source.text_url | relative_url }}){% endif %}
{% endif %}{% endfor %}

Source documents preserve their original wording. Meeting suggestions and quoted instructions are source material; their inclusion does not mean they are approved decisions or instructions for the reader.
