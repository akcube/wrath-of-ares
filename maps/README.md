# Map Design

Any valid map design must follow a certain set of rules for the game to work as intended.

## Map validity
For a map to be considered valid, the following requirements MUST be satisfied.

1. The grid size must be `REQ_HEIGHT` x `REQ_WIDTH` in size. These constants are defined in `../utils/config.py`. Default values are 30x125.
2. Empty area can be any character.
3. The village MUST be enclosed by walls. Walls must be represented by the `#` character. Walls are `1x1` entities.
4. Huts are `5x2` entities. The top left tile of where you wish the hut to be spawned must be marked by `H`.
5. Cannons are `1x1` entitities. Mark the tiles you want cannons in with `C`.
6. The townhall is a `4x2` entity. Mark the top left tile of the town hall with a `T`.
7. The wizard tower is a `5x3` entity. Mark the top left tiles of the toward with a `W`.
8. No building can intersect with another building. Ensure none of the entities larger than `1x1` intersect each other.
9. All entities MUST strictly lie INSIDE the walled enclosure. 
10. The king will always spawn at 1, 1. Do NOT place any other building or spawnpoint there.
11. Mark the barbarian spawn points with `1`, `2` and `3` respectively.
12. There can only be ONE townhall and exactly three barbarian spawnpoints.

A sample is given in `map1.txt`.