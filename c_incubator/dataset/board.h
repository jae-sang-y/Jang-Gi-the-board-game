#ifndef _BOARD_H_
#define _BOARD_H_

#include <list>
#include "common.h"

struct Board {
    unsigned char actor_code[9][10];
};

struct ActorWithPosition {
    int actor_code;
    int x;
    int y;
};

std::list<ActorWithPosition> __declspec(dllexport) board_foreach_actors(const Board& board);

bool board_is_pos_in_board(const Pos& pos)
{
    return (
        (0 <= pos.x && pos.x < 9) &&
        (0 <= pos.y && pos.y < 10)
    );
}

bool board_is_on_palace(const Pos& pos)
{
    return (
        (3 <= pos.x && pos.x <= 5) &&
        (0 <= pos.y && pos.y <= 2)
    ) || (
        (3 <= pos.x && pos.x <= 5) &&
        (7 <= pos.y && pos.y <= 9)
    );
}
bool board_is_on_ears_of_palaces(const Pos& pos)
{
    return (
        (pos.x == 3 || pos.x == 5) &&
        (pos.y == 0 || pos.y == 2)
    ) || (
        (pos.x == 3 || pos.x == 5) &&
        (pos.y == 7 || pos.y == 9)
    );
}

bool board_is_on_center_of_palaces(const Pos& pos)
{
    return (
        (pos.x == 4 && pos.y == 1)
    ) || (
        (pos.x == 4 && pos.y == 8)
    );
}

int board_get_actor(const Board& board, const Pos& pos)
{
    return board.actor_code[pos.x][pos.y];
}

#endif
