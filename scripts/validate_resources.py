"""Static v3.3 checks; use the real GitHub build for Minecraft API compilation."""
import json
from pathlib import Path

def read_checked_json(path: Path):
    """Report the exact offending resource instead of a filename-free traceback."""
    content = path.read_text(encoding='utf-8-sig')
    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        lines = content.splitlines()
        print(f"\nINVALID JSON FILE: {path}", flush=True)
        print(f"ERROR: {exc.msg} (line {exc.lineno}, column {exc.colno}, char {exc.pos})", flush=True)
        for idx in range(max(1, exc.lineno - 3), min(len(lines), exc.lineno + 3) + 1):
            print(f"{idx:4}: {lines[idx-1][:180]}", flush=True)
        if exc.msg == 'Extra data':
            print("HINT: Remove any second JSON object or trailing text after the first JSON value.", flush=True)
        raise SystemExit(1) from exc

root = Path(__file__).resolve().parents[1]
res = root / 'src/main/resources'
dim = read_checked_json(res / 'data/underworld/dimension/underworld.json')
type_ = read_checked_json(res / 'data/underworld/dimension_type/underworld.json')
biome = read_checked_json(res / 'data/underworld/worldgen/biome/wasteland.json')
java = root / 'src/main/java/dev/unstable/underworld'
mod = (java / 'UnderworldMod.java').read_text()
terrain = (java / 'UnderworldTerrain.java').read_text()
math = (java / 'UnderworldMath.java').read_text()
structures = (java / 'UnderworldStructures.java').read_text()
properties = (root / 'gradle.properties').read_text()
workflow = (root / '.github/workflows/build.yml').read_text()

assert dim['type'] == 'underworld:underworld'
gen = dim['generator']
assert gen['type'] == 'minecraft:flat' and gen['settings']['layers'] == []
assert gen['settings']['biome'] == 'underworld:wasteland'
assert gen['settings']['features'] is False and gen['settings']['lakes'] is False
assert gen['settings']['structure_overrides'] == []
assert type_['min_y'] == -192 and type_['height'] == 512
assert type_['skybox'] == 'none' and type_['has_skylight'] is False
assert type_['cardinal_light'] == 'nether'
assert 'minecraft:visual/sky_color' not in biome['attributes']
assert len(biome['features']) == 11
assert 'UNDERWORLD_DROP_Y = 296.0' in mod
assert 'entity.getX()' in mod and 'entity.getZ()' in mod
assert 'GameType.ADVENTURE' in mod and 'restoreOriginalMode(player)' in mod
assert 'UNDERWORLD_LOWER_EXIT_Y' not in mod
assert 'NETHER_RETURN_Y = -7.0' in mod and 'overworldLanding' in mod
assert 'e.getY() > UNDERWORLD_UPPER_EXIT_Y' in mod
assert 'PIT_GRID' not in math
assert 'VERSION_MARKER_Y = -187' in terrain
assert 'boolean v32' in terrain
assert 'UnderworldMath.hasLand(x, z, seed)' in terrain
assert 'UnderworldStructures.generate(chunk, seed)' in terrain
assert 'VERTICAL_THICKNESS = 30' in math
assert 'COMPLETE_VOID = 6400' in math
assert 'UnderworldMath.surfaceY(cx, cz, seed)' in structures
assert 'UnderworldPlacement.inChunk' in structures
assert 'RandomizableContainer' in structures and 'setLootTable(RELICS, h)' in structures
assert 'portalPiece' in structures and 'hasRarePortal' in structures
assert 'UnderworldMath.structureSite(cx, cz, seed, radius(kind))' in structures
for name in ('gate(', 'shrine(', 'tower(', 'citadel(', 'mausoleum(', 'shatteredArchive(', 'fracturedBridge(', 'forgottenMarket('):
    assert name in structures
assert 'mod_version=3.3.2' in properties
assert 'unstable-underworld-3.3.2.jar' in workflow
assert not (res / 'data/minecraft/dimension/the_nether.json').exists()
assert not (res / 'data/minecraft/dimension_type/the_nether.json').exists()
for path in root.rglob('*.json'):
    read_checked_json(path)
lootfile = res / 'data/underworld/loot_table/chests/forgotten_relics.json'
loot = read_checked_json(lootfile)
assert loot['type'] == 'minecraft:chest' and len(loot['pools']) >= 3
# Minecraft Java 26.3 changed loot entry fields functions -> modifier,
# and modifier function -> type. JSON parsing alone DOES NOT catch this.
# Reject the old schema so GitHub fails before publishing a broken mod.
for pool in loot['pools']:
    assert 'functions' not in pool and 'conditions' not in pool, "Legacy loot pool schema (26.2)"
    assert isinstance(pool['entries'], list) and pool['entries']
    for entry in pool['entries']:
        assert 'functions' not in entry and 'conditions' not in entry, "Legacy loot entry schema (26.2)"
        if 'modifier' in entry:
            modifiers = entry['modifier'] if isinstance(entry['modifier'], list) else [entry['modifier']]
            assert modifiers, "Empty modifier"
            for modifier in modifiers:
                assert isinstance(modifier, dict) and 'type' in modifier, "Invalid 26.3 modifier"
                assert 'function' not in modifier and 'conditions' not in modifier, "Legacy 26.2 function schema"
                if modifier['type'] == 'minecraft:set_count':
                    assert 'count' in modifier, "set_count missing count"
entries = [e['name'] for pool in loot['pools'] for e in pool['entries'] if e['type']=='minecraft:item']
for item in ('minecraft:echo_shard', 'minecraft:sculk_sensor', 'minecraft:gilded_blackstone', 'minecraft:ancient_debris'):
    assert item in entries
# In Minecraft 1.21.9+ the chain item was renamed from chain to iron_chain.
# A syntactically valid loot table containing the old ID can fail world datapack loading.
assert 'minecraft:chain' not in entries, 'Invalid 26.3 item identifier minecraft:chain; use minecraft:iron_chain'
assert 'minecraft:iron_chain' in entries
assert all(isinstance(e.get('name'), str) and e['name'].startswith('minecraft:')
           for p in loot['pools'] for e in p['entries'] if e['type'] == 'minecraft:item')
assert (java / 'UnderworldPlacement.java').exists()
assert 'PlacementTest' in workflow
print('PASS: empty dimension, Nether sky, 30-block terrain, void death, randomized ruins, rare portals, loot, migrations and packaging')
