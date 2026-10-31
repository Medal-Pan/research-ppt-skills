# Excel to Python Reference to Origin OLE Workflow

Use this workflow for spreadsheet-driven scientific figures when the deliverable must include:

- an editable Origin `.opju` project,
- a PowerPoint whose first slide contains Origin OLE objects that can be double-clicked back to Origin,
- a Python/R-rendered reference image on a separate slide,
- 300 dpi raster exports and visual validation previews.

This workflow is reference-first: Python/R defines the visual target; Origin supplies editable graph pages and OLE objects.

## Required Order

### 1. Inspect the workbook

Do this before plotting.

- List every sheet, header row, column names, row counts, units, and nonnumeric columns.
- Identify which sheets map to which figure panels.
- Detect special data shapes: dual-y series, categorical bars, highlighted scatter points, offset spectra, charge/discharge segments, literature benchmarks.
- Do not modify the original Excel workbook.

Outputs:

- a short workbook inventory in the status/report,
- cleaned in-memory data frames or copied plotting tables,
- any assumptions about header rows and units.

### 2. Generate the deterministic Python/R reference

Do this before Origin automation when no trusted reference image already exists.

- Render the complete figure from the spreadsheet with matplotlib/R.
- Decide panel count, layout, panel labels, axis ranges, axis count, color mapping, marker size, line width, bar spacing, legends, and which panel spans multiple columns.
- Treat the Python/R color map and legend labels as the visual contract for Origin. Record each visible series label with its exact color and line/marker style.
- Export a 300 dpi JPG and an SVG/vector reference.
- For the normal ace-sci-origin PPT deliverable, insert the Python PNG/JPG reference on slide 2 unchanged. Slide 1 is reserved for Origin OLE.

Outputs:

- `*_python_reference_300dpi.jpg`,
- `*_python_reference.svg`,
- optional per-panel reference PNG/JPG/SVG files,
- a visual style target for Origin.

### 3. Write the panel style and axis contract

Do this before creating Origin pages.

For each panel, record:

- `referenceFirstGate: true` and the exact Python/R reference image path,
- evidence role and chart type,
- Python reference plot type and Origin construction type,
- source sheet and plotting columns,
- visual series model: separate Origin plot objects for every reference-visible group,
- axis ranges and major tick spacing,
- `axis_count` and `reference_axis_sides` from the Python/R reference,
- marker size, line width, bar width/offset, fill/edge colors,
- legend/direct-label strategy,
- Origin page-size policy, normally `origin_default`,
- known Origin/OLE risks.

Use `origin-axis-contract.md` for axis decisions. A two-axis Python reference means bottom x plus left y; a dual-y reference means bottom x plus left y plus right y.

Outputs:

- `*_style_contract.json` or an equivalent script-local contract,
- explicit plotting tables or transformed columns for Origin.

This stage is a hard gate. If the contract does not say how a Python reference panel maps to an Origin construction, do not proceed to Origin graph creation. In particular, mixed figures must not be collapsed into generic x-y placeholder graphs.

### 4. Build Origin-native graph pages

Do this from explicit plotting tables, not raw template defaults.

- Actively launch or attach to Origin/OriginPro before graph creation. Use `origin_launch` and/or `origin_probe`, then run Origin automation with `origin_run_python`; do not treat "Origin is not already open" as a stopping condition.
- If Origin was previously usable on the machine, retry launch/attach once after a short wait and record the actual tool result before reporting a blocker.
- Start a new Origin project.
- Import cleaned data and Origin-specific plotting tables into worksheets.
- Create one graph page per panel or per OLE object.
- Keep each Origin graph page at the Origin software default proportion unless the style contract explicitly overrides it. Do not resize Origin pages to matplotlib figure proportions just to match the composite reference.
- Add data plots as Origin-native plots, not screenshots.
- Select the Origin graph type from the reference contract, not from a generic default. For example:
  - grouped vertical bars -> explicit x positions with offset bar objects or editable rectangle fallback,
  - horizontal bars -> horizontal bar construction or editable horizontal rectangle/line fallback,
  - labeled scatter -> scatter plot plus data-bound text labels,
  - log scatter -> native log axes with marker styling and labels,
  - pie chart -> Origin pie object or documented editable vector fallback,
  - dual-y line -> true right-y layer or documented scaled fallback,
  - multi-series line/spectrum -> one plot object per reference-visible series.
- Split visual groups into separate plot objects: highlighted points, grouped-bar conditions, charge/discharge curves, capacity/energy series, stacked spectra.
- For offset spectra or normalized panels, keep raw values when needed and create clearly named plotted columns.

Outputs:

- editable Origin worksheets,
- editable Origin graph pages,
- no image-only substitute for required editable panels.

### 5. Apply formatting and reapply it after mutating operations

Do this after all plots are added, and repeat after `rescale`, grouping, legend rebuilds, and template operations.

- Apply axis contract: required axis lines, ticks, tick labels, and titles must be explicitly enabled.
- Disable non-data top/right axes unless the reference or user requires them.
- Set exact x/y ranges and tick intervals; do not rely on autoscale.
- Use Arial, white background, no gray internal grid unless requested.
- Set Origin curve and point-line width to `2` by default.
- Do not use Origin curve/line/spectrum widths below `2` unless the user explicitly requests thinner lines and the override is recorded in `generation_status.json`.
- Set scatter marker size/fill/edge explicitly; Origin defaults are often too small.
- Set colors using stable RGB tuples or Origin-safe color values when hex parsing is unreliable.
- Do not leave curves as Origin's default black unless the Python/R reference intentionally uses black for that exact series.
- Delete auto legends that expose raw column names or overlap the panel, then rebuild compact frameless Origin legends or direct labels from the reference labels.
- For multi-series line, curve, spectrum, or point-line panels, a visible legend or direct-label mapping is mandatory before the panel can pass QA.

Outputs:

- styled Origin graph pages that visually resemble the Python/R reference at panel scale.

### 6. Export Origin previews and iterate before PPT

Do this before any OLE paste.

- Export every Origin graph page to PNG.
- Compare panel-by-panel against the Python/R reference.
- Reject and repair any preview that looks like a blank default Origin graph, contains placeholder axis labels, uses default black marks, omits the Python reference chart type, or lacks required legends/direct labels.
- Check axes, marker size, line width, bar spacing, legend economy, plot-area occupancy, and series semantics.
- Check that Origin curve colors match the Python/R reference and are not default black.
- Check that every multi-series curve/line/spectrum panel has a legend or direct labels.
- Check that Origin graph pages keep the Origin default proportion unless the style contract says otherwise.
- Make a contact sheet when there are multiple panels.
- Fix missing bottom/left axes, tiny scatter points, wrong axis ranges, auto legends, and compressed traces before PowerPoint.

Outputs:

- `origin_previews/FigX*.png`,
- optional `*_reference_vs_origin_contact_sheet.png`.

### 7. Save and validate the `.opju`

Do this before or immediately after PowerPoint creation.

- Confirm the Origin stage was actually reached: Origin was launched/attached or `originpro` automation successfully created the project.
- Save the Origin project to a timestamped `.opju` path during iteration.
- Do not trust only the return value of `op.save()`.
- Validate the `.opju` by file existence and a plausible file size after a short wait.
- Keep Origin open until OLE copy is complete, then call `op.exit()`.

Outputs:

- `*_editable_origin_project.opju` or timestamped `*_origin_reference_project_YYYYMMDD_HHMMSS.opju`.

### 8. Create the PowerPoint with the required slide order

For the common "Origin first, Python second" requirement:

- Slide 1: paste Origin graph pages as Origin OLE objects with `GPage.copy_page("OLE")` or the Origin GUI equivalent, so double-click opens the Origin/OLE source.
- Slide 2: insert the Python/R 300 dpi PNG/JPG reference.
- Do not substitute slide 1 with the Python JPG, SVG, or screenshots when double-click-to-Origin is required.
- Do not omit slide 2; if the Python reference image is missing, create or recover it before considering the PPT complete.
- Lock OLE aspect ratio.
- Use PowerPoint COM points for placement and sizing; convert inches with `inches * 72`.
- Use retries and short waits around clipboard/OLE paste.
- Use timestamped PPT filenames during iteration because PowerPoint may lock old files.

Outputs:

- `*_Origin_OLE_group_figure.pptx`,
- slide 1 containing Origin OLE objects,
- slide 2 containing the Python/R PNG/JPG reference.

### 9. Validate OLE editability and visual rendering

Do both package validation and visual validation.

Package validation:

- Inspect `ppt/embeddings/oleObject*.bin`.
- Inspect `ppt/slides/_rels/slide1.xml.rels` for `relationships/oleObject`.
- Count expected OLE relationships on slide 1.

Visual validation:

- Export slide 1 to PNG and inspect it.
- Export slide 2 to PNG and inspect it.
- Compare slide 1 OLE preview against slide 2 Python/R reference.
- Check that axes, scatter marker size, legends, panel geometry, and text are not broken by OLE scaling.
- Check that Origin curve/line/spectrum widths are still at least `2` after OLE scaling unless a recorded override exists.

Outputs:

- `*_PPT_OLE_preview.png`,
- `*_python_JPG_slide_preview.png`,
- `*_generation_status.json` with paths and validation result.

### 10. Report deliverables and residual mismatches

The final response must clearly state:

- `.opju` path,
- `.pptx` path,
- slide 1 preview path,
- slide 2 reference preview path,
- Python/R reference JPG/SVG paths,
- OLE validation result,
- any residual mismatch between editable Origin/OLE output and the Python/R visual reference.

Do not claim a panel is fully Origin-editable if labels, legends, bars, or annotations were rebuilt as PPT-native objects. Report hybrid elements explicitly.

## Required Deliverables

Use clear timestamped or final filenames:

- `*_editable_origin_project.opju` or `*_origin_reference_project_YYYYMMDD_HHMMSS.opju`
- `*_Origin_OLE_group_figure_YYYYMMDD_HHMMSS.pptx`
- `*_python_reference_300dpi.jpg`
- `*_python_reference.svg`
- `*_Origin_OLE_PPT_preview_YYYYMMDD_HHMMSS.png`
- `*_python_JPG_slide_preview_YYYYMMDD_HHMMSS.png`
- `*_generation_status.json`
- optional `origin_previews/*.png`
- optional `*_reference_vs_origin_contact_sheet.png`

## Common Failure Points From This Workflow

- A `.pptx` exists but slide 1 contains pictures instead of Origin OLE objects.
- A `.pptx` exists but slide 2 does not contain the Python PNG/JPG reference.
- A `.opju` was not exported or was not reported, so the double-click-to-Origin requirement is incomplete.
- The Python reference was used as a final screenshot, but Origin pages were not made to match it.
- Origin pages were blank/default x-y graphs rather than compiled from the Python reference style contract.
- Mixed panel types from the Python reference, such as grouped bars, horizontal bars, labeled scatter, log scatter, and pie charts, were all replaced by the same generic Origin x-y template.
- Placeholder labels such as `X 轴标题` or `Y 轴标题` appeared in Origin/PPT previews.
- Origin graph pages contain correct data but missing axes, tiny scatter points, default black styles, or boxed auto legends.
- Origin graph pages use the correct data but leave all curves black, omit legends for multi-series panels, or change Origin page proportions unnecessarily.
- Origin graph pages use line widths below `2`, making curves too thin after PPT scaling.
- `legend -d` did not remove the actual `Legend` GraphObject.
- Origin template or `rescale` reset axis visibility, colors, line widths, or marker sizes.
- PowerPoint COM received EMU units instead of points, causing huge/off-slide OLE panels.
- OLE package validation passed but the exported slide preview still looked wrong.
- Exact dual-y or categorical-label matching was unstable in OLE; the stable Origin/OLE version and the Python visual reference must both be delivered and the mismatch reported.
