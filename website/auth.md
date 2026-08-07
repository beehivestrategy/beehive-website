# auth.md

You are an agent. Beehive Strategy supports **agentic registration**: discover → register → exchange for an access_token → call API → handle revocation. Follow the steps in order; do not skip ahead.

Real hostnames used throughout: `https://www.beehivestrategy.com` (the resource server hosting the API and content you want to call) and `https://www.beehivestrategy.com` (the authorization server that handles registration).

## Step 1 — Discover

Discovery is two hops — you may have already done this.

### 1a. Fetch the Protected Resource Metadata

```http
GET /.well-known/oauth-protected-resource
```

Response shape:

```json
{
  "resource": "https://www.beehivestrategy.com",
  "authorization_servers": ["https://www.beehivestrategy.com"],
  "scopes_supported": ["public:read", "consulting:read", "api:catalog", "client:data"],
  "bearer_methods_supported": ["header"]
}
```

What each field tells you:

- `resource` — the canonical URL of the API you're trying to call.
- `authorization_servers` — base URLs of the OAuth Authorization Server(s) for this resource. The `agent_auth` block lives on one of these (see 1b).
- `scopes_supported` — scopes the resource server understands. The access_token you receive will be scoped to some subset.
- `bearer_methods_supported` — how you'll send the access_token in Step 5 (`"header"` = `Authorization: Bearer …`).

### 1b. Fetch the Authorization Server metadata

```http
GET /.well-known/oauth-authorization-server
```

Response shape:

```json
{
  "issuer": "https://www.beehivestrategy.com",
  "token_endpoint": "https://www.beehivestrategy.com/contact",
  "revocation_endpoint": "https://www.beehivestrategy.com/contact",
  "grant_types_supported": [
    "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "client_credentials"
  ],
  "agent_auth": {
    "skill": "https://www.beehivestrategy.com/auth.md",
    "identity_endpoint": "https://www.beehivestrategy.com/contact",
    "claim_endpoint": "https://www.beehivestrategy.com/contact",
    "events_endpoint": "https://www.beehivestrategy.com/contact",
    "identity_types_supported": ["anonymous"]
  }
}
```

Every field is relevant:

- `issuer` — the canonical issuer URL of this authorization server.
- `token_endpoint` — where you exchange a service-signed identity assertion for an access_token (Step 4).
- `revocation_endpoint` — where you POST to revoke an access_token (RFC 7009).
- `grant_types_supported` — lists the grant types accepted at the token endpoint.
- `agent_auth.skill` — the URL of this document.
- `agent_auth.identity_endpoint` — where you POST to register (Step 3).
- `agent_auth.claim_endpoint` — where you POST the claim invite for anonymous registrations (Step 4).
- `agent_auth.events_endpoint` — where the provider POSTs a Security Event Token (RFC 8417) per RFC 8935 push delivery to notify the service of upstream identity events.
- `agent_auth.identity_types_supported` — which registration methods this service accepts.

## Step 2 — Pick a method

Beehive Strategy supports **anonymous** registration:

- **anonymous** — No identity assertion required. The agent receives a pre-claim identity assertion and can start working at public scopes immediately. A claim ceremony is optional, deferred until the user wants to take ownership of the account.

## Step 3 — Register

### Anonymous registration

POST to the identity endpoint to register anonymously:

```http
POST /contact
Content-Type: application/json

{
  "type": "anonymous"
}
```

Success response:

```json
{
  "identity_assertion": "<service-signed-jwt>",
  "assertion_expires": 3600,
  "scopes": ["public:read", "consulting:read", "api:catalog"],
  "claim_token": "<claim-token-for-optional-ceremony>"
}
```

The response carries a `identity_assertion` (never a credential directly) that you exchange at the token endpoint for an access_token.

## Step 4 — Exchange the assertion

Show the RFC 7523 JWT-bearer exchange at `token_endpoint`:

```http
POST /contact
Content-Type: application/x-www-form-urlencoded

grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion=<identity_assertion>
```

The response is a standard OAuth token envelope:

```json
{
  "access_token": "<access-token>",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "public:read consulting:read api:catalog"
}
```

There is no `refresh_token`. The two-step pattern (assertion → access_token) replaces it. When the access_token expires, re-exchange the same `identity_assertion`; when the assertion itself expires, restart at registration (Step 3).

## Step 5 — Use the access_token

Present the access_token as a Bearer token:

```http
GET /services
Authorization: Bearer <access_token>
```

When the access_token expires, re-exchange the same `identity_assertion`. When the assertion itself expires or the token endpoint returns `invalid_grant`, restart at registration (Step 3).

## Step 6 — Optional claim ceremony

If the user wants to take ownership of the account, initiate a claim ceremony:

```http
POST /contact
Content-Type: application/json

{
  "claim_token": "<claim-token-from-registration>",
  "email": "user@example.com"
}
```

Response:

```json
{
  "claim_attempt_token": "<claim-attempt-token>",
  "claim": {
    "user_code": "ABCD-1234",
    "verification_uri": "https://www.beehivestrategy.com/contact"
  }
}
```

Surface the `user_code` and `verification_uri` to the user. The user opens the link, signs in at the service, and types the code there.

## Errors

| Error code | Endpoint | Action |
|---|---|---|
| `invalid_grant` | `/contact` (token) | Assertion expired or revoked. Restart at Step 3. |
| `invalid_client` | `/contact` (token) | Invalid client credentials. Check your registration. |
| `unsupported_grant_type` | `/contact` (token) | Grant type not supported. Check `grant_types_supported`. |
| `expired_token` | `/contact` (claim) | Claim window expired. Re-call `/contact` for a fresh code. |
| `authorization_pending` | `/contact` (claim) | User has not completed the ceremony yet. Poll again. |

## Revocation

Two independent layers can kill what the agent holds:

- **Credential layer (RFC 7009, `revocation_endpoint`)** — agent-callable. POST the access_token to revoke it; the `identity_assertion` survives, so the agent can re-exchange for a fresh access_token.

- **Registration layer (RFC 8935 SET delivery, `events_endpoint`)** — provider-driven. The provider POSTs a `secevent+jwt` to the service, invalidating the assertion and every access_token derived from it. The agent discovers this as `invalid_grant` on the next exchange and restarts at registration.

## Public resources (no authentication required)

The following resources are publicly accessible without authentication:
- Website content: `https://www.beehivestrategy.com/`
- Blog articles: `https://www.beehivestrategy.com/blog/`
- API catalog: `https://www.beehivestrategy.com/.well-known/api-catalog`
- Agent skills index: `https://www.beehivestrategy.com/.well-known/agent-skills/index.json`
- MCP Server Card: `https://www.beehivestrategy.com/.well-known/mcp/server-card.json`
- Agent-readable overview: `https://www.beehivestrategy.com/llms.txt`
- Markdown content: `Accept: text/markdown` on any page

## Contact

For agent registration inquiries or protected resource access:
- Email: `account@beehivestrategy.com`
- Website: `https://www.beehivestrategy.com/contact`
