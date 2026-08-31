import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "financial-services-ai-fraud-detection-real-time"

EN_ADD2 = """
<h2 id="what-features-actually-move-fraud-model-performance">What Features Actually Move Fraud Model Performance?</h2>
<p>Teams often assume that model choice drives performance. In production fraud systems, feature freshness and entity resolution matter more. A sophisticated model scoring on features computed an hour ago loses to a simpler model scoring on features computed nine milliseconds ago, because most fraud is visible only in the immediate behaviour of the entity — the device that has just been used, the velocity of the last few attempts, the deviation from this cardholder's own recent pattern.</p>
<p>Three feature families carry most of the signal. Velocity features count events over sliding windows — transactions per card per hour, failed attempts per device per day — and they must be computed incrementally as events arrive. Behavioural baselines compare the current event to the entity's own history, which requires a persisted profile per cardholder, device, and merchant, updated on every event. Network features link entities that share attributes — a device seen across many accounts, a bank account receiving from many unrelated senders — and they are what catches organised activity that looks normal individually.</p>
<p>Getting entity resolution right is the prerequisite for all three. If the same device appears under three different identifiers, every velocity count is wrong and every network link is missed. Institutions that invest early in a persistent entity graph consistently outperform those that chase model architecture, which is why the unglamorous work is again where the return sits.</p>
"""

process(SLUG, {}, adds={"EN": EN_ADD2}, tag=SLUG[:24])
