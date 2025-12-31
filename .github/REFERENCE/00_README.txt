# EU5 Modding Reference Files - Quick Guide

This directory contains comprehensive EU5 modding documentation extracted from official .info files and game data.
Total: 15 reference files (~289KB, ~8,000 lines)

## File Index

### Core Scripting (Most Frequently Used)
- EU5_EFFECTS_REFERENCE.txt (390 lines) - All valid effects (add_prestige, set_variable, add_country_modifier, etc.)
- EU5_TRIGGERS_REFERENCE.txt (173 lines) - All valid trigger conditions (is_subject_of, tag, current_date, etc.)
- EU5_SCOPES_REFERENCE.txt (400 lines) - Scope types and context (country, location, character, etc.)
- EU5_SCOPE_LINKS_REFERENCE.txt (685 lines) - How to navigate between scopes (c:TAG, var:name, scope:saved_scope)

### Modifiers & Stats
- EU5_MODIFIERS_REFERENCE.txt (150 lines) - Modifier definitions and categories
- EU5_MODIFIER_TYPES_REFERENCE.txt (711 lines) - Valid modifier property types (monthly_prestige, land_morale_modifier, etc.)
- EU5_ALL_MODIFIERS_SAMPLE.txt (200 lines) - Sample modifier implementations from vanilla game

### Events & Timing
- EU5_ON_ACTIONS_REFERENCE.txt (711 lines) - Event hooks (yearly_country_pulse, on_game_start, etc.)
- EU5_MEAN_TIME_TO_HAPPEN_REFERENCE.txt (733 lines) - MTTH system for event probability/weighting

### Advanced Scripting
- EU5_SCRIPT_VALUES_REFERENCE.txt (706 lines) - Script value definitions and formulas
- EU5_VARIABLES_REFERENCE.txt (604 lines) - Variable system (set_variable, var:name, scope persistence)
- EU5_MACROS_REFERENCE.txt (699 lines) - Reusable script macros

### UI & Localization
- EU5_GUI_SCRIPT_REFERENCE.txt (755 lines) - GUI datamodel, widgets, properties
- EU5_LOCALIZATION_REFERENCE.txt (774 lines) - Localization keys, tokens, scope references

### System Configuration
- EU5_DEFINES_REFERENCE.txt (307 lines) - Game defines and constants

### Guides (How-to Summaries)
- EU5_ACTION_MODDING.txt — Actions
- EU5_EVENT_MODDING.txt — Events
- EU5_MISSION_MODDING.txt — Missions
- EU5_SCRIPTED_GUI.txt — Scripted GUI
- EU5_BUILDING_MODDING.txt — Buildings
- EU5_GOODS_MODDING.txt — Goods
- EU5_ESTATE_MODDING.txt — Estates
- EU5_POP_MODDING.txt — Pops
- EU5_LAW_MODDING.txt — Laws
- EU5_SUBJECT_TYPE_MODDING.txt — Subject types
- EU5_ADVANCE_MODDING.txt — Advances (tech)
- EU5_UNIT_MODDING.txt — Units
- EU5_CHARACTER_MODDING.txt — Characters/interactions
- EU5_CONCEPT_MODDING.txt — Game concepts
- EU5_CULTURE_MODDING.txt — Culture/language
- EU5_MODIFIER_MODDING.txt — Static/auto modifiers
- EU5_INTERNATIONAL_ORGANIZATION_MODDING.txt — International organizations

## Common Troubleshooting Lookup Patterns

### "Unknown effect <name>" errors:
1. Check EU5_EFFECTS_REFERENCE.txt for correct effect name
2. Verify scope context in EU5_SCOPES_REFERENCE.txt
3. If using modifiers, check EU5_MODIFIER_TYPES_REFERENCE.txt for valid properties

### "Unknown trigger type <name>" errors:
1. Check EU5_TRIGGERS_REFERENCE.txt for correct trigger syntax
2. Verify trigger is valid in current scope (EU5_SCOPES_REFERENCE.txt)
3. Check EU5_SCOPE_LINKS_REFERENCE.txt for proper scope navigation

### Event parsing/firing issues:
1. Check EU5_ON_ACTIONS_REFERENCE.txt for proper event hook syntax
2. Review EU5_MEAN_TIME_TO_HAPPEN_REFERENCE.txt for event weighting
3. Verify dynamic_historical_event structure (see copilot-instructions.md)

### Modifier not applying:
1. Verify modifier name exists in EU5_MODIFIERS_REFERENCE.txt
2. Check properties against EU5_MODIFIER_TYPES_REFERENCE.txt
3. Review EU5_ALL_MODIFIERS_SAMPLE.txt for working examples

### GUI data binding errors:
1. Check EU5_GUI_SCRIPT_REFERENCE.txt for datamodel methods
2. Verify property access patterns (GetIncome(), GetScriptValue(), etc.)
3. Check EU5_LOCALIZATION_REFERENCE.txt for proper token syntax

### Scope errors ("Inconsistent effect scopes"):
1. Review EU5_SCOPES_REFERENCE.txt for scope hierarchy
2. Check EU5_SCOPE_LINKS_REFERENCE.txt for navigation patterns
3. Use save_scope_as + set_variable pattern for persistence

### Variable reference issues:
1. Check EU5_VARIABLES_REFERENCE.txt for proper syntax (var:name, scope:name)
2. Verify variable scope persistence rules
3. Review script value access patterns in EU5_SCRIPT_VALUES_REFERENCE.txt

## Quick Reference: File Selection by Task

**Creating events**: EFFECTS, TRIGGERS, ON_ACTIONS, MEAN_TIME_TO_HAPPEN
**Creating modifiers**: MODIFIERS, MODIFIER_TYPES, ALL_MODIFIERS_SAMPLE
**Building GUI**: GUI_SCRIPT, LOCALIZATION
**Debugging scopes**: SCOPES, SCOPE_LINKS, VARIABLES
**Adding formulas**: SCRIPT_VALUES, MACROS
**System configuration**: DEFINES

## Best Practices

1. **Always check reference files before using EU4/CK3 syntax** - EU5 has different effect/trigger names
2. **Verify scope context** - Many effects/triggers only work in specific scopes
3. **Use vanilla examples** - ALL_MODIFIERS_SAMPLE.txt shows working implementations
4. **Cross-reference** - If an effect uses a modifier, check both EFFECTS and MODIFIER_TYPES
5. **Follow encoding rules** - All script files must be UTF-8 with BOM (see LOCALIZATION_REFERENCE)

## Related Documentation

- **../copilot-instructions.md** - Repository-specific modding guidelines and EU5 compliance rules
- **game/in_game/common/*/*.info** - Official Paradox modding documentation (31 files)

## File Maintenance

These reference files are extracted from game data and official .info files. 
Update when:
- Major game patches change scripting API
- New DLC adds effects/triggers/modifiers
- Official .info files are updated

Last verified: Europa Universalis V (current build)
