"""Make the AI Judge Laugh: the Office Joke Open.

Writes a single line of office comedy to $MAKEFUN_OUTPUT_DIR/entry.txt.

The joke: a dead office plant, a Facilities ticket, and a photo standing
in for the real thing. Specific office detail (Facilities ticket marked
"resolved"), a misdirection that pays off in the last word, and tight
enough to read cleanly in one pass.
"""

import os
import sys

JOKE = (
    "Facilities replaced our dead office plant with a photo of a plant "
    "and closed the ticket as 'resolved'."
)

MIN_CHARS = 1
MAX_CHARS = 200


def resolve_output_dir():
    """Return the output directory, honouring MAKEFUN_OUTPUT_DIR."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return out
    return os.path.join(os.getcwd(), "output")


def validate(text):
    """Check the entry text against the competition gate.

    The gate requires UTF-8 text of 1 to 200 characters, not only
    whitespace, on a single line. We additionally reject control
    characters (other than the line ending we never write) and any
    leading/trailing blank padding, so the file the judge reads is
    exactly the joke, byte for byte.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    for ch in text:
        if ord(ch) < 0x20 and ch not in ("\t",):
            raise ValueError("entry must not contain control characters")
        if ord(ch) == 0x7F:
            raise ValueError("entry must not contain control characters")
    text.encode("utf-8")
    return text


def main():
    joke = validate(JOKE)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(joke)
    # Read back what we wrote and verify it before reporting success:
    # the judge reads the file, not the constant, so a truncated or
    # re-encoded write must fail here rather than ship silently.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != joke:
        raise SystemExit("verification failed: entry.txt differs from joke")
    if validate(written) != joke:
        raise SystemExit("verification failed: written entry fails the gate")
    print("wrote %s (%d characters)" % (path, len(joke)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
