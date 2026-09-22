---
title: "Customer journey"
updated: "2026-09-22"
---

Read top to bottom. Each layer has one purpose; the branches show alternate customer routes. **Blue = documented channel or published process. Amber = activity or handling not verified.** Arrows describe the journey, not measured conversion. This map ends when a paid dispatch has a submitted worker request; operations continue in [worker matching and delivery](worker-matching.html).

```mermaid
flowchart TB
    subgraph L1["01 · REACH"]
        Inbound["Organic inbound<br/>Search · LinkedIn · Nextdoor"]
        Other["Other entry routes<br/>Facebook page · direct visit · referral<br/>Activity / attribution unverified"]
        Outbound["Business outbound<br/>Sales partners recruited to prospect<br/>Actual outreach unverified"]
    end

    subgraph L2["02 · ENTRY"]
        Website["Website / service page"]
        Contact["Call · email · platform message<br/>Enquiry channels exist;<br/>booking assistance unverified"]
        Sales["B2B sales conversation<br/>Advertised model"]
    end

    subgraph L3["03 · CONSIDERATION"]
        Understand["Understand tasks, vetting, pricing,<br/>testimonials, and next steps"]
        Pause["Leave · postpone · choose an alternative<br/>Reasons and volumes unknown"]
    end

    subgraph L4["04 · OFFER"]
        Home["Senior / homeowner<br/>$9.99 dispatch<br/>Worker labour paid separately"]
        Business["Business customer<br/>Dispatch vs membership offer<br/>Conflicting local evidence"]
    end

    subgraph L5["05 · CONVERSION"]
        Fee["Pay City Helpers platform fee"]
        Request["Submit worker request"]
        Incomplete["Payment fails or request unfinished<br/>Recovery process unknown"]
    end

    subgraph L6["06 · HANDOFF"]
        Handoff(["Paid dispatch + submitted request<br/>Continue in worker matching diagram"])
    end

    Inbound --> Website
    Inbound --> Contact
    Other -.-> Website
    Other -.-> Contact
    Outbound -.-> Sales
    Website --> Understand
    Contact -.-> Understand
    Sales -.-> Understand
    Understand --> Home
    Understand --> Business
    Understand -.-> Pause
    Home --> Fee
    Business --> Fee
    Fee --> Request
    Fee -.-> Incomplete
    Request -.-> Incomplete
    Request --> Handoff

    %% Invisible layout constraints keep terminal branches inside their layer.
    Pause ~~~ Home
    Incomplete ~~~ Handoff

    classDef documented fill:#e8f2fa,stroke:#397497,color:#17394d;
    classDef unknown fill:#fff3d6,stroke:#b7872c,color:#49350d;
    classDef boundary fill:#e4f2e9,stroke:#45825d,color:#20412c;
    class Inbound,Website,Understand,Home,Fee,Request documented;
    class Other,Outbound,Contact,Sales,Pause,Business,Incomplete unknown;
    class Handoff boundary;
```

**Scope:** seniors booking household help are the current priority; the existing business route is retained for completeness. Nextdoor evidence is from Halifax, not proof of Toronto reach. Facebook page presence does not establish an active campaign. Proposed ads, events, partnerships, and incentives remain in `ideas-and-work/`; they are not shown as existing acquisition channels.

**Handoff:** payment and request submission are separate milestones. A paid fee alone does not prove a request was submitted or a job completed. Customers may retry or return through the entry layer; recovery automation and repeat-booking fees are unknown. Matching, worker payment, complaints, and job outcomes belong exclusively to the operations diagram.

**Sources:** [existing marketing funnel](existing-marketing-funnel.html), [business context](context.html), [open questions](open-questions.html), and the CEO transcript `source-material/ceo-discussion-transcript.txt`. These document the advertised process; the full booking flow has not been tested. The funnel's pricing update conflicts with older subscription figures in `business-context.md`, so the business offer remains unresolved.
