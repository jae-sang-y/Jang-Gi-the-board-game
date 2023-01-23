#ifndef _ACTOR_H_
#define _ACTOR_H_

#include "common.h"
#include "board.h"
#include <vector>

std::vector<Pos> __declspec(dllexport) actor_move_cases(const int& actor_code, const Board& board, const Pos& pos);


int inline actor_get_actor_type(const int& actor_code) {
    return (actor_code-1) % 7 + 1;
};
bool inline actor_is_red(const int& actor_code) {
    return (actor_code < 8) ? true : false;
};

#endif
