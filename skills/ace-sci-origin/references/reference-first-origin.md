# Reference-First Origin Workflow

Use this when editable Origin/PPT output must visually match a polished Nature-style figure.

## Principle

Origin is the editable backend, not the visual oracle. First create or identify a high-quality reference preview from the same spreadsheet data, then make Origin match that preview. Do not stop after Origin has merely plotted the data.

The reference preview may be a deterministic matplotlib/R render, an existing user-provided image, or a journal-style composite generated earlier in the task. It must come from the same table data unless the user explicitly provides an external design reference.

## Required Workflow

1. Generate or identify a reference preview.
   - Use the spreadsheet data to render a Nature-style figure with a deterministic renderer when no reference image is provided.
   - Save both raster and vector references:
     - composite: `*_python_reference_300dpi.jpg` and `*_python_reference.svg`
     - panels when separately rendered: `*_<panel>_python_reference_300dpi.jpg` and `*_<panel>_python_reference.svg`
   - Use JPG for rapid visual inspection, PPT preview, and raster delivery. Use SVG as the vector reference for matching and later editing/redrawing.
   - Record the visual contract: panel count, layout, axis ranges, y-axis meanings, colors, line styles, legends, font sizes, and which panel spans multiple grid cells.

Reference-first gate:

- The Python/R reference is not optional decoration. It is the implementation specification for Origin.
- Before Origin automation, write `referenceFirstGate: true` into the style contract and store the exact Python/R reference image path used for visual matching.
- Each panel contract must state the Python panel's chart type and expected Origin construction type. For example: grouped vertical bars, horizontal bars, scatter with labels, log-log scatter, pie chart, dual-axis line, spectra stack, or editable fallback.
- Origin automation must not start from a blank graph template and then merely add placeholder axes. A graph page with placeholder axis titles, missing reference-matching marks, or default black-only marks fails the gate.

2. Convert the reference into an Origin style map.
   - Read [origin-style-contract.md](origin-style-contract.md) and create a panel-level style contract before automating Origin.
   - Do not build Origin pages directly from spreadsheet columns when a reference-first result is requested.
   - For each panel, write a compact mapping table:
     - chart type
     - data columns
     - x/y axis ranges and units
     - right-axis or second-layer variables
     - series color, line width, line style, marker/bar/hatch
     - legend/direct-label text and position
     - Origin page-size policy, normally `origin_default`
     - panel letter location
   - Use explicit plotting tables for Origin, especially for grouped bars, stacked bars, offset categorical x positions, and dual-axis curves.

3. Build Origin graph pages from the style map.
   - Use Origin-native data plots for editable curves/bars.
   - Compile panel-specific construction from the Python reference. Do not use one generic `add_plot` path for every panel.
   - Disable or delete Origin auto legends if they do not match the reference.
   - Set colors after all plots are added and after grouping/rescale; Origin grouping can overwrite colors.
   - Do not leave line, spectrum, or point-line plots as Origin's default black unless the Python/R reference intentionally uses black for that exact series.
   - Preserve the Python/R reference palette as the authoritative semantic color map. Each condition/sample/trace label should use the same color in Origin previews and PPT OLE previews.
   - For multi-series curve panels, build an Origin-native legend or direct labels that use the same labels as the Python/R reference. A panel with correct colored curves but no legend/direct labels is not acceptable.
   - Keep Origin graph pages at the Origin software default proportion unless the style contract explicitly requests a different Origin page size. Use PowerPoint layout to match the Python composite aspect ratio.
   - For dual axes, use true right-y layers when stable; keep ranges identical to the reference.
   - For grouped/stacked categorical bars, do not let Origin treat category labels as continuous values. Create explicit x-position columns and overlay/offset bars to match the reference.
   - For horizontal bars, use an Origin barh-equivalent construction or explicit editable horizontal line/rectangle fallback, preserve category order, and match the Python reference axis direction.
   - For scatter labels, create separate text labels or Origin annotations tied to the point positions. Do not omit labels when the Python reference labels points.
   - For log axes, set native Origin log scale and tick labels. Do not fake log scale by plotting transformed values unless the status file documents a fallback.
   - For pie panels, use Origin pie chart objects when stable; otherwise use editable vector/shape fallback and document why a native Origin pie was not stable through OLE.
   - Keep worksheet columns for any transformed plotting values next to the true values and name them clearly.
   - For normalized comparison panels, create explicit normalized plotting columns rather than plotting raw values and relying on axis tricks.
   - For Raman/spectra stacks, create explicit offset intensity columns and set y-limits from the stacked display range.
   - After operations that can mutate styles (`rescale`, grouping/ungrouping, legend rebuilds, template application), reapply colors, line widths, symbols, bar fills, legend settings, and page-size policy.
   - Treat unstyled Origin pages as a failure even if they contain the correct data.
   - Useful starting templates:
     - `scripts/build_python_reference.py`
     - `scripts/build_origin_from_style_contract.py`
     - `scripts/validate_origin_against_reference.py`

4. Export Origin previews and compare before creating PPT.
   - Export each Origin graph page to PNG.
   - Compare against the reference panel-by-panel.
   - Use `scripts/validate_origin_against_reference.py` for coarse checks, then inspect visually.
   - Fix visible mismatches before pasting to PPT: wrong colors, giant fonts, weak legends, category spacing errors, missing right axes, compressed traces, excessive white space, or nonmatching panel sizes.

5. Create PowerPoint with Origin OLE objects only after Origin previews are acceptable.
   - Copy each Origin graph page as OLE and paste into PPT.
   - Use a 3-row layout when requested; for 8 panels, let one important panel span two columns only if the reference or data hierarchy supports it.
   - Export the PPT slide to PNG and inspect. OLE scaling can change text and legends even when Origin export looks correct.
   - If the user requests double-click-to-Origin behavior, slide 1 must contain Origin OLE objects copied from graph pages. A PNG/JPG/SVG screenshot on slide 1 is not acceptable, and the matching `.opju` source file must be exported and reported.
   - If the user requests "slide 1 Origin, slide 2 Python reference", implement exactly that: slide 1 is Origin OLE copied from Origin graph pages; slide 2 is the deterministic Python/R JPG reference. Do not make the Python reference slide first or substitute raster panels on slide 1.
   - Verify slide 1 OLE with the PPTX package relationships, not just visually: `ppt/slides/_rels/slide1.xml.rels` should contain `relationships/oleObject`, and `ppt/embeddings/oleObject*.bin` should exist. Then still inspect the exported slide preview.
   - If the user also requests an editable Python/R reference slide, put it on a separate slide: insert the reference SVG, convert it to PowerPoint shapes, then ungroup repeatedly so individual vector elements are editable.
   - Validate both editability modes separately: package-check OLE embeddings for slide 1, and shape-count/type-check the converted SVG slide.

6. Iterate from the PPT OLE preview, not only from the Origin window.
   - Compare slide 1 OLE preview against slide 2 Python/R JPG at the same slide size.
   - Fix missing axes, tiny scatter points, compressed curves, wrong panel geometry, and auto legends before reporting completion.
   - When Origin auto legends remain, delete the `Legend` GraphObject directly and repeat deletion before OLE copy.
   - If exact reference matching requires unstable Origin constructs, such as fragile dual axes or categorical text overlays that hide data, keep the Origin OLE version stable and report the residual mismatch. The Python/R JPG on slide 2 remains the exact visual reference.

## Prompt Template For The Agent

Use this internal checklist before writing code:

```text
Reference-first Origin task:
- Input spreadsheet:
- Reference preview image:
- Final deliverables:
- Editable requirement:
- PPT layout:

For each panel, infer:
1. Evidence role:
2. Chart type:
3. Data columns:
4. Axis limits:
5. Right-axis/dual-layer variables:
6. Series style map:
7. Legend/direct-label placement:
8. Origin-specific construction risk:

Implementation rule:
Generate the Nature-style reference first. Then create a panel-level Origin style contract. Compile Origin graph pages from explicit plotting tables and the style contract. Export Origin previews and iterate until they match the reference. Only then paste Origin pages into PPT as OLE.
```

## Visual Matching Criteria

An Origin graph is not acceptable merely because it contains the same data. It should match the reference in these visible traits:

- A blank default Origin graph with only x/y axes is never acceptable as a reference-matched panel.
- Placeholder titles such as `X 轴标题`, `Y 轴标题`, `X Axis`, or `Y Axis` are a failure unless the Python reference literally uses those labels.
- The panel chart type must match the Python reference. A grouped bar panel cannot be replaced by a default scatter panel; a horizontal bar panel cannot be replaced by a blank x-y graph; a pie panel cannot be replaced by a default line graph.
- Origin graph pages must be judged before any PPT-native repair. A graph page with correct curves but missing legends, missing or hairline bottom/left axes, missing axis titles, or visibly thinner curves than the Python/R reference is not acceptable.
- A graph page with all curves rendered in default black is not acceptable when the Python/R reference uses colored series.
- Multi-series curve, line, and spectrum panels must include an Origin-native legend or direct labels. If a shared PPT-side legend is used as a documented hybrid choice, `generation_status.json` must state which Origin panels omit local legends and why.
- Do not hide Origin y-axis titles and replace them only in PowerPoint unless explicitly documenting a hybrid fallback. For normal line panels, the editable Origin graph page itself should contain the data-bearing axes, tick labels, axis titles, panel label, and either a compact legend or direct labels.
- If Origin OLE scaling makes axis titles or legends unstable, first fix the Origin page geometry, font sizes, layer margins, and legend placement; only then consider PPT-native overlays as a documented final-layout workaround.
- Curve width must be validated visually in the exported Origin preview at the final panel scale. A LabTalk width value existing in code is not enough if the rendered curve is still clearly thinner than the reference.
- Same dominant color mapping for the same sample/condition across all panels.
- Same solid/dotted/dashed semantics, especially for capacity vs CE, charge vs discharge, or true vs reference series.
- Comparable axis limits, tick density, and occupied plot area.
- Comparable legend economy: no large boxed Origin auto legends, no raw column names, no legends covering data.
- Similar panel hierarchy and layout, including any wide/spanning panels.
- Arial-like small publication text; no giant labels after OLE paste.
- Correct categorical bar spacing and stacking/overlay behavior.
- Explicitly requested editability semantics: Origin-OLE slides must double-click back to Origin; SVG-reference slides must be converted to PowerPoint shapes and ungrouped, not left as a single picture.

## Reporting Rule

If exact matching is not possible with stable Origin OLE, deliver both:

- the editable Origin/OLE version, and
- the Python reference/final figure as both JPG and SVG.

State the mismatch explicitly, for example: "The PPT contains 8 Origin OLE objects, but panel e uses simplified editable Origin bars; the raster reference is the visual target for publication."
