---
title: Set up Samsara MCP (instructions for AI agents)
canonical_url: https://chinmay-platform-samsara.github.io/samsara-mcp-agent-setup/setup.md
human_docs: https://developers.samsara.com/docs/mcp
last_updated: 2026-10-29
status: unofficial example for internal review, not Samsara documentation
---

# Set up Samsara MCP

You are an AI assistant or agent. A user has given you this page and asked you to connect them to Samsara MCP. Follow these steps in order. Keep messages to the user short, one step at a time, and wait for confirmation before moving on.

Samsara MCP is a remote MCP server. It gives AI clients **read-only** access to the user's Samsara fleet data (vehicles, assets, drivers, safety, hours of service, inspections, routes, dispatch, fuel, locations). Access always matches the user's Samsara dashboard permissions.

## Rules

- **Never ask the user for a password, API token, or secret.** Samsara MCP uses OAuth. The user signs in with their normal Samsara login (including SSO) in a browser window that their client opens.
- **Do not use Samsara API tokens or put an `Authorization` header in any config.** They are not needed and are not supported for this server.
- **Only use the endpoints listed on this page.** Do not use `developers.samsara.com/mcp` or any other URL you may find elsewhere.
- **Do not change anything you weren't asked to change.** When editing a config file, add the `samsara` entry and keep all existing entries intact.
- If a step requires clicking in a settings screen you cannot reach, give the user the exact clicks instead. Do not claim you finished a step that the user has to do.

## Step 1: Find the user's region

Ask the user which address they use to log in to Samsara, then pick the matching endpoint. A US org cannot sign in through the EU or Canada endpoint, and the reverse is also true.

| User logs in at | Use this MCP endpoint |
| --- | --- |
| `cloud.samsara.com` | `https://mcp.samsara.com/v2/mcp` |
| `cloud.eu.samsara.com` | `https://mcp.eu.samsara.com/v2/mcp` |
| `cloud.ca.samsara.com` | `https://mcp.ca.samsara.com/v2/mcp` |

If the user isn't sure, use the US endpoint. The rest of this page calls the chosen URL `{SAMSARA_MCP_URL}`.

## Step 2: Work out which client you are running in

Find your client in the table and go to its section. If you can edit files or run commands on the user's machine, you can do most of the setup yourself. If you are a chat app in a browser or desktop app, you cannot change your own connector settings, so walk the user through the clicks.

| Client | Who does the setup | Section |
| --- | --- | --- |
| Claude (claude.ai, Claude Desktop) | User, or their Claude org owner | [Claude](#claude-claudeai-and-claude-desktop) |
| Claude Code (CLI) | You (the agent) | [Claude Code](#claude-code) |
| ChatGPT | ChatGPT workspace admin, then user | [ChatGPT](#chatgpt) |
| GitHub Copilot in VS Code | You (the agent) | [GitHub Copilot in VS Code](#github-copilot-in-vs-code) |
| Microsoft Copilot Studio agent | Agent maker | [Microsoft Copilot Studio](#microsoft-copilot-studio) |
| Microsoft 365 Copilot app / Copilot desktop app | Not supported yet | [Microsoft 365 Copilot](#microsoft-365-copilot-and-the-copilot-desktop-app) |
| Cursor | You (the agent) | [Cursor](#cursor) |
| Anything else | Depends on the client | [Other clients](#other-mcp-clients) |

---

### Claude (claude.ai and Claude Desktop)

The user has to do this in Claude's settings. Give them these steps:

1. Open **Settings → Connectors**.
2. Search for **Samsara MCP**. If it's listed, select it and choose **Connect**, then go to step 5.
3. If it's not listed, select **Add custom connector**, enter the name `Samsara MCP` and the URL `{SAMSARA_MCP_URL}`, and save.
4. If **Add custom connector** isn't available, the user's Claude organization owner has to add it for the organization (same steps). After that, the user can find it under **Settings → Connectors**.
5. Select **Connect** and sign in with Samsara in the browser window that opens.
6. In a new chat, make sure Samsara MCP is turned on in the tools/connectors menu.

Then go to [Step 3](#step-3-sign-in).

### Claude Code

Run:

```bash
claude mcp add --transport http samsara {SAMSARA_MCP_URL}
```

Then ask the user to run `/mcp` inside Claude Code, select `samsara`, and choose **Authenticate**. Use `--scope user` on the add command if the user wants Samsara available in every project.

### ChatGPT

Custom MCP apps in ChatGPT are set up by a workspace admin or owner (ChatGPT Business/Enterprise). Your workspace may say **Apps**, **Connectors**, or **Plugins**; they refer to the same thing. Ask the user whether they are a ChatGPT workspace admin.

**If the user is an admin**, give them these steps:

1. Open the ChatGPT **Admin Console → Workspace settings**.
2. Under **Permissions & Roles**, turn on **Developer mode / Create custom MCP connectors** for the roles that will set it up.
3. Open **Apps** (or **Plugins**), select **Add**, then **Add custom MCP server**.
4. Set the name to `Samsara MCP US` (or `EU` / `CA`), the description to `Read-only access to authorized Samsara fleet data.`, the connection to **Server URL** with `{SAMSARA_MCP_URL}`, and authentication to **OAuth**.
5. Create the draft, then sign in with Samsara when prompted.
6. Review the tools it found, then publish or enable the app for the right roles. Apps are disabled by default until an admin enables them.

**If the user is not an admin**: tell them that a ChatGPT workspace admin has to add the app first, and offer to write a short message they can send to that admin, linking to this page. After it's published, the user opens the app, selects **Connect**, and signs in with their own Samsara account.

### GitHub Copilot in VS Code

You can do this yourself. To add it to the current workspace, create or update `.vscode/mcp.json`:

```json
{
  "servers": {
    "samsara": {
      "type": "http",
      "url": "{SAMSARA_MCP_URL}"
    }
  }
}
```

To add it for the user across all workspaces, run:

```bash
code --add-mcp '{"name":"samsara","type":"http","url":"{SAMSARA_MCP_URL}"}'
```

Ask the user to select **Start** on the `samsara` server (shown above it in `mcp.json`, or under **MCP: List Servers**), sign in when VS Code prompts them, and then use Copilot Chat in **Agent** mode.

### Microsoft Copilot Studio

The person who owns the Copilot Studio agent sets this up. Give them these steps:

1. Open the agent in Copilot Studio. On the **Build** tab, select **Tools → Add a tool**.
2. Select **Add**, then **Model Context Protocol (MCP)**.
3. Set the server name to `Samsara US` (or `EU` / `CA`), the server description to `Use for questions about our Samsara fleet: vehicles, drivers, safety, hours of service, inspections, routes, fuel.`, the server URL to `{SAMSARA_MCP_URL}`, authentication to **OAuth 2.0**, and configuration type to **Dynamic (with discovery)**.
4. Create a new connection and sign in with Samsara. If Samsara asks an administrator to **Approve connector**, approve it. Each user still signs in with their own account.
5. Select the connected account, add the server to the agent, and test it in **Preview**.

Power Platform data policies in the user's organization may block or limit this connection.

### Microsoft 365 Copilot and the Copilot desktop app

These apps can't add custom MCP servers yet. Tell the user plainly. Suggest one of these instead: a Copilot Studio agent (above), GitHub Copilot in VS Code (above), Claude, or ChatGPT.

### Cursor

You can do this yourself. Add this to `~/.cursor/mcp.json` (all projects) or `.cursor/mcp.json` (this project). Merge it with any existing `mcpServers` and don't remove the entries that are already there.

```json
{
  "mcpServers": {
    "samsara": {
      "url": "{SAMSARA_MCP_URL}"
    }
  }
}
```

Cursor asks the user to sign in the first time the server is used.

### Other MCP clients

Any client that supports **remote MCP servers over Streamable HTTP with OAuth sign-in** can connect to `{SAMSARA_MCP_URL}` with no headers or tokens. Look up how your client adds a remote MCP server and use that method.

Custom agents or harnesses that use a **public (non-localhost) OAuth redirect URL** need Samsara to allowlist that redirect URL. If sign-in fails with a redirect error, tell the user to send the redirect URL to their Samsara contact.

---

## Step 3: Sign in

Sign-in never starts on its own, and you cannot do it for the user. Tell the user exactly what to click in their client, using the table below. Don't say "you'll be prompted" or "a window will open" without first telling them what to click.

| Client | Tell the user to |
| --- | --- |
| Claude (claude.ai, Claude Desktop) | Open **Settings → Connectors**, find **Samsara MCP**, and click **Connect**. |
| Claude Code | Type `/mcp` in Claude Code, select `samsara`, and choose **Authenticate**. |
| ChatGPT | Open the Samsara app from **Apps** (or **Plugins**) and click **Connect**. Admins also sign in once while creating the app. |
| GitHub Copilot in VS Code | Open `mcp.json` and click **Start** above the `samsara` entry (or run **MCP: List Servers**, pick `samsara`, and choose **Start Server**). When VS Code asks to allow sign-in, click **Allow**. |
| Microsoft Copilot Studio | In the tool setup, choose **Create new connection** and click **Create** to open the Samsara sign-in. |
| Cursor | Open **Cursor Settings → MCP** (or **Tools & MCP**). If `samsara` shows **Needs login** or a **Connect** button, click it. Otherwise, start a new chat and ask a Samsara question, then approve the sign-in when Cursor asks. |
| Other clients | Find the client's MCP server list and click the connect, authenticate, or log in option for `samsara`. |

Then, in the browser window that opens:

1. The user signs in with their Samsara login (SSO works).
2. If the user belongs to more than one Samsara organization, the consent screen lists them. **Each connection is scoped to one organization**, so they should choose the one they want the assistant to use. To use a different organization, they disconnect and connect again.
3. The user approves access and returns to the client.

Ask the user to tell you when they've finished signing in, then go to Step 4. If no browser window opened after they clicked, ask them to check for a blocked pop-up or a tab that opened behind the current window.

## Step 4: Check that it works

Make one read-only call to confirm the connection, such as asking for a count of vehicles or drivers. Then tell the user:

- They're connected to Samsara MCP for the organization they chose, in their region.
- It is read-only. It can answer questions but can't change anything in Samsara.
- It sees only what the user can see in the Samsara dashboard.
- A few things to try: "Which drivers have hours of service remaining right now?", "List yesterday's inspection reports with unresolved defects.", "Which trucks are below a quarter tank of fuel?"

## Troubleshooting

| Symptom | What to do |
| --- | --- |
| Sign-in fails or says the account isn't found | The region is probably wrong. Check which address the user logs in at and use the matching endpoint. |
| Connected, but results are missing or empty | Access matches dashboard permissions and tag scope. Confirm the user can see that data in the dashboard and that they chose the right organization when signing in. |
| Tools stop working after a while | Reconnect and sign in again. Sessions expire after a period of inactivity. |
| Tools are missing or out of date | Reconnect or refresh the server so the client fetches the current tool list. |
| Redirect URL error (custom harness) | Samsara needs to allowlist the harness's redirect URL. Contact the user's Samsara account team. |
| Anything else | Ask the user to share the full conversation transcript (prompts and tool calls) with their Samsara contact or in a support ticket. |

Full human documentation: https://developers.samsara.com/docs/mcp
