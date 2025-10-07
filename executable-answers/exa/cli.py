"""
CLI:
- exa-validate validate <answer.md> [--outdir out] [--tolerance 0.1]
- exa-report   report   [--outdir out]
"""
from __future__ import annotations
import argparse, json, os, sys
from .extract import extract_numeric_growth_claims
from .verify import verify_claims
from .sources import extract_dois

def cmd_validate(args: argparse.Namespace) -> int:
    text = open(args.input, "r", encoding="utf-8").read()
    claims = extract_numeric_growth_claims(text)
    report = verify_claims(claims, epsilon_pp=args.tolerance)
    dois = extract_dois(text)

    os.makedirs(args.outdir, exist_ok=True)
    json.dump({"claims": claims}, open(os.path.join(args.outdir, "claimgraph.json"), "w", encoding="utf-8"), indent=2)
    json.dump(report, open(os.path.join(args.outdir, "verification_report.json"), "w", encoding="utf-8"), indent=2)
    json.dump({"dois": dois}, open(os.path.join(args.outdir, "sources.json"), "w", encoding="utf-8"), indent=2)
    print(f"Wrote {args.outdir}/claimgraph.json")
    print(f"Wrote {args.outdir}/verification_report.json")
    print(f"Wrote {args.outdir}/sources.json")
    return 0

def cmd_report(args: argparse.Namespace) -> int:
    path = os.path.join(args.outdir, "verification_report.json")
    if not os.path.exists(path):
        print("No verification_report.json found. Run exa-validate first.", file=sys.stderr)
        return 1
    print(json.dumps(json.load(open(path, "r", encoding="utf-8")).get("summary", {}), indent=2))
    return 0

def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="exa")
    sub = p.add_subparsers(dest="cmd")

    p_val = sub.add_parser("validate", help="Validate claims in an answer file")
    p_val.add_argument("input")
    p_val.add_argument("--outdir", default="out")
    p_val.add_argument("--tolerance", type=float, default=0.1)
    p_val.set_defaults(func=cmd_validate)

    p_rep = sub.add_parser("report", help="Show summary for the last validation")
    p_rep.add_argument("--outdir", default="out")
    p_rep.set_defaults(func=cmd_report)

    args = p.parse_args(argv)
    if not hasattr(args, "func"):
        p.print_help()
        return 2
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
