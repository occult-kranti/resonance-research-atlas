# Preserved execution failure

Initial runner failed before execution with Python SyntaxError at line15: `else500` lacked a separating space. Full original source is `run-attempt1.py.txt`. No scientific output was produced and no threshold changed. The repair changed `else500` to `else 500`; subsequent execution uses the same frozen contract.

Independent advisor review found that the malformed nonuniform-time CSV test used an output prefix equal to its source stem. The path-protection guard rejected the call first, so its rejection did not test timestamp uniformity. The first run and result/intake/manifest bytes are preserved in `*-before-review.*`. The repair uses a distinct `reject_` output prefix for every malformed case and asserts the specific intended failure reason. No scientific model, fit parameter, threshold or clock fixture changed. The corrected nonuniform-time case must reach the uniform-sampling guard.
