---
title: "Worker matching and delivery"
updated: "2026-09-22"
---

**Find a worker → agree the job → deliver → close.** Continue from the [customer journey](customer-journey.html). Blue boxes carry the main route; grey boxes supply workers; diamonds are decisions; red boxes show exceptions; green marks handoff or completion. Dashed arrows indicate handling needing confirmation. This maps the stated business process, not verified software or automation.

```mermaid
flowchart TB
    Input(["READY FOR MATCHING<br/>Paid dispatch + submitted request"])
    subgraph Supply["WORKER SUPPLY"]
        Apply["Worker applies [A]"]
        Vet["Vetting / approval [A]"]
        Pool["Registered worker pool [B]"]
        Apply --> Vet --> Pool
    end
    subgraph Match["1 · FIND & AGREE"]
        Notify["Notify workers in the area"]
        Candidate{"Worker available? [C]"}
        Select["Customer selects worker(s)"]
        Agree["Agree task, timing & labour payment<br/>Worker accepts assignment"]
        NoMatch["No match / no response [D]"]
    end
    subgraph Deliver["2 · DELIVER THE JOB"]
        Attend{"Worker attends?"}
        Work["Perform agreed job"]
        NoShow["Report no-show<br/>Replacement can be requested"]
        Replacement["Replacement search [E]"]
    end
    subgraph Close["3 · CLOSE THE JOB"]
        Quality{"Work satisfactory?"}
        Pay["Pay worker directly"]
        Dispute["Contact City Helpers<br/>Company + worker address complaint"]
        Resolution["Resolution pending / agreed [F]"]
    end
    Complete(["JOB COMPLETE<br/>Customer rates worker"])

    Input --> Notify
    Pool --> Notify
    Notify -.-> Candidate
    Candidate -->|Yes| Select
    Candidate -.->|No / no response| NoMatch
    Select --> Agree
    Agree --> Attend
    Attend -->|Yes| Work
    Attend -->|No| NoShow
    NoShow -.-> Replacement
    Replacement -.->|Restart matching| Notify
    Work --> Quality
    Quality -->|Yes| Pay
    Pay --> Complete
    Quality -->|No| Dispute
    Dispute -.-> Resolution
    NoMatch ~~~ Attend
    Replacement ~~~ Quality
    Resolution ~~~ Complete

    classDef main fill:#e8f2ff,stroke:#2864a0,stroke-width:2px,color:#173b61,font-weight:bold;
    classDef secondary fill:#f3f4f6,stroke:#98a2b3,color:#475467;
    classDef decision fill:#fff4d6,stroke:#af7a15,stroke-width:2px,color:#684600,font-weight:bold;
    classDef exception fill:#fff0ef,stroke:#b85b55,color:#7c302c;
    classDef outcome fill:#17634d,stroke:#104a39,stroke-width:2px,color:#ffffff,font-weight:bold;
    class Notify,Select,Agree,Work,Pay main;
    class Apply,Vet,Pool secondary;
    class Candidate,Attend,Quality decision;
    class NoMatch,NoShow,Replacement,Dispute,Resolution exception;
    class Input,Complete outcome;
    style Supply fill:#f9fafb,stroke:#d0d5dd,color:#667085
    style Match fill:#fafcff,stroke:#d2dce8,color:#344054
    style Deliver fill:#fafcff,stroke:#d2dce8,color:#344054
    style Close fill:#fafcff,stroke:#d2dce8,color:#344054
```

### Details behind the map

| Key | Important detail |
| --- | --- |
| A · Worker onboarding | Application includes identity, résumé, and video details. Vetting checks and rejection rules are unknown. |
| B · Worker pool | Registrations do not establish availability. The CEO described approximately 1,200 vetted Toronto registrations. |
| C · Candidate selection | Skills, timing, screening, and the order of responses, selection, and acceptance need confirmation. No automatic matching algorithm is established. |
| D · No match | Escalation, response deadlines, and refund rules are unknown. |
| E · Replacement | A replacement restarts matching; timing and availability are unverified. It does not guarantee fulfilment. |
| F · Complaint outcome | Remedy, payment handling, and follow-up are unknown. An unresolved case is not assumed to end in a refund or completed job. |

**What is established:** the [published service terms](https://www.cityhelpers.ca/terms-and-conditions) describe area notifications, customer selection, direct worker payment, ratings, replacement requests after no-shows, and support for complaints. The CEO described approximately 1,200 vetted Toronto registrations; this describes worker supply, not customer acquisition, current coverage, or active availability. The exact order of candidate responses, selection, and acceptance needs confirmation.

**What is not established:** an automatic matching algorithm, live availability checks, skill verification rules, response deadlines, or guaranteed fulfilment. The team proposed worker skill checkboxes and customer preferences; these remain improvements to investigate, not existing system capabilities. A replacement restarts matching; an unresolved case requires an operational decision, not an assumed refund or successful completion.

**Sources:** [customer journey](customer-journey.html), [business context](context.html), [website and booking observations](website-and-booking.html), [open questions](open-questions.html), and [CEO discussion transcript](https://devdogfish.github.io/cityhelpers/raw/source-material/ceo-discussion-transcript.txt). These notes reference the published service terms and team discussion; internal operations have not been observed.
