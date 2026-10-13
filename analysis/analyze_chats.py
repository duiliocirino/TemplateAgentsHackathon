#!/usr/bin/env python3
"""Analyze Copilot Chat exports from the hackathon to find coordination/efficiency issues."""
import json, os, re, sys
from collections import Counter, defaultdict
from datetime import datetime

ROOT = r"C:/Users/d.cirino/Documents/Git Projects/team-mi-nq0or3/export-chat"
OUT = r"C:/Users/d.cirino/Documents/Git Projects/TemplateAgentsHackathon/analysis"

FILES = [
    "d.cirino/chat1.json",
    "d.cirino/chat2.json",
    "FabioArosio.json",
    "m.pazienza/MichelePazienza1.json",
    "m.pazienza/MichelePazienza2.json",
    "s.zuccarella/chat1.json",
    "s.zuccarella/chat2.json",
    "s.zuccarella/chat3.json",
    "ValeriaFroio.json",
]

def ts(ms):
    return datetime.fromtimestamp(ms/1000).strftime("%Y-%m-%d %H:%M:%S")

def part_text(p):
    for key in ("text", "value"):
        v = p.get(key)
        if isinstance(v, str):
            return v
        if isinstance(v, dict):
            return str(v.get("value", ""))
    return ""

def msg_text(m):
    if not m:
        return ""
    t = m.get("text")
    if isinstance(t, str) and t:
        return t
    parts = m.get("parts") or []
    return " ".join(p.get("text", "") for p in parts if isinstance(p, dict))

all_sessions = []
user_msgs = defaultdict(list)     # who -> [(ts, text)]
git_cmds = Counter()              # normalized git subcommand -> count
git_conflict_hits = []            # (who, ts, cmd)
edited_files = Counter()          # filename -> count of edit groups touching it
coord_file_edits = defaultdict(Counter)  # who -> Counter(coord file)
tool_usage = Counter()
conflict_mentions = []            # (who, ts, snippet) from user msgs + agent text
thinking_mentions = []
session_spans = []                # (who, start, end)
turn_times = []                   # (who, ts, elapsedMs, promptTokens, completionTokens)
models = Counter()
slash_or_modes = Counter()

GIT_RE = re.compile(r"\bgit\s+([a-z-]+)")
CONFLICT_RE = re.compile(r"conflict|conflitt", re.IGNORECASE)
COORD_NAMES = ("PLAN.md", "DISCUSSION.md", "AGENTS.md")

for rel in FILES:
    path = os.path.join(ROOT, rel)
    who = os.path.dirname(rel) or os.path.basename(rel).replace(".json", "")
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        d = json.load(f)
    reqs = d.get("requests", [])
    sess = {"who": who, "file": rel, "requests": len(reqs),
            "elapsed_ms": 0, "wait_ms": 0, "prompt_tok": 0, "compl_tok": 0,
            "credits": 0.0, "start": None, "end": None}
    for r in reqs:
        t = r.get("timestamp") or 0
        if t:
            sess["start"] = min(sess["start"] or t, t)
            sess["end"] = max(sess["end"] or t, t)
        sess["elapsed_ms"] += r.get("elapsedMs") or 0
        sess["wait_ms"] += r.get("timeSpentWaiting") or 0
        sess["prompt_tok"] += r.get("promptTokens") or 0
        sess["compl_tok"] += r.get("completionTokens") or 0
        sess["credits"] += r.get("copilotCredits") or 0
        models[r.get("modelId")] += 1
        mi = r.get("modeInfo") or {}
        slash_or_modes[mi.get("kind")] += 1
        # user message
        ut = msg_text(r.get("message"))
        if ut.strip():
            user_msgs[who].append((t, ut))
            if CONFLICT_RE.search(ut):
                conflict_mentions.append((who, ts(t), ut[:400]))
        # response parts
        for p in r.get("response", []):
            kind = p.get("kind")
            if kind == "toolInvocationSerialized":
                tid = p.get("toolId") or "?"
                tool_usage[tid] += 1
                if tid in ("run_in_terminal", "get_terminal_output"):
                    im = p.get("invocationMessage")
                    s = im.get("value", "") if isinstance(im, dict) else (im if isinstance(im, str) else "")
                    for m2 in GIT_RE.finditer(s or ""):
                        git_cmds[m2.group(1)] += 1
                    if CONFLICT_RE.search(s or ""):
                        git_conflict_hits.append((who, ts(t), (s or "")[:300]))
                elif tid in ("runInTerminal", "run_in_terminal"):
                    pass
            elif kind == "textEditGroup":
                uri = p.get("uri") or {}
                fs = uri.get("fsPath", "")
                name = fs.replace("\\", "/").split("/")[-1] if fs else "?"
                edited_files[name] += 1
                for c in COORD_NAMES:
                    if name == c:
                        coord_file_edits[who][c] += 1
            elif kind in ("text", "thinking"):
                txt = p.get("text") or ""
                if CONFLICT_RE.search(txt):
                    (thinking_mentions if kind == "thinking" else conflict_mentions).append(
                        (who, ts(t), txt[:300]))
    all_sessions.append(sess)
    if sess["start"]:
        session_spans.append((who, sess["start"], sess["end"]))

# ---------- report ----------
print("=" * 100)
print("SESSION OVERVIEW")
print("=" * 100)
tot_elapsed = tot_wall = 0
for s in sorted(all_sessions, key=lambda x: x["start"] or 0):
    wall = (s["end"] - s["start"]) / 3600000 if s["start"] else 0
    tot_elapsed += s["elapsed_ms"] / 3600000
    tot_wall += wall
    print(f"{s['who']:<14} {s['file']:<32} turns={s['requests']:>3}  "
          f"{ts(s['start'])} -> {ts(s['end'])}  wall={wall:5.1f}h  "
          f"agent={s['elapsed_ms']/3600000:5.1f}h  wait={s['wait_ms']/60000:6.1f}m  "
          f"tok(p/c)={s['prompt_tok']//1000}k/{s['compl_tok']//1000}k  credits={s['credits']:.0f}")
print(f"\nTOTAL wall={tot_wall:.1f}h  agent-time={tot_elapsed:.1f}h")
print("models:", dict(models))
print("tool usage:", tool_usage.most_common(20))

print()
print("=" * 100)
print("GIT COMMANDS (from terminal tool calls)")
print("=" * 100)
print(git_cmds.most_common(30))
print(f"\ngit/terminal outputs mentioning conflicts: {len(git_conflict_hits)}")
for w, t, s in git_conflict_hits[:25]:
    print(f"  [{w} {t}] {s[:200]}")

print()
print("=" * 100)
print("CONFLICT MENTIONS IN USER/AGENT TEXT")
print("=" * 100)
print(f"total: {len(conflict_mentions)}")
for w, t, s in conflict_mentions[:40]:
    print(f"\n[{w} {t}] {s[:350]}")

print()
print("=" * 100)
print("COORDINATION FILE EDITS (textEditGroup per person)")
print("=" * 100)
for w, c in coord_file_edits.items():
    print(f"{w}: {dict(c)}")
print("\nTop edited files overall:")
for name, n in edited_files.most_common(25):
    print(f"  {n:>4}  {name}")

# ---------- dump user messages per person ----------
os.makedirs(OUT, exist_ok=True)
for who, msgs in user_msgs.items():
    safe = who.replace("/", "_").replace("\\", "_")
    with open(os.path.join(OUT, f"prompts_{safe}.txt"), "w", encoding="utf-8") as f:
        for t, m in sorted(msgs):
            f.write(f"\n===== [{ts(t)}] =====\n{m}\n")
    print(f"wrote prompts_{safe}.txt ({len(msgs)} prompts)")

# ---------- timeline overlap ----------
print()
print("=" * 100)
print("ACTIVITY TIMELINE (overlaps = collision risk)")
print("=" * 100)
events = []
for w, a, b in session_spans:
    events.append((a, 1, w)); events.append((b, -1, w))
events.sort()
active = set()
for e, delta, w in events:
    before = set(active)
    if delta == 1:
        active.add(w)
    else:
        active.discard(w)
    if delta == 1 and before:
        print(f"  {ts(e)}  {w} joins while {sorted(before)} active -> {len(active)} concurrent")
