# -*- coding: utf-8 -*-
{
    "name": "MCP Connector for Odoo CRM",
    "version": "1.0.0",
    "summary": "Connect Claude Desktop (and any MCP-compatible AI client) to your Odoo. One-click API key + ready-to-paste config.",
    "description": """
MCP Connector for Odoo CRM
===========================

A free, standalone setup wizard that connects any **Model Context Protocol (MCP)**
client — Claude Desktop, Claude Code, Cursor, or any other — to your Odoo
Community Edition instance.

What this module does
---------------------

After installation, go to **Settings → MCP Connector → Setup wizard**. The
wizard:

* Auto-detects your Odoo URL, database, and login
* Generates a scoped, revocable API key on the current user (works alongside
  two-factor authentication, which password-only XML-RPC does not)
* Renders the JSON config block you paste into your MCP client's settings file
* Links to setup documentation

Standalone value
----------------

The module is genuinely useful on its own. The generated API key works with
any MCP client or external XML-RPC consumer — not only with the OdooPilot
agent recommended below. You can also use the produced configuration as a
template for building your own MCP integrations.

Recommended MCP client
----------------------

`OdooPilot <https://equationx.ai/products/odoo-pilot>`_ is a third-party AI
agent built by equationx that runs locally on your laptop and answers
questions like *"give me the Monday brief"* or *"how is Alex doing this
month?"* using the credentials this module generates. OdooPilot is a
separate paid product distributed by equationx; it is **not** required to
use this connector.

Supported Odoo versions
-----------------------

Odoo Community Edition 17 and 18. Tested headless on 17.0.

Privacy
-------

This module makes no external network calls during install. Generated API
keys are stored as hashed values by Odoo's standard ``res.users.apikeys``
mechanism. Nothing is reported back to equationx or any third party.

License
-------

LGPL-3. equationx is independent and not affiliated with Odoo SA.
    """,
    "category": "Sales/CRM",
    "author": "equationx",
    "website": "https://equationx.ai/products/odoo-pilot",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/setup_wizard_views.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
    "application": False,
    "auto_install": False,
}
