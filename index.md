---
title: City Helpers knowledge base
---
Our shared reference for understanding City Helpers and developing practical ways to help the business in Toronto/GTA.

**For LLMs:** [Read all context in one text file]({{ '/llms-full.txt' | relative_url }}), including original transcripts and PDF text. [Browse sources and downloads]({{ '/sources.html' | relative_url }}) or use the [compact index]({{ '/llms.txt' | relative_url }}).

{% for group in site.data.navigation %}
## {{ group.label }}

{% for note in group.notes %}
- [{{ note.label }}]({{ note.url | relative_url }})
{% endfor %}
{% endfor %}

Evidence, assumptions, proposals, and results are distinguished within each topic. Navigation follows the local note folders in alphabetical order.
