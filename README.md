# Personal Assistant

A command-line personal assistant for managing contacts, notes, and reminders with support for tags, birthdays, and smart search.

## Features

- **Contact Management**: Store contacts with names, phones, emails, and birthdays
- **Note Management**: Create standalone or contact-linked notes
- **Tag System**: Organize contacts and notes with custom tags
- **Birthday Reminders**: Get notified of upcoming birthdays
- **Data Persistence**: All data stored in SQLite database (`~/contacts.db`)
- **Interactive CLI**: Command history, autocomplete
- **REST API**: REST API with frontend
- **MCP Server**: MCP server for LLM integration

## Requirements

- Python >= 3.13

## Installation

```bash
# Clone the repository
cd goit-pycore-final

# Install dependencies
uv sync
```

## Usage

### CLI Mode (Default)

```bash
uv run main.py
```

### API Mode

```bash
uv run main.py --api
```

API is available at `http://localhost:8000`

MCP server is available at `http://localhost:8000/mcp`, transport SSE

## Setup MCP in Claude Code

```bash
claude mcp add --transport sse magic-8 https://magic-8.azurewebsites.net/mcp/ # Hosted
claude mcp add --transport sse magic-8 http://localhost:8000/mcp/ # Local
claude mcp list # Verify MCP installed correctly
claude --model haiku # Haiku is recommended model
```

## Available Commands

### Contacts
- `add-contact <name> <phone>` - Add new contact (phone: 10 digits)
- `get-contacts [tag]` - List all contacts or filter by tag
- `get-contact <name>` - Show contact details
- `edit-contact <name> <new-name>` - Rename contact
- `delete-contact <name>` - Delete contact
- `add-tag-to-contact <name> <tag>` - Add tag to contact
- `remove-tag-from-contact <name> <tag>` - Remove tag from contact

### Phones
- `add-phone <contact-name> <phone>` - Add phone to contact
- `get-phones <contact-name>` - List contact's phones
- `edit-phone <contact-name> <old-phone> <new-phone>` - Update phone number
- `delete-phone <contact-name> <phone>` - Remove phone

### Emails
- `add-email <contact-name> <email>` - Add email to contact
- `get-emails <contact-name>` - List contact's emails
- `edit-email <contact-name> <old-email> <new-email>` - Update email
- `delete-email <contact-name> <email>` - Remove email

### Birthdays
- `add-birthday <name> <YYYY-MM-DD>` - Set birthday
- `remove-birthday <name>` - Remove birthday
- `get-birthdays <days>` - Show birthdays in next N days

### Notes
- `add-note <text> <tag>` - Create standalone note
- `add-note-to-contact <name> <text> <tag>` - Add note to contact
- `get-notes [tag]` - List all notes or filter by tag
- `get-contact-notes <name> [tag]` - List contact's notes
- `edit-note <fragment> <new-text>` - Update note by text fragment
- `delete-note <fragment>` - Delete note by text fragment
- `add-tag-to-note <fragment> <tag>` - Add tag to note
- `remove-tag-from-note <fragment> <tag>` - Remove tag from note

### General
- `hello` - Greeting
- `exit` or `close` - Quit application
- `history-clear` - Clear command history

## Examples

```bash
# Add contact
add-contact "John Doe" 1234567890

# Add birthday
add-birthday "John Doe" 1990-05-15

# Add email
add-email "John Doe" john@example.com

# Add tag
add-tag-to-contact "John Doe" family

# Find contacts by tag
get-contacts family

# Check upcoming birthdays
get-birthdays 7

# Add note with tag
add-note "Buy groceries" todo

# Search notes by tag
get-notes todo
```

## Data Validation

- **Phone numbers**: Exactly 10 digits (e.g., `1234567890`)
- **Emails**: Standard format (e.g., `user@domain.com`)
- **Dates**: ISO format `YYYY-MM-DD` (e.g., `1990-05-15`)

## CLI Features

- **Tab completion**: Press Tab to see available commands
- **Command history**: Use ↑/↓ arrows to navigate history
- **Auto-suggest**: Type to see suggestions from history
- **Colored output**: Green (success), yellow (warning), red (error)

## Database

Data is stored in SQLite database at `~/contacts.db`. The database is created automatically on first run.

## Project Structure

```
├── cli/           # Command-line interface
├── data/          # Database models and operations (SQLAlchemy, pydantic)
├── api/           # REST API (FastAPI)
├── llm/           # LLM integration (FastMCP)
├── tests/         # Unit tests (pytest)
└── main.py        # Entry point
```

## Running Tests

```bash
uv run pytest
```
