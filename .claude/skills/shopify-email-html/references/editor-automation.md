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

## Lessons from the 2026-10-03 re-sync (CR-2 to CR-4)

- **Typing a whole Code your own email** works reliably in two `type` calls of ≈10–12 KB each,
  split at a card boundary (`</td></tr></table>` line). Strip leading indentation first (the editor
  adds none, and whitespace is irrelevant in this HTML). Verify each call's reported character count
  against the expected length computed locally — an exact match on both halves is the check.
- **Edit email** in the Flow side panel: the first click sometimes only scrolls the panel. Scroll the
  panel to the top and click the button again; wait about 8 seconds for the editor to load.
- **Exit**: find the "Exit" element with `find` and click its ref (coordinate clicks miss). The
  "Leave email in draft state?" dialog's **Leave** button sits at about (519, 326) in an 800×599
  frame; a `find` ref for it is reported off-screen, so click by coordinate.
- **Subject / Preview text**: scroll the preview pane to the very top first. If it is scrolled,
  a click at the Subject position lands on the preview instead and typing goes nowhere.
- **Check the Subject on every email**: CR-4's was empty (the email showed as "Untitled Activity").
- **Flow canvas**: never start a pan-drag on or near a step. A drag that starts on a step moves it
  (the wiring stays, the position is saved, and undo does not revert it). Pan from empty canvas
  far from any node, or use the zoom/fit buttons at bottom-left. If a step was moved, drag it back;
  each drag moves it only about half the pointer distance at reduced zoom.

## Lessons from the 2026-10-04 build (W-1 as sections)

- **Sections email from a Flow step**: Select template → **Blank** → Select. The editor opens with a
  stock Header, a footer and the **Add section** menu already open. Menu items sit in groups
  (Elements, Product, Reengagement, Layout, **Custom** last): search "Custom Liquid" or click the last
  item. Frame coordinates (800×651): Add section pill ≈ (197, 631), Custom Liquid item ≈ (176, 607)
  when the menu is open, code box ≈ (90, 230).
- **One section per fragment**: type fragment 01, Add section → Custom Liquid, type 02, and so on. The
  reported character count equals the file size minus indentation and the trailing newline.
- **Editing one section later**: click the section's padding in the preview (not its text) so the left
  panel shows "Custom Liquid", click the code box, cmd+a, Delete, retype.
- **Hide the Header**: click the Header in the preview (it can take two screenshots to show the
  selection), then the eye icon at the right edge of the header. The preview then shows "Header hidden".
- **Content background**: click empty canvas → "Email colors" → click the Content background swatch →
  triple-click the hex field → type `transparent` → Enter. It is stored as `RGBA(0,0,0,0)`.
- **Redraw lag**: the editor updates about a second after a click. A screenshot taken at once can show
  the previous selection or panel; wait 2-3 seconds before deciding that a click missed.
- **Exit**: the "Leave email in draft state?" dialog appears a few seconds after clicking Exit;
  **Leave** sits at ≈ (530, 353).
- **Shopify Sidekick** (Flow page): see `flow-recipes.md`. In the Sidekick panel, click the input via a
  `find` ref before typing, or the text goes nowhere.
