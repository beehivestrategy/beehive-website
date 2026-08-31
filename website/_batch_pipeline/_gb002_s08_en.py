# -*- coding: utf-8 -*-
"""Expand the EN body of digital-transformation-change-management."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb002_h2 import rename_h2, add_tail_section, replace_faq_list

P = 'blog/articles/digital-transformation-change-management.html'

for old, new in [
    ("Understanding the Current Landscape", "Why Do Digital Transformations Fail on the People Side?"),
    ("Key Principles and Strategic Framework", "What Principles Should a Change Programme Follow?"),
    ("Implementation Approach and Best Practices", "How Should You Run a Change Programme Alongside the Transformation?"),
    ("Measuring Success and Demonstrating ROI", "How Do You Measure Change Management and Prove Its ROI?"),
    ("Common Pitfalls and How to Avoid Them", "What Pitfalls Derail Change Management?"),
    ("Key Takeaways", "What Are the Key Takeaways for Transformation Leaders?"),
    ("Conclusion", "Where Should Transformation Leaders Start?"),
]:
    print(rename_h2(P, old, new))

S1 = """<p>A change-impact assessment is the foundational document of a change programme, and it takes about three weeks for a mid-sized organisation. Its purpose is to replace a generic communication plan with a specific map of whose work changes, how, and how much.</p>
<p>The output has four columns per employee segment: <strong>the population</strong> (role, function, location, and headcount); <strong>the delta</strong> (the specific tasks that stop, start, or change, described in the vocabulary of the job rather than of the system); <strong>the exposure</strong> (how much of the working week is affected, and whether the change removes work, moves it, or adds it); and <strong>the support requirement</strong> (training format, timing, and who delivers it). Adding a fourth-and-a-half column — the metrics that currently govern that segment's performance — is what surfaces the incentive conflicts that quietly kill adoption.</p>
<p>Two practices make the assessment useful rather than documentary. First, build it <em>with</em> frontline representatives rather than for them; they will identify task-level changes the project team has never seen, and their involvement converts potential resistors into contributors. Second, rank segments by change exposure and concentrate spending on the top two or three. Uniform training across every affected population is the most common way change budgets get diluted to the point of ineffectiveness — the segments carrying 80% of the behaviour change usually need a disproportionate share of the investment.</p>"""

S2 = """<p>Middle management is the most consequential and most neglected group in a transformation. They are asked to absorb the change themselves, lead their teams through it, and continue delivering operational results — usually with less context, less training, and less incentive alignment than either the executive sponsors above them or the frontline below.</p>
<p>Three interventions address the gap. <strong>Give them context before asking for advocacy.</strong> Managers cannot answer questions they have not been given answers to; briefing them ahead of the all-hands, with the reasoning and the known trade-offs, is the difference between an advocate and a conduit. <strong>Reduce their delivery load during the transition.</strong> A team expected to hit the same targets while learning a new system will revert to the old system, and managers will permit it. Adjusting targets for the transition period is an unglamorous decision that materially improves outcomes. <strong>Give them something concrete to do.</strong> Managers need a defined role — running a weekly adoption check-in, reviewing team-level usage, escalating design friction — rather than a general expectation of support.</p>
<p>The measurement implication follows directly. Segment-level adoption data should be visible to the manager whose segment it is, with enough latency that they can act on it in the same week. Where managers can see their own team's adoption compared with peers, and have the authority to address it, adoption curves move materially faster than where the data goes only to the programme office.</p>"""

S3 = """<p>Training is where most change budgets are spent and most change value is lost. The dominant format — a one-day workshop before go-live, using sample data — fails for reasons that are well understood: people forget most of it before they need it, the examples do not match their work, and the training ends before the difficult questions arise.</p>
<p>The design that works has four characteristics. <strong>Train in the flow of work</strong>, on real workflows with real data, as close as possible to the moment of need. <strong>Train in short, repeated sessions</strong> spread across the weeks after go-live rather than in one block before it, because retention and relevance both improve when training follows actual use. <strong>Differentiate by segment</strong>, since the segment that uses a system for twenty minutes a week needs a fundamentally different intervention from the one that uses it all day. <strong>Measure competence, not attendance</strong> — completion rates are the vanity metric; task completion time, error rates, and support tickets per user are the real ones.</p>
<p>Support capacity matters as much as training design. The weeks immediately after go-live generate the highest volume of questions and the strongest signal about where the design is failing, and a visible, fast support channel converts that moment from frustration into adoption. Programmes that staff support generously for the first six to eight weeks and taper it as competence rises consistently outperform those that staff it evenly across the year.</p>"""

for sid, title, body in [
    ("how-do-you-run-a-change-impact-assessment", "How Do You Run a Change-Impact Assessment?", S1),
    ("what-role-should-middle-managers-play-in-a-transformation", "What Role Should Middle Managers Play in a Transformation?", S2),
    ("how-should-training-be-designed-for-real-adoption", "How Should Training Be Designed for Real Adoption?", S3),
]:
    print(add_tail_section(P, sid, title, body))

FAQ = [
    ("Why do 70% of digital transformations fail if the technology works?",
     "Because adoption, not capability, is the binding constraint. McKinsey's research consistently finds around 70% of transformations miss their goals, and the causes are behavioural: employees keep doing what they are measured on, the legacy system stays available, and the change programme starts too late to influence how the new workflow is designed. The technology determines what is possible; the change programme determines whether anyone does it."),
    ("How much of the budget should go to change management?",
     "Programmes allocating under a tenth of their budget to adoption activity systematically underperform. The strongest programmes treat adoption as a deliverable with owners, budgets, and deadlines equal to any technical workstream, and they weight spending toward the employee segments carrying the most behaviour change rather than spreading it evenly. The cost of under-investing is not a slightly slower rollout; it is a system that runs in parallel with the old process indefinitely."),
    ("What is the most reliable early indicator that a transformation is working?",
     "Behavioural adoption in the weeks after go-live, measured by task completion in the new system rather than by logins. Specifically: the share of target work performed in the new system versus legacy, time-to-competency for each segment, and support tickets per user. Logins and course completions are vanity metrics that rise even when people open the new tool only to copy its output back into the old process."),
    ("Should we keep the legacy system running as a fallback?",
     "Only with a firm, communicated retirement date. Coexistence guarantees regression, because the path of least resistance under pressure is always the familiar one. The workable design is a dated decommission, communicated early, with sufficient support capacity in the weeks after go-live and a documented exception process for the specific functions that genuinely cannot migrate on schedule."),
    ("How do we handle employees who actively resist the change?",
     "Treat resistance as diagnostic rather than as an obstacle. Active resistors are usually the people who understand the current process best, and their objections tend to be specific and often correct — a workflow that adds steps, a report the new system cannot produce, a control that was quietly lost. Route the objection to someone who can change the design where it is valid, and be explicit where it is not. Resistance that is answered with argument rather than substance hardens quickly."),
    ("Does choosing different technology reduce the change burden?",
     "Materially. Tools that fit inside existing habits inherit adoption instead of competing for it — a conversational analytics layer that answers questions in the chat tools employees already use, for example, requires far less behaviour change than a separate BI application that only analysts open. This is a strategic lever rather than a convenience: the change effort is finite, and spending it on infrastructure adoption leaves less for the workflow change that actually creates value."),
]
print(replace_faq_list(P, FAQ, "en"))
