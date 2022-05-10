from __future__ import annotations

import quarrel

__all__ = ("MemberOrUser",)

MemberOrUser = quarrel.User | quarrel.Member
