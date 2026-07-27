#!/usr/bin/env python3
"""Generate batch-what-is.json with all 20 'What Is' articles."""
import json

WORK = "/Users/kennethkwok/.trae-cn/work/6a5bc5758319ac256488b1d8"
OUT = WORK + "/batch-what-is.json"

articles = []

def make_art(slug, date, section, tags, rt, titles, descs, kw, bodies, tldr, faqs):
    articles.append({
        "date": date, "slug": slug, "section": section,
        "tags": tags, "readingTime": rt,
        "title": titles, "description": descs, "keywords": kw,
        "body": bodies, "tldr": tldr, "faq": faqs
    })

# ============ 1. MCP ============
make_art("what-is-mcp-model-context-protocol","2026-07-25","Technology",["MCP","Model Context Protocol","AI Integration","Anthropic","Enterprise AI","API Standards"],12,
{"en":"What Is MCP (Model Context Protocol)? A Complete Guide","zhCN":"什么是MCP（模型上下文协议）？完整指南","zhTW":"什麼是MCP（模型上下文協議）？完整指南"},
{"en":"MCP is an open standard enabling AI models to securely connect with external data sources and tools.","zhCN":"MCP是一种开放标准，使AI模型能够安全地连接外部数据源和工具。","zhTW":"MCP是一種開放標準，使AI模型能夠安全地連接外部資料源和工具。"},
{"en":"MCP, Model Context Protocol, what is MCP, Anthropic MCP, MCP architecture, enterprise AI integration","zhCN":"MCP, 模型上下文协议, 什么是MCP, MCP架构, 企业AI集成","zhTW":"MCP, 模型上下文協議, 什麼是MCP, MCP架構, 企業AI整合"},
{"en":'<h2>What Is MCP (Model Context Protocol)?</h2><p><strong>MCP (Model Context Protocol)</strong> is an open-source standard developed by Anthropic that provides a universal way for AI models to connect with external data sources, tools, and services. Think of it as the USB-C plug for AI — a single, standardised interface that lets any AI model communicate with any application without building custom integrations.</p><p>MCP solves one of the biggest challenges in enterprise AI deployment: <strong>how do you give AI models access to the right data, at the right time, without compromising security?</strong> Before MCP, every AI integration required a bespoke connector.</p><h2>How Does MCP Work?</h2><p>MCP operates on a client-server architecture with three key participants:</p><ul><li><strong>MCP Hosts</strong> — Applications that initiate connections to AI models.</li><li><strong>MCP Clients</strong> — Lightweight components maintaining one-to-one conversations with MCP servers.</li><li><strong>MCP Servers</strong> — Programs exposing data access, tool execution, or workflow automation.</li></ul><p>The protocol defines three core primitives:</p><ol><li><strong>Resources</strong> — Structured data the AI can read.</li><li><strong>Tools</strong> — Functions the AI can invoke to perform actions.</li><li><strong>Prompts</strong> — Reusable templates that standardise interactions.</li></ol><h2>Key Components</h2><ul><li><strong>JSON-RPC messaging</strong> — All communication uses JSON-RPC 2.0.</li><li><strong>Transport layer</strong> — Supports stdio and SSE for remote connections.</li><li><strong>Security model</strong> — Servers run with explicit permissions, connections are sandboxed.</li></ul><h2>Why Enterprises Need MCP</h2><ul><li><strong>Reduced integration cost.</strong> Build once, reuse everywhere.</li><li><strong>Data governance.</strong> Servers act as controlled gateways with access policies and audit logging.</li><li><strong>Vendor independence.</strong> Open standard means no lock-in.</li><li><strong>Scalability.</strong> New sources only need new MCP servers.</li></ul><h2>MCP Use Cases</h2><ul><li><strong>Data analytics:</strong> MCP servers connected to warehouses let AI answer ad hoc questions.</li><li><strong>DevOps:</strong> CI/CD MCP servers enable AI to monitor builds and trigger deployments.</li><li><strong>Customer support:</strong> Knowledge base MCP servers give AI agents full context.</li><li><strong>Financial analysis:</strong> MCP servers wrapping ERP systems enable AI to pull reports on demand.</li></ul><h2>How Beehive Strategy Leverages MCP</h2><p>At Beehive Strategy, MCP is foundational to our conversational BI platform. We build MCP servers connecting AI models directly to enterprise data warehouses, semantic layers, and business metadata. Clients ask complex questions in natural language and receive accurate, governed answers powered by MCP standardised connector architecture.</p>',
"zhCN":'<h2>什么是MCP（模型上下文协议）？</h2><p><strong>MCP（Model Context Protocol）</strong>是由Anthropic开发的开放标准，为AI模型提供了一种通用的方式来连接外部数据源、工具和服务。可以把它理解为AI领域的USB-C接口——一个标准化接口，让任何AI模型都能与任何应用通信。</p><p>MCP解决了企业AI部署中最大的挑战：<strong>如何让AI模型在正确的时间获取正确的数据，同时不损害安全性？</strong></p><h2>MCP如何工作？</h2><p>MCP采用客户端-服务器架构，有三个关键参与者：主机、客户端和服务器。协议定义三个核心原语：资源、工具和提示模板。</p><h2>企业为什么需要MCP</h2><ul><li><strong>降低集成成本。</strong>构建一次即可复用。</li><li><strong>数据治理。</strong>服务器充当受控网关。</li><li><strong>供应商独立性。</strong>开放标准，不被锁定。</li><li><strong>可扩展性。</strong>新数据源只需添加新服务器。</li></ul><h2>Beehive Strategy如何利用MCP</h2><p>在Beehive Strategy，MCP是对话式BI平台的基础。我们构建MCP服务器，将AI模型直接连接到企业数据仓库、语义层和业务元数据。</p>',
"zhTW":'<h2>什麼是MCP（模型上下文協議）？</h2><p><strong>MCP（Model Context Protocol）</strong>是由Anthropic開發的開放標準，為AI模型提供了一種通用方式來連接外部資料源、工具和服務。可以把它理解為AI領域的USB-C接口。</p><p>MCP解決了企業AI部署中最大的挑戰：<strong>如何讓AI模型在正確的時間獲取正確的資料，同時不損害安全性？</strong></p><h2>MCP如何運作？</h2><p>MCP採用客戶端-伺服器架構，有三個關鍵參與者：主機、客戶端和伺服器。協議定義三個核心原語：資源、工具和提示模板。</p><h2>企業為什麼需要MCP</h2><ul><li><strong>降低整合成本。</strong>構建一次即可複用。</li><li><strong>資料治理。</strong>伺服器充當受控閘道。</li><li><strong>供應商獨立性。</strong>開放標準，不被鎖定。</li></ul><h2>Beehive Strategy如何利用MCP</h2><p>在Beehive Strategy，MCP是對話式BI平台的基礎。我們構建MCP伺服器，將AI模型直接連接到企業資料倉儲和語義層。</p>'},
{"en":"MCP is an open standard giving AI models a universal way to connect with data sources and tools.","zhCN":"MCP是Anthropic开发的开放标准，为AI模型提供连接数据源和工具的通用方式。","zhTW":"MCP是Anthropic開發的開放標準，為AI模型提供連接資料源和工具的通用方式。"},
[{"q":{"en":"Is MCP only compatible with Claude?","zhCN":"MCP只兼容Claude吗？","zhTW":"MCP只相容Claude嗎？"},"a":{"en":"No. MCP is an open standard any AI provider can implement.","zhCN":"不是。MCP是开放标准，任何AI提供商都可以实现。","zhTW":"不是。MCP是開放標準，任何AI提供者都可以實現。"}},{"q":{"en":"What is the difference between MCP resources, tools, and prompts?","zhCN":"MCP资源、工具和提示模板有什么区别？","zhTW":"MCP資源、工具和提示模板有什麼區別？"},"a":{"en":"Resources are read-only data. Tools are callable functions. Prompts are reusable templates.","zhCN":"资源是只读数据。工具是可调用函数。提示模板是可重用模板。","zhTW":"資源是唯讀資料。工具是可呼叫函數。提示模板是可重複使用模板。"}},{"q":{"en":"How secure is MCP for enterprise data?","zhCN":"MCP对企业数据安全吗？","zhTW":"MCP對企業資料安全嗎？"},"a":{"en":"MCP is designed with security at its core. Servers run with explicit permissions and sandboxed connections.","zhCN":"MCP将安全性放在首位。服务器在明确权限下运行，连接沙箱隔离。","zhTW":"MCP將安全性放在首位。伺服器在明確權限下運行，連接沙箱隔離。"}}])

# Load remaining 19 articles from parts module
import sys
sys.path.insert(0, WORK)
from what_is_parts import get_articles
articles.extend(get_articles())

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)
print(f"Written {len(articles)} articles to batch-what-is.json")
