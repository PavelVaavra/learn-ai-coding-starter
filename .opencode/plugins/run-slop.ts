import { Plugin } from "@opencode/plugin";
import { spawn } from "node:child_process";
import { isAbsolute, resolve } from "node:path";

interface RunSlopInput {
  path: string;
}

interface RunSlopResult {
  stdout: string;
  stderr: string;
  exitCode: number;
}

function runSloperator(cwd: string, file: string): Promise<RunSlopResult> {
  return new Promise((settle) => {
    const child = spawn("uv", ["run", "--no-active", "sloperator.py", file], {
      cwd,
      env: process.env,
      stdio: ["ignore", "pipe", "pipe"],
    });

    let stdout = "";
    let stderr = "";

    child.stdout.setEncoding("utf8");
    child.stderr.setEncoding("utf8");
    child.stdout.on("data", (chunk: string) => {
      stdout += chunk;
    });
    child.stderr.on("data", (chunk: string) => {
      stderr += chunk;
    });

    child.on("error", (error) => {
      settle({ stdout, stderr: stderr + error.message, exitCode: -1 });
    });

    child.on("close", (code) => {
      settle({ stdout, stderr, exitCode: code ?? -1 });
    });
  });
}

export default Plugin.define({
  id: "sloperator.run-slop",
  setup: async (ctx) => {
    const projectDirectory = ctx.location.directory;

    await ctx.tool.transform((tools) => {
      tools.add({
        name: "run_slop",
        description:
          "Run a SlopLang (.slop) program with the Sloperator interpreter and return its stdout, stderr, and exit code as JSON.",
        input: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description:
                "Path to the .slop file, relative to the project root (or absolute).",
            },
          },
          required: ["path"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async (input) => {
          const { path } = input as RunSlopInput;
          const file = isAbsolute(path) ? path : resolve(projectDirectory, path);
          const result = await runSloperator(projectDirectory, file);
          return { content: JSON.stringify(result, null, 2) };
        },
      });
    });
  },
});
