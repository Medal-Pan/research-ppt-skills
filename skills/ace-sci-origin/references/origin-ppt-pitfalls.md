# Origin to PowerPoint Pitfalls

Use this reference before creating or repairing editable Origin/PPT scientific figures.

## Pitfalls Observed

### 0. End-to-end requirement drift

Symptoms:

- the user asked for slide 1 as Origin OLE and slide 2 as Python JPG, but the output order or content changed
- the workflow produced a good Python figure but no editable Origin `.opju`
- the PPT looked right but double-click did not return to Origin
- the script treated Origin OLE as optional after the user made it a core requirement

Avoidance:

- Write the deliverable contract before coding: slide 1 contents, slide 2 contents, `.opju` requirement, JPG/SVG exports, and OLE validation.
- For "slide 1 Origin, slide 2 Python reference", implement exactly that order. In ace-sci-origin this is the default complete PPT contract: slide 1 is Origin OLE, slide 2 is the Python PNG/JPG reference.
- Treat Origin OLE and `.opju` as mandatory when double-click-to-Origin is requested.
- Keep a `*_generation_status.json` with all final paths and validation results.

### 1. Origin OLE can visually corrupt complex graph pages

Symptoms:

- huge axis titles or tick labels in PowerPoint
- rotated labels covering adjacent panels
- dual y-axis text exploding in size
- panel letters or labels appearing in the wrong scale

Avoidance:

- Do not paste complex multi-layer dual-axis Origin pages directly into PPT without preview.
- Lock OLE aspect ratio in PowerPoint.
- For final PPT, use a hybrid layout when necessary: Origin OLE for simple curves, PPT-native shapes/text for fragile axes, legends, and annotations.

### 2. Origin legends can be fragile in OLE

Symptoms:

- auto legends remain even after `legend -d`
- raw worksheet names or column numbers appear as legends
- legends are clipped or overlap data after OLE paste
- legend entries like `SCOn` or `SROn`
- failed line breaks
- broken subscript formatting
- unreadable tiny or huge legend text

Avoidance:

- Prefer Origin-native frameless legends when they render correctly.
- Keep legends compact and place them in empty data regions or outside the data layer.
- Avoid building ad hoc legends from separate drawn line objects plus text objects unless Origin's native legend cannot express the needed mapping.
- If an Origin legend breaks after OLE export, simplify and repair it in Origin first. Use PPT-native legend elements only as a documented final-PPT workaround.
- Do not trust `legend -d` alone. In `originpro`, also delete the actual graph label object, for example `gl.label("Legend").remove()` or `gl.remove_label("Legend")`, after all plots/styles are applied and again immediately before `copy_page("OLE")`.
- For `RuO2`, use Origin `RuO\-(2)` or PPT superscript/subscript formatting.

### 3. Four-sided axes are optional and not the same as dual axes

Nature-style plots often use only left and bottom axes. If the user asks for four axis lines/frame sides, that still does not mean four independent data axes.

Symptoms:

- bottom x-axis or left y-axis disappears after a template/rescale/OLE paste
- top x-axis and right y-axis ticks remain visible even though they do not encode data
- a simple voltage-capacity curve looks like it has four axes
- reviewers may interpret decorative top/right ticks as missing or unlabeled secondary axes

Avoidance:

- Create an axis contract before plotting: count visible sides in the Python/R reference for every panel.
- Explicitly enable the required bottom x and left y axes, ticks, tick labels, and titles after templates/rescale/grouping and again before export/OLE copy.
- Do not force top/right frame lines by default.
- For simple plots, use left/bottom axes unless a full frame is requested or scientifically clearer.
- Do not enable secondary axes with labels unless scientifically needed.
- In Origin automation, explicitly disable or hide non-data top/right axes and tick labels after applying templates. Do not assume the template default matches the desired journal style.
- If requested top/right axis lines disappear after OLE, first repair the native Origin axis Line and Ticks settings and validate an exported Origin preview before copying to PPT. Do not use ordinary drawn lines as substitutes for required data axes.

### 3b. Missing required axes are a blocking issue

Symptoms:

- Origin preview contains data and titles but no bottom/left axis lines
- the Origin UI dialog shows axes enabled, but the exported preview or PPT OLE preview lacks them
- a dual-y Python reference becomes a one-y-axis Origin panel without explanation

Avoidance:

- Apply `origin-axis-contract.md` for every reference-first figure.
- Reapply axis visibility after all data plots are added, after `rescale`, after grouping, after legend operations, and immediately before `GPage.copy_page("OLE")`.
- Validate by exported preview, not by the Origin dialog state. Count visible axis sides in the preview at final panel size.
- For a two-axis reference, bottom x plus left y is mandatory. For a true dual-y reference, bottom x plus left y plus right y is mandatory unless a documented stable fallback is used.

### 4. Right y-axis for bar charts can break in OLE

Symptoms:

- giant right-axis title
- right-axis ticks too large
- right-axis label overlaps neighboring panels

Avoidance:

- In Origin, keep a true editable dual-axis graph if needed.
- In PPT final group figure, consider plotting bars as PPT-native editable rectangles and manually placing the right-axis tick labels.
- If plotting dual-axis values on one layer, create scaled columns, e.g. `Specific_activity_scaled`, while preserving true values in adjacent columns.

### 5. File existence is not validation

Failures can produce valid-looking files:

- `op.save()` may return a misleading value. Validate the `.opju` by file existence and size after a short wait.
- `.opju` may be a small shell/preview file if saved incorrectly.
- `.pptx` may contain OLE objects but still render badly.
- JPG may be 300 dpi but visually wrong.
- `.opju` may contain graph pages with real data plots that are still unacceptable because they use Origin defaults: black lines, boxed clipped legends, wrong grouping colors, missing bar offsets, no scaled/offset plotting columns, or no reference-matched panel styling.
- `.pptx` may contain high-resolution pictures that look right but are not double-clickable Origin OLE objects.
- A Python/R SVG inserted into PPT may remain a single SVG picture unless it is explicitly converted to PowerPoint shapes and ungrouped.

Validation:

- Check `.opju` size and page inventory.
- Inspect graph/image page types if possible.
- Export PPT slide to PNG and view it.
- Check JPG DPI metadata.
- Export Origin graph previews and inspect them against the reference. Do not accept an Origin graph page just because the data plotted.
- Inspect the `.pptx` package for `ppt/embeddings` and slide `oleObject` references when Origin OLE was requested.
- For double-click-to-Origin PPTs, inspect slide 1 relationships: `ppt/slides/_rels/slide1.xml.rels` should contain `relationships/oleObject`, and `ppt/embeddings/oleObject*.bin` should exist. A string search in `slide1.xml` alone can miss or misclassify the result.
- Inspect the shape tree or use PowerPoint's Selection Pane when SVG-to-shapes was requested; a single Picture/SVG object is not enough.

### 5b. Origin restyling can be overwritten after plotting

Symptoms:

- a curve turns black after initially being colored
- line widths or symbols revert after `rescale`, grouping, or legend rebuild
- grouped bar colors follow Origin's default palette rather than the reference
- a graph preview exported from Origin differs from the script's intended style map
- highlighted points become ordinary template symbols because the reference categories were not split into separate Origin plot objects
- grouped bars overlap or become too wide because the Origin column template ignores explicit visual spacing

Avoidance:

- Add all plots first, then rescale, then ungroup if needed, then apply colors/line widths/symbols.
- Apply plot styles again after any `layer -g`, `layer.group(...)`, `rescale`, legend rebuild, or template command.
- Prefer RGB tuples or Origin color names/indexes when LabTalk parsing of `#RRGGBB` is unreliable.
- Keep explicit plotting tables for grouped bars, normalized metric lines, scaled dual-axis fallbacks, and offset Raman/spectra traces.
- Split visual categories into separate Origin data plots. For example, make one plot for gray literature points and a second plot for red "This work" points; make separate plots for charge and discharge; make separate plots for each grouped-bar condition.
- If the built-in column/bar template does not preserve reference spacing, use explicit x-position columns or editable thick vertical/horizontal line segments as a controlled fallback, while preserving true values in the worksheet.

### 6. Origin autoscale can produce publication-unusable panels

Symptoms:

- curves occupy only a small fraction of the frame
- large empty areas above or beside spectra
- group figure looks sparse even though each single graph technically contains data
- stacked spectra/FT curves are compressed because autoscale includes irrelevant extremes

Avoidance:

- Compute data ranges sheet-by-sheet before plotting.
- Set explicit x/y limits for each panel after deciding the scientific region of interest.
- For stacked traces, check whether the spreadsheet already contains offsets before adding new offsets.
- Validate the exported group figure at the size it will be read, not only each full-size panel.

### 7. Origin templates are not always good final renderers

Symptoms:

- Origin graph pages are editable but visually loose in a PPT grid
- default margins and fonts dominate the panel
- automatic legends reappear after plots are added
- line widths look acceptable in Origin but too thin after slide scaling
- template-created legends, top/right axes, or rotated axis titles remain after restyling and appear in exported previews

Avoidance:

- Keep editable Origin graph pages in the `.opju`, but use a deterministic renderer for final JPG/PPT panels when precise layout is needed.
- If using a deterministic renderer, state that final PPT panels are image-based or hybrid while the Origin project remains editable.
- Tune font sizes, line widths, margins, and label placement for the final composite scale.
- Remove auto legends after all plots are added, not only before plotting.
- Remove or hide template axis titles before adding replacement labels. If you use small text labels as a workaround for unstable Origin axis-title objects, make sure the old axis-title objects are gone and the preview does not show duplicates.
- Do not judge a graph page from the Origin window alone. Export a PNG preview and compare it beside the reference at the final panel scale; template-driven differences in line width, marker shape, and bar width often become obvious only in a contact sheet.
- If the required first slide is Origin OLE, do not replace the OLE objects with the deterministic renderer. Instead, make the Origin pages as close as practical, export a PPT preview, and state any remaining visual limitations.

### 7b. Correct data can still produce the wrong visual semantics

Symptoms:

- a scatter plot contains all points but fails to highlight "This work"
- a grouped bar panel contains all values but each condition is not independently colored
- normalized metrics appear as loose points instead of bars or horizontal comparisons
- charge/discharge curves use the same line style or a dotted style that does not match the reference
- Raman or spectra curves are correctly offset but lack the direct voltage labels used in the reference

Avoidance:

- Recreate the reference's visual series model explicitly. Each visual group should usually become its own Origin plot object with its own x/y columns, color, line style, marker, and legend/direct label.
- For ordered or segmented traces, split the data at resets or discontinuities before plotting so Origin does not draw false connecting lines.
- Build a side-by-side reference-vs-Origin contact sheet and iterate until the scientific comparison reads the same, even if minor typography remains different.

### 8. Legends and labels can make dense panels worse

Symptoms:

- boxed legends cover peaks or traces
- direct labels collide at curve endpoints
- every-condition labels are unreadable after shrinking to a 3x3 group figure

Avoidance:

- Prefer no-frame compact legends in empty regions for dense XAS/spectrum panels.
- Direct-label only curves with well-separated endpoints.
- Label key conditions and references rather than every trace when the visual density is high.
- For temperature or potential series, offset labels vertically and keep them inside the plot bounds.

### 9. Origin OLE automation has unit and clipboard traps

Symptoms:

- pasted OLE panels are off-slide or huge because PowerPoint COM received EMU values
- OLE objects paste intermittently or paste as the previous clipboard content
- old `.opju` or `.pptx` files cannot be overwritten because Origin/PowerPoint still has a handle open

Avoidance:

- PowerPoint COM uses points. Convert inches to points with `inches * 72`; do not pass `python-pptx` EMU values into COM shape properties.
- After `GPage.copy_page("OLE")`, wait briefly and retry `Shapes.Paste()` several times. Confirm `slide.Shapes.Count` increased.
- Use timestamped output paths during iterative generation, and close PowerPoint presentations plus `op.exit()` at the end.

### 10. Dual axes and categorical labels may not survive reference matching

Symptoms:

- an attempted Origin dual-axis OLE graph loses one series or maps it to the wrong scale
- categorical x/y labels become numeric positions after using explicit plotting columns
- PPT-native labels placed over an OLE panel cover data after export

Avoidance:

- Preserve stable Origin OLE data plots first. If a dual-axis construction is unstable, document the mismatch and keep the Python reference JPG/SVG as the visual target.
- For categorical panels, create explicit plotting tables and then verify the exported OLE preview. If labels are unstable, use minimal PPT-native labels outside the data region or leave the Python reference slide as the exact label reference.
- Do not force text overlays that obscure data just to mimic the reference. A stable OLE figure with a clearly reported mismatch is preferable to a visually cluttered slide.

### 11. Practical lessons from the Figure 4 Excel/Origin/PPT workflow

Observed issues:

- Origin graph pages initially contained data but did not visually match the Python reference.
- Some Origin outputs lost or hid required axes; axis visibility had to be made an explicit contract.
- Scatter markers were too small until marker size was set explicitly from the reference.
- Auto legends survived `legend -d` and had to be removed by deleting the `Legend` GraphObject.
- PowerPoint OLE package checks passed even when the rendered slide still needed visual fixes.
- A true or attempted dual-y Origin/OLE reconstruction could become unstable; stable OLE editability and the Python reference had to be delivered together.
- PowerPoint COM placement uses points, not `python-pptx` EMUs.
- `GPage.copy_page("OLE")` and clipboard paste needed waits/retries.
- Old `.opju` and `.pptx` outputs could be locked by Origin/PowerPoint, so timestamped filenames were safer.

Required response:

- First inspect the Excel workbook.
- Then create the Python/R reference and use it as the visual contract.
- Then build explicit Origin plotting tables and Origin-native graph pages.
- Then apply style and axis contracts repeatedly after Origin mutating operations.
- Then export Origin previews and compare against the reference.
- Then save and validate the `.opju`.
- Then create PPT slide 1 from Origin OLE and slide 2 from the Python/R PNG/JPG. Do not report the PPT complete if slide 2 is missing the Python reference image.
- Then validate OLE package structure and exported slide previews.
- Finally report all paths and residual mismatches.

## Practical Checks

### Origin project inventory

Use `originpro` to open and list pages:

```python
import originpro as op
op.open(r"path\figure.opju")
print("graphs:", [(g.name, g.lname) for g in op.graph_list()])
print("images:", [p.name for p in op.pages("i")])
print("books:", [p.name for p in op.pages("w")])
op.exit()
```

If the user demanded editable Origin curves, `images` should usually be empty or only contain supplementary previews.

### PowerPoint preview export

After creating PPT, export slide 1 to PNG and inspect it:

```powershell
$pp = New-Object -ComObject PowerPoint.Application
$pres = $pp.Presentations.Open("C:\path\figure.pptx", $true, $false, $false)
$pres.Slides.Item(1).Export("C:\path\preview.png", "PNG", 1920, 1080)
$pres.Close()
$pp.Quit()
```

Then use image viewing to inspect for giant text, broken legends, missing axes, or overlaps.

### OLE package check

When the first PPT slide is supposed to double-click back to Origin, check the package:

```python
from pathlib import Path
import zipfile

ppt = Path("figure_Origin_OLE_group_figure.pptx")
with zipfile.ZipFile(ppt) as z:
    names = z.namelist()
    print([n for n in names if "embeddings" in n])
    print([n for n in names if "oleObject" in n])
```

This proves OLE structures exist, but still export the slide to PNG and inspect the rendered result.

### SVG-to-PPT-shapes check

When a Python/R SVG reference must become editable PowerPoint geometry:

1. Insert the SVG on its own slide.
2. Convert it to shapes using PowerPoint's object model/UI command.
3. Ungroup repeatedly until no further ungrouping is available or until ungrouping would destroy text/geometry.
4. Check that the slide is not just one Picture/SVG object.
5. Export a PNG preview and inspect for missing text, broken symbols, or shifted axes.

### PPTX package sanity check

When PowerPoint COM is unstable, check the package:

```python
from pathlib import Path
import zipfile
ppt = Path("figure.pptx")
with zipfile.ZipFile(ppt) as z:
    names = z.namelist()
    print([n for n in names if n.startswith("ppt/slides/slide") and n.endswith(".xml")])
    print([n for n in names if "embeddings" in n or "oleObject" in n])
```

This proves file structure, not visual correctness.

## Style Defaults

Use these unless user specifies otherwise:

- Font: Arial
- Axis/spine color: black
- Background: white
- Grid: off
- Spines: left and bottom by default; four-sided frames only when requested or scientifically useful
- Panel labels: bold, top-left outside/near frame
- Palette: Nature-style restrained colors, e.g. deep blue `#0F4D92`, medium blue `#3775BA`, neutral black `#272727`, muted red `#B64342`, teal `#42949E`, violet `#9A4D8E`
- Legends: Origin-native, compact, frameless where feasible; avoid separate drawn legend lines/text unless repairing an unstable export
- Export: 300 dpi JPG, plus editable `.opju` and `.pptx` when requested

## Communication Rule

Be explicit when a PPT panel is a hybrid:

- "2a and 2c are Origin OLE objects; 2b is PPT-native editable shapes because Origin dual-axis OLE rendered unstable."

Do not claim every PPT element is Origin OLE if text/legend/bar parts are PPT-native.
