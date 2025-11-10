from __future__ import annotations
from typing import Iterable, Optional, List
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from prompt_toolkit.document import Document
from sqlalchemy import Engine

from data.contact_queries import ContactQueries
from data.phone_queries import PhoneQueries

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
    "get-notes", "add-note", "edit-note", "delete-note", "add-tag-to-note", "remove-tag-from-note",
]

# ----------------------- Провайдеры данных -----------------------

def _fetch_contact_names(engine: Engine) -> list[str]:
    try:
        q = ContactQueries(engine)
        return [c.name for c in q.get_contacts()]
    except Exception:
        return []

def _fetch_contact_phones(engine: Engine, contact_name: str) -> list[str]:
    try:
        contact = next((c for c in ContactQueries(engine).get_contacts() if c.name == contact_name), None)
        if not contact:
            return []
        phones: list[str] = []
        for p in getattr(contact, "phones", []) or []:
            if isinstance(p, str):
                phones.append(p)
            elif hasattr(p, "phone_number"):
                phones.append(getattr(p, "phone_number"))
        return sorted(set(phones))
    except Exception:
        return []

def _fetch_contact_emails(engine: Engine, contact_name: str) -> list[str]:
    try:
        contact = next((c for c in ContactQueries(engine).get_contacts() if c.name == contact_name), None)
        if not contact:
            return []
        emails: list[str] = []
        for e in getattr(contact, "emails", []) or []:
            if isinstance(e, str):
                emails.append(e)
            elif hasattr(e, "email"):
                emails.append(getattr(e, "email"))
        return sorted(set(emails))
    except Exception:
        return []

def _fetch_all_tags(engine: Engine) -> list[str]:
    tags: set[str] = set()
    try:
        cq = ContactQueries(engine)
        for c in cq.get_contacts():
            for t in getattr(c, "tags", []) or []:
                if isinstance(t, str):
                    tags.add(t)
                elif hasattr(t, "name"):
                    tags.add(getattr(t, "name"))
    except Exception:
        pass
    # Если позже появится DAL для заметок — можно сюда добавить сбор тегов заметок.
    return sorted(tags)

def _fetch_notes_texts(engine: Engine) -> list[str]:
    # Если у тебя нет DAL для заметок — оставляем пусто (меню просто не будет появляться).
    # Когда появится NoteQueries, верни список текстов заметок.
    return []

def _prefix_match(items: Iterable[str], prefix: str) -> list[str]:
    p = (prefix or "").lower()
    return [x for x in items if x.lower().startswith(p)]

# ----------------------- Правила по аргументам -----------------------
# Позиции считаются с 1 после команды.
COMPLETION_RULES: dict[str, List[str]] = {
    # Contacts
    "get-contacts":                 ["tag?"                 ],
    "get-contact":                  ["name!"                ],
    "add-contact":                  ["free!"                ],
    "edit-contact":                 ["name!", "free!"       ],
    "delete-contact":               ["name!"                ],
    "add-tag-to-contact":           ["name!", "tag!"        ],
    "remove-tag-from-contact":      ["name!", "tag!"        ],
    "get-contact-notes":            ["name!", "tag?"        ],

    # Phones
    "get-phones":                   ["name!"                ],
    "add-phone":                    ["name!", "free!"       ],
    "edit-phone":                   ["name!", "phone(name)!", "free!" ],
    "delete-phone":                 ["name!", "phone(name)!"          ],

    # Emails
    "get-emails":                   ["name!"                ],
    "add-email":                    ["name!", "free!"       ],
    "edit-email":                   ["name!", "email(name)!", "free!" ],
    "delete-email":                 ["name!", "email(name)!"          ],

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
}

# ----------------------- AutoSuggest -----------------------

class CLIAutoSuggest(AutoSuggest):
    def __init__(self, get_candidates):
        # get_candidates(text, cursor_pos, word_index, current_prefix) -> list[str]
        self.get_candidates = get_candidates

    def get_suggestion(self, buffer, document: Document) -> Optional[Suggestion]:
        text = document.text
        before = document.current_line_before_cursor
        parts = before.split()
        idx_in_line = len(parts) - 1 if before and not before.endswith(" ") else len(parts)
        if idx_in_line < 0:
            return None

        current_prefix = ""
        if before and not before.endswith(" "):
            current_prefix = parts[-1]

        cands = self.get_candidates(text, document.cursor_position, idx_in_line, current_prefix)
        if not cands:
            return None

        matches = _prefix_match(cands, current_prefix) if current_prefix else cands
        if len(matches) != 1:
            return None

        only = matches[0]
        if len(only) <= len(current_prefix):
            return None

        remainder = only[len(current_prefix):]
        return Suggestion(remainder)

# ----------------------- Completer -----------------------

class CLICompleter(Completer):
    def __init__(self, engine: Engine, commands: list[str]):
        self.engine = engine
        self.commands = sorted(set(commands or BUILTIN_COMMANDS))

    def get_completions(self, document: Document, complete_event) -> Iterable[Completion]:
        text = document.text_before_cursor
        if not text:
            for cmd in self.commands:
                yield Completion(cmd, start_position=0, display=cmd)
            return

        line = text
        parts = line.split()
        at_word_boundary = line.endswith(" ")
        word_index = len(parts) if at_word_boundary else len(parts) - 1
        current_prefix = "" if at_word_boundary else (parts[-1] if parts else "")

        def complete_words(words: Iterable[str]):
            for w in sorted(set(words)):
                yield Completion(w, start_position=-len(current_prefix), display=w)

        # 0 — команда
        if word_index == 0:
            yield from complete_words(_prefix_match(self.commands, current_prefix))
            return

        # дальше — по правилам команды
        first = parts[0].lower() if parts else ""
        if not first:
            return

        rules = COMPLETION_RULES.get(first)
        if not rules:
            return

        arg_pos = word_index  # 1..N
        if arg_pos <= 0 or arg_pos > len(rules):
            return

        rule = rules[arg_pos - 1].strip().lower()

        # Провайдеры по правилу
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
            yield from complete_words(_prefix_match(phones, current_prefix))
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

        # free / unknown — ничего не подсказываем
        return

# ----------------------- Фабрики -----------------------

def build_completer(engine: Engine, all_commands: list[str]) -> CLICompleter:
    return CLICompleter(engine, all_commands)

def build_auto_suggest(engine: Engine, all_commands: list[str]) -> CLIAutoSuggest:
    completer = CLICompleter(engine, all_commands)

    def _get_candidates(full_text: str, cursor_pos: int, word_index: int, prefix: str) -> list[str]:
        # 0 — команды
        if word_index == 0:
            return list(completer.commands)

        # Аргументы — тот же провайдинг, что и в Completer (без форматирования)
        parts = full_text[:cursor_pos].split()
        first = parts[0].lower() if parts else ""
        rules = COMPLETION_RULES.get(first)
        if not rules:
            return []

        arg_pos = word_index  # 1..N
        if arg_pos <= 0 or arg_pos > len(rules):
            return []

        rule = rules[arg_pos - 1].strip().lower()

        if rule.startswith("name"):
            return _fetch_contact_names(engine)
        if rule.startswith("tag"):
            return _fetch_all_tags(engine)
        if rule.startswith("phone("):
            name = parts[1] if len(parts) > 1 else ""
            return _fetch_contact_phones(engine, name) if name else []
        if rule.startswith("email("):
            name = parts[1] if len(parts) > 1 else ""
            return _fetch_contact_emails(engine, name) if name else []
        if rule.startswith("note-fragment"):
            return _fetch_notes_texts(engine)
        if rule.startswith("days"):
            return ["3", "7", "14", "30"]
        if rule.startswith("date"):
            return ["YYYY-MM-DD"]
        # free / unknown
        return []

    return CLIAutoSuggest(_get_candidates)
