# Origin Axis Contract

Use this reference whenever Origin graphs are generated from a Python/R reference image or when a user reports missing axes in Origin/PPT output.

## Rule

Axis visibility is a contract, not a style afterthought. For every panel, first read the reference figure and write down which axis sides are visible:

- ordinary x-y panel: 2 visible axes, usually bottom x and left y
- true dual-y panel: 3 visible axes, bottom x, left y, and right y
- true dual-x panel: 3 visible axes, bottom x, top x, and left y
- full frame: 4 visible sides only when the reference or user explicitly requires it

Do not infer "four axes" from Origin templates. Do not remove all frame lines just because Nature-style plots often hide top/right. Match the Python/R reference panel by panel.

For ordinary 2D Origin exports, two data axes are the minimum acceptable result: bottom x-axis and left y-axis. Both must be visible in the exported PNG and PPT/OLE preview, not just enabled in the dialog. Set the axis line thickness to `2` by default when no panel-specific contract overrides it.

Axis tick labels or axis titles alone do not prove the axis exists. If an exported Origin preview shows tick labels and titles but the bottom/left axis line itself is absent or too faint to see, the axis contract has failed. Reapply Origin's native Line and Ticks settings for the required axis sides. Do not draw ordinary line objects to imitate axes; that creates a visually plausible but semantically wrong graph.

## Panel Axis Audit

Before building Origin pages, create a compact per-panel axis audit:

```json
{
  "panel": "a",
  "reference_axis_sides": ["bottom", "left", "right"],
  "axis_count": 3,
  "x_axis": {"side": "bottom", "label": "Cycle number", "range": [0, 260], "major_step": 50},
  "y_left": {"label": "Retention (%)", "range": [65, 110], "major_step": 10},
  "y_right": {"label": "Coulombic efficiency (%)", "range": [92, 101], "major_step": 2},
  "hidden_sides": ["top"],
  "origin_risks": ["right-y layer may render differently in OLE"]
}
```

For an ordinary 2-axis panel:

```json
{
  "panel": "b",
  "reference_axis_sides": ["bottom", "left"],
  "axis_count": 2,
  "x_axis": {"side": "bottom", "label": "Areal capacity (mAh cm-2)", "range": [4.05, 4.9]},
  "y_left": {"label": "Cut-off voltage (V)", "range": [0.8, 5.25]},
  "hidden_sides": ["top", "right"]
}
```

## Origin Implementation Pattern

Apply axis visibility after graph creation, after templates, after rescale, and again before export/OLE copy. Origin templates and grouping can silently reset axis options.

Use a helper like this in automation scripts:

```python
def apply_axis_contract(gl, *, right_y=False, top_x=False):
    gl.lt_exec(
        """
        layer.x.show=1; layer.y.show=1;
        layer.x.showAxes=1; layer.y.showAxes=1;
        layer.x.showLabels=1; layer.y.showLabels=1;
        layer.x.ticks=1; layer.y.ticks=1;
        layer.x.ticklength=8; layer.y.ticklength=8;
        layer.x.minorTicks=0; layer.y.minorTicks=0;
        layer.x.label.show=1; layer.y.label.show=1;
        layer.x.postype=0; layer.y.postype=0;
        layer.x.color=color(0,0,0); layer.y.color=color(0,0,0);
        layer.x.thickness=2; layer.y.thickness=2;
        layer.x.tickThickness=2; layer.y.tickThickness=2;
        layer.x.label.pt=18; layer.y.label.pt=18;
        layer.x.title.pt=20; layer.y.title.pt=20;
        layer.x.label.font$="Arial"; layer.y.label.font$="Arial";
        layer.x.title.font$="Arial"; layer.y.title.font$="Arial";
        layer.x.showopposite=0; layer.y.showopposite=0;
        layer.x.opposite=0; layer.y.opposite=0;
        """
    )
    if right_y:
        gl.lt_exec(
            """
            layer.y2.showAxes=1;
            layer.y2.ticks=1;
            layer.y2.label.show=1;
            layer.y2.thickness=2;
            layer.y2.tickThickness=2;
            layer.y2.label.pt=18;
            layer.y2.title.pt=20;
            layer.y2.label.font$="Arial";
            layer.y2.title.font$="Arial";
            """
        )
    if top_x:
        gl.lt_exec(
            """
            layer.x2.showAxes=1;
            layer.x2.ticks=1;
            layer.x2.label.show=1;
            layer.x2.thickness=2;
            layer.x2.tickThickness=2;
            """
        )
```

This pattern intentionally opens bottom/left first, then selectively opens right/top only when the axis audit requires them. In Origin LabTalk, `layer.x.showAxes=1` and `layer.y.showAxes=1` select the bottom x-axis and left y-axis. Avoid setting `layer.x2.showAxes=0` or `layer.y2.showAxes=0` as a way to hide top/right axes in ordinary two-axis plots, because opposite-axis properties can share state with the primary axis direction. Use the primary-axis `showAxes=1` plus `showopposite=0`/`opposite=0` instead.

Do not consider the axis contract applied until an exported preview confirms both data axes are visible. If only one axis is visible, reapply bottom/left axis display and thickness after every `rescale`, template operation, grouping operation, legend rebuild, and immediately before `save_fig` or `copy_page("OLE")`.

Never add fallback axis-line objects for the required bottom/left data axes. If native axes still disappear in the exported preview, treat it as an Origin axis-configuration failure and keep iterating on native Line and Ticks settings before creating PPT OLE.

## Two-Axis Reference Matching

When the Python reference uses two axes, the Origin panel must show:

- bottom x-axis line
- left y-axis line
- bottom and left major ticks
- tick labels on bottom and left
- x and y axis titles unless the reference intentionally omits them
- no top x-axis or right y-axis ticks/labels

Missing bottom/left axes is a failure even if the data curves are correct.

## Dual-Y Reference Matching

When the Python reference uses a left and right y-axis:

- bottom x-axis must be visible
- left y-axis must be visible, with its own title/range/tick color when the reference uses one
- right y-axis must be visible only for the true second y variable
- top x-axis should remain hidden unless the reference shows it
- do not fake a dual-y panel by plotting unlike units on one y-axis without documenting the fallback

If true Origin dual-y OLE is unstable, keep the editable Origin project and state the limitation. A stable 2-axis fallback with true values preserved is better than a broken OLE panel, but it must be reported.

## Validation

For each Origin page and for the final PPT OLE slide:

1. Export a PNG preview.
2. Compare the preview to the Python/R reference at the same panel scale.
3. Count visible axis sides per panel.
4. Confirm all required visible sides have lines, major ticks, tick labels, and axis titles.
5. Confirm all hidden sides are actually hidden, not merely unlabeled.
6. Reapply the axis contract and re-export if any axis side is missing.

The final response should not say the Origin figure is complete until the preview shows the expected axis count for every panel.
