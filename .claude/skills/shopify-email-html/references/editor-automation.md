# Driving the Shopify editors from an automated browser

Applies to the Claude built-in browser pane (and Claude in Chrome). Coordinates below are from an
800×599 screenshot frame; re-check with a screenshot because panels shift.

## What works and what does not

| Action | Notification editor (same origin) | Messaging editor / Flow (cross-origin iframe) |
|---|---|---|
| JS read/write of the code | Yes — `.cm-content` → `.cmView.view` | No |
| `type` action into code box | Works | Works (no auto-closing of tags/quotes observed) |
| cmd+v paste from system clipboard | No (synthetic keys don't paste) | No |
| `navigator.clipboard.readText()` | Permission denied | — |
| Fetch from `127.0.0.1` local server | Blocked | — |
| Native `<select>` (Flow wait unit) | — | Will not open; use seconds |
| Flow step copy/paste (cmd+c/cmd+v) | — | Paste does nothing |

## Notification editor: inject instead of typing

`python3 scripts/pack_for_injection.py <file>` prints a snippet that gunzips a base64 payload,
replaces the CodeMirror document in one transaction (`userEvent: 'input.paste'` so Shopify flags
"Unsaved changes"), and returns `{hash, match}`. Compare the hash with the script's printed
prefix. Then Preview → Save.

Read the rendered preview text for checking:
`[...document.querySelectorAll('iframe')].map(i=>i.contentDocument.body.innerText)`.

## Messaging editor

- Code box focus: click inside it, then cmd+a, Delete before typing a replacement.
- Large payloads: one `type` action handles 20 KB; keep each email/section in one call.
- Selecting a section: click on an empty part of it (padding), not on text — clicking text
  enters inline text editing. Hover the section to reveal the copy/trash icons at its top-right;
  the Header shows an eye (hide) icon instead.
- Add section: the "+ Add section" pill bottom-left → menu → *Custom* → **Custom Liquid** (last
  item). New sections append after the last section, above the Shopify footer.
- Search/replace inside a code box (CodeMirror panel): click code → cmd+f → cmd+a → type the
  search → **triple-click** the Replace field → type → click **replace all**. The panel closes after
  replace all. Do exactly one replacement per opening; chaining several without re-opening sent
  keystrokes into the document.
- Exiting: Exit (top-left) → "Leave email in draft state?" → **Leave**.
- "⋯" menu next to Send test did not open under automation; don't rely on it.
- Subject / Preview text fields are plain inputs: click, cmd+a, type.

## Flow editor

- Pan the canvas with `left_click_drag` on empty space; wheel scrolling is unreliable.
- Add a step: click the grey nub under a step (or under True/False) → **Action** or **Condition**.
- Action search box: click it, type the action name ("Wait", "Send marketing email").
- Conditions: Add a variable → search the field name (e.g. `customerHasNoOrder`) → pick → set the
  value radio (True). The variable search box sometimes needs an extra click before typing.
- Wait: amount field + unit `<select>`; the select is unusable under automation, so type seconds
  (1 h = 3600, 1 day = 86400).
- Steps show a blue "Review" badge until their email is configured; that is expected for drafts.
- The canvas autosaves ("Saved · Last changed …"). Turning the workflow on is a separate,
  explicit button — never click it without approval.

## Clipboard side effects

Some Flow/Messaging clicks fire page copy handlers that overwrite the user's OS clipboard. Tell the
user to check their clipboard before pasting.
