import argparse
import json
from pathlib import Path

from config import get_default_llm
from agents.d2insight_gpt4o import analyze_csv_with_insights
from agents.d2insight_agent_sys import run_domain_detector
from agents.insight2dashboard_tot import generate_analysis


def _cmd_simple(args: argparse.Namespace) -> None:
    """Run the simple GPT‑4o CSV analysis."""
    get_default_llm()  # ensures environment/config are loaded
    result = analyze_csv_with_insights(args.csv_path, args.prompt)
    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
    else:
        print(result)


def _cmd_domain(args: argparse.Namespace) -> None:
    """Run the domain-aware agent."""
    get_default_llm()
    result = run_domain_detector(args.csv_path, max_cycles=args.max_cycles)
    output = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)


def _cmd_tot(args: argparse.Namespace) -> None:
    """Run the Tree-of-Thought analysis generator."""
    llm = get_default_llm()
    model = args.model
    if model is None:
        model = getattr(llm, "model", getattr(llm, "model_name", "gpt-4o"))
    thoughts = generate_analysis(
        args.csv_path,
        args.insight_json_path,
        model=model,
        temperature=args.temperature,
        run_code=not args.no_run_code,
        save_dir=args.save_dir,
    )
    print(thoughts)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Data2Dashboard agent CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_simple = sub.add_parser("simple", help="Run simple GPT-4o CSV analysis")
    p_simple.add_argument("csv_path", help="Path to the CSV file")
    p_simple.add_argument("prompt", help="User prompt text")
    p_simple.add_argument("--output", "-o", help="File to write the JSON result")
    p_simple.set_defaults(func=_cmd_simple)

    p_domain = sub.add_parser("domain", help="Run domain-aware agent")
    p_domain.add_argument("csv_path", help="Path to the CSV file")
    p_domain.add_argument("--max-cycles", type=int, default=5, help="Max improvement cycles")
    p_domain.add_argument("--output", "-o", help="File to write the JSON result")
    p_domain.set_defaults(func=_cmd_domain)

    p_tot = sub.add_parser("tot", help="Run Tree-of-Thought chart generator")
    p_tot.add_argument("csv_path", help="Path to the CSV file")
    p_tot.add_argument("insight_json_path", help="Path to the insight library JSON")
    p_tot.add_argument("--model", help="OpenAI model name")
    p_tot.add_argument("--temperature", type=float, default=0.2, help="Sampling temperature")
    p_tot.add_argument("--save-dir", default=".", help="Directory to save thoughts and code")
    p_tot.add_argument("--no-run-code", action="store_true", help="Do not execute generated code")
    p_tot.set_defaults(func=_cmd_tot)

    return parser


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
