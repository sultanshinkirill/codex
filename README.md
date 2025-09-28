# Codex Script Generation Platform

Codex is a React + Supabase application for creating high quality, on-brand video advertisement scripts for Finnish marketers. The app guides users through client intake, evidence gathering, brand extraction, and structured script generation with OpenAI.

## Project Overview

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS with a custom design system, shadcn/ui (Radix UI bindings), React Router, TanStack Query, Supabase client.
- **Backend**: Supabase PostgreSQL with Row Level Security (RLS), Supabase Edge Functions (Deno runtime), OpenAI GPT integration for structured content generation.
- **Primary Goal**: Deliver reliable, duration-constrained advertisement scripts in Finnish with strict adherence to brand voice and compliance guidelines (no hype, no medical claims).

## Key Features

1. **Authentication & Authorization**
   - Supabase Auth (email/password) with automatic session handling and protected routes.
   - RLS-enforced data isolation per authenticated user.

2. **Client Management**
   - Create and edit client profiles capturing business context, website URL, briefs, requirements, and attachments (JSON payloads).
   - Attachments stored as JSON metadata for downstream processing.

3. **AI-Powered Script Generation**
   - Three-step pipeline: **Evidence → Brand Extract → Script JSON**.
   - Evidence scraping gathers HTML, meta descriptions, headings (h1–h3), lists, and sanitized text from the client website.
   - Brand Extract uses OpenAI to derive product facts, value propositions, tone, audience, and key claims.
   - Script JSON yields multiple script concepts, each with 5–7 frames and duration tracking.
   - Consistent OpenAI parameters: temperature `0.2`, seed `7`, JSON schema responses, and needs_clarification error handling.

4. **Script Editor**
   - Inline frame editing with duration highlighting when exceeding limits.
   - Shareable script links via `/share/[slug]` routes.
   - Real-time validation, localization (Finnish default, English optional), and tone presets (`dead-pan`, `friendly-dry`, `straight`).

5. **Form Parameters & Constraints**
   - Adjustable maximum duration in seconds.
   - Language selection (FI default, EN optional).
   - Tone presets persist through the generation pipeline.

## Database Schema

### clients
| Column        | Type   | Notes                                       |
| ------------- | ------ | ------------------------------------------- |
| id            | uuid   | Primary key                                  |
| user_id       | uuid   | FK → `auth.users`                            |
| name          | text   | Required                                     |
| website_url   | text   | Optional                                     |
| brief         | text   | Optional                                     |
| wants         | text   | Optional                                     |
| attachments   | jsonb  | Optional (structured metadata)               |
| created_at    | timestamptz | Auto-managed                            |
| updated_at    | timestamptz | Auto-managed                            |

### scripts
| Column        | Type   | Notes                                       |
| ------------- | ------ | ------------------------------------------- |
| id            | uuid   | Primary key                                  |
| client_id     | uuid   | FK → `clients.id`                            |
| title         | text   | Required                                     |
| platform      | text   | Optional                                     |
| tone          | text   | Optional                                     |
| duration_sec  | integer| Optional (max seconds constraint)            |
| hooks         | text[] | Optional                                     |
| ctas          | text[] | Optional                                     |
| body          | text   | Optional                                     |
| full_script   | jsonb  | Optional (structured frames)                 |
| created_at    | timestamptz | Auto-managed                            |
| updated_at    | timestamptz | Auto-managed                            |

## Supabase Edge Function: `generate-scripts`

Request payload:

```json
{
  "clientName": "string",
  "websiteUrl": "string",
  "brief": "string",
  "wants": "string",
  "maxDurationSec": 120,
  "tonePreset": "dead-pan",
  "language": "FI"
}
```

Behavior:
- Validates inputs and enforces duration/tone presets.
- Orchestrates evidence scraping, brand extraction, and script generation via OpenAI.
- Logs and bubbles up `needs_clarification` errors for manual follow-up.

## Environment & Configuration

- Supabase URL: `https://agpoiwassjrhceebxdgl.supabase.co`
- Required secrets: `OPENAI_API_KEY`, `SUPABASE_*` keys.
- CORS enabled for the React frontend.
- Follow existing TypeScript conventions, tailwind design tokens, and shadcn/ui component patterns.

## Development Guidelines

- Use Supabase client libraries for data access; avoid raw REST calls to Supabase endpoints.
- Maintain comprehensive error handling (try/catch with user-facing toasts).
- Enforce client-side validation for forms before invoking edge functions.
- Prioritize localization (Finnish first) and reliability over rapid feature delivery.

## Testing & Quality

- Validate edge function flows with logging in the Deno runtime.
- Respect RLS policies in Supabase when adding queries or schema changes.
- Ensure script outputs remain structured JSON with duration metadata and compliance-safe messaging.

