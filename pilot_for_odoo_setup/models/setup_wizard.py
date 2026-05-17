# -*- coding: utf-8 -*-
"""OdooPilot Setup Wizard.

A TransientModel that helps the user connect Claude Desktop to their Odoo
instance via the Model Context Protocol (MCP). It generates an API key for
the current user and produces the JSON config block to paste into
``claude_desktop_config.json``.
"""

import json
import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class OdooPilotSetupWizard(models.TransientModel):
    _name = "pilot.for.odoo.setup.wizard"
    _description = "OdooPilot Setup Wizard"

    # Connection details — auto-populated from environment, read-only.
    odoo_url = fields.Char(string="Odoo URL", readonly=True)
    odoo_db = fields.Char(string="Database", readonly=True)
    odoo_login = fields.Char(string="Login", readonly=True)

    # Filled when the user clicks "Generate".
    api_key = fields.Char(
        string="API Key",
        readonly=True,
        copy=False,
        help="Generated once. Copy now — Odoo won't display it again.",
    )
    config_block = fields.Text(
        string="Claude Desktop config",
        readonly=True,
        copy=False,
        help=(
            "Paste this block under `mcpServers` in your Claude Desktop "
            "config file, then restart Claude Desktop."
        ),
    )

    state = fields.Selection(
        [("start", "Start"), ("generated", "Generated")],
        default="start",
        string="Step",
    )

    config_path_help = fields.Char(
        compute="_compute_config_path_help",
        string="Where to paste",
        readonly=True,
    )

    @api.depends_context("uid")
    def _compute_config_path_help(self):
        for record in self:
            record.config_path_help = (
                "macOS: ~/Library/Application Support/Claude/"
                "claude_desktop_config.json · "
                "Windows: %APPDATA%\\Claude\\claude_desktop_config.json"
            )

    # ------------------------------------------------------------------
    # Defaults
    # ------------------------------------------------------------------

    @api.model
    def default_get(self, fields_list):
        vals = super().default_get(fields_list)
        icp = self.env["ir.config_parameter"].sudo()
        base_url = icp.get_param("web.base.url") or ""
        vals.update(
            {
                "odoo_url": base_url,
                "odoo_db": self.env.cr.dbname,
                "odoo_login": self.env.user.login,
            }
        )
        return vals

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def action_generate(self):
        """Generate an API key on the current user and build the config block."""
        self.ensure_one()
        api_key = self._create_api_key()
        self.write(
            {
                "api_key": api_key,
                "config_block": self._build_config_block(api_key),
                "state": "generated",
            }
        )
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
            "context": dict(self.env.context),
        }

    def action_open_docs(self):
        """Open the OdooPilot product page in a new tab."""
        return {
            "type": "ir.actions.act_url",
            "url": "https://equationx.ai/products/odoo-pilot",
            "target": "new",
        }

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _create_api_key(self):
        """Create a new API key for the current user and return the plaintext.

        Odoo's ``res.users.apikeys._generate`` returns the plaintext key once
        and stores only a hash thereafter. We catch the missing-model case so
        the wizard degrades gracefully on Odoo versions without API key
        support enabled.
        """
        try:
            key_model = self.env["res.users.apikeys"]
        except KeyError:
            raise UserError(
                _(
                    "Your Odoo instance does not expose res.users.apikeys. "
                    "Enable the API Keys feature or generate a key manually "
                    "from your user profile."
                )
            )

        try:
            # Signature has been stable since Odoo 14:
            # _generate(scope, name, expiration_date=False)
            return key_model._generate(
                "rpc",
                "OdooPilot — Claude Desktop",
                False,
            )
        except Exception as err:  # pragma: no cover - depends on Odoo version
            _logger.exception("OdooPilot: API key generation failed")
            raise UserError(
                _(
                    "Failed to generate an API key automatically (%s). "
                    "Create one manually from your user profile under "
                    "Account Security → New API Key, then paste it into the "
                    "ODOO_PASSWORD field of the config block."
                )
                % err
            )

    def _build_config_block(self, api_key):
        """Return the JSON snippet the user pastes into Claude Desktop."""
        snippet = {
            "mcpServers": {
                "odoo-pilot": {
                    "command": "node",
                    "args": [
                        "/PATH/TO/pilot-for-odoo/dist/server.js",
                    ],
                    "env": {
                        "ODOO_URL": self.odoo_url or "",
                        "ODOO_DB": self.odoo_db or "",
                        "ODOO_USERNAME": self.odoo_login or "",
                        "ODOO_PASSWORD": api_key,
                    },
                }
            }
        }
        return json.dumps(snippet, indent=2)
