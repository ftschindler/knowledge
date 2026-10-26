---
type: Guide
title: Add Scaleway as an opencode provider
description: Enabling Scaleway's Generative APIs in opencode with one API key, and pinning every
  oh-my-openagent agent and category slot, from a model catalogue verified with real inference
  calls.
tags:
- guide
- opencode
- scaleway
- oh-my-openagent
- config-management
status: stable
stale_after: '2027-04-26'
generated:
  by: opencode/glm-5.3
  at: '2026-10-26T22:57:02+01:00'
sources:
- id: scw-opencode
  resource: https://www.scaleway.com/en/docs/generative-apis/reference-content/integrate-with-opencode/
  title: Integrating Generative APIs with OpenCode - Scaleway Documentation
  last_modified: '2026-10-26'
- id: scw-api
  resource: https://www.scaleway.com/en/docs/generative-apis/api-cli/using-generative-apis/
  title: Using Generative APIs - Scaleway Documentation
  last_modified: '2026-10-26'
- id: scw-pricing
  resource: https://www.scaleway.com/en/pricing/model-as-a-service/
  title: Model-as-a-Service pricing - Scaleway
  last_modified: '2026-10-26'
- id: scw-models
  resource: https://www.scaleway.com/en/docs/generative-apis/reference-content/supported-models/
  title: Generative APIs supported models - Scaleway Documentation
  last_modified: '2026-10-26'
- id: omo-repo
  resource: https://github.com/code-yeongyu/oh-my-openagent
  title: 'code-yeongyu/oh-my-openagent'
  last_modified: '2026-10-26'
- id: felix-opencode-config
  resource: https://github.com/ftschindler/opencode
  title: 'ftschindler/opencode: an opencode configuration with one profile per provider'
  last_modified: '2026-10-26'
---

Scaleway serves language models over an OpenAI-compatible API at `https://api.scaleway.ai/v1`, and
opencode knows the provider natively: no custom provider definition, no base URL to paste, only an
API key[^scw-opencode]. Enabling it is therefore the short half of this guide. The long half is
what comes with it. oh-my-openagent, the plugin that supplies opencode's agents and its per-task
model routing, has no Scaleway entries in its routing table, so every agent and category it
defines needs an explicit pin to a model Scaleway actually serves.

The model facts below were measured on 2026-10-26 against opencode 1.18.32 and oh-my-openagent
5.1.48. The catalogue came from the models endpoint, each model's chat behaviour from a real
completion call, tool calling from a function-calling probe, and image handling from having each
model describe a picture. Prices and context windows come from Scaleway's pricing page on the same
day[^scw-pricing].

## 1. Get the API key

In the Scaleway console, generate an API key under IAM. The key's bearer is either a user or an IAM
application, and the console shows the secret exactly once, so it gets copied then. The secret is a
UUID.

The bearer needs one of the Generative APIs permission sets: `GenerativeApisModelAccess`, the least
that allows listing and calling models; `GenerativeApisFullAccess`; or the broad
`AllProductsFullAccess`[^scw-api]. `InferenceFullAccess` is the legacy name for the same product's
access and may still be attached to older policies.

## 2. Declare the provider in opencode

Scaleway documents an interactive sign-in that asks for the same key[^scw-opencode]. The
config-file route below is declarative, and it is the one to keep in version control:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "scaleway": {
      "options": {
        "apiKey": "{env:SCW_SECRET_KEY}"
      }
    }
  },
  "model": "scaleway/gpt-oss-120b"
}
```

The `provider` block with an API key is the whole declaration, because `scaleway` is in opencode's
provider registry[^scw-opencode]. `{env:SCW_SECRET_KEY}` reads the key from the environment.
`{file:.env}` reads it from a file next to the config, resolving relative to the directory the
config lives in, which keeps the credential out of the environment and lets it live beside the
config in version control while being ignored by it.

Requests go to `https://api.scaleway.ai/v1` and run on the account's default Project. To run them
on a specific Project, for instance to track its billing separately, set the option
`baseURL` to `https://api.scaleway.ai/{env:SCW_PROJECT_ID}/v1`[^scw-opencode].

## 3. Verify the credential with a real request

```bash
opencode run --model scaleway/gpt-oss-120b "Reply with exactly: OK"
```

The listing proves nothing. The catalogue and the inference endpoint authenticate separately, so a
rejected key can still list every model and then fail the first real request. A reply proves the
key. A `401` names a rejected key; a `403` names a key whose bearer is missing the permission set
from step 1.

## 4. Why every oh-my-openagent slot needs a pin

oh-my-openagent routes each of its agents and task categories through a built-in table that names,
for every slot, an ordered chain of models with the providers that serve them[^omo-repo]. The
table carries no Scaleway entries - confirmed by searching the 5.1.48 build's shipped routing
tables for the provider id - so on a Scaleway session no slot resolves at all.

An unresolved slot produces no error. It falls through to the session's default model, which is how
a cheap high-volume slot ends up quietly running on the most expensive model in the catalogue. The
failure has a documented shape: when a plugin upgrade renamed a routing category, the pins matching
the old key turned inert and the two new slots silently routed to a provider the configuration
existed to exclude, in
[A plugin upgrade renamed a routing category and silently breached provider isolation](../findings/20261001_a_plugin_upgrade_renamed_a_routing_category_and_breached_provider_isolation.md).

A complete set of pins is therefore structural for Scaleway, not a preference.

## 5. The catalogue, as measured

On 2026-10-26 the models endpoint returned seventeen models for this subscription. Scaleway's
supported-models page describes more than a subscription may serve, so the docs table is not a
promise of what a key can call[^scw-models]. Measure, then pin.

Thirteen of the seventeen are chat models. Every one of them answered a completion call and emitted
a correct `tool_calls` structure in a function-calling probe. The images column says `described`
where the model described a test image in its own words, `rejected` where the server refused one
outright, and `text-only` where the docs list no image input and no probe was run[^scw-models].

| model | € in / € out per 1M tokens | context | reasoning | images |
| --- | --- | --- | --- | --- |
| `gpt-oss-120b` | 0.15 / 0.60 | 128k | yes | text-only |
| `mistral-small-3.2-24b-instruct-2506` | 0.15 / 0.35 | 128k | no | described |
| `gemma-4-26b-a4b-it` | 0.25 / 0.50 | 256k | yes | described |
| `qwen3.6-35b-a3b` | 0.25 / 1.50 | 256k | yes | described |
| `deepseek-v4-flash-0731` | 0.40 / 0.80 | 256k | yes | text-only |
| `deepseek-v4.1-flash` | 0.60 / 1.80 | 256k | yes | described |
| `qwen3.5-397b-a17b` | 0.60 / 3.60 | 250k | yes | described |
| `qwen3.8-27b` | 0.60 / 3.30 | 256k | yes | described |
| `qwen3-235b-a22b-instruct-2507` | 0.75 / 2.25 | 250k | no | text-only |
| `llama-3.3-70b-instruct` | 0.90 / 0.90 | 128k | no | rejected |
| `mistral-medium-3.5-128b` | 1.50 / 7.50 | 256k | yes | described |
| `glm-5.2` | 1.80 / 5.50 | 256k | yes | text-only |
| `glm-5.3` | 1.80 / 5.50 | 256k | yes | text-only |

Prices, context windows and the reasoning flag are Scaleway's own values from the pricing
page[^scw-pricing]; the reasoning flag marks models that accept reasoning parameters.

The other four are not chat models and take no turn in an agent session. `bge-multilingual-gemma2`
and `qwen3-embedding-8b` answer the embeddings endpoint, returning 3584 and 4096 dimensions.
`whisper-large-v3` transcribes audio, priced per minute. `lightonocr-3-0.8b` reads text out of
images over its own endpoint; the chat endpoint rejects it.

## 6. Map the models to the slots

Slots differ on two axes: how hard the work is, and how often the slot fires. The volume leaders,
`explore` and `librarian` and the `quick` category, run many calls per session, so their price
dominates and reasoning depth is not required. The capability gates are harder: `multimodal-looker`
must genuinely read images or it fails at its job, and the top-reasoning slots want the strongest
model served, whatever it costs, because they fire rarely.

The mapping below is applied and running in
[Felix's opencode configuration](https://github.com/ftschindler/opencode)[^felix-opencode-config].
It is one settled answer, not the only one; the wants column is the part that transfers when the
catalogue moves.

| agent slot | wants | pinned to |
| --- | --- | --- |
| `sisyphus` | plans, delegates, drives to completion | `glm-5.3` |
| `prometheus` | strategic planning, interview-mode questioning | `glm-5.3` |
| `hephaestus` | autonomous deep work, sustained autonomy | `glm-5.3` |
| `oracle` | read-only consultation, pure reasoning | `glm-5.3` |
| `momus` | adversarial critique, pure reasoning | `glm-5.3` |
| `metis` | ambiguity detection, mid reasoning | `glm-5.3` |
| `atlas` | focused execution, no delegation | `qwen3.5-397b-a17b` |
| `sisyphus-junior` | focused execution, no delegation | `qwen3.5-397b-a17b` |
| `explore` | fired many at once; cost and speed dominate | `gpt-oss-120b` |
| `librarian` | fired many at once; cost and speed dominate | `gpt-oss-120b` |
| `multimodal-looker` | images and PDFs; a hard capability gate | `qwen3.8-27b` |

| category slot | wants | pinned to, in order |
| --- | --- | --- |
| `visual-engineering` | frontend and design; benefits from images | `qwen3.5-397b-a17b`, `qwen3.8-27b`, `mistral-small-3.2-24b-instruct-2506` |
| `deep-low` | autonomous execution, decisions settled from evidence | `qwen3.5-397b-a17b`, `qwen3.6-35b-a3b` |
| `deep-high` | deep work whose decision evidence cannot settle | `glm-5.3`, `qwen3.5-397b-a17b` |
| `quick` | trivial work, high volume | `mistral-small-3.2-24b-instruct-2506`, `gpt-oss-120b` |
| `ultrabrain` | hard logic and architecture | `glm-5.3`, `qwen3.5-397b-a17b` |
| `artistry` | unconventional, creative approaches | `glm-5.3`, `qwen3.5-397b-a17b` |
| `unspecified-low` | moderate work, low effort | `qwen3-235b-a22b-instruct-2507`, `mistral-small-3.2-24b-instruct-2506` |
| `unspecified-high` | broad work, high effort | `glm-5.3`, `qwen3.5-397b-a17b` |
| `writing` | prose quality | `qwen3.5-397b-a17b`, `mistral-medium-3.5-128b` |

**`glm-5.3` takes the pure-reasoning slots.** It is the strongest reasoner in the catalogue and,
at €1.80 in / €5.50 out, among the most expensive. That combination suits its slots: `oracle`,
`momus`, `metis` and `prometheus` are consulted occasionally rather than fired in parallel, so the
price rarely compounds, and none of them needs images.

**`qwen3.5-397b-a17b` takes vision with strong reasoning behind it.** It described a test image and
reasons, at €0.60 in, which is a third of glm-5.3's input price. It leads the slots that want both:
`visual-engineering`, `deep-low` and `writing`, plus the two execution agents that may be handed
either text or screenshots.

**`gpt-oss-120b` takes the highest-volume slots.** Among the models that accept reasoning
parameters it is the cheapest served, at €0.15 in / €0.60 out[^scw-pricing], and every chat model
on the page passed the tool-calling probe, so it can drive the explore and librarian agents that
fire many at once. `mistral-small-3.2-24b-instruct-2506` is cheaper per token still, at €0.15 /
€0.35, but takes no reasoning parameters; it leads `quick` and holds the tail of the low-effort
categories.

The rest of the chat models stay available but unpinned. `glm-5.2` is the previous generation at
glm-5.3's exact price. The two deepseek flashes are cheap reasoners, and `deepseek-v4.1-flash`
described a test image, making both candidates for the volume slots if a reader weights output
price over reasoning parameters. `gemma-4-26b-a4b-it` is a vision-capable 256k-context model at
€0.25 / €0.50, a reasonable alternative lead for `quick`. `llama-3.3-70b-instruct` is text-only,
takes no reasoning parameters, and is outpriced by everything above it in the table.

## 7. One model per agent, a list per category

The two containers differ in what they accept, and the difference is a startup trap. An agent
takes a single `model` string; a `models` array on an agent is rejected by opencode's schema at
startup. A category takes a `models` array, ordered as a fallback chain within the provider. The
plugin reads its model config from `~/.omo/omo.jsonc`, with the opencode harness in a
`"[opencode]"` block[^omo-repo]:

```jsonc
{
  "[opencode]": {
    "agents": {
      "explore": { "model": "scaleway/gpt-oss-120b" },
      "multimodal-looker": { "model": "scaleway/qwen3.8-27b" }
    },
    "categories": {
      "quick": { "models": ["scaleway/mistral-small-3.2-24b-instruct-2506", "scaleway/gpt-oss-120b"] }
    }
  }
}
```

## 8. Keeping it current

Model pins are literal strings, so a retired model becomes a runtime failure the day some agent
happens to be invoked, and a plugin update can retune the slot roster itself. After either, re-run
the plugin's doctor for conformance, list the models the endpoint serves that day, and repeat the
one-line inference check from step 3 against a pinned model.

The check that catches a silently unresolved slot is harder: it replays the plugin's routing
table against the live catalogue and reports each slot as pinned, resolved or falling through.
[Felix's configuration](https://github.com/ftschindler/opencode) carries such
scripts[^felix-opencode-config], and its own replay script broke against plugin builds from 5.1.45
onwards, which is the honest caveat for all of this tooling: a script that reads a routing table
rots with the table.

What this guide does not cover: dedicated, non-serverless deployments, and custom imported
models. Both exist on Generative APIs, neither follows the serverless catalogue this guide
measured, and both would need their own pass.
