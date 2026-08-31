import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "logistics-route-optimization-ai-real-time"

EN_ADD2 = """
<h2 id="what-does-good-driver-adoption-of-a-routing-system-require">What Does Good Driver Adoption of a Routing System Require?</h2>
<p>Drivers are the last mile of any routing deployment, and they are also the most reliable judge of whether a plan is realistic. A system that produces theoretically optimal routes based on average dwell times will be quietly discarded by drivers who know that a particular receiving dock always takes forty minutes, whatever the plan says. Adoption is therefore won by incorporating driver knowledge and by respecting the driver's working reality, not by producing a better objective value.</p>
<p>Three practices matter most. Capture local knowledge explicitly: let drivers flag a stop as consistently problematic, and feed that feedback into dwell-time distributions rather than leaving it in conversation. Explain the plan: show the driver why the sequence is what it is and what would change if a stop slipped, because a driver who understands the reasoning will follow it under pressure and one who does not will revert to habit. And protect the freeze window: once stops are committed, hold them, because nothing destroys confidence faster than instructions that change while the driver is already en route.</p>
<p>Measure adoption directly — the share of suggested sequences actually followed, and the rate of manual overrides with reasons attached. That single metric predicts realised ROI better than any model quality score, because an unused plan has no cost, no benefit, and no future.</p>
"""

process(SLUG, {}, adds={"EN": EN_ADD2}, tag=SLUG[:24])
