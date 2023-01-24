#ifndef _ACTOR_H_
#define _ACTOR_H_

#include "common.h"
#include "board.h"
#include <vector>

std::vector<Pos> __declspec(dllexport) actor_move_cases(const int& actor_code, const Board& board, const Pos& pos);


int __declspec(dllexport) actor_get_actor_type(const int& actor_code);
bool __declspec(dllexport) actor_is_red(const int& actor_code);

#endif
