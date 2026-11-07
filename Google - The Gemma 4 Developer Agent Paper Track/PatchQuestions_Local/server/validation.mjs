import { z } from "./vendor/zod/index.js";
const text = z.string().max(15000),
  short = z.string().max(500),
  id = z.string().max(150);
const https = z
  .string()
  .url()
  .max(2000)
  .refine((x) => x.startsWith("https://"));
export const schema = z
  .object({
    tasks: z
      .array(
        z
          .object({
            id,
            title: short,
            detail: text,
            due: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
            hours: z.number().min(0).max(200),
            status: z.enum(["todo", "doing", "done", "blocked"]),
            priority: z.enum(["high", "medium", "low"]),
            depends: z.array(id).max(50),
            sourceIds: z.array(id).max(50),
          })
          .strict(),
      )
      .max(300),
    experiments: z
      .array(
        z
          .object({
            id,
            title: short,
            hypothesis: text,
            method: text,
            result: text,
            limitation: text,
            command: text,
            status: z.enum(["planned", "running", "complete", "blocked"]),
            metric: short,
            evidence: text,
            created: short,
          })
          .strict(),
      )
      .max(200),
    sourceState: z.record(
      z.object({ read: z.boolean(), saved: z.boolean(), notes: text }).strict(),
    ),
    customSources: z
      .array(
        z
          .object({
            id,
            type: short,
            title: short,
            authors: z.string().max(1500),
            year: z.number().int().min(1900).max(2200),
            category: short,
            priority: short,
            url: https,
            summary: text,
            action: text,
            caveat: text,
            tags: z.array(short).max(30),
            verifiedAt: short,
          })
          .strict(),
      )
      .max(200),
    messages: z
      .array(
        z
          .object({
            id,
            role: z.enum(["user", "assistant"]),
            text: z.string().max(50000),
            created: short,
            model: short.optional(),
            provider: short.optional(),
            usage: short.optional(),
          })
          .strict(),
      )
      .max(200),
    runs: z
      .array(
        z
          .object({
            id,
            name: short,
            created: short,
            rows: z.number().int().positive(),
            results: z.record(z.record(z.number().min(0).max(1))),
            families: z.array(short).max(100),
            fileId: id.optional(),
          })
          .strict(),
      )
      .max(100),
    notes: z
      .array(
        z
          .object({
            id,
            title: short,
            text: z.string().max(50000),
            created: short,
          })
          .strict(),
      )
      .max(200),
    gates: z.record(z.boolean()),
    manuscript: z.string().max(100000),
    settings: z
      .object({
        provider: z.enum([
          "openai",
          "gemini",
          "anthropic",
          "groq",
          "openrouter",
        ]),
        model: short,
        maxTokens: z.number().int().min(512).max(8000),
      })
      .strict(),
  })
  .strict();
