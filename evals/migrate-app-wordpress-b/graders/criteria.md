---
type: llm
weight: 2
---

Score 1 only if ALL hold:

4. Says the classic uploader (`/wp-admin/async-upload.php`) gets `403` from CRS rule `932180` for file names containing `class`, and gives the scoped fix: `ctl:ruleRemoveTargetById=932180;FILES:async-upload` limited to that path, in a `modsec` custom config. It does not remove rule `932180` or `949110` for the whole site.
5. Says a raw upload with `Content-Type: image/jpeg` gets `403` from CRS rule `920420`, and gives a fix scoped to `POST /wp-json/wp/v2/media` (`ctl:ruleRemoveTargetById=920420;REQUEST_HEADERS:Content-Type` in a `modsec-crs` config), or tells the app to send multipart or `application/octet-stream`. It does not turn off rule `920420` or `949110` for the whole site.
6. Carries the source's `client_max_body_size 64m` over as `MAX_CLIENT_SIZE=64m`, or sets another value of at least `30m` and says why: the default `10m` refuses the editors' 30 MB videos with `413`. Leaving `MAX_CLIENT_SIZE` at its default fails.
