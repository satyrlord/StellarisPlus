#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Paradox Script structural validator for Stellaris mods.

Tokenizes .txt / .gfx / .gui / .yml files correctly (handling comments,
quoted strings, inline math, parameter placeholders) and runs checks:

  1. Brace balance per file
  2. Duplicate top-level object keys within the same common/ subfolder
  3. @variable definitions vs references (undefined / unused / shadowed)
  4. GFX sprite definitions vs GUI/script references
  5. textureFile paths pointing to existing DDS files
  6. Duplicate localisation keys
  7. Localisation file format (language header, UTF-8 BOM)
    8. Non-localisation Paradox script files must be UTF-8 without BOM

Usage:
    uv run pdx_validate.py <mod_root> [--check CHECK,...] [--json]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

# ---------------------------------------------------------------------------
# Tokeniser
# ---------------------------------------------------------------------------

# Regex that splits a Paradox Script line into meaningful tokens while
# respecting comments, quoted strings, and @[...] inline math.

_TOKEN_RE = re.compile(
    r"""
    (?P<comment>    \#.*)                       |  # line comment
    (?P<quoted>     "[^"]*")                     |  # double-quoted string
    (?P<inlinemath> @\[[^\]]*\])                 |  # @[ expr ]
    (?P<param>      \$[A-Za-z_][A-Za-z_0-9]*(?:\|[^$]*)?\$)  |  # $PARAM$ or $P|default$
    (?P<paramcond>  \[\[!?[A-Za-z_][A-Za-z_0-9]*\]) |  # [[PARAM] or [[!PARAM]
    (?P<brace>      [{}])                        |  # brace
    (?P<condclose>  \])                          |  # ] closing param condition
    (?P<op>         [<>!=]=?|[?]=)               |  # operators: = != < > <= >= ?=
    (?P<word>       @?[A-Za-z_0-9][A-Za-z_0-9.:@\-]*) |  # word / @var / scope.chain
    (?P<number>     -?\d+(?:\.\d+)?)                # number literal
    """,
    re.VERBOSE,
)


def tokenize(line: str) -> list[tuple[str, str]]:
    """Return [(kind, value), ...] for one line of Paradox Script."""
    tokens: list[tuple[str, str]] = []
    for m in _TOKEN_RE.finditer(line):
        kind = m.lastgroup
        val = m.group()
        if kind is None:
            continue
        if kind == "comment":
            break  # rest of line is comment
        tokens.append((kind, val))
    return tokens


# ---------------------------------------------------------------------------
# File collectors
# ---------------------------------------------------------------------------

_SCRIPT_EXTS = {".txt", ".gfx", ".gui", ".asset"}
_SKIP_DIRS = {"backup", "tmp", ".git", ".github", ".venv"}

_KNOWN_STELLARIS_ROOTS = (
    Path(r"C:/Program Files (x86)/Steam/steamapps/common/Stellaris"),
    Path.home() / ".local/share/Steam/steamapps/common/Stellaris",
    Path.home() / ".steam/steam/steamapps/common/Stellaris",
    Path.home() / "Library/Application Support/Steam/steamapps/common/Stellaris",
)


def _walk(root: Path, exts: set[str]) -> list[Path]:
    """Collect files with given extensions, skipping irrelevant dirs."""
    result: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames if d.lower() not in _SKIP_DIRS
        ]
        for fn in filenames:
            if Path(fn).suffix.lower() in exts:
                result.append(Path(dirpath) / fn)
    return sorted(result)


def _rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


@lru_cache(maxsize=1)
def _get_game_root() -> Path | None:
    """Return the detected Stellaris install root if available."""
    env_candidates = [
        os.environ.get("STELLARIS_VANILLA_DIR", ""),
        os.environ.get("STELLARIS_GAME_DIR", ""),
    ]
    for raw_candidate in env_candidates:
        if not raw_candidate:
            continue
        candidate = Path(raw_candidate).expanduser()
        if (candidate / "stellaris.exe").is_file() and (candidate / "common").is_dir():
            return candidate

    for candidate in _KNOWN_STELLARIS_ROOTS:
        if (candidate / "stellaris.exe").is_file() and (candidate / "common").is_dir():
            return candidate

    return None


@lru_cache(maxsize=1)
def _get_game_content_roots() -> tuple[Path, ...]:
    """Return base-game and DLC roots that can contribute script/assets."""
    game_root = _get_game_root()
    if game_root is None:
        return ()

    content_roots: list[Path] = [game_root]
    dlc_root = game_root / "dlc"
    if dlc_root.is_dir():
        for child in sorted(dlc_root.iterdir()):
            if not child.is_dir():
                continue
            if any((child / section).exists() for section in ("common", "interface", "gfx")):
                content_roots.append(child)

    return tuple(content_roots)


def _content_path_exists(relative_path: str) -> bool:
    """Return True if the relative path exists in the game install or DLC roots."""
    normalised = relative_path.replace("/", os.sep)
    for content_root in _get_game_content_roots():
        if (content_root / normalised).is_file():
            return True
    return False


def _resolve_content_file(relative_path: str) -> Path | None:
    """Return the first matching file from the detected game install or DLC roots."""
    normalised = relative_path.replace("/", os.sep)
    for content_root in _get_game_content_roots():
        candidate = content_root / normalised
        if candidate.is_file():
            return candidate
    return None


@lru_cache(maxsize=1)
def _get_game_scripted_variables() -> set[str]:
    """Collect scripted variable names from the detected game install."""
    variables: set[str] = set()
    for content_root in _get_game_content_roots():
        sv_root = content_root / "common" / "scripted_variables"
        if not sv_root.is_dir():
            continue
        for fp in sorted(sv_root.rglob("*.txt")):
            text = fp.read_text(encoding="utf-8-sig", errors="replace")
            for line in text.splitlines():
                stripped = line.split("#", 1)[0].strip()
                m = _VAR_DEF_RE.match(stripped)
                if m:
                    variables.add(m.group(1))
    return variables


@lru_cache(maxsize=1)
def _get_game_sprite_names() -> set[str]:
    """Collect sprite names from the detected game install and DLCs."""
    names: set[str] = set()
    for content_root in _get_game_content_roots():
        interface_root = content_root / "interface"
        if not interface_root.is_dir():
            continue
        for fp in sorted(interface_root.rglob("*.gfx")):
            text = fp.read_text(encoding="utf-8-sig", errors="replace")
            inside_sprite = False
            for line in text.splitlines():
                stripped = line.split("#", 1)[0].strip()
                if "spriteType" in stripped and "=" in stripped:
                    inside_sprite = True
                if inside_sprite:
                    m = _GFX_NAME_RE.search(stripped)
                    if m:
                        names.add(m.group(1))
    return names


# ---------------------------------------------------------------------------
# Check: brace balance
# ---------------------------------------------------------------------------

def check_brace_balance(root: Path) -> list[dict]:
    """Find files where { and } counts don't match."""
    findings: list[dict] = []
    for fp in _walk(root, _SCRIPT_EXTS):
        text = fp.read_text(encoding="utf-8-sig", errors="replace")
        depth = 0
        first_neg_line = None
        for i, line in enumerate(text.splitlines(), 1):
            for kind, val in tokenize(line):
                if kind == "brace":
                    depth += 1 if val == "{" else -1
                    if depth < 0 and first_neg_line is None:
                        first_neg_line = i
        if depth != 0:
            findings.append({
                "file": _rel(fp, root),
                "severity": "error",
                "check": "brace_balance",
                "message": f"Brace imbalance: depth ends at {depth:+d}",
                "line": first_neg_line or 0,
            })
    return findings


# ---------------------------------------------------------------------------
# Check: duplicate top-level keys within a common/ subfolder
# ---------------------------------------------------------------------------

_EXPECTED_DUPLICATE_SUBFOLDERS = {
    "ambient_objects",
    "component_sets",
    "component_templates",
    "defines",
    "on_actions",
    "special_projects",
    "species_names",
    "start_screen_messages",
}
_EXPECTED_DUPLICATE_KEYS = {
    "scripted_loc": {"defined_text"},
    "terraform": {"terraform_link"},
}


def _iter_top_level_object_keys(text: str) -> list[tuple[str, int]]:
    """Return top-level object keys with their source line numbers."""
    keys: list[tuple[str, int]] = []
    depth = 0
    for i, line in enumerate(text.splitlines(), 1):
        tokens = tokenize(line)
        if (
            depth == 0
            and len(tokens) >= 3
            and tokens[0][0] == "word"
            and tokens[1] == ("op", "=")
            and tokens[2] == ("brace", "{")
            and not tokens[0][1].startswith("@")
        ):
            keys.append((tokens[0][1], i))

        for kind, val in tokens:
            if kind == "brace":
                depth += 1 if val == "{" else -1

    return keys


def _is_expected_duplicate_key(subfolder_name: str, key: str) -> bool:
    """Return True for top-level key patterns Stellaris intentionally merges."""
    if subfolder_name in _EXPECTED_DUPLICATE_SUBFOLDERS:
        return True
    return key in _EXPECTED_DUPLICATE_KEYS.get(subfolder_name, set())


def check_duplicate_keys(root: Path) -> list[dict]:
    """Detect duplicate top-level object names inside each common/ subfolder."""
    findings: list[dict] = []
    common = root / "common"
    if not common.is_dir():
        return findings

    for subfolder in sorted(common.iterdir()):
        if not subfolder.is_dir():
            continue
        # Skip inline_scripts: templates have expected repeated block names
        if subfolder.name == "inline_scripts":
            continue
        key_locations: dict[str, list[tuple[str, int]]] = defaultdict(list)
        for fp in sorted(subfolder.rglob("*.txt")):
            text = fp.read_text(encoding="utf-8-sig", errors="replace")
            for key, line_number in _iter_top_level_object_keys(text):
                if _is_expected_duplicate_key(subfolder.name, key):
                    continue
                key_locations[key].append((_rel(fp, root), line_number))

        for key, locs in sorted(key_locations.items()):
            if len(locs) > 1:
                files_str = "; ".join(f"{f}:{ln}" for f, ln in locs)
                findings.append({
                    "file": _rel(subfolder, root),
                    "severity": "warning",
                    "check": "duplicate_key",
                    "message": (
                        f"Key '{key}' defined {len(locs)} times: "
                        f"{files_str}"
                    ),
                })
    return findings


# ---------------------------------------------------------------------------
# Check: @variable integrity
# ---------------------------------------------------------------------------

_VAR_DEF_RE = re.compile(r"^(@[A-Za-z_][A-Za-z_0-9]*)\s*=")
_VAR_REF_RE = re.compile(r"(?<![A-Za-z_0-9.:-])(@[A-Za-z_][A-Za-z_0-9]*)")
# Variables defined in vanilla Stellaris scripted_variables or by
# commonly-bundled sub-mods.  Last verified against Stellaris v4.3.0.
# Update this set when the game patches or new integrated mods
# introduce additional variables.
_KNOWN_EXTERNAL_VARS = {
    "@EdictMedPrio",
    "@base_district_jobs",
    "@bonus_scaling_district_2_jobs",
    "@bonus_scaling_district_3_jobs",
    "@doubled_scaling_district_2_jobs",
    "@scaling_district_1_job",
    "@scaling_district_2_jobs",
    "@special_district_jobs",
    "@zone_buildtime",
    "@zone_cost",
    "@zone_urban_housing_positive",
}


def check_variable_integrity(root: Path) -> list[dict]:
    """Check @variable definitions vs references across the mod."""
    findings: list[dict] = []

    # Collect all definitions from scripted_variables/
    sv_dir = root / "common" / "scripted_variables"
    defs: dict[str, list[tuple[str, int]]] = defaultdict(list)
    local_defs: dict[str, set[str]] = defaultdict(set)
    if sv_dir.is_dir():
        for fp in sorted(sv_dir.glob("*.txt")):
            text = fp.read_text(encoding="utf-8-sig", errors="replace")
            for i, line in enumerate(text.splitlines(), 1):
                stripped = line.split("#", 1)[0].strip()
                m = _VAR_DEF_RE.match(stripped)
                if m:
                    local_defs[_rel(fp, root)].add(m.group(1))
                    defs[m.group(1)].append((_rel(fp, root), i))

    # Collect file-local @variable definitions from all script files.
    for fp in _walk(root, _SCRIPT_EXTS):
        rel_fp = _rel(fp, root)
        if rel_fp in local_defs:
            continue
        text = fp.read_text(encoding="utf-8-sig", errors="replace")
        for line in text.splitlines():
            stripped = line.split("#", 1)[0].strip()
            m = _VAR_DEF_RE.match(stripped)
            if m:
                local_defs[rel_fp].add(m.group(1))

    # Collect references from script files (skip scripted_variables/ and gfx/)
    # gfx/ .asset files use @ variables defined in vanilla scripted_variables
    refs: dict[str, list[tuple[str, int]]] = defaultdict(list)
    gfx_dir = root / "gfx"
    for fp in _walk(root, _SCRIPT_EXTS):
        # Skip definition files and asset files with vanilla variables
        try:
            fp.relative_to(sv_dir)
            continue
        except (ValueError, TypeError):
            pass
        try:
            fp.relative_to(gfx_dir)
            continue
        except (ValueError, TypeError):
            pass
        text = fp.read_text(encoding="utf-8-sig", errors="replace")
        rel_fp = _rel(fp, root)
        for i, line in enumerate(text.splitlines(), 1):
            # Strip comments
            comment_pos = _find_comment(line)
            code = line[:comment_pos]
            # Skip if this is a definition line (can appear in .txt files)
            if _VAR_DEF_RE.match(code.strip()):
                continue
            for m in _VAR_REF_RE.finditer(code):
                var_name = m.group(1)
                # Skip @[ inline math opener
                if var_name == "@":
                    continue
                if var_name in local_defs.get(rel_fp, set()):
                    continue
                refs[var_name].append((rel_fp, i))

    defined_vars = set(defs.keys()) | _get_game_scripted_variables()
    referenced_vars = set(refs.keys())

    # Undefined references
    for var in sorted(referenced_vars - defined_vars):
        locs = refs[var]
        sample = "; ".join(f"{f}:{ln}" for f, ln in locs[:3])
        findings.append({
            "file": sample.split(":")[0] if locs else "",
            "severity": "info" if var in _KNOWN_EXTERNAL_VARS else "warning",
            "check": "undefined_variable",
            "message": (
                f"Variable '{var}' referenced but not defined in mod "
                f"scripted_variables/"
                f"{' (may be external)' if var in _KNOWN_EXTERNAL_VARS else ''} "
                f"(referenced at: {sample})"
            ),
        })

    # Shadowed definitions
    for var, locs in sorted(defs.items()):
        if len(locs) > 1:
            files_str = "; ".join(f"{f}:{ln}" for f, ln in locs)
            findings.append({
                "file": locs[0][0],
                "severity": "warning",
                "check": "shadowed_variable",
                "message": (
                    f"Variable '{var}' defined {len(locs)} times "
                    f"(first-loaded wins / FIOS): {files_str}"
                ),
            })

    return findings


def _find_comment(line: str) -> int:
    """Find the position of a # comment, respecting quoted strings."""
    in_quote = False
    for i, ch in enumerate(line):
        if ch == '"':
            in_quote = not in_quote
        elif ch == "#" and not in_quote:
            return i
    return len(line)


# ---------------------------------------------------------------------------
# Check: GFX sprite integrity
# ---------------------------------------------------------------------------

_GFX_NAME_RE = re.compile(
    r"""name\s*=\s*"?(GFX_[A-Za-z_0-9.:-]+)"?""",
)
_GFX_REF_RE = re.compile(
    r"""(?:icon|spriteType|gfx)\s*=\s*"?(GFX_[A-Za-z_0-9.:-]+)"?""",
)
_TEXTURE_RE = re.compile(
    r"""[Tt]exture[Ff]ile\s*=\s*"([^"]+)"|[Tt]exture[Ff]ile\s*=\s*(\S+)""",
)


def check_gfx_integrity(root: Path) -> list[dict]:
    """Cross-reference GFX sprite names with GUI/script references."""
    findings: list[dict] = []

    # Collect all GFX definitions
    gfx_defs: dict[str, list[tuple[str, int]]] = defaultdict(list)
    gfx_files = list((root / "interface").rglob("*.gfx")) if (
        root / "interface"
    ).is_dir() else []
    for fp in sorted(gfx_files):
        text = fp.read_text(encoding="utf-8-sig", errors="replace")
        inside_sprite = False
        for i, line in enumerate(text.splitlines(), 1):
            stripped = line.split("#", 1)[0].strip()
            if "spriteType" in stripped and "=" in stripped:
                inside_sprite = True
            if inside_sprite:
                m = _GFX_NAME_RE.search(stripped)
                if m:
                    gfx_defs[m.group(1)].append((_rel(fp, root), i))

    # Collect references from GUI and script files
    gfx_refs: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for fp in _walk(root, _SCRIPT_EXTS):
        text = fp.read_text(encoding="utf-8-sig", errors="replace")
        for i, line in enumerate(text.splitlines(), 1):
            stripped = line.split("#", 1)[0]
            for m in _GFX_REF_RE.finditer(stripped):
                name = m.group(1)
                # Don't count definitions as references
                if "name" in m.group(0).split("=")[0].strip().lower():
                    continue
                gfx_refs[name].append((_rel(fp, root), i))

    # Duplicate GFX names
    for name, locs in sorted(gfx_defs.items()):
        if len(locs) > 1:
            files_str = "; ".join(f"{f}:{ln}" for f, ln in locs)
            findings.append({
                "file": locs[0][0],
                "severity": "warning",
                "check": "duplicate_gfx",
                "message": (
                    f"Sprite '{name}' defined {len(locs)} times: "
                    f"{files_str}"
                ),
            })

    # Missing GFX (referenced but not defined in mod)
    defined_names = set(gfx_defs.keys()) | _get_game_sprite_names()
    for name, locs in sorted(gfx_refs.items()):
        if name not in defined_names:
            sample = "; ".join(f"{f}:{ln}" for f, ln in locs[:3])
            findings.append({
                "file": locs[0][0] if locs else "",
                "severity": "info",
                "check": "missing_gfx",
                "message": (
                    f"Sprite '{name}' referenced but not found in mod or detected game install: {sample}"
                ),
            })

    return findings


# ---------------------------------------------------------------------------
# Check: textureFile paths
# ---------------------------------------------------------------------------

def check_texture_paths(root: Path) -> list[dict]:
    """Verify textureFile paths point to existing files."""
    findings: list[dict] = []
    gfx_files = list((root / "interface").glob("*.gfx")) if (
        root / "interface"
    ).is_dir() else []
    for fp in sorted(gfx_files):
        text = fp.read_text(encoding="utf-8-sig", errors="replace")
        for i, line in enumerate(text.splitlines(), 1):
            stripped = line.split("#", 1)[0]
            m = _TEXTURE_RE.search(stripped)
            if m:
                tex_path = m.group(1) or m.group(2)
                full = root / tex_path.replace("/", os.sep)
                if not full.is_file() and not _content_path_exists(tex_path):
                    findings.append({
                        "file": _rel(fp, root),
                        "severity": "info",
                        "check": "missing_texture",
                        "message": (
                            f"Texture '{tex_path}' not found in mod or detected game install"
                        ),
                        "line": i,
                    })
    return findings


# ---------------------------------------------------------------------------
# Check: script encoding
# ---------------------------------------------------------------------------

def check_script_encoding(root: Path) -> list[dict]:
    """Ensure Paradox script files do not start with a UTF-8 BOM.

    Exception: common/name_lists/ files must have BOM (Stellaris lexer.cpp
    requirement for name list files).
    """
    findings: list[dict] = []

    name_lists_dir = (root / "common" / "name_lists").resolve()

    for fp in _walk(root, _SCRIPT_EXTS):
        raw = fp.read_bytes()
        # name_lists/*.txt files require BOM — skip the no-BOM check for them
        if fp.resolve().is_relative_to(name_lists_dir):
            if not raw.startswith(b"\xef\xbb\xbf"):
                findings.append({
                    "file": _rel(fp, root),
                    "severity": "error",
                    "check": "script_bom",
                    "message": "name_lists file must be UTF-8 with BOM (Stellaris lexer requirement)",
                })
            continue
        if raw.startswith(b"\xef\xbb\xbf"):
            findings.append({
                "file": _rel(fp, root),
                "severity": "error",
                "check": "script_bom",
                "message": "Paradox script file must be UTF-8 without BOM",
            })

    return findings


# ---------------------------------------------------------------------------
# Check: localisation
# ---------------------------------------------------------------------------

def check_localisation(root: Path) -> list[dict]:
    """Validate localisation files: BOM, header, duplicate keys."""
    findings: list[dict] = []
    loc_dir = root / "localisation"
    if not loc_dir.is_dir():
        return findings

    all_keys: dict[tuple[str, str], list[tuple[str, int]]] = defaultdict(list)
    lang_re = re.compile(r"^\s*(l_\w+):\s*$")
    key_re = re.compile(r"^\s+([A-Za-z_0-9.]+)\s*:\s*\d*\s+\"")

    for fp in sorted(loc_dir.rglob("*.yml")):
        raw = fp.read_bytes()
        # Check BOM
        if not raw.startswith(b"\xef\xbb\xbf"):
            findings.append({
                "file": _rel(fp, root),
                "severity": "error",
                "check": "missing_bom",
                "message": "Localisation file missing UTF-8 BOM",
            })

        text = raw.decode("utf-8-sig", errors="replace")
        lines = text.splitlines()

        # Check language header
        has_header = False
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if lang_re.match(line):
                has_header = True
            break
        if not has_header:
            findings.append({
                "file": _rel(fp, root),
                "severity": "error",
                "check": "missing_lang_header",
                "message": "First non-empty line is not a language header",
            })

        # Collect keys and detect duplicates within file
        file_keys: dict[tuple[str, str], list[int]] = defaultdict(list)
        current_language = ""
        for i, line in enumerate(lines, 1):
            lang_match = lang_re.match(line)
            if lang_match:
                current_language = lang_match.group(1)
                continue
            m = key_re.match(line)
            if m:
                key = m.group(1)
                scoped_key = (current_language, key)
                file_keys[scoped_key].append(i)
                all_keys[scoped_key].append((_rel(fp, root), i))

        for (language, key), line_nums in file_keys.items():
            if len(line_nums) > 1:
                lines_str = ", ".join(str(ln) for ln in line_nums)
                language_note = (
                    f" in {language}" if language else " before any language header"
                )
                findings.append({
                    "file": _rel(fp, root),
                    "severity": "warning",
                    "check": "duplicate_loc_key",
                    "message": (
                        f"Localisation key '{key}' duplicated on "
                        f"lines {lines_str}{language_note}"
                    ),
                })

    # Cross-file duplicates for the same language only.
    for (language, key), locs in sorted(all_keys.items()):
        unique_files = {f for f, _ in locs}
        if len(unique_files) > 1:
            files_str = "; ".join(
                f"{f}:{ln}" for f, ln in locs
            )
            language_note = (
                f" for {language}" if language else " before any language header"
            )
            findings.append({
                "file": locs[0][0],
                "severity": "warning",
                "check": "cross_file_dup_loc",
                "message": (
                    f"Localisation key '{key}' defined in multiple "
                    f"files{language_note}: {files_str}"
                ),
            })

    return findings


# ---------------------------------------------------------------------------
# Check: inline script parameter matching
# ---------------------------------------------------------------------------

_INLINE_CALL_RE = re.compile(
    r"inline_script\s*=\s*\{",
)
_SCRIPT_PATH_RE = re.compile(
    r"(?:^|\s)script\s*=\s*(\S+)",
    re.MULTILINE,
)
_PARAM_PLACEHOLDER_RE = re.compile(
    r"\$([A-Za-z_][A-Za-z_0-9]*)\$",
)


def check_inline_scripts(root: Path) -> list[dict]:
    """Verify inline_script calls match template parameters."""
    findings: list[dict] = []
    inline_root = root / "common" / "inline_scripts"
    if not inline_root.is_dir():
        return findings

    for fp in _walk(root, {".txt"}):
        # Skip template files themselves (they may contain nested inline_script
        # calls that use $PARAM$ for the script path, which we can't resolve)
        try:
            fp.relative_to(inline_root)
            continue
        except (ValueError, TypeError):
            pass
        text = fp.read_text(encoding="utf-8-sig", errors="replace")
        lines = text.splitlines()

        i = 0
        while i < len(lines):
            line = lines[i]
            code = line.split("#", 1)[0]
            if "inline_script" in code and "{" in code:
                # Gather the block
                block_lines = [code]
                depth = code.count("{") - code.count("}")
                j = i + 1
                while depth > 0 and j < len(lines):
                    bline = lines[j].split("#", 1)[0]
                    block_lines.append(bline)
                    depth += bline.count("{") - bline.count("}")
                    j += 1
                block_text = "\n".join(block_lines)

                # Extract script path
                sm = _SCRIPT_PATH_RE.search(block_text)
                if sm:
                    script_path = sm.group(1).strip('"')
                    # Skip if the path contains $PARAM$ (can't resolve)
                    if "$" in script_path:
                        i = j
                        continue
                    tmpl_file = inline_root / (
                        script_path.replace("/", os.sep) + ".txt"
                    )

                    game_template_path = (
                        f"common/inline_scripts/{script_path}.txt"
                    )
                    template_source = tmpl_file
                    if not template_source.is_file():
                        template_source = _resolve_content_file(game_template_path)

                    if template_source is None:
                        findings.append({
                            "file": _rel(fp, root),
                            "severity": "info",
                            "check": "missing_inline_template",
                            "message": (
                                f"Inline script template not found in mod or detected game install: "
                                f"common/inline_scripts/{script_path}.txt"
                            ),
                            "line": i + 1,
                        })
                    else:
                        # Compare call params vs template params
                        tmpl_text = template_source.read_text(
                            encoding="utf-8-sig", errors="replace",
                        )
                        tmpl_params = set(
                            _PARAM_PLACEHOLDER_RE.findall(tmpl_text),
                        )

                        # Extract passed params from call block. Strip quoted strings
                        # first so multiline code payloads do not look like params.
                        call_params: set[str] = set()
                        param_assign_re = re.compile(
                            r"([A-Za-z_][A-Za-z_0-9]*)\s*=",
                        )
                        block_without_strings = re.sub(
                            r'"[^"]*"',
                            '""',
                            block_text,
                            flags=re.DOTALL,
                        )
                        for pm in param_assign_re.finditer(block_without_strings):
                            pname = pm.group(1)
                            if pname not in {"inline_script", "script"}:
                                call_params.add(pname)

                        missing = tmpl_params - call_params
                        extra = call_params - tmpl_params
                        if missing:
                            findings.append({
                                "file": _rel(fp, root),
                                "severity": "error",
                                "check": "inline_missing_param",
                                "message": (
                                    f"Inline call missing params for "
                                    f"'{script_path}': "
                                    f"{', '.join(sorted(missing))}"
                                ),
                                "line": i + 1,
                            })
                        if extra:
                            findings.append({
                                "file": _rel(fp, root),
                                "severity": "info",
                                "check": "inline_extra_param",
                                "message": (
                                    f"Inline call passes unused params "
                                    f"for '{script_path}': "
                                    f"{', '.join(sorted(extra))}"
                                ),
                                "line": i + 1,
                            })
                i = j
            else:
                i += 1

    return findings


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

ALL_CHECKS = {
    "braces": check_brace_balance,
    "duplicates": check_duplicate_keys,
    "variables": check_variable_integrity,
    "gfx": check_gfx_integrity,
    "textures": check_texture_paths,
    "script_encoding": check_script_encoding,
    "localisation": check_localisation,
    "inline": check_inline_scripts,
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Paradox Script structural validator",
    )
    parser.add_argument(
        "mod_root",
        type=Path,
        help="Path to the mod root directory",
    )
    parser.add_argument(
        "--check",
        default=",".join(ALL_CHECKS.keys()),
        help=f"Comma-separated checks to run (default: all). "
             f"Available: {', '.join(ALL_CHECKS.keys())}",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output findings as JSON",
    )
    args = parser.parse_args()

    root = args.mod_root.resolve()
    if not root.is_dir():
        print(f"Error: '{root}' is not a directory", file=sys.stderr)
        return 1

    checks = [c.strip() for c in args.check.split(",")]
    for c in checks:
        if c not in ALL_CHECKS:
            print(
                f"Error: unknown check '{c}'. "
                f"Available: {', '.join(ALL_CHECKS.keys())}",
                file=sys.stderr,
            )
            return 1

    all_findings: list[dict] = []
    for check_name in checks:
        all_findings.extend(ALL_CHECKS[check_name](root))

    # Sort: errors first, then warnings, then info
    severity_order = {"error": 0, "warning": 1, "info": 2}
    all_findings.sort(key=lambda f: (
        severity_order.get(f["severity"], 9),
        f.get("file", ""),
        f.get("line", 0),
    ))

    if args.json:
        json.dump(all_findings, sys.stdout, indent=2)
        print()
    else:
        counts = defaultdict(int)
        for f in all_findings:
            counts[f["severity"]] += 1
            sev = f["severity"].upper()
            loc = f["file"]
            if f.get("line"):
                loc += f":{f['line']}"
            print(f"[{sev}] {loc}: {f['message']}")

        print()
        total = len(all_findings)
        print(
            f"Total: {total} finding(s) "
            f"({counts['error']} error, "
            f"{counts['warning']} warning, "
            f"{counts['info']} info)",
        )
        return 1 if counts["error"] > 0 else 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
