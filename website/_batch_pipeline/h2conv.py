#!/usr/bin/env python3
"""Convert statement-style EN H2s to question form, preserving id attributes.
Safe: only rewrites the <h2>...</h2> text; never touches other markup."""
import re, sys, os
ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

# per-slug list of (old_exact_text, new_question_text)
MAP = {
"explainable-ai-in-analytics-making-black-boxes-transparent-a-2026-update": [
 ("The Current Landscape","What Is the Current Regulatory Landscape for Explainable AI?"),
 ("Key Implementation Challenges","What Are the Key Challenges in Implementing Explainable AI?"),
 ("What Does \"Explainable\" Mean in Practice?","What Does \"Explainable\" Mean in Practice for Analytics?"),
 ("Practical Approaches That Work","Which Practical Approaches Actually Work for Explainable AI?"),
 ("Key Takeaways","What Are the Key Takeaways for Explainable AI?"),
 ("Conclusion","What Should Enterprises Do Next to Make AI Accountable?"),
],
"real-time-data-streaming-for-ai-powered-decision-making-part-2": [
 ("Beyond Batch: The Streaming-First Paradigm Shift","Why Are Enterprises Moving Beyond Batch to a Streaming-First Model?"),
 ("Architecture Patterns for Production Streaming Pipelines","Which Architecture Patterns Work for Production Streaming?"),
 ("Real-Time Feature Engineering at Scale","How Do You Engineer Real-Time Features at Scale?"),
 ("Operationalising Streaming Analytics: Metrics and Governance","How Do You Run Streaming Analytics with Governance?"),
 ("Key Takeaways","What Are the Key Takeaways on Streaming Analytics?"),
 ("Conclusion","What Should You Do Next with Streaming Analytics?"),
],
"china-ai-model-wave-conversational-bi-evolution-2026": [
 ("China's AI Model Acceleration","What Is Driving China's AI Model Acceleration?"),
 ("The Conversational BI Evolution","How Has Conversational BI Evolved?"),
 ("Alibaba's QwenWork Consolidation","What Does Alibaba's QwenWork Consolidation Signal?"),
 ("Implications for Global Enterprise AI","What Are the Implications for Global Enterprise AI?"),
],
"competitive-advantage-through-ai": [
 ("Understanding the Current Landscape","What Is the Current AI Competitive Landscape?"),
 ("Key Principles and Strategic Framework","Which Principles Define an AI Competitive Strategy?"),
 ("Implementation Approach and Best Practices","How Should You Implement an AI Competitive Strategy?"),
 ("Measuring Success and Demonstrating ROI","How Do You Measure AI Advantage and Demonstrate ROI?"),
 ("Common Pitfalls and How to Avoid Them","Which Pitfalls Undermine AI Competitive Advantage?"),
 ("Key Takeaways","What Are the Key Takeaways on AI Advantage?"),
 ("Conclusion","What Should Enterprises Do Next on AI Advantage?"),
],
"agentic-workflows-enterprise-automation": [
 ("Why it matters","Why Do Agentic Workflows Matter for Enterprises?"),
 ("Common challenges","What Challenges Arise When Deploying Agents?"),
 ("What can agents actually do today?","What Can Agents Actually Do in Enterprises Today?"),
 ("How to get started","How Do You Get Started with Agentic Workflows?"),
 ("Governance is the deployment plan","Why Is Governance the Real Deployment Plan for Agents?"),
 ("Key takeaways","What Are the Key Takeaways on Agentic Workflows?"),
 ("Frequently asked questions","What Questions Do Enterprises Ask About Agentic Workflows?"),
],
"enterprise-ai-governance-board-framework": [
 ("The Strategic Imperative for Enterprise AI in 2025","Why Is AI Governance a Strategic Imperative in 2025?"),
 ("Framework for AI Strategy Development","How Do You Build an AI Governance Framework?"),
 ("Measuring Success and Demonstrating ROI","How Do You Measure AI Governance Success and ROI?"),
 ("Implementation Roadmap and Key Success Factors","What Does an AI Governance Implementation Roadmap Look Like?"),
],
"conversational-bi-human-resources-people-analytics": [
 ("The Rise of Conversational Business Intelligence","Why Has Conversational BI Risen in the Enterprise?"),
 ("Architecture for Enterprise Conversational BI","What Does an Enterprise Conversational BI Architecture Look Like?"),
 ("Implementation Strategies and Best Practices","How Should You Implement Conversational BI for HR?"),
],
"case-study-consultancy-cut-reporting-time-mcp-bi": [
 ("The Reporting Bottleneck Facing Professional Services","What Reporting Bottleneck Faces Professional Services?"),
 ("The Challenge: 72 Hours to Answer a Client Question","What Was the Challenge of Answering Client Questions in 72 Hours?"),
 ("The Solution: MCP-Powered Conversational BI","How Did MCP-Powered Conversational BI Solve It?"),
 ("Implementation: From Scoping to Live in 10 Days","How Was the MCP BI Solution Implemented in 10 Days?"),
 ("The Results: 71% Faster Reporting and a New Commercial Edge","What Results Did the MCP BI Deployment Deliver?"),
 ("Why This Model Works for Other Service Firms","Why Does This Model Work for Other Service Firms?"),
 ("Conclusion","What Can Other Firms Learn from This Case?"),
],
"event-driven-architecture-for-ai-agent-orchestration-a-2026-update": [
 ("The Current Landscape","What Is the Current Landscape for AI Agent Orchestration?"),
 ("Key Implementation Challenges","What Challenges Arise in AI Agent Orchestration?"),
 ("Practical Approaches That Work","Which Practical Approaches Work for Event-Driven Orchestration?"),
 ("Key Takeaways","What Are the Key Takeaways on Event-Driven AI?"),
 ("Conclusion","What Should You Do Next with Event-Driven AI?"),
],
"mcp-vs-traditional-apis-why-context-protocol-changes-everything": [
 ("The Integration Tax Every Enterprise Pays","What Is the Integration Tax Enterprises Pay?"),
 ("The Semantic Layer Advantage","What Advantage Does the Semantic Layer Bring to MCP?"),
 ("Key Takeaways","What Are the Key Takeaways on MCP?"),
 ("Conclusion","What Should You Do Next with MCP?"),
],
"enterprise-data-catalog-ai-readiness-oct2025": [
 ("Key Benefits and ROI Considerations","What ROI and Benefits Does a Data Catalog Deliver?"),
 ("Implementation Roadmap and Next Steps","What Does a Data Catalog Implementation Roadmap Look Like?"),
],
"rag-architecture-patterns-enterprise-2025": [
 ("The Current State of Enterprise Architecture","What Is the Current State of Enterprise RAG Architecture?"),
 ("Technical Implementation Patterns","What Technical Patterns Implement RAG in Production?"),
 ("Performance and Scalability Considerations","How Do You Scale RAG for Performance?"),
 ("Security and Compliance Integration","How Do You Integrate Security and Compliance in RAG?"),
 ("Looking Ahead: What to Expect","What Should You Expect from RAG Next?"),
],
"cybersecurity-ai-threat-landscape-q4-2025": [
 ("The Evolving AI-Powered Threat Landscape","How Is the AI-Powered Threat Landscape Evolving?"),
 ("Key Benefits and ROI Considerations","What ROI Do AI Defenses Deliver?"),
 ("Implementation Roadmap and Next Steps","What Does an AI Security Roadmap Look Like?"),
],
"ai-success-metrics-beyond-accuracy": [
 ("Strategic Context and Market Dynamics","What Is the Strategic Context for AI Success Metrics?"),
 ("Key Decision Points for Enterprise Leaders","What Decision Points Should Leaders Weigh for AI Metrics?"),
 ("Organizational Readiness Assessment","How Do You Assess Organizational Readiness for AI Metrics?"),
 ("Measuring Success and ROI","How Do You Measure AI Success and ROI?"),
 ("Actionable Recommendations for H2 2025","What Are the Actionable Recommendations for H2 2025?"),
],
"why-edge-ai-manufacturing-logistics-energy": [
 ("5 Reasons Edge AI Is Reshaping Heavy Industry","Why Is Edge AI Reshaping Heavy Industry?"),
 ("Edge AI vs. Cloud AI for Industry","How Does Edge AI Compare with Cloud AI for Industry?"),
 ("How Beehive Strategy Helps","How Does Beehive Strategy Help with Edge AI?"),
],
"the-future-of-work-ai-augmented-decision-making": [
 ("The Current Landscape","What Is the Current Landscape for AI-Augmented Work?"),
 ("Key Implementation Challenges","What Challenges Arise in AI-Augmented Decision-Making?"),
 ("Practical Approaches That Work","Which Approaches Work for AI-Augmented Decisions?"),
 ("Key Takeaways","What Are the Key Takeaways on AI-Augmented Work?"),
 ("Conclusion","What Should Enterprises Do Next on AI-Augmented Work?"),
],
"text-to-sql-accuracy-enterprise-trust": [
 ("Why it matters","Why Does Text-to-SQL Accuracy Matter for Enterprise Trust?"),
 ("Common challenges","What Challenges Undermine Text-to-SQL Accuracy?"),
 ("How to get started","How Do You Get Started with Trustworthy Text-to-SQL?"),
 ("Key takeaways","What Are the Key Takeaways on Text-to-SQL?"),
 ("Frequently asked questions","What Questions Do Teams Ask About Text-to-SQL?"),
],
"2026-ai-budget-planning-enterprise-guide-nov2025": [
 ("What Realistic 2026 AI Budgets Look Like","What Do Realistic 2026 AI Budgets Look Like?"),
 ("Key Benefits and ROI Considerations","What ROI Should AI Budget Decisions Target?"),
 ("Implementation Roadmap and Next Steps","What Does a 2026 AI Budget Implementation Roadmap Look Like?"),
],
}

def conv(html, pairs):
    for old, new in pairs:
        pat = re.compile(r'(<h2[^>]*>)' + re.escape(old) + r'(</h2>)', re.S)
        html, n = pat.subn(lambda m: m.group(1) + new + m.group(2), html)
    return html

if __name__ == "__main__":
    slug = sys.argv[1]
    p = os.path.join(ROOT, "blog/articles", slug + ".html")
    h = open(p, encoding='utf-8').read()
    if slug in MAP:
        h2 = conv(h, MAP[slug])
        if h2 != h:
            open(p,'w',encoding='utf-8').write(h2)
            print(f"{slug}: {sum(1 for _ in MAP[slug])} H2s converted")
        else:
            print(f"{slug}: no change (check text)")
    else:
        print(f"{slug}: no map")
