---
title: City Helpers knowledge base
---
Our shared reference for understanding City Helpers and developing practical ways to help the business in Toronto/GTA.

{% for group in site.data.navigation %}
## {{ group.label }}

{% for note in group.notes %}
- [{{ note.label }}]({{ note.url | relative_url }})
{% endfor %}
{% endfor %}

Evidence, assumptions, proposals, and results are distinguished within each topic. Navigation follows the local note folders in alphabetical order.
