# M09 Visual QA Report

**PASS FOR TECHNICAL MODEL PRESENTATION**, with explicit source/model limits.

Automated: 18 flows PASS, errors0, missingassets0, externalrequests0. Class views10 PASS. Desktop1920×1080/tablet1024×768/mobile390×844. Renderer: ANGLE (AMD, AMD Radeon Graphics (0x000015BF) Direct3D11 vs_5_0 ps_5_0, D3D11).

## Reviewed actual screenshots

| File under presentation_demo/m09/qa | Review |
|---|---|
| aerial-overview.png | Actual Chrome screenshot inspected; source/model assumptions remain labelled. |
| main-corridor-2026.png | Actual Chrome screenshot inspected; source/model assumptions remain labelled. |
| reverse-corridor.png | Actual Chrome screenshot inspected; source/model assumptions remain labelled. |
| gedangan-intersection.png | Actual Chrome screenshot inspected; source/model assumptions remain labelled. |
| frontage-road.png | Actual Chrome screenshot inspected; source/model assumptions remain labelled. |
| railway-closed-train.png | Actual Chrome screenshot inspected; source/model assumptions remain labelled. |
| railway-release.png | Actual Chrome screenshot inspected; source/model assumptions remain labelled. |
| traffic-signals.png | Actual Chrome screenshot inspected; source/model assumptions remain labelled. |
| high-density-2040.png | Actual Chrome screenshot inspected; source/model assumptions remain labelled. |
| before-after-split.png | Actual Chrome screenshot inspected; source/model assumptions remain labelled. |
| fullscreen-presentation.png | Actual Chrome screenshot inspected; source/model assumptions remain labelled. |
| vehicle-classes-follow.png | Actual Chrome screenshot inspected; source/model assumptions remain labelled. |
| tablet-playback.png | Actual Chrome screenshot inspected; source/model assumptions remain labelled. |
| mobile-playback.png | Actual Chrome screenshot inspected; source/model assumptions remain labelled. |
| class-motorcycle.png | Actual Chrome screenshot inspected; source/model assumptions remain labelled. |
| class-bus.png | Actual Chrome screenshot inspected; source/model assumptions remain labelled. |
| class-m05_train.png | Actual Chrome screenshot inspected; source/model assumptions remain labelled. |

## Review boundaries

- Whole-network aerial makes meter-scale vehicles small; corridor/follow views are provided
- Buildings and furniture are stylized/model assumptions, not measured physical inventory
- Follow-train is a close view and can crop train ends; railway preset supplies whole-crossing view
- Some source junction/short-lane geometry remains visually angular; no hidden traffic-network repair
- Physical elevations, stop lines, boom placement, clearance, access legality and empirical validity remain unverified

These are real playback/selection/fullscreen screenshots, not generated mockups. Initial NaN/keyboard failures were fixed and retested. See browser-qa.json, class-qa.json, visual-review.json, performance-summary.json and regression logs. A headless Chrome render is not a claim of manual native IAB inspection. No optional captured demo video is provided.
