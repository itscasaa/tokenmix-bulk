"""Client for the cilaaa.my.id (CasaTemp) disposable inbox API.

cilaaa.my.id exposes a bot-friendly REST API for automated registration:

* ``GET  /api/bot/generate?name={name}&domain={domain}`` -> create/generate mailbox
* ``GET  /api/bot/inbox?email={address}``                -> list received messages
* ``GET  /api/bot/message/{id}``                         -> single message details
* ``GET  /api/bot/otp?email={address}&timeout={seconds}`` -> auto wait & extract OTP
* ``POST /api/bot/clear?email={address}``                -> reset/clear mailbox
"""

from __future__ import annotations

import random
import time
from dataclasses import dataclass, field

import requests

DEFAULT_BASE_URL = "https://cilaaa.my.id"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


class CilaaaError(RuntimeError):
    """Raised when the cilaaa.my.id API returns an unexpected response."""


@dataclass
class Message:
    """A single inbox message."""

    id: str
    sender: str
    subject: str
    body_text: str = ""
    body_html: str = ""
    created_at: str = ""

    @property
    def code(self) -> str | None:
        """Extract the first 4-8 digit numeric verification code, if present."""
        import re

        haystack = f"{self.subject}\n{self.body_text}"
        match = re.search(r"(?<!\d)(\d{4,8})(?!\d)", haystack)
        return match.group(1) if match else None


@dataclass
class Inbox:
    """A created disposable inbox on cilaaa.my.id."""

    address: str
    password: str = ""
    token: str = ""
    username: str = ""
    domain: str = "cilaaa.my.id"
    base_url: str = DEFAULT_BASE_URL
    _session: requests.Session = field(default_factory=requests.Session, repr=False)


class CilaaaClient:
    """Wrapper around the cilaaa.my.id REST API."""

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        *,
        timeout: float = 20.0,
        retries: int = 3,
        session: requests.Session | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self._session = session or requests.Session()
        self._headers = {
            "Accept": "application/json",
            "User-Agent": DEFAULT_USER_AGENT,
        }

    # -- low level ---------------------------------------------------------
    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        headers = {**self._headers, **kwargs.pop("headers", {})}
        last_error: Exception | None = None
        for attempt in range(1, self.retries + 1):
            try:
                response = self._session.request(
                    method, url, headers=headers, timeout=self.timeout, **kwargs
                )
            except requests.RequestException as exc:
                last_error = exc
            else:
                if response.status_code < 500:
                    return response
                last_error = CilaaaError(
                    f"server error {response.status_code} for {path}"
                )
            if attempt < self.retries:
                time.sleep(0.8 * attempt)
        raise CilaaaError(f"request to {path} failed: {last_error}")

    @staticmethod
    def _json(response: requests.Response):
        try:
            payload = response.json()
        except ValueError as exc:
            raise CilaaaError(
                f"invalid JSON from server: {response.text[:200]}"
            ) from exc
        if response.status_code >= 400:
            message = ""
            if isinstance(payload, dict):
                message = payload.get("message") or payload.get("error") or ""
            raise CilaaaError(
                f"HTTP {response.status_code}: {message or response.text[:200]}"
            )
        return payload

    # -- public API --------------------------------------------------------
    def domains(self) -> list[str]:
        """Return supported domains."""
        return ["cilaaa.my.id"]

    def pick_domain(self) -> str:
        """Return the default domain."""
        return "cilaaa.my.id"

    def create_inbox(self, name: str | None = None, domain: str | None = None) -> Inbox:
        """Create a new inbox."""
        params: dict[str, str] = {}
        if name:
            params["name"] = name
        if domain:
            params["domain"] = domain
        payload = self._json(self._request("GET", "/api/bot/generate", params=params))
        address = payload.get("email")
        if not address:
            raise CilaaaError("cilaaa.my.id did not return an email address")
        return Inbox(
            address=address,
            token=payload.get("token", ""),
            username=payload.get("username", ""),
            domain=payload.get("domain", domain or "cilaaa.my.id"),
            base_url=self.base_url,
            _session=self._session,
        )

    def messages(self, inbox: Inbox) -> list[Message]:
        """Return the messages currently in ``inbox``."""
        payload = self._json(
            self._request("GET", "/api/bot/inbox", params={"email": inbox.address})
        )
        raw_list = payload.get("emails", []) if isinstance(payload, dict) else payload
        messages: list[Message] = []
        for m in raw_list:
            if not isinstance(m, dict):
                continue
            messages.append(
                Message(
                    id=str(m.get("id", "")),
                    sender=m.get("from", "") or m.get("sender", ""),
                    subject=m.get("subject", ""),
                    body_text=m.get("body_text", "") or m.get("text", "") or "",
                    body_html=m.get("body_html", "") or m.get("html", "") or "",
                    created_at=str(m.get("date", "") or m.get("created_at", "")),
                )
            )
        return messages

    def read_message(self, inbox: Inbox, message_id: str) -> Message:
        """Fetch a single message."""
        payload = self._json(self._request("GET", f"/api/bot/message/{message_id}"))
        data = payload.get("message", payload) if isinstance(payload, dict) else payload
        return Message(
            id=str(data.get("id", message_id)),
            sender=data.get("from", "") or data.get("sender", ""),
            subject=data.get("subject", ""),
            body_text=data.get("body_text", "") or data.get("text", "") or "",
            body_html=data.get("body_html", "") or data.get("html", "") or "",
            created_at=str(data.get("date", "") or data.get("created_at", "")),
        )

    def fetch_otp(self, inbox: Inbox, timeout: int = 30) -> str | None:
        """Query /api/bot/otp directly with long-polling."""
        try:
            payload = self._json(
                self._request(
                    "GET",
                    "/api/bot/otp",
                    params={"email": inbox.address, "timeout": str(timeout)},
                )
            )
            if isinstance(payload, dict) and payload.get("success") and payload.get("otp"):
                return str(payload["otp"])
        except Exception:
            pass
        return None

    def wait_for_code(
        self,
        inbox: Inbox,
        *,
        sender_contains: str | None = "tokenmix",
        timeout: float = 120.0,
        interval: float = 3.0,
        seen: set[str] | None = None,
    ) -> str:
        """Poll until verification code arrives."""
        seen = seen if seen is not None else set()
        deadline = time.monotonic() + timeout
        last_error: Exception | None = None

        while time.monotonic() < deadline:
            try:
                for message in self.messages(inbox):
                    if message.id in seen:
                        continue
                    if sender_contains and sender_contains.lower() not in message.sender.lower():
                        continue
                    seen.add(message.id)
                    full = self.read_message(inbox, message.id)
                    if full.code:
                        return full.code
            except CilaaaError as exc:
                last_error = exc
            time.sleep(interval)

        raise CilaaaError(
            f"no verification code for {inbox.address} within {timeout:.0f}s"
            + (f" (last error: {last_error})" if last_error else "")
        )
