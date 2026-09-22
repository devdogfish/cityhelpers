# Worker matching and delivery

Operational companion to [client acquisition](customer-journey.md). The shared boundary is **paid dispatch + submitted request**; this map contains no marketing channels, sales conversations, or checkout steps. Read top to bottom: inputs → matching → agreement → delivery → closure. **Blue = stated process. Amber = operational detail needing confirmation.** This is a business-process map, not evidence of implemented software or automated matching.

```mermaid
flowchart TB
    subgraph L1["01 · INPUTS"]
        Input(["Paid dispatch + submitted request<br/>From acquisition diagram"])
        Apply["Worker applies<br/>Identity · resume · video details"]
        Vet["Vetting / approval<br/>Checks and rejection rules unknown"]
        Pool["Registered worker pool<br/>Registration does not prove availability"]
        Apply --> Vet --> Pool
    end

    subgraph L2["02 · MATCHING"]
        Notify["Notify registered workers in the area"]
        Candidate["Identify suitable, available candidates<br/>Skills, timing, and screening process unknown"]
        NoMatch["No suitable worker / no response<br/>Escalation, timing, and refund rules unknown"]
    end

    subgraph L3["03 · AGREEMENT"]
        Select["Customer selects worker(s)"]
        Agree["Agree task, timing, and labour payment<br/>Worker accepts assignment"]
    end

    subgraph L4["04 · DELIVERY"]
        Attend{"Worker attends?"}
        Work["Worker performs agreed job"]
        NoShow["Customer reports no-show<br/>Replacement can be requested"]
        Replacement["Replacement search<br/>Returns to matching;<br/>timing and availability unverified"]
    end

    subgraph L5["05 · CLOSURE"]
        Quality{"Work satisfactory?"}
        Pay["Customer pays worker directly"]
        Rate["Customer rates worker<br/>Job complete"]
        Dispute["Customer contacts City Helpers<br/>Company and worker address complaint"]
        Resolution["Resolution pending / agreed<br/>Remedy, payment handling,<br/>and follow-up outcome unknown"]
    end

    Input --> Notify
    Pool --> Notify
    Notify -.-> Candidate
    Candidate --> Select
    Candidate -.-> NoMatch
    Select --> Agree
    Agree --> Attend
    Attend -->|"Yes"| Work
    Attend -->|"No"| NoShow
    NoShow -.-> Replacement
    Work --> Quality
    Quality -->|"Yes"| Pay
    Pay --> Rate
    Quality -->|"No"| Dispute
    Dispute -.-> Resolution

    %% Invisible layout constraints preserve chronological layer boundaries.
    NoMatch ~~~ Select
    Replacement ~~~ Quality

    classDef documented fill:#e8f2fa,stroke:#397497,color:#17394d;
    classDef unknown fill:#fff3d6,stroke:#b7872c,color:#49350d;
    classDef boundary fill:#e4f2e9,stroke:#45825d,color:#20412c;
    class Apply,Pool,Notify,Select,Agree,Attend,Work,NoShow,Quality,Pay,Rate,Dispute documented;
    class Vet,Candidate,NoMatch,Replacement,Resolution unknown;
    class Input boundary;
```

**What is established:** the local funnel records area notifications, customer selection, direct worker payment, ratings, replacement requests after no-shows, and support for complaints. The CEO described approximately 1,200 vetted Toronto registrations; this does not establish current coverage or available workers. The exact order of candidate responses, selection, and acceptance needs confirmation.

**What is not established:** an automatic matching algorithm, live availability checks, skill verification rules, response deadlines, or guaranteed fulfilment. The team proposed worker skill checkboxes and customer preferences; these remain improvements to investigate, not existing system capabilities. A replacement restarts matching; an unresolved case requires an operational decision, not an assumed refund or successful completion.

**Sources:** [existing marketing funnel](existing-marketing-funnel.md), [business context](business-context.md), [website and booking observations](../ideas-and-work/website-and-booking.md), [open questions](../looking-ahead/open-questions.md), and `ceo-discussion-transcript.txt`. These local notes reference the published service terms and team discussion; internal operations have not been observed.
