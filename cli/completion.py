from __future__ import annotations
from typing import Iterable, Optional, List, TYPE_CHECKING
import shlex
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from prompt_toolkit.document import Document
from sqlalchemy import Engine

from data.contact_queries import ContactQueries
from data.phone_queries import PhoneQueries
from data.email_queries import EmailQueries
from cli.note_commands import NoteCommandHandlers

if TYPE_CHECKING:
    from data.models import Tag


BUILTIN_COMMANDS = [
    "hello", "exit", "close",
    # Contacts
    "get-contacts", "get-contact", "add-contact", "edit-contact", "delete-contact",
    "add-tag-to-contact", "remove-tag-from-contact", "get-contact-notes",
    # Phones
    "get-phones", "add-phone", "edit-phone", "delete-phone",
    # Emails
    "get-emails", "add-email", "edit-email", "delete-email",
    # Birthdays
    "add-birthday", "remove-birthday", "get-birthdays",
    # Notes (global)
    "get-notes", "add-note", "edit-note", "delete-note",
    "add-tag-to-note", "remove-tag-from-note",
    # Notes (contact-scoped)
    "add-note-to-contact",
]

def _split_words(s: str) -> list[str]:
    """Шелл-разбор для корректной работы с кавычками.
    Фоллбек на .split() если кавычки не закрыты."""
    if not s:
        return []
    try:
        return shlex.split(s, posix=True)
    except ValueError:
        return s.split()
    
def _needs_quotes(s: str) -> bool:
    if not s:
        return False
    if any(ch.isspace() for ch in s):
        return True
    return '"' in s

def _quote_token(s: str) -> str:
    escaped = s.replace('\\', '\\\\').replace('"', '\\"')
    return f'"{escaped}"'

def _tag_label(tag_obj: 'Tag | str') -> str | None:
    if isinstance(tag_obj, str):
        return tag_obj or None
    
    return tag_obj.label or None

def _note_text(note_obj) -> str | None:
    txt = getattr(note_obj, "text", None)
    return str(txt) if txt else None

def _fetch_contact_names(engine: Engine) -> list[str]:
    try:
        q = ContactQueries(engine)
        return [c.name for c in q.get_contacts()]
    except Exception:
        return []

def _fetch_contact_phones(engine: Engine, contact_name: str) -> list[str]:
    try:
        pq = PhoneQueries(engine)
        phones = pq.get_contact_phones_by_name(contact_name)  # list[Phone]
        res: list[str] = []
        for p in (phones or []):
            num = p.phone_number
            if num:
                res.append(num)
        return sorted(set(res))
    except Exception:
        return []

def _fetch_contact_emails(engine: Engine, contact_name: str) -> list[str]:
    try:
        eq = EmailQueries(engine)
        emails = eq.get_contact_emails_by_name(contact_name)  # list[Email]
        res: list[str] = []
        for e in (emails or []):
            addr = e.email_address
            if addr:
                res.append(addr)
        return sorted(set(res))
    except Exception:
        return []

def _fetch_all_tags(engine: Engine) -> list[str]:
    tags: set[str] = set()

    try:
        cq = ContactQueries(engine)
        for c in cq.get_contacts():
            for t in (c.tags or []):
                lab = _tag_label(t)
                if lab:
                    tags.add(lab)
    except Exception:
        return []

    try:
        for lab in NoteCommandHandlers.list_note_tags(engine):
            tags.add(lab)
    except Exception:
        # игнорим теги заметок, но уже есть теги контактов
        return sorted(tags)

    return sorted(tags)

def _fetch_notes_texts(engine: Engine) -> list[str]:
    try:
        return NoteCommandHandlers.list_note_texts(engine)
    except Exception:
        return []


def _prefix_match(items: Iterable[str], prefix: str) -> list[str]:
    p = (prefix or "").lower()
    return [x for x in items if x.lower().startswith(p)]

COMPLETION_RULES: dict[str, List[str]] = {
    # Contacts
    "get-contacts":                 ["tag?"                 ],
    "get-contact":                  ["name!"                ],
    "add-contact":                  ["free!", "phone-new!"  ],
    "edit-contact":                 ["name!", "free!"       ],
    "delete-contact":               ["name!"                ],
    "add-tag-to-contact":           ["name!", "tag!"        ],
    "remove-tag-from-contact":      ["name!", "tag!"        ],
    "get-contact-notes":            ["name!", "tag?"        ],

    # Phones
    "get-phones":                   ["name!"                ],
    "add-phone":                    ["name!", "phone-new!"  ],
    "edit-phone":                   ["name!", "phone(name)!"],
    "delete-phone":                 ["name!", "phone(name)!" ],

    # Emails
    "get-emails":                   ["name!"                ],
    "add-email":                    ["name!", "free!"       ],
    "edit-email":                   ["name!", "email(name)!", "free!" ],
    "delete-email":                 ["name!", "email(name)!" ],

    # Birthdays
    "add-birthday":                 ["name!", "date!"       ],
    "remove-birthday":              ["name!"                ],
    "get-birthdays":                ["days!"                ],

    # Notes (global)
    "get-notes":                    ["tag?"                 ],
    "add-note":                     ["free!", "tag?"        ],
    "edit-note":                    ["note-fragment!", "free!" ],
    "delete-note":                  ["note-fragment!"       ],
    "add-tag-to-note":              ["note-fragment!", "tag!" ],
    "remove-tag-from-note":         ["note-fragment!", "tag!" ],
    # Notes (contact-scoped)
    "add-note-to-contact":          ["name!", "free!", "tag!" ],
}

PHONE_MASKS = ["050########", "067########"]

class CLIAutoSuggest(AutoSuggest):
    def __init__(self, get_candidates):
        self.get_candidates = get_candidates

    def get_suggestion(self, buffer, document: Document) -> Optional[Suggestion]:
        text = document.text
        before = document.current_line_before_cursor

        parts = _split_words(before)
        at_word_boundary = before.endswith(" ")

        idx_in_line = (len(parts)) if at_word_boundary else (len(parts) - 1)
        if idx_in_line < 0:
            return None

        current_prefix = "" if at_word_boundary else (parts[-1] if parts else "")

        cands = self.get_candidates(text, document.cursor_position, idx_in_line, current_prefix)
        if not cands:
            return None

        matches = _prefix_match(cands, current_prefix) if current_prefix else cands
        if len(matches) != 1:
            return None

        only = matches[0]

        if _needs_quotes(only) and not (current_prefix.startswith('"') or current_prefix.startswith("'")):
            return None

        if len(only) <= len(current_prefix):
            return None

        remainder = only[len(current_prefix):]
        return Suggestion(remainder)


class CLICompleter(Completer):
    def __init__(self, engine: Engine, commands: list[str]):
        self.engine = engine
        self.commands = sorted(set(commands or BUILTIN_COMMANDS))

    def get_completions(self, document: Document, complete_event) -> Iterable[Completion]:
        line = document.text_before_cursor

        parts = _split_words(line)
        at_word_boundary = line.endswith(" ")

        word_index = (len(parts)) if at_word_boundary else (len(parts) - 1)
        current_prefix = "" if at_word_boundary else (parts[-1] if parts else "")

        def complete_words(words: Iterable[str], meta: str | None = None):
            in_quotes = current_prefix.startswith('"') or current_prefix.startswith("'")
            for w in sorted(set(words)):
                insert_text = w
                if not in_quotes and _needs_quotes(w):
                    insert_text = _quote_token(w)
                display_text = _quote_token(w) if (not in_quotes and _needs_quotes(w)) else w
                yield Completion(
                    insert_text,
                    start_position=-len(current_prefix),
                    display=display_text,
                    display_meta=meta  # ← метка справа в меню
                )

        if not line:
            for cmd in self.commands:
                yield Completion(cmd, start_position=0, display=cmd)
            return

        if word_index == 0:
            yield from complete_words(_prefix_match(self.commands, current_prefix))
            return

        first = parts[0].lower() if parts else ""
        if not first:
            return

        rules = COMPLETION_RULES.get(first)
        if not rules:
            return

        arg_pos = word_index
        if arg_pos <= 0 or arg_pos > len(rules):
            return

        rule = rules[arg_pos - 1].strip().lower()

        if rule.startswith("name"):
            names = _fetch_contact_names(self.engine)
            yield from complete_words(_prefix_match(names, current_prefix))
            return

        if rule.startswith("tag"):
            tags = _fetch_all_tags(self.engine)
            yield from complete_words(_prefix_match(tags, current_prefix))
            return

        if rule.startswith("phone("):
            name = parts[1] if len(parts) > 1 else ""
            phones = _fetch_contact_phones(self.engine, name) if name else []

            # Для add-phone показываем и шаблоны, и реальные номера
            if first == "add-phone":
                yield from complete_words(_prefix_match(PHONE_MASKS, current_prefix), meta="mask")

            yield from complete_words(_prefix_match(phones, current_prefix), meta="existing")
            return

        if rule.startswith("email("):
            name = parts[1] if len(parts) > 1 else ""
            emails = _fetch_contact_emails(self.engine, name) if name else []
            yield from complete_words(_prefix_match(emails, current_prefix))
            return

        if rule.startswith("note-fragment"):
            frags = _fetch_notes_texts(self.engine)
            yield from complete_words(_prefix_match(frags, current_prefix))
            return

        if rule.startswith("days"):
            yield from complete_words(_prefix_match(["3", "7", "14", "30"], current_prefix))
            return

        if rule.startswith("date"):
            yield from complete_words(_prefix_match(["YYYY-MM-DD"], current_prefix))
            return

        if rule.startswith("phone-new"):
            yield from complete_words(_prefix_match(PHONE_MASKS, current_prefix), meta="mask")
            return

        # free — ничего не подсказываем
        return

def build_completer(engine: Engine, all_commands: list[str]) -> CLICompleter:
    return CLICompleter(engine, all_commands)

def build_auto_suggest(engine: Engine, all_commands: list[str]) -> CLIAutoSuggest:
    completer = CLICompleter(engine, all_commands)

    def _get_candidates(full_text: str, cursor_pos: int, word_index: int, prefix: str) -> list[str]:
        if word_index == 0:
            return list(completer.commands)

        parts = _split_words(full_text[:cursor_pos])
        first = parts[0].lower() if parts else ""
        rules = COMPLETION_RULES.get(first)
        if not rules:
            return []

        arg_pos = word_index
        if arg_pos <= 0 or arg_pos > len(rules):
            return []

        rule = rules[arg_pos - 1].strip().lower()

        if rule.startswith("name"):
            return _fetch_contact_names(engine)
        if rule.startswith("tag"):
            return _fetch_all_tags(engine)
        if rule.startswith("phone("):
            name = parts[1] if len(parts) > 1 else ""
            phones = _fetch_contact_phones(engine, name) if name else []
            if first == "add-phone":
                return PHONE_MASKS + phones
            return phones
        if rule.startswith("email("):
            name = parts[1] if len(parts) > 1 else ""
            return _fetch_contact_emails(engine, name) if name else []
        if rule.startswith("note-fragment"):
            return _fetch_notes_texts(engine)
        if rule.startswith("days"):
            return ["3", "7", "14", "30"]
        if rule.startswith("date"):
            return ["YYYY-MM-DD"]
        if rule.startswith("phone-new"):
            return PHONE_MASKS
        # free 
        return []

    return CLIAutoSuggest(_get_candidates)
