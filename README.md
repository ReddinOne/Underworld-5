# Unstable Underworld v3.3 — Minecraft Java 26.3 / Fabric

A separate Underworld dimension that you fall into from below the Nether. The original Nether terrain generator and existing Nether chunks remain untouched.

## New in v3.3

- **Eight handcrafted procedural ruin families**, including gothic gates, shrines, towers, citadels, mausoleums, shattered archives, fractured bridges, and lost markets.
- **No perfectly-aligned structure grid:** deterministic seed-based, rotated and jittered candidate locations, 30% deliberate empty cells, and neighbor spacing rejection. Existing v3.2 structure positions change once per upgraded Underworld chunk.
- **Loot chests** (68% primary chest + 24% independent secondary chest chance per generated ruin). The custom `underworld:chests/forgotten_relics` loot table mixes ancient-city/sculk finds and bastion/Nether treasures with mostly atmospheric low-to-mid rewards and rare valuable relics.
- **Very rare usable Overworld portals:** eligible kinds = gates and mausoleums; 1/110 chance *per eligible ruin*. Active violet portal blocks in black obsidian frames send entities to safe solid Overworld surfaces. They do not generate or modify Nether/Overworld blocks beyond destination selection.
- **Returning to the Nether via `/underworld return` or rising above Y=315 now puts entities at exact Y=-7, same X/Z.** This is deliberately below the Nether floor, so entities can fall back into the Underworld. Survival mode is restored on return.

## Previous behavior retained

- Minecraft **Java Edition 26.3**, Fabric Loader and Fabric API, Java 25 / Gradle 9.7.1.
- Independent Underworld dimension with Nether-type reddish sky, no sun, and no clouds.
- The player remains at original X/Z while falling from the Nether into the Underworld from Y=296; no spawn platform; downward velocity preserved.
- Automatic Adventure mode inside Underworld; restores saved mode upon leaving.
- The Underworld has about 30 blocks of thickness, shallow mountains, far-reaching soul sand/soul soil and blackstone regions, huge void chasms, and no land beyond radius 6,400 blocks.
- Falling out the *bottom* of the Underworld results in regular Minecraft void damage and death (never returns you to Nether).

## Commands

`/underworld enter`: fall into the dimension at your current X/Z coordinates.

`/underworld return`: return to Nether at Y=-7 (your X/Z are preserved).

## Building on GitHub

1. Upload the contents of this ZIP to the **root** of your repository (not inside an extra folder).
2. Go to **Actions → Build Minecraft 26.3 mod → Run workflow**.
3. Download the artifact and extract `unstable-underworld-3.3.0.jar`.
4. Install Fabric Loader and the matching Fabric API, and put this JAR into `mods/`.

GitHub Actions runs the pure Java geometry tests, static resource validation, and a real Gradle/Fabric build. The source is supplied uncompiled; a successful compile and in-game functionality must be verified via GitHub and Minecraft.

## IMPORTANT: BACK UP YOUR WORLD

The Underworld migrates v3.0–v3.2 chunks by clearing their existing land/ruins and generating the v3.3 layout, **destroying any player builds or chests in affected Underworld chunks.** The vanilla Nether is never changed by this mod. Existing v3.3 chunks are marked and skip regeneration.

## Note about generated portals

Portal blocks are *real* vanilla portal blocks in frames. The server-side Underworld-to-Overworld redirect executes upon contact, prior to vanilla's delayed Nether portal transition. The Overworld destination is the nearest safe air space on a solid surface (up to 24 blocks horizontal displacement); nothing is placed in the Overworld. If no safe site is found, teleportation is refused. The spawning height in the Nether when returning is **always -7**, even if it causes an immediate fall.

## Architectural notes

Terrain and structure locations are pure functions of coordinates + world seed. Generation writes only the current chunk (no recursive neighbor loading), including containers and portal frame pieces. The structure rejection algorithm uses the same candidate neighborhood regardless of chunk load order. Loot chests carry a custom loot-table key and per-location deterministic seed; they populate when first opened.

## Sources / rights

Original procedural geometry, not copied from any YouTube map. Minecraft is a trademark of Mojang/Microsoft. License: MIT, as provided in LICENSE.
