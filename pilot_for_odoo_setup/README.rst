==========================
MCP Connector for Odoo CRM
==========================

A free, standalone setup wizard that connects any Model Context Protocol (MCP)
client — Claude Desktop, Claude Code, Cursor, or any other — to your Odoo
Community Edition instance.

What this module does
=====================

After installation, open **Settings → MCP Connector → Setup wizard**. The
wizard:

* Auto-detects your Odoo URL, database, and login
* Generates a scoped, revocable API key on the current user
* Renders the JSON configuration block to paste into your MCP client
* Provides a one-click link to setup documentation

The generated API key works alongside two-factor authentication, which
password-only XML-RPC authentication does not.

Standalone value
================

This module is genuinely useful on its own. The API key it generates works
with any MCP-compatible client or external XML-RPC consumer — not only with
the OdooPilot agent mentioned below. You can also use the produced config
as a template for building your own MCP integrations.

Recommended MCP client
======================

`OdooPilot <https://equationx.ai/products/odoo-pilot>`_ is a ready-made MCP
client for Odoo CRM. It is a separate paid product distributed by equationx
(USD 199, one-time) that lives in Claude Desktop and answers questions like
*"give me the Monday brief"* or *"how is Alex doing this month?"*

OdooPilot is **not** required to use this connector. Any MCP client works.

Installation steps
==================

#. Install this module in your Odoo instance.
#. Open **Settings → MCP Connector → Setup wizard**.
#. Click **Generate API key & config**.
#. Copy the JSON block; paste it into your MCP client's configuration:

   * Claude Desktop, macOS:
     ``~/Library/Application Support/Claude/claude_desktop_config.json``
   * Claude Desktop, Windows:
     ``%APPDATA%\\Claude\\claude_desktop_config.json``

#. Replace ``/PATH/TO/your-mcp-server`` with the actual install path.
#. Fully restart your MCP client.

Customisations and support
==========================

Every Odoo deployment is different — custom fields, custom modules,
nonstandard stage names, multi-company setups, Enterprise-only features.
The connector handles the standard case out of the box; for non-trivial
deployments, equationx offers paid setup and customisation support:

* `Contact equationx <https://equationx.ai/contact>`_ — send your config
  and constraints
* `Book a call <https://equationx.ai/book>`_ — 20-minute setup session

Privacy
=======

This module makes no external network calls during install or use.
Generated API keys are stored as hashed values via Odoo's standard
``res.users.apikeys`` mechanism. Nothing is reported back to equationx
or any third party.

Compatibility
=============

* Odoo Community Edition 16, 17, 18
* Works with Odoo Enterprise as a superset
* Requires XML-RPC enabled (default on Community Edition)

License
=======

LGPL-3.

equationx is independent and not affiliated with Odoo SA.
