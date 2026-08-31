import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "enterprise-ai-security-threat-landscape-2026"

EN_ADD = """
<h2 id="how-do-you-red-team-an-ai-system-in-practice">How Do You Red-Team an AI System in Practice?</h2>
<p>Red-teaming an AI system is not the same discipline as red-teaming a network, because the vulnerability is semantic. There is no port to scan and no patch to apply; instead there is a set of instructions that can be persuaded, and the test is whether persuasion changes behaviour in a way that matters. The practical method is to enumerate the system's trust boundaries first, then attack each one with a specific technique, then record which controls held.</p>
<p>Four boundaries matter in most deployments. The input boundary covers everything a user or a retrieved document can place in front of the model: direct instruction override, indirect injection hidden in a web page or PDF the model retrieves, and encoded or multilingual payloads that bypass naive filters. The tool boundary covers what the agent can call: attempts to invoke a tool outside the granted scope, to escalate parameters, or to chain two benign tools into a harmful capability. The data boundary covers what the model can reach: attempts to widen retrieval scope, to infer the existence of records the user cannot read, or to extract training data through repeated probing. The output boundary covers what leaves the system: exfiltration through rendered content, through links, or through a downstream system the model can write to.</p>
<table class="article-table">
<thead><tr><th>Boundary</th><th>Representative technique</th><th>Control that should hold</th></tr></thead>
<tbody>
<tr><td>Input</td><td>Indirect injection in a retrieved document</td><td>Instruction/data separation; retrieved text treated as untrusted</td></tr>
<tr><td>Tool</td><td>Out-of-scope or escalated tool invocation</td><td>Parameter allowlists; per-call authorisation at the gateway</td></tr>
<tr><td>Data</td><td>Retrieval scope widening; membership inference</td><td>Inherited row and column security; retrieval scope pinned to the caller</td></tr>
<tr><td>Output</td><td>Exfiltration via rendered links or downstream writes</td><td>Egress filtering; output classification before delivery</td></tr>
<tr><td>Supply chain</td><td>Poisoned fine-tuning set or compromised model artefact</td><td>Provenance verification; behavioural diff against a known baseline</td></tr>
</tbody>
</table>
<p>Two operating rules make red-teaming useful rather than theatrical. Run it continuously, not annually: every change to prompts, tools, retrieval corpora, or model versions can reintroduce a vulnerability that was previously closed, and an annual test tells you nothing about the drift in between. And record the result as a control gap rather than an individual finding — "indirect injection succeeded because retrieved documents were not marked untrusted" leads to a fix, whereas "the model was tricked on Tuesday" leads to a shrug.</p>
<h2 id="what-does-an-ai-specific-incident-response-playbook-contain">What Does an AI-Specific Incident Response Playbook Contain?</h2>
<p>Most incident response plans assume an attacker who is inside a system and moving laterally. AI incidents break that assumption in two ways: the attacker may never be inside at all, and the compromised component may be a behaviour rather than a host. A playbook that only covers containment of infrastructure will leave responders without a procedure for the most likely event — a model that is behaving badly while every server is healthy.</p>
<p>The essential addition is a behaviour kill switch. Responders need a documented, tested way to revoke a specific capability — disable a tool, withdraw a prompt, revert a model version, or narrow a retrieval scope — in minutes, without a full redeployment. That requires every one of those elements to be versioned and independently switchable, which is an architecture decision made long before the incident. Alongside it, the playbook needs a decision tree for scope: was this a single malicious request, a poisoned context source, or a systemic permission error? Each branch has a different remediation and a different notification obligation.</p>
<table class="article-table">
<thead><tr><th>Playbook element</th><th>Content</th><th>Why traditional IR misses it</th></tr></thead>
<tbody>
<tr><td>Capability kill switch</td><td>Documented, tested steps to revoke a tool, prompt, or model version</td><td>Traditional IR contains hosts, not behaviours</td></tr>
<tr><td>Prompt and context forensics</td><td>Retained inputs, retrieved documents, and tool calls for the affected window</td><td>Logs usually capture the response, not the context</td></tr>
<tr><td>Scope decision tree</td><td>Distinguishes malicious input, poisoned source, and permission error</td><td>No equivalent in host-based triage</td></tr>
<tr><td>Affected-data assessment</td><td>Which records were observable during the incident</td><td>Requires data-lineage knowledge, not network knowledge</td></tr>
<tr><td>Notification template</td><td>Pre-drafted language for customers and regulators on AI incidents</td><td>Existing templates do not cover model behaviour</td></tr>
<tr><td>Restoration criteria</td><td>Conditions that must be met before the capability is re-enabled</td><td>Re-enabling is often treated as a rollback, not a decision</td></tr>
</tbody>
</table>
<p>Finally, the playbook should be exercised with a tabletop that uses a realistic AI scenario — a data leak caused by indirect prompt injection through a supplier document, for example — and should include the communications function from the start. In AI incidents the hardest part is rarely the technical containment; it is explaining, within hours, what the system did, what data it could see, and what has been done about it. Organisations that rehearse that explanation handle the event far better than those improvising it under deadline.</p>
"""

H2FIX = {
    "EN": [
        ("the-technology-landscape-in-2026", "What Does the Technology Landscape Look Like in 2026?"),
        ("technical-architecture-and-implementation", "What Technical Architecture and Implementation Are Required?"),
        ("integration-with-enterprise-systems", "How Do You Integrate Security with Enterprise Systems?"),
        ("performance-optimization-and-cost-management", "How Do You Optimize Security Performance and Manage Cost?"),
        ("frequently-asked-questions", "What Questions Come Up Most Often?"),
    ],
    "CN": [
        ("technical-architecture-and-implementation", "What Technical Architecture and Implementation Are Required?"),
        ("integration-with-enterprise-systems", "How Do You Integrate with Enterprise Systems?"),
        ("performance-optimization-and-cost-management", "How Do You Optimize Performance and Manage Cost?"),
        ("常见问题", "常见问题有哪些？"),
        ("规模化推广的关键成功因素", "规模化推广的关键成功因素有哪些？"),
        ("技术基础设施与实施考量", "技术基础设施与实施考量是什么？"),
        ("中国市场特有的实施优势", "中国市场特有的实施优势有哪些？"),
    ],
    "TW": [
        ("2026-年的技術景觀", "2026 年的技術景觀是什麼？"),
        ("技術架構與實施", "技術架構與實施是什麼？"),
        ("與企業系統整合", "如何與企業系統整合？"),
        ("效能最佳化與成本管理", "效能最佳化與成本管理如何進行？"),
    ],
}

process(SLUG, H2FIX, adds={"EN": EN_ADD}, tag=SLUG[:24])
