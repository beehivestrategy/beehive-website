import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "voice-interface-enterprise-analytics-accessibility"

EN_ADD2 = """
<h2 id="how-do-you-keep-voice-analytics-governed-and-auditable">How Do You Keep Voice Analytics Governed and Auditable?</h2>
<p>Voice introduces governance questions that text interfaces do not, and they are worth resolving before deployment rather than after the first awkward incident. The first is audience: a spoken answer is audible to everyone within range, which makes the physical context part of the permission model. A query about individual employee performance asked on a shop floor is a disclosure whether or not the asker was entitled to the answer, so sensitive data classes should default to a screen-only or silent response, with an explicit opt-in required to have them spoken aloud.</p>
<p>The second is identity. Voice is trivially spoofable by comparison with a logged-in session, so any voice surface that can reach sensitive data needs a stronger binding — a device-bound session, a PIN for sensitive classes, or a re-authentication step inside the companion app. The third is record-keeping: spoken queries must be logged like any other query, with the transcribed text, the resolved intent, the data returned, and the identity that authorised it, while the raw audio is retained only where policy requires and for the shortest period allowed.</p>
<p>Handled well, these controls are invisible to the user and reassuring to the compliance function. Handled late, they produce the worst outcome in enterprise software: a capability that has to be withdrawn after people have come to rely on it.</p>
"""

process(SLUG, {}, adds={"EN": EN_ADD2}, tag=SLUG[:24])
