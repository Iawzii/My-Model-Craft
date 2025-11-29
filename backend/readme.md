## User settings navigation

- `PATCH /api/settings/user/avatar` — 更新头像
- `PATCH /api/settings/user/bio` — 更新简介
- `PATCH /api/settings/user/username` — 更新用户名（校验唯一性）
- `PATCH /api/settings/user/email` — 更新邮箱（校验唯一性）
- `POST /api/settings/user/password` — 修改密码（提供 `currentPassword` 与 `newPassword`）

## Password reset flow

- `POST /api/auth/forgot` — supply a registered email to receive a one-time code.
- `POST /api/auth/reset` — submit `email`, `code`, and `newPassword` to complete the reset.

All endpoints return `401` when the token is invalid (where applicable) and `4xx` errors when validation fails.
