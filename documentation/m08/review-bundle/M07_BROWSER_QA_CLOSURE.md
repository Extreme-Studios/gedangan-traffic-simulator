# M07 Browser QA Closure — M08 audit

**Status: CLOSED_WITH_KNOWN_ISSUE.** This is not an unconditional PASS. Empirical forecast validity remains blocked. Historical M07reports/status/source are unchanged.

The stale M07tab returned `browser.user is unavailable`. A working M08-created tab could navigate to the unchanged M07page, resolving the tab-specific problem without changing security settings. The earlier BLOCKED_BY_ENVIRONMENT observation was superseded by completed functional checks.

Verified:all15years2026–2040 against canonical demand; LOW/REFERENCE/HIGH; custom car growth4.2% yielding376requests for2040; versioned custom save; Run endpoint initiation and COMPLETE status for verified cached actual run2d80fd22e8e5550afeb6; recorded frame positions/play/pause; NOT RUN with playback disabled; actual2026-versus2040comparison with parity/censoring warning; all five panels at1920×1080 and390×844; final console0errors/warnings.

Finding M07-UI-01:mobile Comparison panel has scrollWidth412px versus390px viewport,22px horizontal overflow. Other checked panels did not overflow. Functional comparison worked. The finding is retained and the old source is not rewritten under the M08immutability constraint. An early commentary saying no overflow was corrected after the automated width audit.

Custom config/job writes were isolated into documentation/m08/m07-qa. Original M07bytes are checked by the M08baseline manifest. The Run-button check reused a verified existing SUMOcache; it is not a new physics run. Fresh actual evidence remains in originalM07tripinfo/FCD/manifests. M08SUMOexperiments are separate.

Evidence:m07-desktop.jpg,m07-mobile.jpg,m07-comparison-desktop.jpg,m07-playback-desktop.jpg,m07-browser-closure.json. No milestone-old screenshot was substituted for this QA. This addendum closes inspection with a known layout issue; it does not upgrade scientific readiness or authorize M09.
