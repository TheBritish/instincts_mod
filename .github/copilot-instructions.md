# Copilot instructions — Europa Universalis V (repo: game assets)

**At A Glance**
- **Purpose:** What this repo contains and how to run the game locally.
- **Quick start:** Local test commands, log locations, and debug settings.
- **Essential rules:** Syntax, encoding and critical EU5 pitfalls to avoid.
- **Where to look:** Key directories and canonical example files.
- **Workflow:** PR guidance, testing, and incremental change advice.

This repository contains runtime game data and assets (Paradox-style content): UI definitions, localization, configuration files (game scripts), graphics, and packaging manifests. The engine that consumes these files is the `eu5.exe` binary found in the `binaries/` folder.

## Official EU5 Modding Documentation

**CRITICAL**: Before generating ANY EU5 code, ALWAYS consult the files in `.github/REFERENCE/`:

- **📋 EU5_MODDING_MASTER_REFERENCE.txt** — **START HERE**: Comprehensive index of all EU5 modding documentation with quick access guides, validation checklists, and critical pitfalls to avoid.

- **Official reference (canonical):**
  - **EU5_Scripted_Content.txt** — Actions, scripted GUI, events, missions, situations (event structure, DHE syntax, option blocks)
  - **EU5_ILLUSTRATION_TAGS_REFERENCE.txt** — Complete reference for illustration_tags in Dynamic Historical Events (DHE)
  - **EU5_Scripted_Types.txt** — Buildings, goods, estates, laws, pops, advances, units, subject types, IOs
  - **EU5_Systems.txt** — Characters, concepts, culture, modifiers, international organizations
  - **EU5_EFFECTS_REFERENCE.txt** — All valid effects (add_prestige, set_variable, trigger_event, etc.)
  - **EU5_TRIGGERS_REFERENCE.txt** — All valid triggers (tag, current_date, is_subject_of, etc.)
  - **EU5_LOCATIONS_REFERENCE.txt** — Complete list of all 22,995 valid location names (province names, cities, geographic locations)
  - **EU5_INVALID_SYNTAX_REFERENCE.txt** — Common mistakes, invalid effects/triggers, EU4→EU5 migration traps
  - **EU5_COMMON_PATTERNS_REFERENCE.txt** — Best practices, working code examples, implementation patterns
  - **EU5_MODIFIERS_REFERENCE.txt** & **EU5_MODIFIER_TYPES_REFERENCE.txt** — Valid modifier properties
  - **EU5_ON_ACTIONS_REFERENCE.txt** — Event hooks (monthly_pulse, yearly_country_pulse, on_game_start, etc.)
  - **EU5_SCOPES_REFERENCE.txt** & **EU5_SCOPE_LINKS_REFERENCE.txt** — Scope navigation and context

- **Guides (how-to summaries; see `INDEX.txt`):**
  - **EU5_ACTION_MODDING.txt**, **EU5_EVENT_MODDING.txt**, **EU5_MISSION_MODDING.txt**, **EU5_SCRIPTED_GUI.txt**
  - **EU5_BUILDING_MODDING.txt**, **EU5_GOODS_MODDING.txt**, **EU5_ESTATE_MODDING.txt**, **EU5_POP_MODDING.txt**, **EU5_LAW_MODDING.txt**, **EU5_SUBJECT_TYPE_MODDING.txt**, **EU5_ADVANCE_MODDING.txt**, **EU5_UNIT_MODDING.txt**
  - **EU5_CHARACTER_MODDING.txt**, **EU5_CONCEPT_MODDING.txt**, **EU5_CULTURE_MODDING.txt**, **EU5_MODIFIER_MODDING.txt**, **EU5_INTERNATIONAL_ORGANIZATION_MODDING.txt**

When implementing ANY game mechanic (events, modifiers, laws, buildings, IOs, etc.), search these reference files FIRST to verify correct syntax, available attributes, and structure. Do NOT guess or infer syntax from other Paradox games (EU4, CK3, etc.) — EU5 has unique patterns.

- **MANDATORY:** You MUST not use old code or patterns copied from other games; all new or modified code must be derived from, and consistent with, the provided EU5 REFERENCE files in `.github/REFERENCE/`.

Guiding principles for AI agents working here:

- Begin with the big picture: `game/` is the primary content branch (game assets, data, localization, GUI). `clausewitz/` contains engine/editor UI assets and shared localization used by engine/tools. `jomini/` contains tool-specific assets (Jomini toolkit). The running game loads these assets via the binary in `binaries/`.
- Prefer minimal, targeted edits: preserve file style, keep changes focused, and avoid mass reformatting.

Important directories (quick reference)
- `binaries/` — runtime binary and DLLs (use for manual local testing).
- `game/in_game/common/` — game rules, countries, traits, scripts (Paradox script format `.txt` / `.eu5`).
- `game/in_game/gui/` — UI definitions (.gui). Use `ui_library.gui` and `shared/` components as canonical examples.
- `game/in_game/gfx/` — images, atlases, illustrations; mapping files like `gfx/images/00_images.txt` link textures to triggers.
- `game/in_game/localization/` and `clausewitz/loading_screen/localization/` — YAML localization files (`*_l_english.yml`, etc.).
- `platform_specific_game_data/` — local platform config and logging; adjust `log_settings_live.json` for debug logging.

Load order (important):
- `main_menu` assets and localization are loaded at game startup (menu UI and related localization).
- `loading_screen` assets/localization are loaded during the game's loading sequences and before `in_game` content is applied.
- `in_game` content (rules, events, traits, gfx used in gameplay) is loaded when entering gameplay — use this order when deciding where to place UI vs runtime content.

Encoding and localization rules (must-follow)
- All localization files and any new text files should be saved as UTF-8 with BOM to ensure the engine loads them reliably.
- Trait description keys: use the canonical pattern `desc_<trait>` for description entries (do not rely on legacy alias keys like `<trait>_desc`).
- For in-game text that references scopes, use the proper scope tokens: `[target_country.GetName]` or `[target_country.GetNameWithNoTooltip]` and ensure `save_scope_as = target_country` is used in events when you need a persistent scope.

- Dynamic localisation note: Dynamic tokens and scope-based tokens can be used in `main_menu` localisation when formatted according to the official Localisation reference. Follow `.github/REFERENCE/EU5_LOCALIZATION_REFERENCE.txt` for correct token names, scope promotion rules, and examples.

Paradox data conventions & best practices
- Scripts: nested `key = { }` blocks; comments use `#`. Preserve existing whitespace/brace style.
- Keys: prefer lowercase snake_case for data keys (traits, events, variables), and follow existing naming conventions used in `game/`.
- **Trait validation**: ALWAYS verify trait names exist in base game before using. Common valid traits: `expansionist`, `well_connected`, `ambitious_2` (NOT `ambitious`), `diplomatic_2` (NOT `diplomatic`). Search `game/in_game/common/traits/` for available traits.
- **Advances system**: Advances are unlocked through research requirements by default, but can be granted directly via events using `research_advance = <advance_key>` effect (country scope). Ensure the advance is defined in `common/advances/` files.
- **Multiple IO Membership**: Countries can be members of multiple International Organizations simultaneously by default. Use `can_join_trigger` with conditional logic to allow specific combinations (e.g., HRE members can join Hanseatic League).
- **Custom Modifiers**: For effects without direct triggers, create custom static modifiers in `main_menu/common/static_modifiers/` with `game_data = { category = country }`. Use `add_country_modifier` in events to apply them.
- **DHE Events**: Dynamic Historical Events require `tag = BARE_TAG` (not c:TAG), date ranges (`from = YYYY.M.D` to `to = YYYY.M.D`), `monthly_chance = N`, and `illustration_tags` for proper display.
- **IO Leadership**: Expand `can_lead_trigger` beyond single tags to include founding members for more flexible confederation leadership.
- **Scope references - CRITICAL**:
  * ✅ **CORRECT**: Use getter methods for character/country properties: `root.GetPrimaryCulture`, `root.GetStateReligion`, `root.GetRuler`.
  * ❌ **WRONG**: Direct property access like `root.primary_culture`, `root.state_religion` will cause "unknown data type" errors.
- **Geography filters (location scope)**:
  * ✅ **CORRECT**: `region ?= region:brabant_region` and `area ?= area:picardy_area` (use `?=` safe accessor in location filters).
  * ❌ **WRONG**: `location_region = region:brabant_region`, `location_area = area:picardy_area`, or bare `region = brabant_region` (unsupported/invalid).
- **Government rank effects**:
  * ✅ **CORRECT**: `set_government_rank_value = N` (sets rank to specific value).
  * ❌ **WRONG**: `set_government_rank = N` (doesn't exist in EU5).
- **Character succession**: `set_new_ruler = scope:character` automatically handles ruler replacement. DO NOT call `kill_character_silently` before it - unnecessary and risks errors if no ruler exists.
- Scope persistence: when an event selects a country or character and you need to reference it later, use `random_neighbor_country = { save_scope_as = target_country }` then `set_variable = { name = investigation_target_country value = scope:target_country }` and reference via `var:investigation_target_country` in follow-ups.
- Localization tokens: include scope tokens in localization strings (e.g., `[target_country.GetName]`) if the event uses `save_scope_as = target_country`.

Developer workflows (fast iteration)
- Local testing: modify content under `game/` or `clausewitz/`, then launch `binaries/eu5.exe` to load assets — no compilation step required for content-only changes.
- Launch from PowerShell (example):
```powershell
Set-Location 'D:\SteamLibrary\steamapps\common\Europa Universalis V'

# Copilot instructions — Europa Universalis V (concise)

Purpose
- This repo contains runtime game data & assets used by the `binaries/eu5.exe` engine (scripts, GUI, gfx, localization).

Quick start (must-read)
- Always consult `.github/REFERENCE/EU5_MODDING_MASTER_REFERENCE.txt` before changing syntax or effects.
- Test locally (PowerShell):
```powershell
Set-Location 'D:\SteamLibrary\steamapps\common\Europa Universalis V'
Start-Process -FilePath '.\binaries\eu5.exe'
```
- Check logs at `%USERPROFILE%\Documents\Paradox Interactive\Europa Universalis V\logs`; set `platform_specific_game_data/log_settings_live.json` to `debug` if needed.

Essential rules for agents
- Preserve existing whitespace/brace style; avoid mass reformatting.
- Save `.txt` and `.yml` files as UTF-8 with BOM.
- Use the canonical reference files (`.github/REFERENCE/`) for effects, triggers, DHE illustration tags, scopes, and modifiers.
- DHE: `tag = BARE_TAG`; always include `from`, `to`, `monthly_chance`, and `illustration_tags`.
- Use getters and safe accessors (`root.GetRuler`, `region ?= region:brabant_region`).
- Use `main_menu/common/biases/*.txt` for opinion modifiers; do NOT use `add_opinion = { value = N }`.
- NEVER use invalid/deprecated syntax (e.g., `owns = 54`, `is_triggered_only`). If unsure, search the reference docs.

Where to look (examples)
- `game/in_game/common/traits/` — trait patterns
- `game/in_game/common/international_organizations/` (see `hanseatic_league.txt`) — IO definitions
- `main_menu/common/biases/` vs `main_menu/common/static_modifiers/` — bias vs static modifier semantics
- `game/in_game/gfx/images/00_images.txt` — illustration mapping
- `game/in_game/gui/ui_library.gui` — GUI patterns and shared widgets

Workflow & PR guidance
- Make small, focused edits and test immediately; check `error.log` for parsing/orphan issues.
- Prefer feature branches and PRs for anything non-trivial.
- For bulk edits, validate braces and structure before committing; run a logs pass after changes.

Questions or gaps
- If this terse guide misses something you expect (example files, workflows, or edge-cases), tell me which area and I will expand the doc with concrete examples.
````instructions
# Copilot instructions — Europa Universalis V (repo: game assets)

This repository contains runtime game data and assets (Paradox-style content): UI definitions, localization, configuration files (game scripts), graphics, and packaging manifests. The engine that consumes these files is the `eu5.exe` binary found in the `binaries/` folder.

## Official EU5 Modding Documentation

**CRITICAL**: Before generating ANY EU5 code, ALWAYS consult the files in `.github/REFERENCE/`:

- **📋 EU5_MODDING_MASTER_REFERENCE.txt** — **START HERE**: Comprehensive index of all EU5 modding documentation with quick access guides, validation checklists, and critical pitfalls to avoid.

- **Official reference (canonical):**
  - **EU5_Scripted_Content.txt** — Actions, scripted GUI, events, missions, situations (event structure, DHE syntax, option blocks)
  - **EU5_ILLUSTRATION_TAGS_REFERENCE.txt** — Complete reference for illustration_tags in Dynamic Historical Events (DHE)
  - **EU5_Scripted_Types.txt** — Buildings, goods, estates, laws, pops, advances, units, subject types, IOs
  - **EU5_Systems.txt** — Characters, concepts, culture, modifiers, international organizations
  - **EU5_EFFECTS_REFERENCE.txt** — All valid effects (add_prestige, set_variable, trigger_event, etc.)
  - **EU5_TRIGGERS_REFERENCE.txt** — All valid triggers (tag, current_date, is_subject_of, etc.)
  - **EU5_LOCATIONS_REFERENCE.txt** — Complete list of all 22,995 valid location names (province names, cities, geographic locations)
  - **EU5_INVALID_SYNTAX_REFERENCE.txt** — Common mistakes, invalid effects/triggers, EU4→EU5 migration traps
  - **EU5_COMMON_PATTERNS_REFERENCE.txt** — Best practices, working code examples, implementation patterns
  - **EU5_MODIFIERS_REFERENCE.txt** & **EU5_MODIFIER_TYPES_REFERENCE.txt** — Valid modifier properties
  - **EU5_ON_ACTIONS_REFERENCE.txt** — Event hooks (monthly_pulse, yearly_country_pulse, on_game_start, etc.)
  - **EU5_SCOPES_REFERENCE.txt** & **EU5_SCOPE_LINKS_REFERENCE.txt** — Scope navigation and context

- **Guides (how-to summaries; see `INDEX.txt`):**
  - **EU5_ACTION_MODDING.txt**, **EU5_EVENT_MODDING.txt**, **EU5_MISSION_MODDING.txt**, **EU5_SCRIPTED_GUI.txt**
  - **EU5_BUILDING_MODDING.txt**, **EU5_GOODS_MODDING.txt**, **EU5_ESTATE_MODDING.txt**, **EU5_POP_MODDING.txt**, **EU5_LAW_MODDING.txt**, **EU5_SUBJECT_TYPE_MODDING.txt**, **EU5_ADVANCE_MODDING.txt**, **EU5_UNIT_MODDING.txt**
  - **EU5_CHARACTER_MODDING.txt**, **EU5_CONCEPT_MODDING.txt**, **EU5_CULTURE_MODDING.txt**, **EU5_MODIFIER_MODDING.txt**, **EU5_INTERNATIONAL_ORGANIZATION_MODDING.txt**

When implementing ANY game mechanic (events, modifiers, laws, buildings, IOs, etc.), search these reference files FIRST to verify correct syntax, available attributes, and structure. Do NOT guess or infer syntax from other Paradox games (EU4, CK3, etc.) — EU5 has unique patterns.

Guiding principles for AI agents working here:

- Begin with the big picture: `game/` is the primary content branch (game assets, data, localization, GUI). `clausewitz/` contains engine/editor UI assets and shared localization used by engine/tools. `jomini/` contains tool-specific assets (Jomini toolkit). The running game loads these assets via the binary in `binaries/`.
- Prefer minimal, targeted edits: preserve file style, keep changes focused, and avoid mass reformatting.

Important directories (quick reference)
- `binaries/` — runtime binary and DLLs (use for manual local testing).
- `game/in_game/common/` — game rules, countries, traits, scripts (Paradox script format `.txt` / `.eu5`).
- `game/in_game/gui/` — UI definitions (.gui). Use `ui_library.gui` and `shared/` components as canonical examples.
- `game/in_game/gfx/` — images, atlases, illustrations; mapping files like `gfx/images/00_images.txt` link textures to triggers.
- `game/in_game/localization/` and `clausewitz/loading_screen/localization/` — YAML localization files (`*_l_english.yml`, etc.).
- `platform_specific_game_data/` — local platform config and logging; adjust `log_settings_live.json` for debug logging.

Load order (important):
- `main_menu` assets and localization are loaded at game startup (menu UI and related localization).
- `loading_screen` assets/localization are loaded during the game's loading sequences and before `in_game` content is applied.
- `in_game` content (rules, events, traits, gfx used in gameplay) is loaded when entering gameplay — use this order when deciding where to place UI vs runtime content.

Encoding and localization rules (must-follow)
- All localization files and any new text files should be saved as UTF-8 with BOM to ensure the engine loads them reliably.
- Trait description keys: use the canonical pattern `desc_<trait>` for description entries (do not rely on legacy alias keys like `<trait>_desc`).
- For in-game text that references scopes, use the proper scope tokens: `[target_country.GetName]` or `[target_country.GetNameWithNoTooltip]` and ensure `save_scope_as = target_country` is used in events when you need a persistent scope.

Paradox data conventions & best practices
- Scripts: nested `key = { }` blocks; comments use `#`. Preserve existing whitespace/brace style.
- Keys: prefer lowercase snake_case for data keys (traits, events, variables), and follow existing naming conventions used in `game/`.
- **Trait validation**: ALWAYS verify trait names exist in base game before using. Common valid traits: `expansionist`, `well_connected`, `ambitious_2` (NOT `ambitious`), `diplomatic_2` (NOT `diplomatic`). Search `game/in_game/common/traits/` for available traits.
- **Advances system**: Advances are unlocked through research requirements by default, but can be granted directly via events using `research_advance = <advance_key>` effect (country scope). Ensure the advance is defined in `common/advances/` files.
- **Multiple IO Membership**: Countries can be members of multiple International Organizations simultaneously by default. Use `can_join_trigger` with conditional logic to allow specific combinations (e.g., HRE members can join Hanseatic League).
- **Custom Modifiers**: For effects without direct triggers, create custom static modifiers in `main_menu/common/static_modifiers/` with `game_data = { category = country }`. Use `add_country_modifier` in events to apply them.
- **DHE Events**: Dynamic Historical Events require `tag = BARE_TAG` (not c:TAG), date ranges (`from = YYYY.M.D` to `to = YYYY.M.D`), `monthly_chance = N`, and `illustration_tags` for proper display.
- **IO Leadership**: Expand `can_lead_trigger` beyond single tags to include founding members for more flexible confederation leadership.
- **Scope references - CRITICAL**:
  * ✅ **CORRECT**: Use getter methods for character/country properties: `root.GetPrimaryCulture`, `root.GetStateReligion`, `root.GetRuler`.
  * ❌ **WRONG**: Direct property access like `root.primary_culture`, `root.state_religion` will cause "unknown data type" errors.
- **Geography filters (location scope)**:
  * ✅ **CORRECT**: `region ?= region:brabant_region` and `area ?= area:picardy_area` (use `?=` safe accessor in location filters).
  * ❌ **WRONG**: `location_region = region:brabant_region`, `location_area = area:picardy_area`, or bare `region = brabant_region` (unsupported/invalid).
- **Government rank effects**:
  * ✅ **CORRECT**: `set_government_rank_value = N` (sets rank to specific value).
  * ❌ **WRONG**: `set_government_rank = N` (doesn't exist in EU5).
- **Character succession**: `set_new_ruler = scope:character` automatically handles ruler replacement. DO NOT call `kill_character_silently` before it - unnecessary and risks errors if no ruler exists.
- Scope persistence: when an event selects a country or character and you need to reference it later, use `random_neighbor_country = { save_scope_as = target_country }` then `set_variable = { name = investigation_target_country value = scope:target_country }` and reference via `var:investigation_target_country` in follow-ups.
- Localization tokens: include scope tokens in localization strings (e.g., `[target_country.GetName]`) if the event uses `save_scope_as = target_country`.

Developer workflows (fast iteration)
- Local testing: modify content under `game/` or `clausewitz/`, then launch `binaries/eu5.exe` to load assets — no compilation step required for content-only changes.
- Launch from PowerShell (example):
```powershell
Set-Location 'D:\SteamLibrary\steamapps\common\Europa Universalis V'
Start-Process -FilePath '.\binaries\eu5.exe'
```
- Logs: check `Documents\Paradox Interactive\Europa Universalis V\logs` for parsing or localization errors; set `log_settings_live.json` to `debug` for extra detail.

Common change examples (safe edits)
- Add a new trait: 1) Place trait definition under `game/in_game/common/traits/` (use existing files as templates). 2) Add localization entries using `desc_<trait>` in `*_l_<lang>.yml`. 3) If the trait is limited, add conservative `allow = { ... }` checks (mutual exclusion with vanilla traits, or ADM/DIP/MIL thresholds).
- Add a new GUI control: 1) Add `.gui` under `game/in_game/gui/` or `shared/`. 2) Reuse `ui_library.gui` controls for layout. 3) Provide localized strings in `*_l_<lang>.yml`.
- Add an illustration: edit `game/in_game/gfx/images/00_images.txt` and add an `illustration_image = { texture_file = "gfx/your_path.png" trigger = {...} }` block.

Key pitfalls & checks
- Localization mismatch: if keys appear in-game, verify the YAML file exists, contains the `l_english:` top-level entry, is UTF-8 with BOM, and the key names match exactly.
- Missing textures: ensure `texture_file` paths in `00_images.txt` are correct; check logs for missing texture names.
- Script syntax: Paradox scripts are brace/whitespace sensitive. Use nearby canonical files as templates and avoid changing unrelated lines.
- Invalid effects: Effects like `add_advance` do not exist; use `research_advance` for advances. Always verify effects in `EU5_EFFECTS_REFERENCE.txt` before using.
- Advance requirements: When using `research_advance`, ensure the advance key is defined in `common/advances/` files; undefined advances will cause errors.
- **Invalid Direct Effects**: Don't use `add_tolerance_heretic`, `add_stability_cost_modifier`, `add_naval_morale_modifier` - create custom modifiers instead and use `add_country_modifier`.
- **Multiple IO Membership**: Allowed by default, but check `can_join_trigger` restrictions. Use conditional logic for specific combinations.
- **DHE Event Requirements**: Must include `illustration_tags` with mood/setting pairs, proper date ranges, and `tag = BARE_TAG` (not c:TAG).
- **Custom Modifier Categories**: Static modifiers use `game_data = { category = country }`; opinion biases use plain structure without game_data wrapper.
- **Invalid Province Ownership Triggers**: 
  * ❌ **WRONG**: `owns = 54` — This syntax does NOT exist in EU5 and causes PostValidate failures, making events orphaned.
  * ✅ **CORRECT**: `location:magdeburg = { owner ?= root }` — Use location names with safe owner checks.
  * Province ID to name mapping: 54=magdeburg, 61=leipzig, 66=nuremberg, 67=augsburg. Always use location names, never raw province IDs.
  * Orphaned events: Invalid triggers cause events to become orphaned (not fireable), check `error.log` for "orphaned event" messages.

Search & investigation shortcuts
- Find localization files: `**/*_l_english.yml`.
- Find GUI definitions: `game/in_game/gui/**/*`.
- Find occurrences of a key: grep for the symbol (e.g., `incompetent_fool`) across `game/`.

When to PR vs modify locally
- Small content fixes (typo, single localization key, small image): commit on a short-lived feature branch and open a PR.
- System-level changes (new schema, wide localization additions): create an issue and discuss before wide changes.

Examples to open first when orienting to an area
- `game/in_game/common/<topic>/**`
- `game/in_game/gui/ui_library.gui` and `game/in_game/gui/shared/`
- `game/in_game/gfx/images/00_images.txt`
- `clausewitz/loading_screen/localization/`
- `platform_specific_game_data/log_settings_live.json`

Official modding documentation (.info files)
The game includes 31 `.info` files with official Paradox documentation for modders. Key references:

-- **Traits**: `game/in_game/common/traits/_traits.info` — trait structure (`category`, `allow`, `modifier`, `chance`), MTTH system
-- **Events/On Actions**: `game/in_game/common/on_action/on_actions.info` — event triggering (`events`, `random_events`, `first_valid`), delays, weight-based selection
-- **Script Values**: `game/in_game/common/script_values/_script_values.info` — static values and formulas, scope chaining, list iteration
-- **Trigger Localization**: `game/in_game/common/trigger_localization/_trigger_localization.info` — tooltip display for triggers, pronouns, comparisons
-- **Scripted Modifiers**: `game/in_game/common/scripted_modifiers/scripted_modifiers.info` — weight modifiers for `random_list`, parameters
-- **Scripted Lists**: `game/in_game/common/script_values/_script_values.info` — custom list definitions
-- **Game Rules**: `game/main_menu/common/game_rules/_game_rules.info` — ironman/achievement flags, define overrides
-- **Search for all `.info` files: `**/*.info` (31 files total)**
-- **File cleanup**: Remove unused override files from mods—they can cause load order issues or unexpected vanilla behavior changes. Only keep files you've actually modified.

International Organizations (IO) - Advanced Modding
- **Exclusivity rule**: Countries CANNOT be members of multiple IOs simultaneously unless explicitly allowed by BOTH IO definitions (check HRE for Swiss Confederation precedent: `trigger_if` blocks in `can_join_trigger`).
- **Setup file structure**: Match vanilla patterns exactly (e.g., `swiss_confederation`). IO setup blocks should contain: `type`, `creation_date`, `leader` (optional), `members`, `areas` (preferred over `regions`/`provinces`), and `laws`. Do NOT include definition-only properties like `map_color`, `leader_title_key`, or behavior flags in setup files.
- **Definition vs Setup separation**: IO definitions (`game/in_game/common/international_organizations/*.txt`) define behavior, triggers, modifiers, and UI properties. Setup files (`game/main_menu/setup/start/*.txt`) create instances at game start with minimal configuration.
- **Event-based initialization**: For IOs with conflicting vanilla memberships (e.g., countries already in HRE), use `on_game_start` events with `join_international_organization` to add members post-initialization rather than overriding massive vanilla setup files.
- **Avoid setup file overrides**: NEVER copy entire vanilla setup files (e.g., `15_international_organizations.txt`) to mods - they're ~1600+ lines and will break with patches. Use separate numbered files (e.g., `15_custom_io.txt`) or event-based membership instead.
- **BOM corruption**: When creating setup files, use `create_file` tool (not `replace_string_in_file` on corrupted files) to ensure UTF-8 with BOM. Check `error.log` for "Unexpected token: ï»¿" messages indicating BOM issues.
- **Leader assignment**: Leaders can be assigned in setup via `leader = TAG` or dynamically via IO definition's `leader` block with voting/selection logic.
- **Areas vs regions**: Vanilla IOs prefer `areas = { area_name_1 area_name_2 }` over `regions` or `provinces` for territorial scope in setup files.

Events & On-Actions - Best Practices
- **fire_only_once**: Events with `fire_only_once = yes` do NOT need additional cooldown modifiers or global variables - the flag prevents re-firing automatically.
- **is_triggered_only**: ❌ DO NOT USE. This flag does NOT exist in EU5 and will cause parsing errors. Use `fire_only_once = yes` for one-time events or omit for repeatable events.
- **Scope persistence**: When saving scopes for later use, combine `save_scope_as` with `set_variable`: `random_neighbor_country = { save_scope_as = target_country }` then `set_variable = { name = target_var value = scope:target_country }`, reference later via `var:target_var`.
- **Event-to-event triggering**: Use `trigger_event = { id = event.name days = 30 }` to fire an event from within another event. The receiving event must have `fire_only_once = yes` (not `is_triggered_only`, which doesn't exist). Example: after Scotland chooses to support Jacobites, England receives `trigger_event = { id = historical_flavor.2020 days = 30 }`.
- **Date triggers**: Use `current_date >= YYYY.M.D` for date-based event triggers rather than `game_start_date` (which checks scenario start dates, not current game time).
- **ai_chance blocks**: Used in event options to weight AI decision-making. Format: `ai_chance = { base = N modifier = { factor = X trigger = { ... } } }`. Common in situation events and complex DHE chains (e.g., flavor_chi.txt, flavor_DLH.txt), but less common in simple flavor events.
- **Opinion effects - CRITICAL**: 
  * ❌ **WRONG**: `add_opinion = { target = X value = 50 }` — This syntax does NOT exist in EU5 and returns 0 values in-game.
  * ✅ **CORRECT**: `add_opinion = { target = X modifier = modifier_name }` where `modifier_name` is defined in `main_menu/common/biases/*.txt` (not static_modifiers) with `value = N` and optional `yearly_decay = X`. Example: `burgundy_relations_positive = { value = 50 yearly_decay = 5 }`.
  * Opinion modifiers MUST be placed in `main_menu/common/biases/*.txt`, NOT `main_menu/common/static_modifiers/`. Static modifiers (country/location category) and opinion biases are separate systems.
  * Bias structure: `modifier_name = { value = 50 yearly_decay = 5 }` (opinion points/year decay). No `game_data` wrapper needed for biases.
- **Trust mechanics**: Trust effects use `add_trust = { modifier = trust_modifier_name target = scope:country }` format. Trust modifiers must be defined separately (similar to opinion modifiers). Used extensively in situation events and diplomatic DHE chains.
- **Advance research in events**: To grant an advance via event, use `research_advance = <advance_key>` (country scope). The advance must be defined in `common/advances/`; this bypasses normal research requirements.
- **Dynamic Historical Events (DHE) - Modern Syntax**:
  * ✅ **CRITICAL - Tag syntax**: Use BARE tags in `dynamic_historical_event` blocks: `tag = BUR` (NOT `tag = c:BUR`). The c: prefix is only used in event triggers/effects, NOT in DHE definitions.
  * REQUIRED fields: `tag = BARE_TAG`, `from = YYYY.M.D`, `to = YYYY.M.D` (end date), `monthly_chance = N`.
  * Missing `to =` date causes event to fire indefinitely if other triggers match; always specify event end date explicitly.
  * Example: `dynamic_historical_event = { tag = BUR from = 1390.1.1 to = 1400.12.31 monthly_chance = 100 }`.
  * Multiple tags possible: `tag = ARM` and `tag = SYU` in same event (base game pattern in flavor_arm.txt).
  * `illustration_tags` block with mood/setting pairs is REQUIRED for proper event art display. Format: `illustration_tags = { 10 = mood 10 = setting }` (see EU5_ILLUSTRATION_TAGS_REFERENCE.txt for all valid values).
  * `historical_option = yes` on the canonically-correct option path for historical flavor. Helps track which path the AI should prefer.
  * Reference historical context via `historical_info = namespace.event.historical_info` in event header for tooltip explanations.
  * **DHE events do NOT use on_actions** - they fire via the dynamic_historical_event block, not on_action hooks. Delete any on_action files for DHE events.
- **Optional scope access**: Use `?=` prefix in triggers when a scope may not exist (e.g., `c:FRA ?= { exists = yes }` prevents error if France doesn't exist). Base game uses this extensively in DHE chains.
 - **Location filters**: In `every_owned_location`/`any_owned_location` limits, use `area ?= area:<name>` and `region ?= region:<name>`; do not use `location_area`/`location_region`.

Modding notes (examples)
- Partial location transfers: filter inside `every_owned_location` with `area ?= area:picardy_area` (e.g., Treaty of Arras transferring only Picardy).
- Full annexations: omit the limit block to transfer all owned locations.

Modding Workflow - Lessons Learned
- **Incremental testing**: After each major change (new IO, event hook, setup file), test immediately rather than batching changes - errors compound quickly.
- **File structure validation**: When bulk-editing events (adding illustration_tags, removing ai_chance, converting opinion syntax), validate the file structure BEFORE and AFTER to catch malformed option blocks, missing trigger closing braces, or orphaned code from regex operations. Use `get_errors` tool after major changes.
- **Regex caution**: Regex replacements can create subtle corruption (missing whitespace, orphaned code blocks, duplicate statements) if not carefully crafted. After regex operations, always check for:
  * Missing closing braces on `trigger`, `option`, and `if` blocks.
  * Orphaned variable assignments or modifiers outside their parent blocks.
  * Improper indentation that breaks nested scoping.
  * Extra closing braces at end of file.
- **Opinion mechanic research**: When opinion effects show 0 values in-game, do NOT assume raw `value =` syntax is wrong — verify EU5 actually supports it by grep_searching vanilla base game events. Many EU4 patterns don't carry forward to EU5.
- **Error log priority**: Check `Documents\Paradox Interactive\Europa Universalis V\logs\error.log` first for parsing errors. BOM issues, missing scopes, and syntax errors appear here with line numbers.
- **Vanilla pattern analysis**: When implementing custom systems (IOs, laws, etc.), use `Select-String` to find ALL vanilla examples, then cross-reference setup files and definition files to understand the complete pattern.
- **Commit granularly**: Commit after each working feature (event set, IO visibility fix, etc.) rather than waiting for "complete" state - makes debugging easier via git bisect.
- **UTF-8 with BOM everywhere**: All `.txt`, `.yml`, and script files MUST be UTF-8 with BOM. Use `create_file` tool to ensure proper encoding from start.
- **Orphaned event detection**: After fixing invalid triggers, check `error.log` for "orphaned event" messages. Events become orphaned when triggers fail PostValidate, preventing them from firing. Common causes: invalid `owns = <id>` syntax, missing scope accessors, or undefined modifier references.

GUI Data Binding - Critical Patterns
- **EconomyView context**: In `economy_lateralview.gui`, use `EconomyView.GetIncome('category')` to access income values (categories: `trade`, `interest`, `food`, `diplomacy`, `io_payments`, `mercenary`, `foreign`, `other`). Do NOT try to access `Player.monthly_income_*` properties directlythey're not exposed to GUI.
- **Math in GUI**: Use `Add_CFixedPoint()`, `Multiply_CFixedPoint()`, `Subtract_CFixedPoint()` for calculations. Nest them for complex formulas (e.g., `Multiply_CFixedPoint(Add_CFixedPoint(value1, value2), '(CFixedPoint)12')`).
- **GetScriptValue() unavailable**: Script values defined in `common/script_values/` cannot be called from GUI via `GetScriptValue()`. Use direct calculations or find the appropriate datacontext method instead.
- **Tooltip templates**: Use `ContextualTooltipType` for consistent tooltip styling. Place custom tooltips in `in_game/gui/shared/` and reference via `tooltipwidget = { using = template_name }`.
- **Default fallback**: If a GUI expression returns "default" or empty string, the property/method doesn't exist or isn't callable in that datacontext. Check vanilla files for the correct accessor pattern.
- **Datamodel iteration**: For dynamic lists, use `TooltipScrolledStringPairList` with `textcontext` or `datamodel`. Note: many ranked/sorted lists (like top-10 countries by GDP) are NOT exposed by the engineverify existence in vanilla GUI before implementing.

Mod Structure - instincts_mod
- **Mod location**: User mods live in `Documents\Paradox Interactive\Europa Universalis V\mod\<mod_name>\`. Override vanilla files by mirroring the path structure (e.g., `in_game/gui/economy_lateralview.gui` overrides the vanilla file).
- **Partial overrides**: When overriding GUI files, copy the entire vanilla file and modify only the necessary sections. Use blockoverrides where possible to minimize changes.
- **Script values**: Place custom script values in `in_game/common/script_values/`. Use them in triggers/effects, but remember they're not GUI-callable.
- **Static modifiers - CRITICAL**: Static modifiers belong in `main_menu/common/static_modifiers/`, organized by category:
  * Country/location modifiers: `main_menu/common/static_modifiers/*.txt` with `game_data { category = country }` or `category = location`.
  * Opinion biases (NOT static modifiers): `main_menu/common/biases/*.txt` with plain structure `modifier_name = { value = N yearly_decay = X }`.
  * Do NOT define opinion modifiers in static_modifiers.txt; they must go in biases instead.
- **Localization structure**: 
  * DHE events: `main_menu/localization/english/events/DHE/<flavor>_l_english.yml`
  * General events: `main_menu/localization/english/events/<feature>_l_english.yml`
  * UI/startup content: `main_menu/localization/english/<feature>_l_english.yml`
  * In-game features (GUI overrides): `in_game/localization/english/<feature>_l_english.yml`
- **International Organizations - Hanseatic League Example**:
  * **IO Definition**: `in_game/common/international_organizations/hanseatic_league.txt` - defines membership, modifiers, leadership
  * **IO Laws**: `in_game/common/laws/22_hanseatic_league.txt` - 11 categories with 40+ policies using `international_organization_modifier`
  * **Setup**: `main_menu/setup/start/15_hanseatic_league.txt` - creates IO at game start with members, areas, and starter laws
  * **Events**: `in_game/events/hanseatic_league_events.txt` - 20 DHE events with proper `tag = BARE_TAG`, date ranges, and `illustration_tags`
  * **Custom Modifiers**: `main_menu/common/static_modifiers/historical_flavor_modifiers.txt` - for effects without direct triggers
  * **Biases**: `main_menu/common/biases/hanseatic_league_biases.txt` - opinion/trust modifiers between members
  * **Multiple IO Membership**: Allow HRE members to join via conditional `can_join_trigger` logic
  * **Leadership**: Expand `can_lead_trigger` to include founding members (HSA, LUB, HAM, BRM)
- **File cleanup**: Remove unused override files from mods—they can cause load order issues or unexpected vanilla behavior changes. Only keep files you've actually modified.

**Recent Findings**
- **Pop types discovered:** `nobles`, `clergy`, `burghers`, `peasants`, `laborers`, `soldiers`, `slaves`, `tribesmen`.
- **Applied pattern:** for member-reaction flavor we use a pop-targeted satisfaction change: `every_pop = { limit = { pop_type = pop_type:clergy } add_pop_satisfaction = pop_satisfaction_ultimate_penalty }` to reduce clergy satisfaction when appropriate.
- **Guidance:** When adding pop-targeted effects, prefer `every_pop`/`scope:target_pop` patterns over global effects; always validate `pop_type:` tokens against the base game (`game/in_game/common/scripted_triggers/pop_triggers.txt`).

---
Addendum — Hanseatic League (instincts_mod)

- **Root cause:** Several PostValidate/parser errors were caused by using country-only triggers (e.g., `num_locations`, `any_owned_location`) inside an `international_organization` scope.
- **Dispatcher fixes:** Use country-scoped candidate selection (e.g., `any_country { limit = { num_locations = 1 any_owned_location = { is_coastal = yes } } }`), correct tokens (`num_of_locations` → `num_locations`, `coastal` → `is_coastal`), and prefer `yearly_country_pulse` for invite dispatchers instead of monthly.
- **Event fixes:** Convert in-effect event blocks to canonical `country_event` entries and fire follow-ups with `trigger_event = { id = namespace.event days = 0 target = scope:target }`. Use `scope:target` (or the event `target`) for candidate references rather than `scope:recipient` when the dispatcher supplies `target`.
- **IO definition guidance:** Keep `can_join_trigger` at IO scope minimal (founder tags, area/region checks). Delegate per-country ownership and coastal checks to a country-scoped dispatcher to avoid wrong-scope triggers.
- **Follow-up:** Audit any remaining `scope:recipient` uses inside `ai_desire` blocks in `in_game/common/international_organizations/hanseatic_league.txt` if PostValidate reports warnings.

This addendum documents the recent fixes applied in the `instincts_mod` branch and provides practical patterns to avoid similar parser errors in future IO/event work.

***

- **Mod location**: User mods live in `Documents\Paradox Interactive\Europa Universalis V\mod\<mod_name>\`. Override vanilla files by mirroring the path structure (e.g., `in_game/gui/economy_lateralview.gui` overrides the vanilla file).
- **Partial overrides**: When overriding GUI files, copy the entire vanilla file and modify only the necessary sections. Use blockoverrides where possible to minimize changes.
- **Script values**: Place custom script values in `in_game/common/script_values/`. Use them in triggers/effects, but remember they're not GUI-callable.
- **Static modifiers - CRITICAL**: Static modifiers belong in `main_menu/common/static_modifiers/`, organized by category:
  * Country/location modifiers: `main_menu/common/static_modifiers/*.txt` with `game_data { category = country }` or `category = location`.
  * Opinion biases (NOT static modifiers): `main_menu/common/biases/*.txt` with plain structure `modifier_name = { value = N yearly_decay = X }`.
  * Do NOT define opinion modifiers in static_modifiers.txt; they must go in biases instead.
- **Localization structure**: 
  * DHE events: `main_menu/localization/english/events/DHE/<flavor>_l_english.yml`
  * General events: `main_menu/localization/english/events/<feature>_l_english.yml`
  * UI/startup content: `main_menu/localization/english/<feature>_l_english.yml`
  * In-game features (GUI overrides): `in_game/localization/english/<feature>_l_english.yml`
- **International Organizations - Hanseatic League Example**:
  * **IO Definition**: `in_game/common/international_organizations/hanseatic_league.txt` - defines membership, modifiers, leadership
  * **IO Laws**: `in_game/common/laws/22_hanseatic_league.txt` - 11 categories with 40+ policies using `international_organization_modifier`
  * **Setup**: `main_menu/setup/start/15_hanseatic_league.txt` - creates IO at game start with members, areas, and starter laws
  * **Events**: `in_game/events/hanseatic_league_events.txt` - 20 DHE events with proper `tag = BARE_TAG`, date ranges, and `illustration_tags`
  * **Custom Modifiers**: `main_menu/common/static_modifiers/historical_flavor_modifiers.txt` - for effects without direct triggers
  * **Biases**: `main_menu/common/biases/hanseatic_league_biases.txt` - opinion/trust modifiers between members
  * **Multiple IO Membership**: Allow HRE members to join via conditional `can_join_trigger` logic
  * **Leadership**: Expand `can_lead_trigger` to include founding members (HSA, LUB, HAM, BRM)
- **File cleanup**: Remove unused override files from mods—they can cause load order issues or unexpected vanilla behavior changes. Only keep files you've actually modified.
