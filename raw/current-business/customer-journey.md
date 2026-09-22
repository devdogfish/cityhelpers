# Customer journey

**Discover → understand → book → hand off.** Follow the blue boxes for the main household route. Grey boxes show alternative routes; diamonds are choices; red boxes are incomplete outcomes; green marks the handoff. Dashed arrows indicate unverified activity or handling. Choices represent customer behaviour, not confirmed website screens.

```mermaid
flowchart TB
    subgraph Reach["1 · DISCOVERY"]
        Inbound["Organic discovery [A]<br/>Search · LinkedIn · Nextdoor"]
        Other["Other routes [B]<br/>Facebook · direct visit · referral"]
        Outbound["Business outreach [B]<br/>Sales partner → sales conversation"]
    end
    subgraph Evaluate["2 · EVALUATION"]
        Website["Visit website"]
        Contact["Call · email · message [C]"]
        Understand["Check tasks, trust & cost [D]"]
        Ready{"Continue?"}
        Pause["Leave or postpone [E]"]
    end
    subgraph Book["3 · BOOK HELP"]
        Type{"Customer type?"}
        Home["Senior / homeowner<br/>$9.99 dispatch + separate labour"]
        Business["Business customer [F]<br/>Offer needs confirmation"]
        Fee["Pay platform fee"]
        Request["Submit worker request"]
        Incomplete["Payment failed / request unfinished [E]"]
    end
    Handoff(["READY FOR MATCHING<br/>Paid dispatch + submitted request"])

    Inbound --> Website
    Inbound --> Contact
    Other -.-> Website
    Other -.-> Contact
    Outbound -.-> Understand
    Website --> Understand
    Contact -.-> Understand
    Understand --> Ready
    Ready -->|Yes| Type
    Ready -->|No / later| Pause
    Type -->|Household| Home
    Type -->|Business| Business
    Home --> Fee
    Business --> Fee
    Fee --> Request
    Fee -.-> Incomplete
    Request -.-> Incomplete
    Request --> Handoff
    Pause ~~~ Type
    Incomplete ~~~ Handoff

    classDef main fill:#e8f2ff,stroke:#2864a0,stroke-width:2px,color:#173b61,font-weight:bold;
    classDef secondary fill:#f3f4f6,stroke:#98a2b3,color:#475467;
    classDef decision fill:#fff4d6,stroke:#af7a15,stroke-width:2px,color:#684600,font-weight:bold;
    classDef exception fill:#fff0ef,stroke:#b85b55,color:#7c302c;
    classDef outcome fill:#17634d,stroke:#104a39,stroke-width:2px,color:#ffffff,font-weight:bold;
    class Inbound,Website,Understand,Home,Fee,Request main;
    class Other,Outbound,Contact,Business secondary;
    class Ready,Type decision;
    class Pause,Incomplete exception;
    class Handoff outcome;
    style Reach fill:#fafcff,stroke:#d2dce8,color:#344054
    style Evaluate fill:#fafcff,stroke:#d2dce8,color:#344054
    style Book fill:#fafcff,stroke:#d2dce8,color:#344054
```

### Details behind the map

| Key | Important detail |
| --- | --- |
| A · Organic discovery | Channels are documented; Nextdoor evidence is from Halifax, not proof of Toronto reach. |
| B · Other routes | Facebook presence does not prove active campaigns. Referral/direct attribution and actual sales-partner outreach are unverified. The B2B sales conversation is an advertised model. |
| C · Contact | Enquiry channels exist; staff-assisted booking is unverified. |
| D · Evaluation | Customers review task suitability, worker vetting, pricing, testimonials, and next steps. |
| E · Incomplete outcomes | Exit reasons, volumes, and recovery processes are unknown. Customers may retry or return through an entry route. |
| F · Business offer | Dispatch and membership descriptions conflict in local evidence. |

**Scope:** seniors booking household help are the current priority; the existing business route is retained for completeness. Nextdoor evidence is from Halifax, not proof of Toronto reach. Facebook page presence does not establish an active campaign. Proposed ads, events, partnerships, and incentives remain in the Brainstorming section; they are not shown as existing acquisition channels.

**Handoff:** payment and request submission are separate milestones. A paid fee alone does not prove a request was submitted or a job completed. Customers may retry or return through the entry layer; recovery automation and repeat-booking fees are unknown. Matching, worker payment, complaints, and job outcomes belong exclusively to the operations diagram.

**Sources:** [existing marketing funnel](existing-marketing-funnel.md), [business context](business-context.md), [open questions](../looking-ahead/open-questions.md), and the [CEO discussion transcript](https://devdogfish.github.io/cityhelpers/raw/source-material/ceo-discussion-transcript.txt). These document the advertised process; the full booking flow has not been tested. The funnel's pricing update conflicts with older subscription figures in [business context](https://devdogfish.github.io/cityhelpers/context.html), so the business offer remains unresolved.
