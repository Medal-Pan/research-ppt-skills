# Nature Style for Origin and PPT

Use this reference to adapt the `nature-figure` contract and visual stance to an Origin-first workflow. Do not import the Python/R backend gate from `nature-figure`; this skill is for Origin, PowerPoint OLE, and spreadsheet-driven figure delivery.

## Figure Contract

Before drawing, define:

- Core conclusion: one sentence that the figure must defend.
- Evidence chain: each panel must provide a distinct reason to believe the conclusion.
- Archetype: quantitative grid, schematic-led composite, image plate + quant, or asymmetric mixed-modality figure.
- Export contract: editable Origin graph pages, PPT group layout, OLE expectations, 300 dpi JPGs, and final page size.
- Review risks: ambiguous units, missing `n`, unclear error bars, hidden data transformations, axis ranges that exaggerate or hide effects, and non-editable deliverables when editability was requested.

For spreadsheet-only requests, infer the contract from sheet names, units, and data shape. If the science claim cannot be known, use a neutral contract such as "compare trends and magnitude differences across the provided experimental conditions" and make the panel roles explicit.

## Layout Stance

- The chart serves the scientific argument. Do not add panels only to fill space.
- Prefer one visually dominant panel plus smaller supporting panels when the data naturally has a main result.
- Use equal-size panels only for true parallel comparisons.
- Panel labels should be small, bold, lowercase letters near the top-left edge.
- Use whitespace and alignment for grouping; avoid decorative panel boxes.
- Use direct labels or one shared legend strip when possible. Avoid repeated legends inside every axis.
- Keep gutters tight but real. Increase spacing when a dual-axis or dense annotation needs room.

## Typography

- Use Arial consistently in Origin, PowerPoint, and exported raster images.
- At final journal-like scale, use approximately 5-7 pt for dense tick/legend text and about 8 pt for panel labels.
- For slide-sized editable PPT previews, scale text so the exported 300 dpi JPG remains readable without looking like a poster.
- Keep labels short and unit-complete. Prefer `Potential (V vs. RHE)` over ambiguous axis names.
- Preserve case, chemical notation, and exponents. In Origin use escape codes for superscript/subscript when needed, for example `cm\+(-2)` and `RuO\-(2)`.

## Axes and Frames

- Follow the `nature-figure` default for most quantitative plots: show left and bottom axes/spines; top and right frame lines are optional and should appear only when the user asks for a full frame, when a journal/template requires it, or when the chart type genuinely benefits from a four-sided frame.
- When matching a Python/R reference, count the visible axis sides per panel and follow that count. A two-axis reference means bottom x and left y must both be visible; a true dual-y reference means bottom x, left y, and right y must be visible.
- Do not use gray internal grid lines unless the data type absolutely requires them.
- Use black axis/spine lines, sparse ticks, and tight but honest ranges.
- Do not rely on autoscale for final output. Set ranges after inspecting data and known scientific context.
- Never force a 0 baseline when values occupy a narrow high range unless the quantity or chart type requires it.
- For multiple comparable panels, reuse axis ranges and tick logic where the comparison depends on geometry.

## Color

Use a restrained Nature-like palette with consistent semantic mapping across all panels:

- Key/hero series: deep blue `#0F4D92` or medium blue `#3775BA`.
- Secondary/reference: neutral dark `#272727`, neutral mid `#767676`, neutral light `#CFCECE`.
- Positive direction or improvement: green `#2E9E44` or muted green `#8BCF8B`.
- Negative direction, loss, or callout: muted red `#B64342` or red `#E53935`.
- Accent, used sparingly: teal `#42949E` or violet `#9A4D8E`.

Rules:

- Keep the same condition mapped to the same color in every panel.
- Prefer related hue families over many saturated unrelated colors.
- Reserve bright red/green for directional meaning, thresholds, or callouts.
- Use hatches, marker shapes, or line styles when grayscale interpretability matters.

## Chart-Type Choices

- Line/curve plots: use for spectra, temporal traces, voltage/current profiles, and continuous x values. Use direct labels or a compact frameless Origin legend. In Origin, set Plot Details / Line / Width (`绘图细节 -> 线条 -> 宽度`) to `2` by default.
- Point-line plots: use when x is ordered but discrete, such as cycle metrics, time-course summaries, rate steps, or repeated ordered conditions. Do not use bars just because x labels are categorical if the ordering/trend is the evidence. In Origin, set line width to `2` by default.
- Scatter with fit or guide line: use for relationships, calibration, correlations, and paired measurements. Avoid connecting independent scatter points unless the order has scientific meaning.
- Bars/grouped bars: use for small categorical comparisons, composition summaries, or single-value condition summaries with clear definitions. Use black edges and modest saturation. Avoid bars for distributions when raw replicates are available.
- Error-bar plots: use when the sheet includes mean with SD/SEM/CI or replicate-derived uncertainty. Show what the error bar means in labels/captions or worksheet column names; do not invent error bars.
- Box/violin/strip: use for distributions, repeated measurements, or replicate-level comparisons instead of hiding variability in bars. Overlay strip points when sample size is small.
- Heatmaps/cloud maps/contour maps: use for matrices, dense pairwise comparisons, 2D spatial fields, parameter sweeps, or intensity maps. Use perceptually ordered palettes and clear colorbar units. Use contour/filled contour only when interpolation is scientifically defensible.
- 2D image/map panels: use for microscopy, spatial maps, diffraction/intensity images, or any data already representing a field. Preserve aspect ratio and add scale bars/colorbars when meaningful.
- Sankey/alluvial: use only for real flow/composition transitions, mass/energy/material pathways, or category transitions where conserved quantities or counts move between states. Do not use Sankey for ordinary categorical summaries.
- Dual axes: avoid unless units are genuinely coupled and the visual mapping is stable in Origin/PPT. If OLE breaks dual-axis output, document a hybrid PPT-native reconstruction while keeping editable Origin data and graph pages.

## PowerPoint OLE Translation

- Simple Origin graphs can be pasted as OLE objects and resized with locked aspect ratio.
- Complex Origin graphs may render differently after OLE paste. Before delivery, export a PPT preview PNG and inspect it.
- If OLE corrupts legends, rotated labels, dual axes, or text sizes, first simplify the Origin graph. Use a hybrid layout only when needed: keep the Origin graph/data editable in `.opju`, but rebuild fragile labels or shape-heavy components in PPT.
- Do not claim a PPT element is Origin-editable unless it is an actual Origin OLE object.

## Reference-Driven Origin Styling

When a polished reference preview exists, treat it as the style target:

- Export each Origin graph page to PNG and compare it to the reference before making the PPT.
- Build a side-by-side contact sheet for multi-panel figures: Python/R reference on the left and Origin export on the right for each panel. Use it to catch mismatched axis ranges, line widths, marker shapes, bar widths, missing highlights, missing direct labels, and template legends.
- Set plot colors after all data plots have been added and after any Origin grouping or rescale operation; Origin can overwrite colors and line styles during grouping.
- Never accept Origin default black curves for colored reference series. Copy the Python/R reference palette into explicit Origin series styles and reapply it before preview export and OLE copy.
- Set curve/point-line width to `2` after all data plots have been added and after any Origin grouping or rescale operation; Origin can overwrite line widths during grouping.
- Delete or disable Origin auto legends if they show raw column names or large boxes. Rebuild compact legends or direct labels to match the reference. For ace-sci-origin multi-series curve, line, point-line, and spectrum panels, an Origin-side legend or direct-label mapping is mandatory unless the status file documents a shared PPT-side legend as a hybrid exception.
- Keep each Origin graph page in the Origin software default proportion unless the style contract explicitly overrides the page size. Use PPT OLE placement to match the multi-panel Python reference layout.
- For dual-axis panels, prefer true right-y layers with the same ranges as the reference. Avoid scaled fake-axis values unless the final report states the transformation clearly.
- For grouped or stacked categorical bars, create explicit x-position plotting columns. Do not let Origin's default category spacing or grouped-column template decide the visual geometry if the reference uses offset bars, overlays, hatches, or stacked components.
- Split visual series into explicit Origin plot objects. Ordinary points and highlighted points, charge and discharge curves, each grouped-bar condition, and each stacked spectrum should usually be separate plots with their own columns and styles.
- If Origin's native template cannot reproduce reference geometry, use controlled editable fallbacks: thick line segments for bar-like panels, explicit offset columns for grouped categories, or PPT-native shapes for final fragile annotations. Keep the true data in the Origin workbook and document the workaround.
- For PPT OLE, inspect the slide export after paste; text that looks correct in Origin can still resize badly in PowerPoint.

## Final QA

Check every final package for:

- `.opju` contains editable worksheets and graph pages, not only imported images.
- PPT contains the expected OLE objects or clearly documented hybrid components.
- Axis/spine visibility matches the requested style; do not require top/right frame lines by default.
- Required axis sides from the reference are visible in both Origin previews and PPT/OLE previews. Missing bottom/left axes is a failure, even when curves and labels are otherwise correct.
- No gray grid lines inside curve panels unless intentionally required.
- Arial is used, with correct case and notation.
- Axis ranges and tick labels match the intended scientific comparison.
- Visual series match the intended scientific comparison: highlighted points, grouped bars, segmented curves, and stacked spectra are not collapsed into one template-styled plot.
- Colored reference series are still colored in Origin previews and are not reset to default black.
- Legends are frameless, compact, present for multi-series Origin curve panels, and not broken by OLE export.
- 300 dpi JPG exports have correct DPI metadata.
- A visual preview of the PPT group figure has been exported and inspected.
