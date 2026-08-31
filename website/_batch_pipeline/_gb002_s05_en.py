# -*- coding: utf-8 -*-
"""Expand the EN body of data-retention-policies-for-ai-training-datasets-a-2026-update."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb002_h2 import rename_h2, add_tail_section, ensure_faq_section

P = 'blog/articles/data-retention-policies-for-ai-training-datasets-a-2026-update.html'

for old, new in [
    ("The Current Landscape", "Why Has AI Training Data Retention Become a Governance Problem?"),
    ("Key Implementation Challenges", "What Makes Training-Data Retention So Hard to Implement?"),
    ("Practical Approaches That Work", "Which Retention Practices Actually Work in Production?"),
    ("Key Takeaways", "What Are the Key Takeaways for Training-Data Retention?"),
    ("Conclusion", "Where Should You Start With AI Training Data Retention?"),
]:
    print(rename_h2(P, old, new))

S1 = """<p>A trained model is not a copy of its training data, but it is derived from it, and that distinction drives every retention decision downstream. Four artefact classes need separate treatment.</p>
<table class="data-table"><thead><tr><th>Artefact</th><th>What it is</th><th>Retention posture</th></tr></thead><tbody>
<tr><td>Raw source extracts</td><td>Original records pulled from operational systems</td><td>Shortest life; delete once the training run is validated, unless a contractual or statutory hold applies</td></tr>
<tr><td>Processed and labelled datasets</td><td>Cleaned, deduplicated, feature-engineered, and annotated versions</td><td>Retain for the model's operational life plus the audit window; these are needed to reproduce a result</td></tr>
<tr><td>Model weights and configurations</td><td>The trained artefact and the parameters that produced it</td><td>Retain for the model's lifecycle plus regulatory evidence requirements</td></tr>
<tr><td>Evaluation and lineage records</td><td>Holdout results, training-run metadata, data lineage</td><td>Retain longest; these are the evidence that a decision was made properly</td></tr>
</tbody></table>
<p>The reason for separating them is that collapsing them into one policy produces the two classic failures. Treat everything as training data and you delete the evaluation records that demonstrate your model was tested — evidence you will be asked for after an incident. Treat everything as a model artefact and you retain raw personal data indefinitely on the theory that it "might be needed for retraining", which is exactly the accumulation that storage-limitation rules prohibit.</p>
<p>Lineage is what makes the separation operable. If every model version can be traced to the exact input snapshot, the preprocessing code, and the dataset version that produced it, you can delete the raw extract confidently once the snapshot is captured, because reproducibility no longer depends on keeping the original. Organisations without lineage keep everything precisely because they cannot prove what depends on what.</p>"""

S2 = """<p>Erasure is the hardest problem in training-data retention, and it is better solved by design than by deletion. Once personal data has influenced model weights, there is no reliable surgical removal: the information is distributed across parameters, and attempts to unlearn it tend to degrade the model or leave residual traces.</p>
<p>Three designs are defensible, and most organisations end up using a combination:</p>
<ol>
<li><strong>Exclude erasure-prone data from training.</strong> Data categories with a high likelihood of erasure requests — customer service transcripts, marketing engagement histories, anything tied to a short-lived consent — are excluded from training corpora by policy and used only in retrieval contexts where deletion is straightforward. This is the cleanest option where the data is not essential to model quality.</li>
<li><strong>Retrain on a defined cadence.</strong> Maintain an erasure register, and retrain from the curated corpus at a documented interval — quarterly or monthly depending on volume — so that erased records are absent from the corpus used for the next model version. The operational requirement is version discipline: the old model must be retired on schedule, not left running alongside the new one.</li>
<li><strong>De-identify before training.</strong> Where the analytical value is in the pattern rather than the individual, de-identify or aggregate before the training step. Properly anonymised data falls outside much of the personal-data regime, which means an erasure request does not reach the model at all. The standard to meet is genuine anonymisation — the point at which re-identification is not reasonably possible — not pseudonymisation, which remains personal data.</li>
</ol>
<p>The design decision should be made before the first training run, not after the first erasure request. Retrofitting an erasure strategy onto a model already in production usually means retraining from scratch, and the cost of that is the argument for deciding early.</p>"""

S3 = """<p>Retention rules do not converge globally, and an AI programme that trains on data from multiple regions has to accommodate the strictest applicable rule or segregate its corpora. Three patterns cover most of the variation.</p>
<ul>
<li><strong>Purpose-bound retention with a defined maximum.</strong> The GDPR model: keep personal data no longer than necessary for the documented purpose, with storage-limitation breaches carrying fines up to €20 million or 4% of annual global turnover. Sector rules layer on top — financial services record-keeping, for example, can mandate minimum periods that override a general preference for deletion.</li>
<li><strong>Sector-specific minimums.</strong> Regulated industries often impose minimum rather than maximum periods: a bank cannot delete transaction records it is required to produce. The practical resolution is to separate the mandatory record from the training corpus — keep the record under its statutory schedule, and exclude it from training data that would otherwise be retained on a shorter cycle.</li>
<li><strong>Documented retention with cross-border constraints.</strong> Several Asia-Pacific regimes require retention to be limited and documented, and add localisation or transfer conditions that affect where training corpora may be stored and processed. Korea's AI Framework Act, effective January 2026, is the most recent addition to this group.</li>
</ul>
<p>Two operating decisions follow. First, tag datasets with jurisdiction at ingestion, because retrofitting jurisdiction tags to a corpus that has already been mixed is extremely expensive. Second, decide whether to apply the strictest rule globally or to segregate corpora by region. Global application is simpler to operate and easier to defend; segregation preserves more data utility but requires enforcement that regional corpora never mix, which is a harder engineering problem than it appears.</p>"""

S4 = """<p>Regulators ask the same four questions in almost every examination of retention practice, and an automated framework answers each with a query rather than a reconstruction.</p>
<ol>
<li><strong>What is the policy, and who approved it?</strong> A retention schedule per data category, with an owner, an approval record, and an effective date.</li>
<li><strong>What purpose justifies each retention period?</strong> A documented purpose per category, tied to the business or legal basis for holding the data.</li>
<li><strong>Was the policy applied to everything in scope?</strong> Coverage reporting — the share of datasets carrying a retention tag and an automated schedule — stated honestly rather than implied.</li>
<li><strong>Can you show enforcement?</strong> Deletion and archival logs with timestamps, plus an exception register listing what was held past its date, why, and who authorised it.</li>
</ol>
<p>The exception register is where most examinations are actually decided. Every organisation holds something past its retention date — litigation holds, ongoing investigations, contractual obligations — and a register that documents those holds with named approvers and expiry dates is evidence of a controlled process. An undocumented hold discovered during an examination reads as a systemic failure regardless of how good the rest of the framework is.</p>
<p>The most useful preparation is a rehearsal: run the four queries internally before anyone asks, and fix what they surface. Organisations that do this routinely discover categories of data that were never tagged, scheduled jobs that stopped running months earlier, and copies of deleted datasets persisting in downstream environments and backups. All three are cheap to fix when found internally and expensive to explain when found by someone else.</p>"""

for sid, title, body in [
    ("how-do-retention-rules-apply-to-model-weights-and-derived-artefacts", "How Do Retention Rules Apply to Model Weights and Derived Artefacts?", S1),
    ("how-do-you-handle-erasure-requests-when-data-is-already-in-a-model", "How Do You Handle Erasure Requests When Data Is Already in a Model?", S2),
    ("how-should-retention-differ-across-jurisdictions", "How Should Retention Differ Across Jurisdictions?", S3),
    ("how-do-you-prove-retention-compliance-to-a-regulator", "How Do You Prove Retention Compliance to a Regulator?", S4),
]:
    print(add_tail_section(P, sid, title, body))

FAQ = [
    ("Is there a standard retention period for AI training data?",
     "No, and any single number offered without context is misleading. The defensible approach is tiered: raw source extracts are usually deleted once a training run is validated; processed and labelled datasets are kept for the model's operational life plus the audit window, commonly two to seven years depending on jurisdiction and sector; model weights and evaluation records are retained as evidence; and anything without a documented purpose should not be retained at all. What makes the framework defensible is the structure — every category has a purpose, a period, an owner, and automated enforcement — rather than the specific number of months."),
    ("Can we keep training data indefinitely if we anonymise it?",
     "Genuine anonymisation changes the analysis substantially, because data that no longer identifies an individual falls outside much of the personal-data regime. The bar, however, is higher than many teams assume: removing names and IDs is pseudonymisation, not anonymisation, and re-identification through combinations of quasi-identifiers is often feasible. The test is whether re-identification is reasonably possible given the data and the means available. Where the analytical value lies in patterns rather than individuals, aggregate or de-identified features are usually the better training input."),
    ("What happens if someone requests erasure after their data trained our model?",
     "It depends on which design you chose before training. If the data category was excluded from training by policy, deletion is straightforward. If you retrain on a cadence, the record is removed from the corpus and the next model version is built without it, with the previous version retired on schedule. If the data genuinely influenced weights, there is no reliable surgical removal, which is why the erasure strategy belongs in the design phase rather than the response phase. Documenting the approach and applying it consistently is what regulators assess."),
    ("Do we have to delete data that is under legal hold?",
     "No, and you should not. A legal hold suspends the deletion schedule for the specific data in scope, and the obligation to preserve it overrides a routine retention policy. The requirement is that the hold is documented: what is held, under what authority, until when, and who approved it. Holds without documentation are the most common finding in retention examinations, because an undocumented hold is indistinguishable from data that was simply never deleted."),
    ("How do we apply retention to copies of data in backups and downstream systems?",
     "Treat deletion as a propagation problem, not a single-system operation. A defensible approach maintains an inventory of every location a dataset reaches — warehouses, feature stores, vector indexes, notebooks, downstream marts, backups — and defines the deletion path for each. Backups are typically handled by expiry rather than surgical deletion: confirm the backup retention window, document it, and ensure the data is not reintroduced on restore. Locations that cannot be deleted from should be classified as out of scope for personal data from the outset."),
    ("Who should own retention policy for AI training data?",
     "A named data governance owner should own the policy, but the schedule cannot be set without three inputs: legal or compliance on statutory minimums and maximums, the data or ML engineering team on what is technically enforceable in the pipeline, and the business owner on what period the use case genuinely requires. Retention fails most often when it is owned entirely by one function — legal produces a schedule nobody can enforce, engineering builds tooling nobody defined a purpose for, and the business keeps data because no one asked."),
]
print(ensure_faq_section(P, FAQ, "en"))
