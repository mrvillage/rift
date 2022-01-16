from __future__ import annotations

from .flags import Flags, flag

__all__ = ("CredentialsPermissions", "RolePermissions")


class CredentialsPermissions(Flags):
    @flag
    def send_nation_bank(self):
        return 1 << 1

    @flag
    def send_alliance_bank(self):
        return 1 << 2

    @flag
    def view_nation_bank(self):
        return 1 << 3

    @flag
    def view_alliance_bank(self):
        return 1 << 4

    @flag
    def manage_alliance_treaties(self):
        return 1 << 5

    @flag
    def manage_alliance_positions(self):
        return 1 << 6

    @flag
    def manage_alliance_taxes(self):
        return 1 << 7

    @flag
    def manage_alliance_announcements(self):
        return 1 << 8

    @flag
    def manage_nation(self):
        return 1 << 9

    @flag
    def send_messages(self):
        return 1 << 10

    @flag
    def create_trade(self):
        return 1 << 11

    @flag
    def manage_trades(self):
        return 1 << 12

    @flag
    def declare_war(self):
        return 1 << 13

    @flag
    def manage_wars(self):
        return 1 << 14


class RolePermissions(Flags):
    max_rank: int

    @flag
    def manage_roles(self):
        return 1 << 0

    @flag
    def leadership(self):
        return 1 << 1

    @flag
    def view_alliance_bank(self):
        return 1 << 2

    @flag
    def send_alliance_bank(self):
        return 1 << 3

    @flag
    def view_nation_banks(self):
        return 1 << 4

    @flag
    def view_nation_spies(self):
        return 1 << 5

    @flag
    def view_offshores(self):
        return 1 << 6

    @flag
    def send_offshore_banks(self):
        return 1 << 7

    @flag
    def manage_offshores(self):
        return 1 << 8

    @flag
    def create_bank_accounts(self):
        return 1 << 9

    @flag
    def view_bank_accounts(self):
        return 1 << 10

    @flag
    def manage_bank_accounts(self):
        return 1 << 11

    @flag
    def view_grants(self):
        return 1 << 12

    @flag
    def request_grants(self):
        return 1 << 13

    @flag
    def approve_grants(self):
        return 1 << 14

    @flag
    def manage_grants(self):
        return 1 << 15

    @flag
    def manage_alliance_taxes(self):
        return 1 << 16

    @flag
    def manage_alliance_positions(self):
        return 1 << 17

    @flag
    def manage_treaties(self):
        return 1 << 18

    @flag
    def create_alliance_announcements(self):
        return 1 << 19

    @flag
    def delete_alliance_announcements(self):
        return 1 << 20
