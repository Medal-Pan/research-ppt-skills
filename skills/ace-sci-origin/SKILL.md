---
name: ace-sci-origin
description: Create publication-grade scientific figures from spreadsheet data using Python/R references, editable Origin .opju projects, and PowerPoint slides with Origin OLE objects. Use when Codex must make or repair Origin scientific plots, match a Python/R reference, enforce native Origin axes/ticks/line widths, remove Origin-side panel letters, add panel labels in PPT, arrange multi-panel group figures, export 300 dpi images, or validate Origin-to-PPT rendering.
---

# Ace Sci Origin

Use this skill for high-quality spreadsheet-to-Origin scientific figures where the output must include an editable Origin project, a polished PowerPoint group figure, and visual validation against a deterministic reference.

This skill is stricter than `sci-origin`: it treats the Python/R reference as the visual contract, keeps Origin pages as clean editable data panels, and performs final panel lettering and group layout in PowerPoint.

## Required References

Read only the references needed for the task:

- `references/excel-python-origin-ole-workflow.md` for end-to-end Excel -> Python reference -> Origin `.opju` -> PPT OLE work.
- `references/reference-first-origin.md` when matching a Python/R or user-provided reference figure.
- `references/origin-axis-contract.md` whenever axes are missing, thin, hidden, or inconsistent with the reference.
- `references/origin-ppt-pitfalls.md` before creating or repairing PowerPoint OLE output.
- `references/origin-style-contract.md` before writing a panel-level plotting contract.
- `references/nature-style-origin.md` for Nature/top-journal typography, spacing, and visual economy.

## Non-Negotiable Output Contract

For ordinary 2D panels, the Origin graph page must show at least two native data axes:

- bottom x-axis
- left y-axis
- axis lines visible
- major ticks visible
- tick labels visible
- axis titles visible unless the reference intentionally omits them

Do not draw ordinary line objects to fake axes. If axes are missing or too thin, repair Origin's native Line and Ticks settings and export again.

Set native Origin bottom/left axis line thickness to `2` by default. Apply both common Origin/LabTalk forms where possible:

```python
gl.lt_exec("""
layer.x.show=1; layer.y.show=1;
layer.x.showAxes=1; layer.y.showAxes=1;
layer.x.showLabels=1; layer.y.showLabels=1;
layer.x.showopposite=0; layer.y.showopposite=0;
layer.x.opposite=0; layer.y.opposite=0;
layer.x.postype=0; layer.y.postype=0;
layer.x.color=color(0,0,0); layer.y.color=color(0,0,0);
layer.x.width=2; layer.y.width=2;
layer.x.thickness=2; layer.y.thickness=2;
layer.x.ticks=1; layer.y.ticks=1;
layer.x.ticklength=8; layer.y.ticklength=8;
layer.x.tickThickness=2; layer.y.tickThickness=2;
layer.x.ticks.width=2; layer.y.ticks.width=2;
layer.x.minorTicks=0; layer.y.minorTicks=0;
layer.x.label.show=1; layer.y.label.show=1;
layer.x.title.show=1; layer.y.title.show=1;
layer.x.grid.show=0; layer.y.grid.show=0;
""")
```

Reapply this contract after graph creation, after adding plots, after `rescale`, after legend operations, after setting ranges, before Origin export, and immediately before `copy_page("OLE")`.

## Origin Styling Hard Rules

For curve, spectrum, line, point-line, and multi-series 2D panels, Origin must visually follow the Python/R reference instead of Origin defaults:

- The scaffold files created by `ace_sci_origin_scaffold` are only starting points. A final run must replace TODO placeholders with panel-specific Origin construction code. Do not report a scaffold-only Origin script, generic `add_plot` loop, or default graph-page template as a completed Origin implementation.
- Treat `*_reference_match_report.json` as a required QA artifact whenever a Python/R reference exists. It must state, for every panel, the Python plot type, Origin construction type, expected reference styles, Origin preview path, and whether the preview passed checks for chart type, non-default colors, legend/direct labels, line width, and non-placeholder axes.
- The Python/R reference is the design source of truth. Origin is only the editable rendering backend. Do not use a generic Origin scatter/line/bar template as the first acceptable result.
- Before calling `origin_run_python`, compile a `reference_style_contract` from the Python/R reference and spreadsheet data. The contract must include panel layout, chart type, axes, ranges, tick density, colors, line widths, markers, bar offsets, legends, annotations, and panel occupancy.
- If the Python reference has grouped bars, horizontal bars, scatter labels, log axes, pie charts, or mixed panel types, Origin must create the same chart type for that panel. A default two-axis scatter or empty line graph is a failed panel.
- A panel with only default x/y axes, placeholder labels such as `X 轴标题` or `Y 轴标题`, default black markers, or missing plotted colored series is not an Origin implementation of the Python reference.
- The style contract must name the Python reference file used for matching and record `referenceFirstGate: true`. Do not proceed to "completed" status without this gate.
- Do not leave Origin curves as default black unless the Python/R reference explicitly uses a black series for that exact condition.
- Set Origin curve, spectrum, line, and point-line width to `2` by default, and do not go below `2` unless the user explicitly asks for thinner lines and the status file records that override.
- Every reference-visible series must have an explicit style map in the contract: semantic label, color, line style, marker style when relevant, and legend text.
- Apply series colors after plots are added, after grouping, after rescale, after legend rebuilds, and again immediately before exporting previews or copying OLE.
- A multi-series curve panel must contain an Origin-native legend or clear direct labels. For this skill, a missing legend/direct-label mapping is a failure, even if the data curves are correct.
- Prefer a compact frameless Origin legend that matches the Python reference labels. If Origin auto legend shows raw column names, delete it and rebuild a manual legend.
- Do not resize Origin graph pages to arbitrary Python figure dimensions. Use the Origin software default graph-page proportion unless the user or style contract explicitly requires another Origin page size. Match the Python reference composition later in PowerPoint by arranging OLE objects, not by distorting each Origin page.

## Figure-Building Workflow

1. Inspect the workbook first: sheet names, headers, row counts, units, conditions, and data shape.
2. Generate a deterministic Python or R reference from the spreadsheet unless the user supplies a trusted reference.
3. Write a panel-level style contract from the Python/R reference, not from Origin defaults: plot type, data columns, axes, ranges, tick spacing, colors, line widths, marker sizes, bar spacing, legends, annotations, panel layout, and OLE risks.
4. Before the Origin stage, actively open or attach to Origin/OriginPro and verify it is available through `origin_launch`, `origin_probe`, visible process/window evidence, or `originpro` COM readiness. Do not skip Origin automation just because Origin is not already open.
5. Build one Origin-native graph page per panel from explicit plotting tables and the compiled style contract. Do not build blank placeholder pages and call them panels.
6. Keep Origin graph pages clean: no panel letters `a/b/c` inside Origin unless the user explicitly asks for Origin-side panel labels.
7. Set Origin curves to the Python/R reference colors and width `2` or thicker when matching a bold Python reference; reapply after grouping/rescale/legend changes.
8. Export every Origin panel preview and compare against the reference before creating PPT.
   If a preview looks like a default Origin graph, has placeholder axis labels, has default black plots, or does not match the Python panel type, return to the Origin script and repair it before PPT.
9. Create slide 1 with Origin OLE objects copied from Origin graph pages. Do not replace OLE panels with screenshots when editability is required; slide 1 must remain double-clickable back to Origin/OLE.
10. In PowerPoint, arrange the OLE panels into the final group-figure layout and add panel letters as PPT text boxes near the upper-left corner of each panel, matching the Python reference placement.
11. Group each PPT panel letter with its corresponding OLE object when possible so each panel moves as one unit.
12. Put the Python/R reference PNG/JPG on slide 2. For the normal ace-sci-origin delivery, slide 2 is required, not optional.
13. Export PPT slide previews and validate visually and structurally.

## Continuation and Failure Policy

Do not stop after environment diagnosis, output-folder creation, scaffold generation, or checking only the first sheet. Those steps are preparation, not deliverables.

For a prompt like "use ace-sci-origin to process the current folder's fig3/ifg3 spreadsheet", continue autonomously through the full workbook inventory and generate as many required outputs as the environment allows:

- Python reference JPG/SVG and workbook inventory.
- panel-level style contract.
- editable Origin `.opju` or the best available Origin automation attempt.
- Origin panel previews.
- PowerPoint group figure where slide 1 contains Origin OLE objects and slide 2 contains the Python reference PNG/JPG when Origin/PowerPoint automation is available.
- PPT preview PNG and OLE validation report.
- `generation_status.json` with final paths, checks, missing deliverables, and exact failure reasons.

If a runtime dependency is missing, first attempt the available bootstrap or install path, then continue. If a single panel or OLE feature is unstable, produce the stable partial deliverables and document the residual mismatch in `generation_status.json`; do not abandon the entire workflow.

When Origin is installed or previously worked on the same machine, the correct behavior is to actively launch or attach to it and continue. Do not answer that Origin was not opened, not entered, or not yet attempted unless `origin_launch`/`origin_probe`/`origin_run_python` were actually tried and their tool results show a real blocker.

Only stop early when the user explicitly asks to stop, when a required file cannot be found after searching likely names and asking is unavoidable, or when a permission/runtime blocker remains after attempted repair. Even then, write `generation_status.json` and list the artifacts already produced.

## PowerPoint Layout Rules

Panel labels belong in PPT by default, not inside Origin graph pages. Use small bold Arial letters, usually lowercase, placed near the upper-left corner of each panel. The label should sit outside or just inside the panel's visual bounding box according to the Python reference, and it must not cover tick labels, axes, legends, or data.

Use a 16:9 PowerPoint slide by default. Do not change the slide aspect ratio to match a Python/R reference unless the user explicitly asks for a non-16:9 slide. The Python/R reference controls the composition inside the slide: panel order, group-block aspect ratio, relative outer margins, row gaps, column gaps, label placement, and panel occupancy.

When the Python/R reference is near-square or portrait, place the entire multi-panel figure as a compact group block inside the 16:9 slide. Do not stretch the grid across the full widescreen width. Center the block or align it according to the requested slide design, leaving intentional side margins. The group block should visually resemble the Python/R composite, while the slide canvas remains 16:9.

For regular grid figures:

- Keep the PowerPoint slide at 16:9 unless instructed otherwise.
- Use the reference composite image dimensions to derive the group-block aspect ratio, not the slide aspect ratio.
- Keep the same number of rows and columns as the reference.
- Match relative outer margins and inter-panel gaps, not just panel order.
- Keep each OLE panel's width/height close to the reference panel's visual bounding box.
- Export the PPT preview and compare the OLE group block against the Python reference after cropping or mentally isolating the group block from 16:9 slide margins.
- If the OLE panels are spread apart merely to fill the 16:9 slide, the layout has failed even when every panel is present.

When using COM automation:

- Treat PowerPoint coordinates and sizes as points; convert inches with `inches * 72`.
- Paste each Origin graph with `GPage.copy_page("OLE")`, then resize and position the OLE shape.
- Insert the Python/R PNG or JPG reference onto slide 2 after slide 1 OLE objects are placed. Do not put the Python reference on slide 1 when double-click-to-Origin is required.
- Add the panel label with `Shapes.AddTextbox`.
- Set label font to Arial bold and size appropriate to final slide scale.
- Group `[OLE shape, label textbox]` where possible.
- Export the slide to PNG and inspect the result.

## Validation Checklist

Do not report completion until:

- The `.opju` exists and contains editable Origin graph pages, not only images.
- Origin was actively launched or attached for the Origin stage, with evidence from `origin_launch`, `origin_probe`, a visible Origin window/process, or successful `originpro` automation.
- Origin panel previews show native bottom/left axes with thickness `2`, major ticks, tick labels, and titles.
- Origin panel previews reproduce the Python/R reference panel type and visual encoding: grouped bars remain grouped bars, horizontal bars remain horizontal bars, labeled scatter remains labeled scatter, log axes remain log axes, and pie panels remain pie/donut-like panels or a documented editable fallback.
- The reference match report exists and marks every required panel as passed, or records a panel-specific residual mismatch and fallback reason. A run with no reference match report is incomplete.
- No Origin preview is a blank/default placeholder graph with only axes and no reference-matching data marks.
- Axis titles are the actual reference labels, not placeholder titles such as `X 轴标题` or `Y 轴标题`.
- Origin graph pages do not contain unwanted panel letters when PPT-side labeling is requested.
- Origin curve colors match the Python/R reference and are not left as default black except for intentionally black reference series.
- Origin curve, spectrum, line, and point-line widths are `2` or greater unless a user-approved override is recorded.
- Every multi-series curve panel has a compact Origin legend or explicit direct labels matching the reference labels.
- Origin graph-page dimensions keep the Origin default proportion unless a panel-specific contract explicitly overrides it.
- Curves are visibly thick enough at final scale.
- PPT slide 1 contains Origin OLE embeddings copied from Origin graph pages and supports double-click-to-Origin behavior.
- PPT slide 2 contains the Python reference PNG/JPG.
- PPT panel letters are present, consistently placed, and grouped or aligned with the OLE panels.
- PPT slide remains 16:9 by default, while the OLE group block's aspect ratio, row gaps, column gaps, and panel occupancy visually match the Python/R composite reference.
- PPT preview PNGs for slide 1 and slide 2 have been exported and inspected.
- A reference-vs-Origin or reference-vs-PPT comparison exists when matching a Python/R reference.
- Any remaining mismatch is stated plainly.
