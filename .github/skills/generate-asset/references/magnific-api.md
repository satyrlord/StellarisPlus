# Magnific API Reference

## Purpose & Scope

Reference notes for the Magnific HTTP API used by this workspace.

---

## Authentication

All requests require the legacy `x-freepik-api-key` header.

- `MAGNIFIC_API_KEY` is preferred in `.env.local` (git-ignored)
- `FREEPIK_API_KEY` is still accepted for backward compatibility
- Load into the shell before running generation commands:

```powershell
$env:MAGNIFIC_API_KEY = (Get-Content .env.local | Where-Object { $_ -match '^MAGNIFIC_API_KEY=' }) -replace '^MAGNIFIC_API_KEY=', ''
if (-not $env:MAGNIFIC_API_KEY) {
    $env:MAGNIFIC_API_KEY = (Get-Content .env.local | Where-Object { $_ -match '^FREEPIK_API_KEY=' }) -replace '^FREEPIK_API_KEY=', ''
}
```

---

## Base URL

```HTTP
https://api.freepik.com
```

---

## Async Processing Pattern

Most AI endpoints use async processing:

1. POST request returns `task_id` and `status: CREATED`
2. Poll GET `/{task-id}` until `status` is `COMPLETED` or `FAILED`
3. Or use `webhook_url` parameter for automatic notification

---

## Key Endpoints for Image Generation

Only endpoints that support uploading a reference image are listed here.

| Endpoint | Method | Notes | Reference image |
| -------- | ------ | ----- | --------------- |
| `/v1/ai/text-to-image/flux-kontext-pro` | POST | Context-aware, guided generation | `input_image` (base64, 1 image) |

## Utility Endpoints

| Endpoint | Method | Notes |
| -------- | ------ | ----- |
| `/v1/ai/beta/remove-background` | POST | Background removal (beta, synchronous, requires public `image_url`) |
| `/v1/ai/image-upscaler` | POST | Upscale with Magnific |

---

## NSFW Filtering Parameters

Different endpoints use different parameter names:

| Endpoint | Parameter | Disable value |
| -------- | --------- | ------------- |
| Flux Kontext Pro | `enable_safety_checker` | `false` |

---

## Pricing

Costs per operation, sorted cheapest to most expensive.

Last updated: 2026-03-28

### Reference-Image-Capable Models

| Model | Cost/image | Images per 5 EUR |
| ----- | ---------: | ---------------: |
| Flux 2 Pro | 0.03 EUR | 166 |
| Flux Kontext Pro | 0.034 EUR | 147 |
