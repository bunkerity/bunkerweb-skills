---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Migrate this Express.js route handler from callbacks to async/await: app.get('/u/:id', (req, res) => { db.find(req.params.id, (err, u) => { if (err) return res.status(500).end(); res.json(u); }); });
