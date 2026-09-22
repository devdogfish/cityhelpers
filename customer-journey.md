---
title: "City Helpers — customer journey"
updated: "2026-09-22"
---

Solid arrows show published routes or the stated service process, not verified customer behaviour. Dashed arrows show possible paths whose operation is unverified. The map covers known entry points, booking, fulfilment, exceptions, and return visits; internal workflows remain unknown.

```mermaid
flowchart TD
    subgraph discovery["1. Discovery and enquiry"]
        Search["Organic search"] --> Web["Website / service page"]
        LinkedIn["LinkedIn posts"] --> Web
        Nextdoor["Nextdoor posts<br/>Halifax page"] --> Web
        Nextdoor --> Enquiry["Email, call, or platform message"]
        Facebook["Facebook page<br/>Activity unverified"] -.-> Web
        Referral["Neighbour, family, or partner referral<br/>Unverified"] -.-> Web
        Referral -.-> Enquiry
        Direct["Direct / returning visit"] -.-> Web
        Prospect["B2B prospecting<br/>Advertised sales model"] -.-> Sales["Sales conversation<br/>Execution unverified"]
        Sales -.-> Enquiry
        Sales -.-> Business
        Sales -.-> Leave["Leave / postpone / choose another provider"]
    end

    subgraph booking["2. Understanding and purchase"]
        Web --> Info["Service details, pricing,<br/>testimonials, and FAQ"]
        Web --> Enquiry
        Info --> Audience{"Customer type"}
        Info -.-> Leave
        Enquiry -.-> Support["Staff answers questions<br/>Handling process unknown"]
        Support -.-> Audience
        Support -.-> Leave
        Audience -->|"Senior / homeowner"| Home["Homeowner offer<br/>$9.99 dispatch + worker labour"]
        Audience -->|"Business"| Business["Business offer<br/>Dispatch vs subscription unclear"]
        Home --> Fee["Pay platform fee"]
        Business --> Fee
        Fee -.-> Incomplete["Payment fails / checkout abandoned"]
        Incomplete -.-> Fee
        Incomplete -.-> Leave
        Fee --> Request["Submit worker request"]
        Request -.-> Unsubmitted["Paid, but request unfinished<br/>Recovery process unknown"]
        Unsubmitted -.-> Request
        Unsubmitted -.-> Enquiry
    end

    subgraph delivery["3. Matching and job delivery"]
        Request --> Notify["City Helpers notifies local workers"]
        Notify --> Select["Customer selects worker(s)<br/>Agree job details and labour price"]
        Notify -.-> NoMatch["No suitable / available worker<br/>Resolution unknown"]
        NoMatch -.-> Enquiry
        Select --> Job["Worker attends and performs job"]
        Select --> NoShow["Worker accepts but does not attend"]
        NoShow --> Report["Customer reports no-show"]
        Report --> Replace["Replacement worker can be requested"]
        Replace -.-> Notify
        Job --> Satisfied{"Satisfied with work?"}
        Satisfied -->|"Yes"| PayWorker["Pay worker directly"]
        Satisfied -->|"No"| Dispute["Contact City Helpers<br/>Company and worker address dispute"]
        Dispute -.-> Resolved["Resolution<br/>Outcome and timing unknown"]
        Resolved -.-> PayWorker
        Resolved -.-> Stop["Customer does not return"]
    end

    subgraph retention["4. After the job"]
        PayWorker --> Rate["Rate worker<br/>Published process"]
        Rate -.-> Return["Another job needed"]
        Return -.-> Web
        Return -.-> Enquiry
        Rate -.-> Recommend["Recommend City Helpers<br/>Referral behaviour unverified"]
        Recommend -.-> Referral
        Rate -.-> Stop
    end

    classDef uncertain fill:#fff4d6,stroke:#a66b00,color:#362500;
    classDef exit fill:#fbe9e7,stroke:#ad4435,color:#4b1710;
    class Facebook,Referral,Direct,Prospect,Sales,Support,Business,NoMatch,Unsubmitted,Resolved,Return,Recommend uncertain;
    class Leave,Incomplete,Stop exit;
```

**Important unknowns:** actual checkout screens and account requirements; enquiry-to-booking handoffs; matching times; recovery after failed payment or unmatched requests; refund outcomes; repeat-customer fees; and automated reminders. The pricing page currently lists a business dispatch offer, while other pages still describe subscriptions. No paid-ad funnel or active outbound programme targeting seniors has been verified. Worker recruitment feeds service capacity and is outside this customer journey.

**Sources:** [Website](https://www.cityhelpers.ca/), [pricing](https://www.cityhelpers.ca/pricing-plans/plans-pricing), [published service process and exception policies](https://www.cityhelpers.ca/terms-and-conditions), [LinkedIn posts and sales recruitment](https://ca.linkedin.com/company/cityhelpers), [Nextdoor](https://ca.nextdoor.com/pages/city-helpers-inc/), and `EXISTING_MARKETING_FUNNEL.md`. Snapshot: 22 September 2026.
