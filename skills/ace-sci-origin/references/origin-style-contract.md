# Origin Style Contract

Use this before automating Origin graph pages for publication figures. The contract is the bridge between the Python/R reference figure and editable Origin output.

## Rule

Do not let Origin templates decide the final visual style. For each panel, create a style contract first, then compile it into Origin commands/properties.

## Required Contract Fields

Each panel should have a JSON-like contract with these fields:

```json
{
  "referenceFirstGate": true,
  "referenceImage": "Fig4_python_reference_300dpi.jpg",
  "panel": "4a",
  "role": "cycling stability with capacity and CE",
  "plot_type": "dual_y_line",
  "python_reference_plot_type": "dual_y_line",
  "origin_construction": "true_right_y_layer_line",
  "data": {
    "sheet": "Figure 4a",
    "x": "cycle",
    "y_left": ["MA-21.capacity_ah", "MA-1.capacity_ah", "MA-22.capacity_ah"],
    "y_right": ["MA-21.ce_pct", "MA-1.ce_pct", "MA-22.ce_pct"]
  },
  "layout": {
    "origin_page_size": "default",
    "page_aspect": "origin_default_unless_explicitly_overridden",
    "layer_rect_pct": [14, 12, 78, 74],
    "panel_label": {"text": "a", "x_pct": -10, "y_pct": 106}
  },
  "axes": {
    "axis_count": 3,
    "reference_axis_sides": ["bottom", "left", "right"],
    "x": {"label": "Cycle number", "range": [0, 260], "major_step": 50, "minor_ticks": 1},
    "y_left": {"label": "Capacity (Ah)", "range": [0, 0.85], "major_step": 0.2, "minor_ticks": 1},
    "y_right": {"label": "CE (%)", "range": [20, 105], "major_step": 20, "minor_ticks": 1},
    "visible_sides": ["bottom", "left", "right"],
    "hidden_sides": ["top"]
  },
  "typography": {
    "font": "Arial",
    "tick_pt": 6,
    "axis_title_pt": 7,
    "panel_label_pt": 8,
    "legend_pt": 6
  },
  "strokes": {
    "axis_pt": 0.7,
    "tick_pt": 0.65,
    "main_line_pt": 2,
    "secondary_line_pt": 0.65
  },
  "series": {
    "MA-21": {"color": "#0F4D92", "left_style": "solid", "right_style": "dot"},
    "MA-1": {"color": "#B64342", "left_style": "solid", "right_style": "dot"},
    "MA-22": {"color": "#42949E", "left_style": "solid", "right_style": "dot"}
  },
  "visual_series_model": {
    "split_into_origin_plots": true,
    "examples": ["one plot per condition", "separate highlighted points", "separate charge/discharge segments"],
    "fallback_primitives": ["thick vertical line segments for grouped bars", "thick horizontal line segments for normalized bars"]
  },
  "legend": {
    "mode": "manual",
    "frame": false,
    "position": "lower_left",
    "entries": ["MA-21", "MA-1", "MA-22"]
  },
  "origin_risks": ["right-y layer text can resize in OLE", "auto legend may return raw column names"]
}
```

The fields `referenceFirstGate`, `referenceImage`, `python_reference_plot_type`, and `origin_construction` are mandatory for ace-sci-origin. They prevent the Origin stage from falling back to a generic blank graph.

## Defaults

Use these as starting values for Nature-like panels:

- Font: Arial
- Tick labels: 5.5-6.5 pt
- Axis titles: 6.5-7.5 pt
- Panel labels: 8 pt bold
- Axis line width: 0.6-0.8 pt
- Tick width: 0.6-0.7 pt
- Visible axes: derive per panel from the Python/R reference. Use bottom x and left y only for ordinary two-axis panels; add right y only for true secondary y data; add top x only for true secondary x data or an explicitly requested full frame.
- Main Origin curve/point-line width: `2` in Plot Details / Line / Width (`绘图细节 -> 线条 -> 宽度`)
- Secondary/dotted lines: 0.55-0.75 pt
- Background: white
- Grid: off
- Origin page size/proportion: keep the Origin software default graph-page proportion by default. Do not force matplotlib `figsize` or composite-image proportions onto each Origin page unless the user or panel contract explicitly requires that page size. Match the full Python reference composition later by arranging OLE panels in PowerPoint.
- Series colors: copy the Python/R reference color map into explicit Origin RGB/hex values. Do not leave curve, spectrum, point-line, or multi-series plots as Origin's default black unless that exact series is black in the reference.
- Legend: required for multi-series curve/line/spectrum panels unless clear direct labels are present in the Origin graph. Use frameless, compact legends outside dense regions. A missing legend or raw-column-name legend is a failed panel.
- Visual series: split every reference-visible group into a separate Origin plot object unless the plot type has a reliable native grouping mechanism that previews correctly.
- Placeholder labels are forbidden. Axis titles and legends must come from the Python/R reference or workbook semantic labels, not from Origin defaults such as `X 轴标题`, `Y 轴标题`, `X Axis`, or `Y Axis`.

## Contract-To-Origin Compilation Checklist

For each panel:

1. Create explicit plotting worksheets.
   - Include one x/y pair per visual series when the reference uses distinct colors, markers, line styles, highlights, or bar offsets.
2. Choose the Origin construction from `python_reference_plot_type` and `origin_construction`. Do not use one default x-y plot for every panel.
3. Create graph page using the Origin default page proportion unless the contract explicitly overrides it; set layer geometry before final formatting.
4. Set layer rectangle in page-percent coordinates so the plot area fills the intended panel.
5. Add all data plots.
6. Add secondary/right-y layers only when the contract requires them.
7. Set exact axis ranges and major/minor tick spacing.
8. Apply fonts, tick sizes, axis thickness, line widths, and axis-side visibility from `reference_axis_sides`. Explicitly enable required bottom/left/right/top axes and their major ticks/tick labels; explicitly hide non-data top/right axes and ticks after applying templates.
9. Apply colors and line styles after all plots are added and after grouping/rescale.
   - Compile the Python/R reference palette into Origin commands. Do not rely on Origin color cycling or default black lines.
   - For multi-series curves, every plotted series must have a contract entry with label, color, line style, and legend text before Origin automation starts.
   - For curve and point-line plots, explicitly set line width to `2` after grouping/rescale/template operations. Do not rely on Origin's default width.
   - For scatter plots, explicitly set marker shape, size, fill/interior, edge, and color. Do not rely on Origin's scatter template if the reference has highlighted points or category-specific markers.
   - For grouped bars, verify bar width and offset in an exported preview. If Origin's bar template overrides spacing, switch to explicit x positions or editable thick line/rectangle primitives.
10. Delete Origin auto legends if they expose raw column names or boxed legends.
11. Delete or hide template-created axis titles that are not part of the contract, especially duplicate rotated titles left by dual-axis templates.
12. Rebuild legend/direct labels according to the contract. For multi-series curve panels, verify the exported Origin preview contains either the legend or direct labels; absence is a failure.
13. Export an Origin PNG preview and compare it to the Python reference before pasting to PPT.
14. Count visible axis sides in the exported preview. A two-axis reference must show bottom and left; a dual-y reference must show bottom, left, and right; a full-frame reference must show all four sides.
15. Reject the preview if it is blank/default, uses placeholder labels, lacks the Python reference chart type, or leaves marks in default black.
16. Create a contact sheet when matching a Python/R reference: reference panel on the left, Origin export on the right, repeated for every panel. Use this to audit axis count, axis limits, line widths, marker shapes, bar widths, label placement, and legend economy.

## Special Cases

### Dual-Axis Curves

Use a true right-y layer when OLE remains stable. Keep ranges and tick intervals identical to the reference. If right-y OLE text explodes in PowerPoint, document a hybrid fallback: Origin data/graph remains editable, while right-axis labels or final visible panel may be PPT/Python-rendered.

Do not use a true right-y layer merely to create a visual frame. If a right axis is unstable and the final Origin page uses a scaled fallback column, keep the true values in adjacent columns with names such as `CE_true_pct` and `CE_scaled_for_left_axis`, and state the fallback in the status report.

### Axis Visibility

Read `origin-axis-contract.md` before implementing axes. Every panel must state `axis_count` and `reference_axis_sides`.

For ordinary two-axis panels, explicitly enable bottom x and left y axis lines, major ticks, tick labels, and axis titles. Do this even if those axes appear in the Origin UI, because templates and OLE export can drop or resize them.

For reference panels with two y axes, use bottom x plus left y plus right y. The right y-axis is required only when the Python/R reference uses it for a real second variable. Do not leave top x or right y visible as a decorative frame when the reference is a two-axis plot.

Apply the axis contract after every Origin operation that can reset layer state: template application, `rescale`, grouping, adding/removing plots, legend rebuilds, and before `copy_page("OLE")`.

### Grouped Or Stacked Bars

Do not rely on Origin's default category spacing for publication panels. Create explicit x-position columns:

- group center: `1, 2, 3...`
- sample offset: `center - 0.18`, `center + 0.18`
- stacked/overlay values in separate columns

Keep true values and plotting positions in the worksheet with clear names.

If the Origin column/bar template still produces wrong spacing or bar width in the exported preview, use thick editable vertical line segments or PPT-native editable rectangles as a documented fallback. Preserve the true numeric values and the plotted positions in the Origin workbook.

### Highlighted Scatter Points

When the reference distinguishes ordinary points from highlighted points such as "This work", create separate x/y columns and separate Origin plot objects. Style each plot object explicitly. Do not plot all points as one scatter series and expect Origin's template or point-by-point formatting to preserve the highlight through export/OLE.

### Segmented Curves

For voltage-capacity, charge/discharge, cycling segments, or any trace with x resets, split the curve into separate columns before plotting. This prevents false connecting lines and lets each segment have its own line style, label, and legend entry.

### Legends

Origin auto legends are allowed only if their exported preview matches the reference. Otherwise delete them and rebuild compact manual legends. Never leave raw column names such as `capacity_ah` or `ce_scaled_for_display` in the final visual.

For line, spectrum, and point-line panels with more than one visible series, a legend or direct label set is mandatory. If the Python reference uses a shared legend, each Origin panel should still contain enough native legend/direct-label information to identify its series before PPT layout, unless the final PPT intentionally uses a shared PPT-side legend and the status file documents that hybrid choice.

## Validation

A graph page passes only when the exported Origin preview has:

- no huge or tiny text,
- comparable plot-area fill to the Python reference,
- matching axis limits and tick density,
- matching axis count and visible axis sides from the reference,
- matching color/line semantics,
- no default-black multi-series curves unless those series are black in the reference,
- matching visual-series semantics: separate highlighted points, grouped-bar conditions, charge/discharge segments, and stacked traces are represented by separate Origin plots or documented editable fallbacks,
- no intrusive boxed legend,
- a visible compact legend or direct labels for every multi-series curve/line/spectrum panel,
- no meaningless top/right axes or ticks for panels that only have one x and one y variable,
- no gray grid lines unless intentionally requested,
- readable line widths at the final PPT/composite scale.
- curve/point-line plots have Plot Details / Line / Width set to `2` unless a panel-specific contract intentionally overrides it.
