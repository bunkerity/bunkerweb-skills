---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Write a Semgrep rule that flags string-concatenated SQL queries passed to cursor.execute() in Python.
