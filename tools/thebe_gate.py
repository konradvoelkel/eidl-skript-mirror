#!/usr/bin/env python3
"""Load thebe-core only on pages that have something computable on them.

    python3 tools/thebe_gate.py <html-dir>

Run from the deploy workflow, after the HTML build and after `vendor_assets.py` -- it
edits the same client bundles, and this one checks that its own edit is the only thing it
changed, so it wants to be last.


What it is for
--------------

`thebe-core.min.js` is **359 kB on the wire and 1,278 kB decoded**, and the SEO audit of
2026-10-17 measured it loading on all thirty pages, twelve of which are Markdown chapters
with no executed cell on them at all -- including the landing page, the most common search
entry point. On those twelve it buys nothing: there is no cell to attach to, no output to
render, and this site configures no kernel server, so nothing can be run anywhere.

The audit's prescription was to strip a `<script>` tag. **There is no such tag.** Measured
on all thirty built pages before writing this: the only thebe reference in the markup is a
stylesheet (dropped by `head_meta.py`, its section 5). The script is appended to
`document.head` at runtime, by thebe-react's `ThebeBundleLoaderProvider`, from an effect
in the theme's own `ExecuteScopeProvider` that reads

    useEffect(() => { core || loading || load() }, [core, load, loading])

-- i.e. unconditionally, on every page, with no reference to whether the page has
anything to compute. So this cannot be done in the HTML, and it is not a MyST setting:
the provider is mounted for every page and takes no option that reaches that effect.


What it changes
---------------

One expression, in the one client chunk that contains that effect:

    core || loading || load()
    core || loading || !Object.values(state.pages).some(_c => _c.computable) || load()

`state.pages[slug].computable` is **MyST's own flag**, not a new notion invented here:
the theme computes it as `computables.length > 0 || kind === Notebook` when the page
enters the execute scope, where `computables` are the figure and embed nodes that have
`output` children. It is true on the eighteen notebook pages and false on the twelve
Markdown chapters, which is exactly the partition `head_meta.py` finds in the markup from
the `myst-jp` class prefix -- two independent routes to the same twelve pages, which is
the reason to trust either.

The pages that do have output are untouched: there the effect still fires on mount, and
the two output renderers that call `load()` themselves when they are asked to render a
mime bundle are not patched at all. So "the page can compute" still implies "thebe is
loaded", and the only thing removed is loading it where nothing can.


Why patching a vendored bundle is acceptable here, and how it refuses
---------------------------------------------------------------------

It is a rewrite of minified third-party JavaScript, which is a thing to do carefully and
not often. Three reasons it is this and not something cleverer:

* the alternative that needs no bundle edit is to pre-set `window.thebeCore` so the
  loader believes it is already loaded -- which forges an API the page then calls into,
  and which (traced through the loader's retry loop) either white-screens the page or
  spins an interval forever. A stub that lies is worse than a patch that is honest.
* `pages.yml` already rewrites these bundles for the CDN references
  (`tools/vendor_assets.py`), and `head_meta.py` already rewrites the hydration payload.
  The precedent and the failure modes are known.
* the real fix is upstream, in `myst-theme`, and is recorded in UPSTREAM-NOTES.md.

The refusal is the important half. The identifiers in the pattern are minified and will
be renamed by the next mystmd release, so the pattern is anchored on the structure rather
than on any one name, and **a build in which it is not found fails** instead of quietly
shipping the 359 kB again -- which is the way round this has to fail, because nothing
downstream would notice the difference.

The postcondition is the file itself: after the edit the chunk must differ from what it
was by exactly the inserted expression and nothing else, and the gate must appear exactly
once. Running it twice is a no-op: the second run finds the gate already in place, says
so, and changes nothing.


Verifying it
------------

Serve the built directory and load a Markdown chapter and a notebook chapter with the
network panel open: `thebe-core.min.js` must be absent on the first and present on the
second, and the notebook figures must still render. Measured 2026-10-17 on this build:
absent on all twelve Markdown chapters, present on all eighteen notebook pages.
"""

from __future__ import annotations

import pathlib
import re
import sys

# The component: it destructures core/load/loading off useThebeLoader and takes the
# execute-scope reducer's state. Anchored on that shape, because every name in it is
# minified and none of them is stable across mystmd releases.
COMPONENT = re.compile(
    r"function\s+\w+\(\{state:(?P<state>\w+),dispatch:\w+\}\)\{"
    r"let\{core:(?P<core>\w+),load:(?P<load>\w+),loading:(?P<loading>\w+)\}"
    r"=\(0,\w+\.useThebeLoader\)\(\)"
)


def gate(state: str) -> str:
    """The inserted expression: skip the load when no page in scope is computable."""
    return f"!Object.values({state}.pages).some(_c=>_c.computable)||"


def patch(source: str) -> tuple[str, str]:
    """Returns (patched source, what happened). Raises SystemExit on anything unclear."""
    found = list(COMPONENT.finditer(source))
    if len(found) != 1:
        return source, f"found {len(found)} candidate components, expected exactly 1"

    m = found[0]
    core, load, loading = m["core"], m["load"], m["loading"]
    effect = f"(()=>{{{core}||{loading}||{load}()}},["
    gated = f"(()=>{{{core}||{loading}||{gate(m['state'])}{load}()}},["

    if gated in source:
        return source, "already gated"
    if source.count(effect) != 1:
        return source, (
            f"found {source.count(effect)} copies of the loader effect, expected 1"
        )

    out = source.replace(effect, gated, 1)
    # The postcondition is the file: one gate, and a length that grew by exactly the
    # inserted expression. Anything else means the replacement hit more than it should.
    if out.count(gated) != 1:
        sys.exit("::error::thebe_gate: the gate was inserted more than once")
    if len(out) - len(source) != len(gated) - len(effect):
        sys.exit("::error::thebe_gate: the patched chunk changed by more than the gate")
    return out, "gated"


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    root = pathlib.Path(sys.argv[1])

    # Only the theme's own chunks: thebe-core.min.js and thebe-lite.min.js are the
    # payload being deferred, not the thing that loads it.
    candidates = [
        f
        for f in sorted(root.rglob("*.js"))
        if not f.name.endswith(("thebe-core.min.js", "thebe-lite.min.js"))
        and "useThebeLoader" in f.read_text(encoding="utf-8", errors="replace")
    ]
    if len(candidates) != 1:
        print(
            f"::error::expected exactly one client chunk containing the thebe loader, "
            f"found {len(candidates)}: {[str(f) for f in candidates]}\n"
            f"  The theme's bundling changed. See the docstring: this must fail rather "
            f"than leave 359 kB of thebe-core loading on every page unnoticed."
        )
        return 1

    target = candidates[0]
    source = target.read_text(encoding="utf-8")
    out, what = patch(source)
    if what not in ("gated", "already gated"):
        print(
            f"::error::{target}: {what}.\n"
            f"  The minified shape this patch is anchored on has moved, which a mystmd\n"
            f"  upgrade will do. Re-read the effect in the theme's ExecuteScopeProvider\n"
            f"  and re-anchor COMPONENT in tools/thebe_gate.py, or drop this step and\n"
            f"  accept 359 kB of thebe-core on the twelve pages that cannot use it."
        )
        return 1
    if what == "gated":
        target.write_text(out, encoding="utf-8")
    print(f"✓ thebe_gate: {target.relative_to(root)} {what}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
