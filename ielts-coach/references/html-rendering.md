# HTML Answer Page (ielts_answers.html)

Loaded from SKILL.md Phase 3. Start from `assets/answer_template.html`.

After each session, update the local HTML file `ielts_answers.html` in the project directory.

## Step 3.1: Check if HTML file exists

- If no `ielts_answers.html` exists → create the full page with CSS framework
- If it exists → update the existing file: expand the new day's section, collapse older days

## Step 3.2: HTML Design Requirements

The HTML page must be:
- **Beautiful & modern** — Use a clean, reading-friendly design
- **Collapsible by day** — Each day is a `<details>` card; only the latest day is expanded by default, older days are collapsed
- **Highlight-rich** — Key expressions visually distinct (colored badges/cards)
- **Responsive** — Works on desktop and mobile
- **Printable** — The user may want to print for offline review
- **No navigation bar needed** — The collapsible layout replaces the need for a filter/nav bar

## Step 3.3: HTML Structure (Collapsible Day Cards)

The page uses native HTML `<details>/<summary>` elements for each day. This provides
built-in expand/collapse without JavaScript dependencies.

```
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>IELTS Coach - My Model Answers</title>
  <style>
    /* Complete CSS embedded */
    /* Day card: <details> with styled <summary> header */
    /* Summary shows: day number circle, date, status badge, topic pills, chevron */
    /* Content area: answer cards nested inside */
  </style>
</head>
<body>
  <header>
    <!-- Exam countdown, target scores, progress bar -->
  </header>
  <main>
    <!-- Each day as a collapsible <details class="day-card"> -->
    <details class="day-card completed" open>  <!-- open = expanded by default -->
      <summary>
        <div class="day-number">D1</div>
        <div class="day-info">
          <div class="day-title">Day 1 <span class="status-badge done">✓ Completed</span></div>
          <div class="day-date">July 7, 2026</div>
          <div class="day-topics-preview">
            <span class="topic-pill p1">🎤 Part 1: Work or Studies</span>
            <span class="topic-pill p2">🎙️ Part 2: An Interesting Video</span>
          </div>
        </div>
        <span class="chevron">▸</span>
      </summary>
      <div class="day-content">
        <!-- Answer cards for this day -->
      </div>
    </details>
    <!-- More days... -->
  </main>
</body>
</html>
```

**Key rules for the collapsible layout:**
- Use `<details class="day-card">` for each day — no JavaScript needed for expand/collapse
- Add `open` attribute to the most recent day so it's expanded by default
- Older days have no `open` attribute — they stay collapsed
- The `<summary>` header shows: day number (green circle if completed, gray if pending), date, status badge, topic pills, and a chevron arrow that rotates on expand
- Topic pills use the same color coding as answer cards (teal for P1, coral for P2/P3, gold for writing)
- On mobile, hide topic pills to save space — show only day number, title, and status

## Step 3.4: Design Elements

Use these visual elements:
- **Header**: Navy blue (#1a237e) background with gold (#ffc107) accents
- **Day cards**: White cards with rounded corners and subtle shadows
- **Day number**: 44px circle with gradient (green = completed, gray = pending)
- **Topic pills**: Small rounded badges in the summary header (color-coded by type)
- **Answer cards**: Nested inside day content area, lighter background (#fafbfc)
- **Highlight badges**: Gradient background cards for vocabulary/expressions
- **Band score indicator**: Color-coded tag showing target band
- **Copy button**: Small button to copy each answer
- **Icons**: Use emoji for sections (🎤 Speaking, ✍️ Writing, 📅 Date, 🎯 Target)
- **Chevron**: ▸ arrow that rotates 90° when expanded
