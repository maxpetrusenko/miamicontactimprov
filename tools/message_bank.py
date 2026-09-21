#!/usr/bin/env python3
"""Read `docs/ads/messages.yaml` with the standard library.

The tool is meant to run from a cron job on whatever interpreter the machine already
has, so it does not pull PyYAML in for one file. The bank is a tidy subset of YAML and
this reader covers exactly that subset:

* comments on their own line, blank lines ignored;
* `key: value` scalars, where only the first colon separates the two, so copy that
  contains `7:00 to 9:00 PM` survives;
* nested mappings by indentation;
* block sequences, of scalars (`- climbers`) or of mappings (`- slug: come-alone`
  followed by more keys at the sequence's indent plus two);
* literal blocks (`body: |`), dedented and joined with newlines, interior blank lines
  kept because they separate the paragraphs of the ad copy.

Anything else - quotes, flow collections (`[]`, `{}`), anchors, folded blocks - raises
with the line number instead of being guessed at. A reader that half-understands a file
of ad copy would publish the wrong words, which is worse than refusing to start.

Fuller syntax for this file lives in `tools/ad_statics.py` (PyYAML, via uv), which
renders the posters. This module exists so the ad operator runs anywhere.
"""

import pathlib


class BankError(ValueError):
    """The bank uses YAML this reader does not understand."""


def load(path) -> dict:
    """Parse `path`. Raises BankError naming the line it could not read."""
    reader = _Reader(pathlib.Path(path).read_text(encoding="utf-8"), str(path))
    value = reader.block(0)
    if not isinstance(value, dict):
        raise BankError(f"{path}: the top level is not a set of keys")
    return value


class _Reader:
    def __init__(self, text: str, name: str):
        self.lines = text.split("\n")
        self.name = name
        self.i = 0

    # ------------------------------------------------------------------ line handling
    def _line(self):
        return self.lines[self.i]

    def _indent(self, line) -> int:
        return len(line) - len(line.lstrip(" "))

    def _skip_trivia(self) -> None:
        """Step over blanks and full-line comments between nodes."""
        while self.i < len(self.lines):
            text = self.lines[self.i].strip()
            if text and not text.startswith("#"):
                return
            self.i += 1

    def _fail(self, message: str):
        raise BankError(f"{self.name} line {self.i + 1}: {message}")

    # ---------------------------------------------------------------------- the grammar
    def block(self, indent: int):
        """The next mapping, sequence or scalar at `indent` or deeper."""
        self._skip_trivia()
        if self.i >= len(self.lines):
            return None
        line = self._line()
        if self._indent(line) < indent:
            return None
        if line.strip().startswith("- "):
            return self.sequence(self._indent(line))
        return self.mapping(self._indent(line))

    def sequence(self, indent: int) -> list:
        items = []
        while True:
            self._skip_trivia()
            if self.i >= len(self.lines):
                break
            line = self._line()
            text = line.strip()
            if self._indent(line) != indent or not text.startswith("- "):
                break
            body = text[2:].strip()
            self.i += 1
            if _looks_like_key(body):
                # `- slug: come-alone`, with the item's other keys indented two deeper.
                key, value = self._pair(body)
                if not value or value == "|":
                    self._fail(f"a sequence item's first key needs an inline value: {body!r}")
                items.append(self.mapping(indent + 2, seed={key: value}))
            else:
                self._reject(body)
                items.append(body)
        return items

    def mapping(self, indent: int, seed=None) -> dict:
        out = dict(seed or {})
        while True:
            self._skip_trivia()
            if self.i >= len(self.lines):
                break
            line = self._line()
            if self._indent(line) != indent or line.strip().startswith("- "):
                break
            text = line.strip()
            if not _looks_like_key(text):
                self._fail(f"expected `key: value`, got {text!r}")
            key, value = self._pair(text)
            self.i += 1
            if value == "|":
                out[key] = self.literal_block(indent)
            elif value == ">":
                self._fail("folded blocks (`>`) are not supported; use `|`")
            elif value:
                out[key] = value
            else:
                out[key] = self.block(indent + 1)
        return out

    def literal_block(self, parent_indent: int) -> str:
        """A `|` block: every following line indented deeper than its key."""
        kept, block_indent = [], None
        while self.i < len(self.lines):
            raw = self._line()
            if not raw.strip():
                kept.append("")
                self.i += 1
                continue
            if self._indent(raw) <= parent_indent:
                break
            if block_indent is None:
                block_indent = self._indent(raw)
            # Comments inside a block scalar are copy, not comments: keep them.
            kept.append(raw[block_indent:])
            self.i += 1
        while kept and not kept[-1]:
            kept.pop()
        return "\n".join(kept)

    # ------------------------------------------------------------------------- helpers
    def _pair(self, text: str) -> tuple:
        key, sep, value = text.partition(":")
        if not sep:
            self._fail(f"expected `key: value`, got {text!r}")
        key, value = key.strip(), value.strip()
        self._reject(value)
        return key, value

    def _reject(self, value: str) -> None:
        """Say no to syntax this reader would otherwise guess at."""
        if value[:1] in ("'", '"', "[", "{", "&", "*", "!"):
            self._fail(f"quoted or flow values are not supported, got {value!r}")
        if value.endswith(",") and ":" in value:
            self._fail(f"flow mappings are not supported, got {value!r}")


def _looks_like_key(text: str) -> bool:
    """`slug: come-alone` is a key; `7:00 to 9:00 PM` and a bare word are not."""
    head, sep, _ = text.partition(":")
    return bool(sep) and " " not in head.strip() and head.strip().isprintable()
