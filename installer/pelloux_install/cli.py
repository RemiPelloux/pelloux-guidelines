"""pelloux install: write the rules for each agent, then wire the machine checks."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from pelloux_audit.languages import BY_NAME

from . import AGENTS, DEFAULT_AGENTS, LOCALES, SOURCE, agents, detect, enforce
from .compose import bundle
from .writer import Writer


def main(argv: list) -> int:
    args = _parser().parse_args(argv)
    root = Path(args.target).resolve()
    langs = _split(args.lang) or detect.languages(root)
    unknown = [lang for lang in langs if lang not in BY_NAME]
    chosen = list(AGENTS) if args.agents == "all" else _split(args.agents)
    if unknown or not set(chosen) <= set(AGENTS):
        print(f"Unknown language or agent: {unknown or chosen}. Languages: {', '.join(BY_NAME)}.")
        return 2
    w = Writer(root, args.dry_run)
    install(w, langs, chosen, args)
    if args.skills:
        install_skills(w)
    _print_summary(w, langs, chosen)
    return 0


def install(w: Writer, langs: list, chosen: list, args) -> None:
    w.write(agents.GUIDE, bundle(langs, args.locale))
    for name in chosen:
        agents.WRITERS[name](w, langs, args.locale)
    if args.rules_only:
        return
    enforce.vendor_tool(w)
    enforce.write_config(w, langs)
    enforce.seed_baseline(w, langs)
    enforce.precommit(w)
    if args.ci:
        enforce.workflow(w)


def install_skills(w: Writer) -> None:
    """Copy the skills where Claude Code, Codex and other agents look for them."""
    home = Path.home()
    targets = [home / ".claude" / "skills"]
    targets += [d / "skills" for d in (home / ".codex", home / ".agents") if d.is_dir()]
    for skill in sorted((SOURCE / "skills").iterdir()):
        for target in targets:
            w.log.append(f"{'skill':7} {target / skill.name}")
            if not w.dry_run:
                shutil.copytree(skill, target / skill.name, dirs_exist_ok=True)


def _print_summary(w: Writer, langs: list, chosen: list) -> None:
    labels = ", ".join(BY_NAME[lang].label for lang in langs) or "none detected (core rules only)"
    print(f"Pelloux Guidelines → {w.root}\n  profiles: {labels}\n  agents:   {', '.join(chosen)}\n")
    print("\n".join(f"  {line}" for line in w.log))
    if w.dry_run:
        print("\nDry run: nothing was written.")
        return
    print("\nNext: python3 .pelloux/pelloux.py audit, then commit pelloux-baseline.json on its own.")


def _split(value: str) -> list:
    return [part.strip() for part in (value or "").split(",") if part.strip()]


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="install.py", description=__doc__)
    p.add_argument("--target", default=".", help="repository to install into (default: here)")
    p.add_argument("--lang", help=f"comma list, default: detected ({', '.join(BY_NAME)})")
    p.add_argument("--agents", default=",".join(DEFAULT_AGENTS),
                   help=f"comma list or 'all' ({', '.join(AGENTS)})")
    p.add_argument("--locale", default="en", choices=LOCALES, help="language of the rules")
    p.add_argument("--rules-only", action="store_true", help="skip the audit, baseline and hook")
    p.add_argument("--ci", action="store_true", help="also add a GitHub Actions workflow")
    p.add_argument("--skills", action="store_true", help="also install the agent skills globally")
    p.add_argument("--dry-run", action="store_true", help="show what would change")
    return p
