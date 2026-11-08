# Runtime credentials

Before the next deployment, copy the existing working API_ID and API_HASH into the private `.env` file already used by Compose. Keep BOT_TOKEN there too. Do not change their values merely to change storage. Restrict `.env` and `cookies.txt` to the server owner (0600).

`cookies.txt` remains a server-side bind mount at `/app/cookies.txt`. It is intentionally excluded from Git and image builds. Removing it from Git does not remove the existing server file. A fresh installation must supply its own cookie file before starting Compose.

Cookies and API credentials previously committed remain in repository history. Replace the exposed Instagram session with fresh cookies in a controlled maintenance step; deleting the tracked file alone does not invalidate leaked sessions. Never revoke the working session before replacement cookies are available.

Do not rebuild/recreate the running container solely to apply the Git cleanup. Older image layers may still contain old credentials; retire those images after a separately verified clean rebuild.
