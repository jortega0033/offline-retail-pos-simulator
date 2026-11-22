# Releasing

Only the owner releases. Agents never tag, create a GitHub release or publish anything.

## What a release is here

The product is a simulator run from source with the Python standard library. There is no package, installer or deployment. A release is a Git tag on `main` plus a GitHub release page that points at it.

## When a release is possible

- The epic's finish line ([#1](https://github.com/jortega0033/offline-retail-pos-simulator/issues/1)) is met, or the owner picks an earlier state on purpose.
- No licence is selected yet (owner decision D13). Choose one and add `LICENSE` before the first public release.

## Steps

1. On a clean checkout of `main`, confirm CI is green for the latest commit on `main` (Linux and Windows, Python 3.12 and 3.13).
2. Run `python -m unittest` and `python -m retail_pos.evidence` (planned, ticket #7) from a scratch directory. Both must exit 0. Keep the evidence report output.
3. In `CHANGELOG.md`, rename `Unreleased` to the new version and date, and start a new empty `Unreleased` section.
4. Merge that change through a pull request.
5. Tag the merge commit as `vMAJOR.MINOR.PATCH` (start at `v0.1.0`) and push the tag.
6. Create the GitHub release from the tag. Paste the changelog section and the evidence report summary, and state which runs were not made.
