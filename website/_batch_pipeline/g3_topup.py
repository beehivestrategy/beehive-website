#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixlib as F

TOP = {
"mcp-tool-use-advanced-patterns": """
<h2 id="how-does-mcp-compare-with-function-calling-and-plain-apis">How Does MCP Compare With Function Calling and Plain APIs?</h2>
<p>These three are frequently confused, and the confusion produces bad architecture decisions. Function calling is a model capability: the model emits a structured request describing a call it wants to make. It says nothing about how the call is executed, who is authorised to make it, or how the result is logged. A plain API is an execution endpoint with its own contract, auth model, and operational profile. MCP is the layer in between: a standard way to describe, discover, and invoke capabilities so that any compatible client can use any compatible server without bespoke integration code.</p>
<p>Practically, you use all three together. Function calling is how the model expresses intent; MCP is how that intent is routed to a capability the model was told about; the API is the system that does the work. The reason MCP matters is not that it replaces either — it is that it standardises the middle. Every enterprise that skipped that layer ended up with a bespoke registry, a bespoke auth model, and a bespoke audit trail for every agent-to-system pair, and those bespoke parts are exactly where security reviews fail.</p>
<p>The test for whether you need MCP is simple. Count your agents and count your systems. If the product of the two is larger than the number of integrations you are willing to maintain individually, you need a common protocol. For most enterprises in 2026, that threshold was passed some time ago.</p>
""",
"measuring-ai-maturity-enterprise-assessment-model": """
<h2 id="what-should-the-assessment-output-actually-contain">What Should the Assessment Output Actually Contain?</h2>
<p>A maturity assessment that produces a report produces nothing. The deliverable should be short enough to be argued with and specific enough to be funded. Four artefacts, and nothing else.</p>
<p>First, a one-page profile: four dimension scores, each with a one-sentence justification naming the evidence. Second, a named binding constraint with a short explanation of why it blocks the others — this is the single most important sentence in the document. Third, one funded initiative targeted at that constraint, with a target level, a named executive owner, a date, and the metric that will prove the move happened. Fourth, a re-assessment date.</p>
<p>Everything else — the lengthy dimension narratives, the workshop notes, the benchmark comparisons — belongs in an appendix that most readers will never open. Teams that deliver a forty-page assessment get a forty-page discussion; teams that deliver one page and one funded initiative get a decision. If your assessment cannot be summarised on a single page, it has not yet identified the constraint.</p>
""",
}

for slug, block in TOP.items():
    s = F.load(slug, "EN")
    b = F.get_body(s)
    if block.strip()[:80] in b:
        print("skip", slug); continue
    anchor = '<section class="faq-section"'
    b = b.replace(anchor, block.strip() + "\n\n            " + anchor, 1)
    F.save(slug, "EN", F.set_body(s, b))
    s = F.load(slug, "EN")
    s = F.sync_toc(s)
    F.save(slug, "EN", s)
    print(slug, F.stats(s))
