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

## Existing acquisition channels

Public-source snapshot, 22 September 2026. City Helpers markets in Halifax and Toronto; this project's priority is seniors booking for themselves in Toronto/GTA. These are visible channels and advertised processes; traffic, conversion, sales activity, and the full booking flow have not been verified. Proposed campaigns remain in Brainstorming.

| Inbound channel | Evidence and role | What remains unknown |
| --- | --- | --- |
| [LinkedIn](https://ca.linkedin.com/company/cityhelpers) | Regular household-help, business-labour, and worker-recruitment posts, usually linking to the website. | Customer reach, clicks, enquiries, and sales. |
| [Nextdoor](https://ca.nextdoor.com/pages/city-helpers-inc/) | Halifax business page with promotional posts, website/contact links, and a public service enquiry. | Toronto reach and whether enquiries become bookings. |
| [Facebook](https://www.facebook.com/profile.php?id=61563866975989) | Company page documented in the [introduction](business-context.md). | Posting activity, group participation, and campaign results. |
| [Website / organic search](https://www.cityhelpers.ca/) | Indexed service pages, testimonials, and customer calls to action. | Search rankings, organic traffic, and an active SEO programme. |

The website displays business partners, but their referral contribution is unverified. A project participant suggested finding customers through Facebook community groups; the CEO welcomed the idea. This does not establish an existing group-marketing programme.

**Outbound business sales:** a [LinkedIn recruitment post](https://ca.linkedin.com/company/cityhelpers) seeks commission-based sales partners to prospect, meet business owners, sell memberships, and maintain relationships, using company-generated opportunities and their own prospecting. This establishes recruitment for that model, not active representatives or sales results. Cold email, cold calling, direct messages, outreach volume, and follow-up processes remain unverified. No comparable outbound programme targeting seniors is established.

## Booking and return visits

The [published terms](https://www.cityhelpers.ca/terms-and-conditions) describe platform payment followed by a worker request. Payment and submission are separate milestones; neither proves a completed job. Email and messaging enquiry routes exist, but their handling and staff-assisted booking are unverified. Customers may leave, retry, or return; recovery processes, repeat-booking fees, reminders, referral incentives, and customer email campaigns remain unknown. Continue to [worker matching and delivery](worker-matching.md) for fulfilment, worker payment, ratings, and complaints.

**Pricing inconsistency:** the pricing-page snapshot recorded $9.99 dispatch offers for homeowners and businesses, while the [introduction](business-context.md) records earlier $99/month and $999/year business plans. Subscription language also appears elsewhere. Confirm the offer used at checkout and by sales representatives before treating either as settled. [Pricing page](https://www.cityhelpers.ca/pricing-plans/plans-pricing).

See [business objectives](business-objectives.md) for measurement gaps, [Q&A](open-questions.md) for pending questions, and the [CEO discussion transcript](https://devdogfish.github.io/cityhelpers/raw/source-material/ceo-discussion-transcript.txt) for the project discussion.
