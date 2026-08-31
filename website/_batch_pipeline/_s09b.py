import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "microsoft-teams-analytics-dashboards"

EN_ADD2 = """
<h2 id="what-should-you-measure-to-know-it-worked">What Should You Measure to Know It Worked?</h2>
<p>Adoption metrics for a chat analytics surface are easy to collect and easy to misread. Question volume flatters a bot that is confusing, because unclear answers generate follow-up questions. The metrics that actually predict value are time-to-answer, repeat usage, and escalation rate. Time-to-answer compares the elapsed time from question to accepted answer against the previous reporting queue — this is the number that converts a pilot into budget. Repeat usage counts distinct people who ask a second question in a separate week, which separates habit from novelty. Escalation rate measures how often an answer had to be corrected or handed to an analyst, which is the honest measure of quality.</p>
<p>Report all three monthly for the first two quarters, and add one qualitative input: a standing prompt in the channel asking what the assistant got wrong. The corrections users volunteer are worth more than any log analysis, because they tell you which definitions are missing rather than which queries failed.</p>
"""

process(SLUG, {}, adds={"EN": EN_ADD2}, tag=SLUG[:24])
