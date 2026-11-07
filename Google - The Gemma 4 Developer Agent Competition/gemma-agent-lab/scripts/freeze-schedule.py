"""Freeze an ordered IDs-only development or holdout schedule from task JSONL."""

import argparse
from collections import defaultdict, deque
import hashlib
import json
import os
from pathlib import Path
import tempfile


def read_tasks(path):
    with path.open(encoding="utf-8-sig") as source:
        for line_number, line in enumerate(source, 1):
            if line.strip():
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as error:
                    raise ValueError(f"Invalid JSON at line {line_number} in {path}.") from error


def freeze_schedule(tasks, mode, holdout_repo, count, seed="gemma-main-v1"):
    if mode not in ("development", "holdout"):
        raise ValueError("Mode must be development or holdout.")
    if type(count) is not int or count < 1:
        raise ValueError("Count must be a positive integer.")
    if not isinstance(holdout_repo, str) or not holdout_repo.strip() or holdout_repo != holdout_repo.strip():
        raise ValueError("Provide the exact held-out repository name.")
    if not isinstance(seed, str) or not seed.strip():
        raise ValueError("Provide a nonblank seed.")

    repositories = defaultdict(list)
    seen = set()
    for index, task in enumerate(tasks, 1):
        if not isinstance(task, dict):
            raise ValueError(f"Task {index} must be an object.")
        for field in ("instance_id", "repo"):
            value = task.get(field)
            if not isinstance(value, str) or not value.strip() or value != value.strip():
                raise ValueError(f"Task {index} has a missing or invalid {field}.")
        instance_id, repo = task["instance_id"], task["repo"]
        if instance_id in seen:
            raise ValueError(f"Duplicate instance_id: {instance_id}.")
        seen.add(instance_id)
        repositories[repo].append(instance_id)
    if holdout_repo not in repositories:
        raise ValueError(f"Held-out repository is absent from the input: {holdout_repo}.")

    if mode == "holdout":
        eligible = [holdout_repo]
    else:
        eligible = [repo for repo in repositories if repo != holdout_repo]
    available = sum(len(repositories[repo]) for repo in eligible)
    if count > available:
        raise ValueError(f"Requested {count} tasks but only {available} are eligible for {mode}.")

    def rank(kind, value):
        key = json.dumps([seed, kind, value], ensure_ascii=True, separators=(",", ":")).encode("ascii")
        return hashlib.sha256(key).digest(), value

    rotation = deque(sorted(eligible, key=lambda repo: rank("repo", repo)))
    queues = {
        repo: deque(sorted(repositories[repo], key=lambda task: rank("task", task)))
        for repo in eligible
    }
    schedule = []
    while len(schedule) < count:
        repo = rotation.popleft()
        schedule.append({"instance_id": queues[repo].popleft(), "repo": repo})
        if queues[repo]:
            rotation.append(repo)
    return schedule


def write_schedule(path, schedule):
    # Atomically publish a complete file. A concurrent freeze can never replace the first.
    staging = tempfile.NamedTemporaryFile(dir=path.parent, mode="w", encoding="utf-8", newline="\n", delete=False)
    try:
        with staging:
            json.dump(schedule, staging, indent=2)
            staging.write("\n")
        os.link(staging.name, path)
    finally:
        Path(staging.name).unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tasks", type=Path, help="Task JSONL containing instance_id and repo")
    parser.add_argument("output", type=Path, help="New schedule JSON file")
    parser.add_argument("--mode", choices=("development", "holdout"), required=True)
    parser.add_argument("--holdout-repo", required=True, help="Exact repository reserved for confirmation")
    parser.add_argument("--count", type=int, required=True, help="Exact number of eligible tasks to freeze")
    parser.add_argument("--seed", default="gemma-main-v1", help="Predeclared ranking seed (default: %(default)s)")
    args = parser.parse_args()
    try:
        schedule = freeze_schedule(read_tasks(args.tasks), args.mode, args.holdout_repo, args.count, args.seed)
        write_schedule(args.output, schedule)
    except FileExistsError:
        parser.exit(1, f"Schedule already exists: {args.output}\n")
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")
    print(f"Froze {len(schedule)} {args.mode} tasks in {args.output}. Held-out repository: {args.holdout_repo}.")


if __name__ == "__main__":
    main()
