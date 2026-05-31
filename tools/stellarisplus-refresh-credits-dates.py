#!/usr/bin/env python3
"""Refresh Last updated dates in credits.md from git history."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

WORKSHOP_ID_RE = re.compile(r"Workshop ID:\s*(\d+)")
LAST_UPDATED_RE = re.compile(r"^(\s*)Last updated:\s*\d{4}-\d{2}-\d{2}\s*$")


def git(repo_root: Path, *args: str) -> str:
	result = subprocess.run(
		["git", *args],
		capture_output=True,
		text=True,
		check=False,
		cwd=repo_root,
	)
	return result.stdout.strip()


def max_date(*dates: str) -> str:
	valid = [date for date in dates if date and len(date) == 10 and date[4] == "-" and date[7] == "-"]
	return max(valid) if valid else ""


def load_probes(tools_dir: Path) -> dict:
	path = tools_dir / "credits_date_probes.json"
	with path.open(encoding="utf-8") as handle:
		return json.load(handle)


def resolve_mod_probes(workshop_id: str, probes: dict) -> tuple[list[str], list[str]]:
	mod_probe = probes.get("mods", {}).get(workshop_id, {})
	group_name = mod_probe.get("group")
	group_probe = probes.get("groups", {}).get(group_name, {}) if group_name else {}
	grep_terms = list(mod_probe.get("grep", [])) + list(group_probe.get("grep", []))
	paths = list(mod_probe.get("paths", [])) + list(group_probe.get("paths", []))
	if workshop_id not in grep_terms:
		grep_terms.append(workshop_id)
	return grep_terms, paths


def last_updated_for_mod(repo_root: Path, workshop_id: str, probes: dict) -> str:
	dates: list[str] = []
	pickaxe = git(repo_root, "log", "-1", "--format=%ad", "--date=short", "-S" + workshop_id, "--", ".")
	if pickaxe:
		dates.append(pickaxe)
	grep_terms, paths = resolve_mod_probes(workshop_id, probes)
	for term in grep_terms:
		grep_date = git(
			repo_root,
			"log",
			"-1",
			"--format=%ad",
			"--date=short",
			"--grep=" + term,
			"-i",
			"--all",
		)
		if grep_date:
			dates.append(grep_date)
	existing_paths = [path for path in paths if (repo_root / path).exists()]
	if existing_paths:
		path_date = git(
			repo_root,
			"log",
			"-1",
			"--format=%ad",
			"--date=short",
			"--",
			*existing_paths,
		)
		if path_date:
			dates.append(path_date)
	return max_date(*dates)


def parse_entries(text: str) -> tuple[str, list[dict]]:
	lines = text.splitlines()
	prefix_end = 0
	for index, line in enumerate(lines):
		if line.strip() == "Integrated Workshop mods:":
			prefix_end = index + 1
			while prefix_end < len(lines) and lines[prefix_end].strip() == "":
				prefix_end += 1
			break
	prefix_lines = lines[:prefix_end]
	body_lines = lines[prefix_end:]
	entries: list[dict] = []
	current: dict | None = None
	for line in body_lines:
		if line.startswith("- "):
			if current is not None:
				entries.append(current)
			current = {"title_lines": [line], "detail_lines": []}
			continue
		if current is None:
			continue
		if line.strip() == "":
			continue
		if LAST_UPDATED_RE.match(line):
			current["detail_lines"].append({"kind": "last_updated", "indent": LAST_UPDATED_RE.match(line).group(1)})
		else:
			current["detail_lines"].append(line)
	if current is not None:
		entries.append(current)
	return "\n".join(prefix_lines), entries


def normalize_prefix(prefix: str) -> str:
	lines = [
		"# StellarisPlus -- Credits",
		"",
		"The following Workshop mods have been integrated into StellarisPlus.",
		"Their original authors are credited below.",
		"",
		"Last updated dates are derived from git commit history (initial integration",
		"and subsequent content changes).",
		"",
		"Integrated Workshop mods:",
	]
	return "\n".join(lines)


def workshop_id_from_entry(entry: dict) -> str | None:
	for line in entry["title_lines"]:
		match = WORKSHOP_ID_RE.search(line)
		if match:
			return match.group(1)
	for line in entry["detail_lines"]:
		if isinstance(line, str):
			match = WORKSHOP_ID_RE.search(line)
			if match:
				return match.group(1)
	return None


def set_last_updated(entry: dict, date: str) -> None:
	filtered: list = []
	for item in entry["detail_lines"]:
		if isinstance(item, dict) and item.get("kind") == "last_updated":
			continue
		filtered.append(item)
	entry["detail_lines"] = [{"kind": "last_updated", "indent": "  ", "date": date}, *filtered]


def render_entries(entries: list[dict]) -> str:
	lines: list[str] = []
	for entry in entries:
		lines.extend(entry["title_lines"])
		for item in entry["detail_lines"]:
			if isinstance(item, dict) and item.get("kind") == "last_updated":
				lines.append(f"{item['indent']}Last updated: {item['date']}")
			else:
				lines.append(item)
		lines.append("")
	while lines and lines[-1] == "":
		lines.pop()
	return "\n".join(lines)


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument(
		"--credits",
		type=Path,
		default=Path("credits.md"),
		help="Path to credits.md (default: repo-root credits.md)",
	)
	parser.add_argument("--dry-run", action="store_true", help="Print dates without writing")
	parser.add_argument("--check", action="store_true", help="Exit 1 if credits.md is stale")
	args = parser.parse_args()

	repo_root = Path(__file__).resolve().parent.parent
	tools_dir = Path(__file__).resolve().parent
	credits_path = args.credits if args.credits.is_absolute() else repo_root / args.credits
	probes = load_probes(tools_dir)
	original = credits_path.read_text(encoding="utf-8")
	_, entries = parse_entries(original)
	changes: list[tuple[str, str, str]] = []
	for entry in entries:
		workshop_id = workshop_id_from_entry(entry)
		if workshop_id is None:
			continue
		new_date = last_updated_for_mod(repo_root, workshop_id, probes)
		if not new_date:
			print(f"warning: no git date found for Workshop ID {workshop_id}", file=sys.stderr)
			continue
		old_date = ""
		for item in entry["detail_lines"]:
			if isinstance(item, dict) and item.get("kind") == "last_updated":
				old_date = item.get("date", "")
				break
		if old_date != new_date:
			changes.append((workshop_id, old_date or "(missing)", new_date))
		set_last_updated(entry, new_date)
	new_text = normalize_prefix("") + "\n\n" + render_entries(entries) + "\n"
	if args.dry_run or args.check:
		for workshop_id, old_date, new_date in changes:
			print(f"{workshop_id}: {old_date} -> {new_date}")
		if args.check and changes:
			return 1
		return 0
	if new_text != original:
		credits_path.write_text(new_text, encoding="utf-8", newline="\r\n")
		for workshop_id, old_date, new_date in changes:
			print(f"updated {workshop_id}: {old_date} -> {new_date}")
	else:
		print("credits.md dates are already current")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
