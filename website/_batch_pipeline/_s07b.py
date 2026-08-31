import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "what-is-ai-agent-autonomous-system"

EN_ADD2 = """
<h2 id="what-does-an-ai-agent-cost-to-run">What Does an AI Agent Cost to Run?</h2>
<p>Agent economics are frequently modelled wrong because teams budget for the model and forget the loop. A single question answered once costs one inference; an agent completing a task may reason, call three tools, retry a failed step, summarise, and verify — a dozen or more inferences for the same user request. Multiply that by the fraction of tasks that need retries and the unit cost of an agent task is typically five to twenty times the cost of the chat answer it replaced. That is still a good trade when the task is valuable, but only if you measured it before you committed to a price.</p>
<p>Three levers control the number. The first is task scoping: narrow goals complete in fewer steps, and a well-specified task with a defined success criterion routinely costs half of an open-ended one. The second is model routing — use a small, cheap model for classification, extraction, and routing steps, and reserve the expensive model for genuine reasoning and synthesis. The third is caching and determinism: any step whose output cannot change should be computed once, and any tool response that is reused across tasks should be served from cache rather than re-fetched.</p>
<table class="article-table">
<thead><tr><th>Cost component</th><th>What drives it</th><th>Practical control</th></tr></thead>
<tbody>
<tr><td>Model inference</td><td>Reasoning steps, retries, and context length</td><td>Model routing by step difficulty; tighter task scoping</td></tr>
<tr><td>Tool calls</td><td>Number and latency of external systems touched</td><td>Cache stable responses; batch where the API allows</td></tr>
<tr><td>Context</td><td>Growing conversation and memory history</td><td>Summarise rather than replay; expire stale memory</td></tr>
<tr><td>Human review</td><td>Approval queues and exception handling</td><td>Raise autonomy only where audit history supports it</td></tr>
<tr><td>Failure and rework</td><td>Tasks that fail late in the trajectory</td><td>Fail fast with early validation; clear escalation rules</td></tr>
</tbody>
</table>
<p>The discipline that keeps agent programmes solvent is to report cost per completed task alongside success rate from the first pilot, not from the first invoice. Teams that do this discover quickly which tasks are worth automating and which are cheaper left to a human with a good dashboard — and that distinction, more than any architectural choice, is what separates a productive agent deployment from an expensive one.</p>
"""

process(SLUG, {}, adds={"EN": EN_ADD2}, tag=SLUG[:24])
