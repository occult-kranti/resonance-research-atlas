# S5B — final plan-to-report dryrun

The batch tool reads a frozen plan and acquisition manifest. It requires trial IDs/order/condition labels, raw-file hashes, an impact time per file and declared device, gain, geometry, clock and impact-alignment metadata. Those declarations are not authentication or physical calibration. Each valid file passes through the unchanged protected intake.

The first valid trial has1 second of prepended silence and impact_time_s=1. Its absolute fit window becomes1.05–1.8 s and matches the original decay. Assigning impact zero to that same file instead reaches the silence rejection. This directly exercises alignment rather than assuming every recording starts at impact.

Seven recording suites cover the complete16-trial plan, a missing trial, four specific negative-control replacements, missing metadata, duplicate ID, wrong condition and wrong impact. Root review found that an empty or one-condition plan could be called complete, so the initial implementation/results are retained under pre-review/. The narrow repair adds pre-output validation for nonempty plans, known A/B codes with both present, and matching declared count. Four direct controls verify those exact plan gates and that no output directory is created. Every intended rejection reason is asserted. All raw hashes and a preexisting output directory remain unchanged. The four incomplete recording suites have primaryContrast=null; their explicitly descriptive survivor contrasts are never substituted for the preregistered primary result.

The successful contrast is still a synthetic recorded-channel comparison subject to S5A's identical condition-linked gain rival. No household bench has been run, and no material, biological or consciousness effect has been established. This is the tenth and final sound loop; later work requires new independent physical recordings and a separately frozen pilot-informed plan.

