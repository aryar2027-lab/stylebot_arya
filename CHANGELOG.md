# Changelog

All notable changes to StyleBot. See `git log` for every commit.

## [1.2.0] – Testing, features and Mac support
### Added
- Unit tests (`tests/test_stylebot.py`, 19 tests) and a GitHub Actions workflow that runs them on macOS, Windows and Linux
- New occasions: **Haldi / Mehendi** and **Graduation / Convocation**
- Delete saved looks (with confirmation)
- Export a look as a **Markdown shopping list** with checkboxes and clickable links (`e`)
- Gender added to every search ("women block heels") for more relevant results
- `run_on_mac.command`: double-click launcher for macOS
- Friendly message on Python versions older than 3.8

### Fixed
- `Rs. 3000` was rejected as an invalid budget (found by unit tests)
- Item prices could add up to **more** than the budget (found by unit tests); totals now match exactly
- Choosing a saved look by title could pick the wrong one when two titles were identical

## [1.1.0] – Event-aware outfits
### Added
- Outfits depend on the event (dressy / smart / relaxed), with colour palettes and styling tips
- Fusion style; 30 outfit templates; accessories matched to ethnic or western looks
- Budget split across items; Indian number format (₹1,25,000)
- Six shopping sites: Myntra, Ajio, Amazon.in, Nykaa Fashion, Zara, H&M (Zara/H&M skipped for ethnic wear)
- Open links in browser, show another colour, save and view looks
- Warning when a style is unusual for the event

### Fixed
- Crash on Windows consoles using a legacy code page (emoji / ₹)
- Main garment now gets a bigger share of the budget
- `3000.50` was read as ₹3,00,050

## [1.0.1] – First bug fixes
### Fixed
- Crash on budgets like `₹3,000`
- Menu choice `0` silently picked the last option; `9` or letters crashed
- Blank colour produced `" kurta"` and broken links
- Links were not URL-encoded

## [1.0.0] – Initial AI-generated version
- Basic outfit suggestion with shopping links for Myntra, Amazon and Ajio
