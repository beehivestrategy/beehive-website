# -*- coding: utf-8 -*-
"""Content specs for gbatch_001 slugs 7-11."""

SPECS = {}

# --------------------------------------------------------------------------- 7
SPECS["cross-border-data-transfer-framework-2025-compliance"] = {
    "EN": {
        "rename": {
            "global-regulatory-landscape-overview":
                "What Does the Global Cross-Border Transfer Landscape Look Like?",
            "compliance-requirements-for-enterprise-ai":
                "What Do Enterprise AI Systems Require for Transfer Compliance?",
            "building-a-sustainable-compliance-program":
                "How Do You Build a Sustainable Transfer Compliance Program?",
            "enterprise-ai-compliance-system-construction-guide":
                "How Should You Construct an Enterprise AI Compliance System?",
            "building-a-transfer-compliance-roadmap-for-2025":
                "How Do You Build a Transfer Compliance Roadmap?",
        },
        "new": [
            ("what-counts-as-a-cross-border-transfer-in-an-ai-pipeline",
             "What Counts as a Cross-Border Transfer in an AI Pipeline?",
             ["<p>Transfer analysis is usually applied to the obvious cases — replicating a production "
              "database to another region, or syncing customer records to a global CRM — and missed "
              "entirely in the places where AI systems actually move data. Three of those places cause "
              "most of the surprise findings in an audit.</p>",
              "<p>The first is remote access. If an engineer in Singapore can query a dataset physically "
              "stored in Frankfurt, several regulators treat that access as a transfer, even though no "
              "copy is made. The same logic applies to a support engineer viewing a screen share of "
              "personal data, and to a vendor's administrator logging in from a third country. "
              "Documentation that only tracks replication jobs will show zero transfers while the "
              "organisation is transferring continuously.</p>",
              "<p>The second is inference. Sending a prompt that contains personal information to a model "
              "endpoint hosted in another jurisdiction is a transfer of that personal information. This is "
              "the single most common gap in AI deployments, because the data path runs through an SDK "
              "call rather than a pipeline, and because the prompt content is often assembled at runtime "
              "from several systems. It applies to third-party model APIs and to self-hosted models in "
              "another region alike.</p>",
              "<p>The third is the derived-data chain. Embeddings, feature stores, evaluation sets, and "
              "fine-tuning corpora are all derived from source personal information, and in most "
              "frameworks they inherit its status. A vector index is not anonymised data simply because it "
              "is a list of floats; if the source records can be reconstructed or re-identified from it, "
              "it remains personal data. Treat every derived artefact as in-scope until you have a "
              "documented basis for saying otherwise.</p>"]),
            ("how-do-you-document-a-transfer-impact-assessment",
             "How Do You Document a Transfer Impact Assessment?",
             ["<p>A transfer impact assessment exists to answer one question: will the data be protected "
              "to an equivalent standard after it leaves, and if not, what compensating measures close "
              "the gap. Regulators in the EU, the UK, China, and increasingly elsewhere expect a "
              "documented answer, and they expect it to be specific to the transfer rather than a "
              "generic statement about the destination country.</p>",
              "<p>A usable assessment has five parts. A description of the transfer: the data categories, "
              "the volume, the exporter and importer, the purposes, and the onward transfers the importer "
              "will make. The mechanism relied upon and why it is the right one for this transfer. An "
              "analysis of the destination jurisdiction's laws and practices as they apply to this "
              "importer — government access powers, remedy availability, and the importer's practical "
              "experience with them. The identified risks. And the supplementary measures: encryption "
              "with keys held by the exporter, pseudonymisation, contractual commitments to challenge "
              "overbroad requests, transparency reporting, and audit rights.</p>",
              "<p>The part teams get wrong is the third. Assessments tend to describe the destination "
              "country's laws in the abstract, which is neither defensible nor useful. What matters is "
              "whether <em>this</em> importer is subject to those laws, whether it has received such "
              "requests, and what it would do if it did. Asking the vendor those questions directly, and "
              "recording the answers, is both the strongest evidence and the fastest way to find out that "
              "a vendor cannot answer them.</p>",
              "<p>Treat the assessment as a living document with an owner and a review trigger. Reassess "
              "on a change of importer, a change of sub-processor, a material change in volume or data "
              "categories, and on any change in the destination jurisdiction's legal position. Keeping a "
              "register of assessments keyed by transfer stream is what turns a regulatory request into a "
              "lookup rather than a project.</p>"]),
            ("what-breaks-when-standard-contracts-meet-ai-vendors",
             "What Breaks When Standard Contract Terms Meet AI Vendors?",
             ["<p>Standard contractual clauses and their equivalents were drafted for a world of "
              "deterministic processing: the importer receives data, processes it for a defined purpose, "
              "and returns or deletes it. AI vendors break three assumptions embedded in that model, and "
              "each break needs explicit drafting rather than a signature.</p>",
              "<p>The first is training. Many vendor agreements permit the provider to use customer data "
              "to improve models. Under most transfer regimes that is a new purpose, and a new purpose "
              "needs its own lawful basis and its own disclosure to the individuals concerned. The "
              "practical fix is a contractual prohibition on training with your data unless specifically "
              "agreed, plus a written confirmation of which tier of the vendor's service enforces it — "
              "this is often the difference between an enterprise and a consumer plan.</p>",
              "<p>The second is sub-processing depth. An AI vendor typically relies on a model provider, a "
              "cloud provider, an observability provider, and sometimes an annotation contractor. Each "
              "onward transfer needs to be identified and each party needs to be bound to equivalent "
              "obligations. Vendors frequently disclose only the first tier, so the negotiation needs to "
              "require a maintained sub-processor list with advance notice of additions and a right to "
              "object.</p>",
              "<p>The third is retention and deletion. Logs, prompts, embeddings, and evaluation sets all "
              "persist, frequently longer than the primary data, and often outside the deletion workflow "
              "that governs the main dataset. Deletion clauses need to name these artefacts explicitly and "
              "specify a maximum retention window for each. Where the vendor cannot delete an artefact — "
              "a model weight influenced by your data, for example — say so in the contract and treat it "
              "as a risk to be accepted in writing rather than a gap discovered during an audit.</p>"]),
            ("how-do-you-keep-a-transfer-inventory-current",
             "How Do You Keep a Transfer Inventory Current?",
             ["<p>Every compliance programme builds a data map once. Almost none of them keep it current, "
              "because the map is maintained by hand and the estate changes weekly. The result is a "
              "document that is accurate on the day it is finished and progressively less useful "
              "afterwards — which is precisely when a regulator or a customer asks for it.</p>",
              "<p>The only durable approach is to generate the inventory from the systems that actually "
              "move data rather than from interviews. Three sources cover most of the estate: "
              "orchestration metadata, which knows every job and its destinations; network egress logs "
              "and API gateway records, which capture the flows that bypass orchestration, including "
              "model API calls; and infrastructure-as-code or cloud configuration, which tells you where "
              "the data physically rests.</p>",
              "<p>Sampling and reconciling these against the declared inventory is what produces an "
              "honest picture, and the reconciliation is where the findings come from. In practice, the "
              "first reconciliation almost always surfaces flows nobody declared: a SaaS integration "
              "configured by a business team, a back-up replicating to a second region by default, a "
              "model endpoint added during a proof of concept and never removed.</p>",
              "<p>Then make keeping it current someone's job with a trigger, not a calendar reminder. "
              "Wire it into change management: a new pipeline, a new vendor, or a new region requires an "
              "inventory entry before deployment, and the deployment checklist fails without one. Pair "
              "that with a quarterly automated reconciliation that reports drift. Organisations that do "
              "this answer due-diligence questionnaires in days; those that do not spend weeks "
              "rediscovering their own architecture.</p>"]),
        ],
    },
    "zh-CN": {
        "rename": {
            "全球监管格局概览": "全球跨境传输监管格局是怎样的？",
                        "构建可持续的合规计划": "如何构建可持续的传输合规计划？",
            "合规技术工具与自动化合规方案": "哪些技术工具可以实现合规自动化？",
                        "战略实施路径与关键成功因素": "战略实施路径与关键成功因素是什么？",
            "企业实施路线图与成功因素": "企业实施路线图应如何设计？",
            "行业数字化转型深度分析": "行业数字化转型有哪些深层驱动力？",
        },
        "rename_text": {
            "企业AI系统的合规要求": "企业 AI 系统需要满足哪些传输合规要求？",
            "企业AI合规体系构建指南": "企业应如何构建 AI 合规体系？",
        },
    },
}

# --------------------------------------------------------------------------- 8
SPECS["secure-mcp-deployment"] = {
    "EN": {
        "rename": {
            "understanding-the-current-landscape":
                "What Is the Current MCP Security Landscape?",
            "key-principles-and-strategic-framework":
                "What Are the Core Principles of MCP Security?",
            "implementation-approach-and-best-practices":
                "How Should You Implement MCP Securely?",
            "measuring-success-and-demonstrating-roi":
                "How Do You Measure the ROI of MCP Security?",
            "common-pitfalls-and-how-to-avoid-them":
                "What Are the Most Common MCP Security Pitfalls?",
            "how-a-managed-conversational-bi-service-fits-in":
                "Where Does a Managed Conversational BI Service Fit?",
            "key-takeaways": "What Are the Key Takeaways?",
            "conclusion": "Where Should You Start With MCP Security?",
        },
        "new": [
            ("how-do-you-scope-what-an-mcp-server-may-expose",
             "How Do You Scope What an MCP Server May Expose?",
             ["<p>The security question that matters is not whether MCP is safe but what a particular "
              "server is permitted to expose, to whom, and under what conditions. MCP is a transport and "
              "a tool-description protocol; it faithfully executes whatever you authorise. Every serious "
              "incident we have reviewed had the same shape: a server was given broader access than the "
              "task required, and the model used it exactly as designed.</p>",
              "<p>Start from the tool inventory rather than the data inventory. For each tool the server "
              "exposes, write down the minimum rows, columns, and time range needed to answer the "
              "questions it exists to serve, and the side effects it is allowed to cause. Tools that read "
              "should be read-only at the database role level, not merely documented as such. Tools that "
              "write need an explicit approval threshold and an idempotency key so that a repeated "
              "invocation is a no-op rather than a duplicate transaction.</p>",
              "<p>Then decide who may invoke each tool. The identity that matters is the identity of the "
              "human on whose behalf the model is acting, not the identity of the service account running "
              "the server. Propagating the end-user identity through to the data layer is what makes "
              "row-level policy enforceable, and it is the difference between an assistant that respects "
              "permissions and one that becomes a universal read path around them.</p>",
              "<p>Finally, treat tool descriptions as security-relevant content. A description that tells "
              "the model a tool is harmless and broadly applicable invites broad use. Descriptions "
              "should state scope, preconditions, and constraints, and they should be reviewed under "
              "change control — a change to a tool description is a change to the model's effective "
              "permissions.</p>"]),
            ("what-does-prompt-injection-look-like-through-an-mcp-tool",
             "What Does Prompt Injection Look Like Through an MCP Tool?",
             ["<p>Indirect prompt injection is the threat model that MCP deployments must be designed "
              "against, and it is structurally different from the injection patterns teams are used to. "
              "The attacker does not talk to the model; they place instructions in content the model will "
              "later read — a support ticket, a document in a retrieval corpus, a row in a table, a "
              "comment field. When the assistant processes that content, the embedded instruction competes "
              "with the user's instruction, and it may win.</p>",
              "<p>The consequence specific to MCP is action, not just output. A model with access to "
              "tools that send email, modify records, or move money can be induced to invoke them by "
              "content it retrieved. A poisoned row in a table an assistant summarises can carry an "
              "instruction to export the rest of the table. This is why the standard mitigations for "
              "output-side injection are insufficient on their own.</p>",
              "<p>Three controls reduce the exposure materially. Constrain tool side effects: writes "
              "require explicit human confirmation above a defined threshold, and no tool should be able "
              "to exfiltrate data to an arbitrary external destination. Separate retrieved content from "
              "instructions: mark retrieved text clearly as untrusted data rather than as part of the "
              "prompt, and prefer tool schemas that accept structured arguments over free-text blobs. "
              "And log every invocation with its inputs, so that an induced action can be traced back to "
              "the content that caused it.</p>",
              "<p>Testing matters as much as design. Include injection cases in the evaluation set — "
              "documents that attempt to redirect the assistant — and run them on every change to "
              "prompts, tools, or models. A red-team exercise that only probes the chat surface will miss "
              "the paths that actually cause damage.</p>"]),
            ("how-do-you-audit-an-mcp-deployment",
             "How Do You Audit an MCP Deployment?",
             ["<p>Auditability is the property that turns an MCP deployment from an interesting prototype "
              "into something a risk committee will approve, and it has to be designed in rather than "
              "added later. The question an auditor asks is not whether the system is secure in general "
              "but what happened in a specific case: who asked, what the model did, what data it touched, "
              "and what policy permitted it.</p>",
              "<p>Answering that requires four records per interaction, captured at the time rather than "
              "reconstructed. The request, including the resolved user identity and the authenticated "
              "client. The tool invocations, with arguments and returned row counts — not the full result "
              "set, which would double your exposure. The policy decision that permitted each invocation, "
              "including the name of the policy and the version that evaluated it. And the response, or "
              "at minimum a hash of it, so that a disputed answer can be verified.</p>",
              "<p>Those records need to be tamper-evident and retained according to a documented "
              "schedule. Append-only storage with restricted administrative access is the baseline; "
              "separating the audit store from the application's own credentials is what prevents an "
              "attacker who compromises the application from erasing the evidence of the compromise.</p>",
              "<p>Then use them. Review a sample of interactions on a cadence, look for tools invoked "
              "outside their expected pattern, and alert on anomalies such as a sudden increase in "
              "result-set size or in denied invocations. Audit logging that is never read is a compliance "
              "artefact rather than a control, and the organisations that get value from it are the ones "
              "that treat the logs as an operational signal.</p>"]),
        ],
    },
    "zh-CN": {
        "rename": {
            "理解当前格局": "当前 MCP 的安全格局是怎样的？",
            "关键原则与战略框架": "MCP 安全的核心原则是什么？",
            "实施方法与最佳实践": "应如何安全地实施 MCP？",
            "衡量成功与展示投资回报率": "如何衡量 MCP 安全的投资回报？",
            "常见陷阱及规避方法": "最常见的 MCP 安全陷阱有哪些？",
            "关键要点": "关键要点是什么？",
            "结论": "MCP 安全应从哪里起步？",
        },
        "new": [
            ("如何界定mcp服务可以暴露什么",
             "如何界定 MCP 服务可以暴露什么？",
             ["<p>真正重要的安全问题不是 MCP 是否安全，而是某个具体服务被允许向谁、在什么条件下暴露什么。MCP 是传输与工具描述协议，它会忠实地执行你所授权的一切。我们复核过的每一起严重事件形态相同：服务被赋予了超出任务所需的访问权限，而模型只是按设计使用了它。</p>",
              "<p>从工具清单而非数据清单开始。对服务暴露的每一个工具，写明回答其存在意义所必需的最小行、列与时间范围，以及它允许产生的副作用。只读工具应在数据库角色层面即为只读，而不只是在文档中声明如此。会写入的工具需要显式审批阈值与幂等键，使重复调用成为空操作而非重复交易。</p>",
              "<p>接着决定谁可以调用每个工具。关键身份是模型所代表的那个人，而非运行服务的服务账号。把最终用户身份贯穿到数据层，是行列级策略得以执行的前提，也是&quot;助手遵守权限&quot;与&quot;助手成为绕过权限的通用读取通道&quot;之间的区别。</p>",
              "<p>最后，把工具描述视为与安全相关的内容。告诉模型某工具无害且适用范围广泛的描述，会诱发广泛使用。描述应写明范围、前置条件与约束，并纳入变更控制——修改工具描述，等于修改模型的实际权限。</p>"]),
            ("通过mcp工具的提示注入长什么样",
             "通过 MCP 工具的提示注入长什么样？",
             ["<p>间接提示注入是 MCP 部署必须针对设计的威胁模型，其结构与团队熟悉的注入模式根本不同。攻击者并不与模型对话，而是把指令放进模型稍后会读取的内容里——工单、检索语料中的文档、表中的一行、备注字段。当助手处理这些内容时，嵌入的指令会与用户指令竞争，并可能胜出。</p>",
              "<p>MCP 特有的后果是行动，而不只是输出。一个拥有发信、改记录、转帐工具的模型，可能被它检索到的内容诱导去调用它们。助手所汇总的表中若有一行被投毒，可能携带把整张表导出的指令。这正是仅做输出侧注入缓释不足的原因。</p>",
              "<p>三项控制能实质性降低暴露面。约束工具副作用：超过既定阈值的写操作需要显式人工确认，且任何工具都不能把数据外传到任意外部目的地。区分检索内容与指令：把检索文本明确标记为不可信数据而非提示的一部分，并优先采用接收结构化参数的工具模式，而非自由文本大块内容。以及记录每次调用的输入，使被诱导的行动可追溯到导致它的内容。</p>",
              "<p>测试与设计同等重要。在评估集中纳入注入用例——试图劫持助手的文档——并在提示、工具或模型每次变更时运行。只探测对话界面的红队演练，会漏掉真正造成损害的路径。</p>"]),
            ("如何对mcp部署做审计",
             "如何对 MCP 部署做审计？",
             ["<p>可审计性是把 MCP 部署从有趣的原型变成风险委员会愿意批准的事物的属性，且必须在设计阶段内置，而非事后追加。审计者的问题不是系统在总体上是否安全，而是某个具体case发生了什么：谁提问、模型做了什么、触达了哪些数据、以及什么策略允许了它。</p>",
              "<p>回答这个问题需要每次交互留存四条记录，且须在当时采集而非事后还原。请求本身，含已解析的用户身份与已认证的客户端。工具调用，含参数与返回行数——而非完整结果集，那会让暴露面翻倍。允许每次调用的策略判定，含策略名称与评估所用版本。以及响应，或至少其哈希，使有争议的答案可被验证。</p>",
              "<p>这些记录需要具备防篡改属性，并按成文周期留存。基线是追加写入存储配合受限管理权限；把审计库与应用自身凭据分离，才能防止攻破应用的攻击者抹掉被攻破的证据。</p>",
              "<p>然后要使用它们。按节奏抽样复核交互，寻找调用模式偏离预期的工具，并对异常（如结果集规模突增、被拒绝调用突增）发出告警。从未被读取的审计日志只是合规制品而非控制，能从中获得价值的组织，是把日志当运营信号来用的那些。</p>"]),
        ],
    },
}

# --------------------------------------------------------------------------- 9
SPECS["ai-vendor-contract-negotiation-tips-nov2025"] = {
    "EN": {
        "rename": {
            "key-benefits-and-roi-considerations":
                "What Benefits and ROI Should an AI Contract Actually Secure?",
            "implementation-roadmap-and-next-steps":
                "What Should Your Negotiation Roadmap Look Like?",
        },
        "new": [
            ("how-do-you-price-an-ai-contract-that-scales",
             "How Do You Price an AI Contract That Scales?",
             ["<p>AI pricing is usually negotiated on the wrong unit. Vendors price per seat, per token, "
              "or per outcome, and each of those shifts a different risk onto the buyer. Per-seat pricing "
              "looks safe until usage concentrates: three power users generate most of the value and most "
              "of the consumption, and you end up paying for idle licences while hitting overage on the "
              "ones that matter. Per-token pricing aligns cost with consumption but makes the bill "
              "unpredictable, which is a problem for any team that has to forecast.</p>",
              "<p>The practical approach is to model three scenarios before you negotiate: a pilot with a "
              "known user count, a rollout at ten times the adoption, and a worst case where a single "
              "workflow becomes popular inside a large team. Ask the vendor to quote all three, in "
              "writing. Vendors who will only quote the pilot are telling you something about how the "
              "price behaves at scale, and it is worth listening.</p>",
              "<p>Then negotiate the structural terms, which matter more than the headline number. "
              "Committed-use discounts should be paired with a ramp so that unused commitment carries "
              "forward rather than expiring. Overage rates should be capped, and the cap should be a "
              "price renegotiation trigger rather than a penalty. Price-increase protection should be "
              "tied to an index and capped, and it should survive renewal. And the definition of a "
              "billable unit should be written down in the contract, because &quot;token&quot; is "
              "vendor-specific and changes as models change.</p>",
              "<p>Finally, tie a portion of the fee to adoption or outcome. A contract where the vendor "
              "is paid the same whether the tool is used by ten people or two thousand gives the vendor "
              "no incentive to help with the change management that determines whether the deployment "
              "succeeds. Even a modest milestone-based tranche changes that dynamic substantially.</p>"]),
            ("what-data-rights-should-you-insist-on",
             "What Data Rights Should You Insist On?",
             ["<p>Data terms are where AI contracts diverge most from conventional SaaS agreements, and "
              "where the largest unpriced risks sit. Four clauses deserve specific attention, and in each "
              "case the default vendor position is usually not the one you want.</p>",
              "<p>Training rights. The question is whether your inputs and outputs may be used to train "
              "or improve the vendor's models. Many agreements permit it by default or describe it "
              "vaguely as service improvement. Insist on an explicit prohibition unless separately "
              "agreed, and confirm in writing which service tier enforces it — enterprise terms frequently "
              "differ from the terms the same vendor offers self-serve.</p>",
              "<p>Retention and deletion. Prompts, completions, logs, and evaluation data all persist, "
              "often under different schedules than the primary data. The contract should specify a "
              "maximum retention window for each category and a deletion SLA that covers backups and "
              "derived artefacts. Ask specifically about abuse-monitoring copies, which vendors typically "
              "retain longer and are the most common exception buried in the fine print.</p>",
              "<p>Sub-processor and model-change transparency. You need a maintained list of "
              "sub-processors with notice before additions, and notice before a material change to the "
              "models serving you, because a model swap can change accuracy, latency, cost, and data "
              "handling without any change on your side.</p>",
              "<p>Finally, portability and exit. Specify the format and timeliness of data export, "
              "including conversation history, prompts, and any fine-tuned artefacts you paid for. Ask "
              "what happens to a customised model at termination: whether you can take the weights, "
              "whether you can take only the training data, or whether you lose it entirely. Discovering "
              "the answer at renewal is the worst possible time.</p>"]),
            ("how-do-you-negotiate-liability-for-model-errors",
             "How Do You Negotiate Liability for Model Errors?",
             ["<p>Standard vendor liability caps were written for software that fails in binary ways. "
              "An AI system fails probabilistically and fluently, and it fails in a way that is hard to "
              "attribute: was the wrong answer the vendor's fault, your prompt's fault, your data's "
              "fault, or an inherent property of the model. Vendors lean on that ambiguity to disclaim "
              "nearly everything, and the resulting allocation is usually unacceptable for any "
              "decision-grade use.</p>",
              "<p>Get specific about what is warranted. Accuracy claims should be tied to a measurable "
              "benchmark on your evaluation set, not to marketing language. Where the vendor will not "
              "warrant accuracy, negotiate an uptime and latency SLA with meaningful credits, plus a "
              "commitment to notify you of material model changes so you can re-run your own "
              "evaluations.</p>",
              "<p>Then carve out the categories that a general cap should not swallow. Indemnity for "
              "third-party IP claims arising from the vendor's model or training data is the most "
              "important, because it is the risk you cannot manage yourself and the one most likely to "
              "arrive from outside. Breach of confidentiality and data protection obligations should sit "
              "outside the general cap as well, typically at a multiple of fees.</p>",
              "<p>Where the vendor will not move on the cap, buy insurance or restructure the deployment "
              "instead. Keeping the model out of the decision path for the highest-consequence cases — "
              "using it to draft rather than to decide — is a legitimate design response to a liability "
              "allocation you cannot shift, and it is often faster to implement than another month of "
              "negotiation.</p>"]),
            ("what-should-be-in-the-exit-clause",
             "What Should Be in the Exit Clause?",
             ["<p>Exit terms decide whether a failed deployment is an inconvenience or a crisis, and they "
              "are the clauses most often skimmed because nobody is thinking about failure during "
              "procurement. Three provisions do most of the work.</p>",
              "<p>Termination rights. You want the ability to terminate for convenience with reasonable "
              "notice, not only for cause, and you want any committed spend to be refunded pro rata "
              "rather than forfeited. Multi-year commitments should include an off-ramp at the end of "
              "each year tied to adoption or performance thresholds, so that a deployment that is not "
              "working can be ended without a write-off.</p>",
              "<p>Transition assistance. Specify a defined period during which the vendor continues to "
              "provide service at the current rates after termination, long enough to migrate — ninety "
              "to one hundred and eighty days is typical. Without this, the practical cost of switching "
              "includes an outage, and the vendor knows it.</p>",
              "<p>Data and artefact return. The contract should state what you get back, in what format, "
              "and within how many days: your inputs, your outputs, any configurations, and any "
              "fine-tuned models or evaluation sets you funded. It should also state what the vendor "
              "deletes and when, with written confirmation on request. And it should survive termination "
              "— an exit clause that expires with the agreement is not an exit clause.</p>",
              "<p>Put a named owner and a date against the review of these terms well before renewal. "
              "The strongest negotiating position is the one where the vendor believes, credibly, that "
              "you are prepared to leave.</p>"]),
        ],
    },
    "zh-CN": {
        "rename": {
            "核心收益与投资回报考量": "AI 合同应锁定哪些收益与投资回报？",
            "实施路线图与后续步骤": "谈判路线图应如何设计？",
            "常见问题解答": "常见合同条款疑问有哪些？",
            "案例分析与行业洞察": "有哪些可借鉴的行业案例？",
            "未来展望与行动建议": "未来趋势与行动建议是什么？",
            "关键成功因素与常见陷阱": "关键成功因素与常见陷阱有哪些？",
            "蜂启咨询的专业洞察": "蜂启咨询有哪些专业洞察？",
        },
    },
}

# -------------------------------------------------------------------------- 10
SPECS["audit-ai-models-bias-fairness"] = {
    "EN": {
        "rename": {
            "why-bias-auditing-matters-more-than-ever":
                "Why Does Bias Auditing Matter More Than Ever?",
            "the-four-dimensions-of-a-comprehensive-bias-audit":
                "What Are the Four Dimensions of a Comprehensive Bias Audit?",
            "building-automated-bias-detection-into-the-pipeline":
                "How Do You Build Automated Bias Detection Into the Pipeline?",
            "governance-documentation-and-regulatory-compliance":
                "What Governance and Documentation Does a Bias Audit Require?",
        },
        "new": [
            ("which-fairness-metric-should-you-actually-use",
             "Which Fairness Metric Should You Actually Use?",
             ["<p>Choosing a fairness metric is the first substantive decision in any audit and the one "
              "teams most often defer to a library default. That is a mistake, because the common metrics "
              "encode different moral positions and cannot all be satisfied at once — a result known "
              "formally as the impossibility of simultaneous fairness.</p>",
              "<p>Demographic parity requires that the rate of positive outcomes be equal across groups. "
              "It is easy to measure and easy to explain, and it is the right choice when the concern is "
              "disparate representation — who gets shown an advert, who gets surfaced as a candidate. It "
              "is the wrong choice when the underlying base rates genuinely differ, because enforcing "
              "equal outcome rates then requires treating similar individuals differently.</p>",
              "<p>Equalised odds requires equal true-positive and false-positive rates across groups. It "
              "is the right choice when the cost of a false positive and a false negative is the thing "
              "you care about — credit decisions, fraud flags, clinical screening — because it asks "
              "whether the model is equally accurate for each group rather than whether it produces equal "
              "counts. Predictive parity, which requires equal precision, matters when a positive "
              "prediction triggers a costly intervention.</p>",
              "<p>The practical guidance is to compute several metrics, present them together, and "
              "document which one the deployment is optimised for and why. That documentation is the "
              "deliverable: it converts an unavoidable value judgement into a reviewable decision with an "
              "owner, and it is what an auditor or regulator will ask to see.</p>"]),
            ("how-do-you-audit-a-model-without-protected-attributes",
             "How Do You Audit a Model Without Protected Attributes?",
             ["<p>Many organisations do not hold reliable data on protected attributes, and some are "
              "prohibited from collecting it. That does not make an audit impossible, but it does change "
              "the method, and the limitations need to be stated honestly in the report rather than "
              "papered over.</p>",
              "<p>The first option is proxy inference. Geography, name-derived features, language "
              "preference, and school or employer history can estimate group membership well enough to "
              "detect material disparity, even when they are poor at classifying individuals. The ethical "
              "and legal position here is delicate: you are inferring sensitive attributes for the "
              "purpose of measuring harm. It should be done under a documented protocol, with the "
              "inferred attributes used only for aggregate measurement, stored separately, and deleted "
              "after the analysis.</p>",
              "<p>The second is intersectional analysis on the attributes you do have. Disparity is often "
              "concentrated in combinations — region and tenure, or role and contract type — that "
              "single-attribute analysis averages away. Slicing by combinations of non-protected "
              "attributes frequently surfaces the same underlying problems without requiring sensitive "
              "data at all.</p>",
              "<p>The third is qualitative and outcome-based review: who is being approved or rejected, "
              "what the complaint and appeal patterns look like, and whether the operational override "
              "rate differs by channel or geography. Where quantitative group analysis is not possible, "
              "this evidence is better than nothing and considerably better than an unaudited claim of "
              "fairness. State the method and its limits in the report; an audit that overstates its "
              "coverage is worse than one that bounds it.</p>"]),
            ("what-does-a-bias-audit-report-need-to-contain",
             "What Does a Bias Audit Report Need to Contain?",
             ["<p>A bias audit is only useful if its output can be acted on by people who were not in "
              "the room, and reviewed months later by someone external. That constrains both the content "
              "and the format more than teams expect.</p>",
              "<p>Seven elements belong in the report. Scope: which model version, which data snapshot, "
              "which population, and which use case — a report without a version identifier is not "
              "reproducible. Methodology: the metrics used, the subgroups defined, the sample sizes, and "
              "the confidence intervals, because subgroup analyses on small samples produce noisy numbers "
              "that look like findings. Findings: measured disparity against each metric, with the "
              "threshold used to decide materiality stated in advance rather than after seeing the "
              "numbers.</p>",
              "<p>Then the interpretation, which is the part most reports omit. A disparity is not "
              "automatically discrimination; it may reflect a legitimate business factor, a data quality "
              "problem, or a proxy variable. The report should state the plausible explanations "
              "considered and the evidence for each. Then the recommendation: mitigate, monitor, restrict "
              "the use case, or accept with documented rationale. Then the owner and the date of the next "
              "review.</p>",
              "<p>Keep the report short enough to be read. Ten to fifteen pages with the detailed "
              "analysis in an appendix is more likely to be acted on than a hundred-page document. And "
              "version it alongside the model so that the report and the artefact it describes can never "
              "drift apart.</p>"]),
            ("how-do-you-mitigate-bias-once-you-find-it",
             "How Do You Mitigate Bias Once You Find It?",
             ["<p>Finding disparity is the easy half. Mitigating it without breaking the model — or "
              "creating a different problem — is where audits stall, and the options are frequently "
              "presented as a menu without guidance on when each applies.</p>",
              "<p>Pre-processing addresses the data before training. Reweighting or resampling balances "
              "group representation; removing or transforming proxy features reduces the pathway by which "
              "a protected attribute leaks in. These approaches are model-agnostic and easy to deploy, "
              "and they are the right first move when the disparity originates in the data — which is "
              "most of the time. Their limitation is that proxy removal is never complete, because "
              "correlated features remain.</p>",
              "<p>In-processing builds the constraint into training, typically through a regularisation "
              "term that penalises disparity. It can achieve better fairness-accuracy trade-offs than "
              "pre-processing, but it requires retraining, needs the sensitive attribute available at "
              "training time, and makes the objective harder to explain to a business owner.</p>",
              "<p>Post-processing adjusts outputs, for example by selecting different decision thresholds "
              "per group. It is the most surgical option and the easiest to deploy on an existing model, "
              "and it is often the only option when you cannot retrain. It is also the most legally "
              "sensitive in some jurisdictions, because it means treating individuals differently by "
              "group membership — which is a decision that needs explicit legal sign-off, not an "
              "engineering default.</p>",
              "<p>Whichever route is taken, re-run the full evaluation afterwards. Mitigation that "
              "improves one metric frequently degrades another, and the only way to know the net effect "
              "is to measure all of them again and record the trade-off that was accepted.</p>"]),
        ],
    },
    "zh-CN": {
        "rename": {
            "为什么偏见审计比以往更重要": "为什么偏见审计比以往更重要？",
            "全面偏见审计的四个维度": "全面偏见审计包含哪四个维度？",
            "将自动化偏见检测构建到管道中": "如何将自动化偏见检测构建到流水线中？",
                    },
    },
}

# -------------------------------------------------------------------------- 11
SPECS["enterprise-architecture-ai-era"] = {
    "EN": {
        "rename": {
            "understanding-the-current-landscape":
                "What Is Changing in Enterprise Architecture for AI?",
            "key-principles-and-strategic-framework":
                "What Principles Should Guide AI-Era Architecture?",
            "implementation-approach-and-best-practices":
                "How Should You Implement an AI-Era Architecture?",
            "measuring-success-and-demonstrating-roi":
                "How Do You Measure Architectural ROI?",
            "common-pitfalls-and-how-to-avoid-them":
                "What Are the Most Common Architectural Pitfalls?",
            "the-semantic-layer-as-the-new-operating-core":
                "Why Is the Semantic Layer the New Operating Core?",
            "key-takeaways": "What Are the Key Takeaways?",
            "conclusion": "Where Should You Start?",
        },
        "new": [
            ("where-should-the-agent-boundary-sit",
             "Where Should the Agent Boundary Sit?",
             ["<p>The architectural question that now generates the most debate is where to place the "
              "boundary between the model and the enterprise. Three patterns are in use, and they have "
              "very different consequences for governance, cost, and lock-in.</p>",
              "<p>The first, embedding model calls directly in applications, is the fastest to build and "
              "the hardest to govern. Each team makes its own choices about prompts, retrieval, and "
              "access, so there is no single place to enforce policy or to audit behaviour. It is fine "
              "for a proof of concept and expensive at scale, because every team re-solves the same "
              "problems and every audit requires visiting every application.</p>",
              "<p>The second, a central gateway that all model traffic passes through, gives you one "
              "enforcement point for authentication, rate limiting, logging, and content policy. It is a "
              "large improvement and a common intermediate step. Its limitation is that the gateway sees "
              "prompts and responses but not the tools behind them, so it can control what is said but "
              "not what is done.</p>",
              "<p>The third, a tool boundary built on a standard protocol such as MCP, places the "
              "boundary at the action layer. Every capability the model can exercise is declared as a "
              "tool with typed inputs, an authorisation policy, and an audit record. This is the pattern "
              "that scales, because governance attaches to capability rather than to application, and "
              "because the same tool set can serve a chat assistant, an agent, and a scheduled job "
              "without each consumer implementing its own access logic.</p>",
              "<p>The recommendation is to adopt the third as the target and the second as the "
              "interim control, and to be explicit that the first is technical debt with a due date.</p>"]),
            ("how-do-you-avoid-rebuilding-the-semantic-layer-twice",
             "How Do You Avoid Rebuilding the Semantic Layer Twice?",
             ["<p>Semantic layer projects fail in a particular way: the first version is built as "
              "BI metadata — a set of field labels and joins for a reporting tool — and then has to be "
              "rebuilt when AI consumers arrive, because the metadata that supports a chart is not the "
              "metadata that supports a question.</p>",
              "<p>A chart needs a label, a format, and a join path. A question needs all of that plus the "
              "things that determine whether the answer is correct: the grain of the metric and whether "
              "it is additive, which dimensions it may legally be sliced by, what the default time "
              "aggregation is, how to handle nulls and late-arriving data, and what to do when the "
              "question is ambiguous. Most first-generation semantic layers do not carry that "
              "information, which is why a model querying them produces confident nonsense.</p>",
              "<p>The way to avoid the rebuild is to design for questions from the start, even if the "
              "first consumer is a dashboard. Concretely: declare grain explicitly for every metric; "
              "record additivity; attach default and permitted aggregations; and write a plain-language "
              "business definition for each term, because that definition is what the model will be "
              "matching against. Treat synonyms as first-class, since users say &quot;revenue&quot;, "
              "&quot;sales&quot;, and &quot;turnover&quot; interchangeably.</p>",
              "<p>Then version it and test it. Metric definitions change, and a change that fixes one "
              "dashboard can break twenty questions. Keeping definitions in version control with a "
              "regression suite of representative questions is what lets the semantic layer evolve "
              "without becoming the thing everyone is afraid to touch.</p>"]),
            ("what-should-you-centralise-and-what-should-you-federate",
             "What Should You Centralise and What Should You Federate?",
             ["<p>Enterprises tend to oscillate between two failure modes: a central data team that "
              "becomes a bottleneck because every request routes through it, and full federation that "
              "produces forty incompatible definitions of revenue. The answer is not a compromise between "
              "them but a deliberate split along a specific line.</p>",
              "<p>Centralise the things that are expensive to duplicate and require consistency: identity "
              "and access management, the catalogue and lineage service, the semantic layer's core "
              "entity and metric definitions, the enforcement point for policy, and the audit store. "
              "These are platforms. Each additional implementation makes the estate worse rather than "
              "better, and none of them benefit from local variation.</p>",
              "<p>Federate the things that require domain knowledge: metric definition within a domain, "
              "data quality rules for domain datasets, and the selection of use cases. A finance team "
              "should own what &quot;recognised revenue&quot; means, subject to a central standard for "
              "how a metric is declared, tested, and published. This is the domain-ownership principle "
              "applied to meaning rather than to storage.</p>",
              "<p>The mechanism that makes the split work is a contract rather than a committee: a "
              "published interface that says how a domain contributes metric definitions, what tests they "
              "must pass, and what the platform guarantees in return. Where that contract exists, "
              "federation scales. Where it does not, federation becomes fragmentation and the "
              "organisation eventually re-centralises — usually at considerable cost and considerable "
              "loss of trust from the teams who were told to own their data.</p>"]),
        ],
    },
    "zh-CN": {
        "rename": {
            "理解当前格局": "面向 AI 的企业架构正在发生什么变化？",
            "关键原则与战略框架": "AI 时代的架构应遵循哪些原则？",
            "实施方法与最佳实践": "应如何实施 AI 时代的架构？",
            "衡量成功与展示投资回报率": "如何衡量架构的投资回报？",
            "常见陷阱及规避方法": "最常见的架构陷阱有哪些？",
            "关键要点": "关键要点是什么？",
            "结论": "应从哪里开始？",
        },
        "new": [
            ("智能体边界应设在哪里",
             "智能体边界应设在哪里？",
             ["<p>当前争议最大的架构问题，是模型与企业之间的边界应设在哪里。实践中存在三种模式，它们在治理、成本与锁定上的后果截然不同。</p>",
              "<p>其一是把模型调用直接嵌入应用。构建最快，治理最难。每个团队自行决定提示词、检索与访问方式，因此没有统一位置来执行策略或审计行为。做概念验证尚可，规模化时代价高昂：每个团队重复解决同样的问题，每次审计都要走访每个应用。</p>",
              "<p>其二是所有模型流量经过的中央网关。它提供了认证、限流、日志与内容策略的单一执行点，是很大的改进，也是常见的中间步骤。局限在于网关只看得到提示与响应，看不到其后的工具，因此能管住&quot;说什么&quot;，却管不住&quot;做什么&quot;。</p>",
              "<p>其三是基于 MCP 等标准协议构建的工具边界，把边界设在行动层。模型可调用的每种能力都声明为带有类型化输入、授权策略与审计记录的工具。这一模式最能扩展，因为治理依附于能力而非应用，同一套工具集可服务于对话助手、智能体与定时任务，而无需每个消费方各自实现访问逻辑。</p>",
              "<p>建议以第三种为目标、第二种为过渡控制，并明确第一种是带到期日的技术债。</p>"]),
            ("如何避免语义层被重建两次",
             "如何避免语义层被重建两次？",
             ["<p>语义层项目有一种特定的失败方式：第一版按 BI 元数据来建——为报表工具准备的一组字段标签与关联关系——等到 AI 消费方出现时不得不重建，因为支撑图表的元数据并不是支撑提问的元数据。</p>",
              "<p>图表需要标签、格式与关联路径。提问需要这些，以及决定答案是否正确的那些信息：指标的粒度及其是否可加、允许按哪些维度切分、默认时间聚合是什么、空值与迟到数据如何处理、以及问题有歧义时该怎么办。多数第一代语义层不承载这些信息，这正是模型查询它们会产出自信废话的原因。</p>",
              "<p>避免重建的方法是从一开始就为提问而设计，即便第一个消费方是看板。具体做法：为每个指标显式声明粒度；记录可加性；附上默认与允许的聚合方式；并为每个术语撰写平实的业务定义，因为模型匹配的就是这个定义。把同义词当作一等公民，因为用户会混用&quot;营收""销售""营业额&quot;。</p>",
              "<p>然后做版本管理与测试。指标定义会变，一个修复了某张看板的变更可能破坏二十个问题。把定义纳入版本控制，并配备一组代表性问题的回归集，这正是语义层得以演进、而不至于变成人人不敢碰的东西的原因。</p>"]),
            ("哪些能力应集中哪些应联邦",
             "哪些能力应集中、哪些应联邦？",
             ["<p>企业往往在两种失败模式之间摆动：中央数据团队因所有请求都要经过它而成为瓶颈；或完全联邦，产出四十种互不兼容的收入定义。答案不是折中，而是沿一条明确的界线做有意的切分。</p>",
              "<p>集中那些重复成本高、且要求一致性的能力：身份与访问管理、目录与血缘服务、语义层中的核心实体与指标定义、策略执行点，以及审计库。这些是平台。每多一套实现只会让整体更糟，且它们都不从本地差异中获益。</p>",
              "<p>联邦那些需要领域知识的能力：领域内的指标定义、领域数据集的数据质量规则，以及用例选择。财务团队应当拥有&quot;已确认收入&quot;的定义权，但须服从中心关于指标如何声明、测试与发布的标准。这是把领域所有权原则应用于&quot;语义&quot;而非&quot;存储&quot;。</p>",
              "<p>使切分生效的机制是契约而非委员会：一份发布出来的接口，约定领域如何贡献指标定义、必须通过哪些测试，以及平台在回报上保证什么。有契约，联邦才能扩展；没有契约，联邦就退化为碎片化，组织最终会重新集中化——通常代价高昂，并显著损耗那些曾被要求&quot;拥有自己数据&quot;的团队的信任。</p>"]),
        ],
    },
}
