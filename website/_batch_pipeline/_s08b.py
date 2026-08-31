import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "chinese-manufacturers-ai-quality-control"

EN_ADD2 = """
<h2 id="what-should-buyers-ask-before-signing-an-ai-inspection-contract">What Should Buyers Ask Before Signing an AI Inspection Contract?</h2>
<p>Procurement questions determine whether an inspection system is an asset or a maintenance obligation. Five belong in every evaluation. What are the recall and false-positive rates per defect class, measured on our product and our line, not on a vendor benchmark? What happens to accuracy when material, lighting, or tooling changes, and who pays for the retraining? How long does it take to add a new defect class, and does that require the vendor or can our engineers do it? Which data leaves the plant, and where is it stored? And what is the annual cost after year one, including model operations, hardware replacement, and support?</p>
<p>The answers reveal the commercial model underneath the technology. Vendors who quote only accuracy have usually not operated a system through a material change. Vendors who cannot price retraining are planning to charge for it later. And vendors who require every new defect class to go through their professional services team have built a recurring revenue stream rather than a capability transfer. Manufacturers that insist on written answers to all five before signing consistently report fewer surprises in year two — which, in a market where inspection systems are expected to run for a decade, matters more than the demonstration.</p>
"""

process(SLUG, {"EN": [("how-manufacturers-can-adopt-this-without-building-it",
                       "How Can Manufacturers Adopt This Without Building It?")]},
       adds={"EN": EN_ADD2}, tag=SLUG[:24])
