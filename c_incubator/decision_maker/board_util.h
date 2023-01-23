#include "../dataset/board.h"

void __declspec(dllexport) board_util_loads_board(const wchar_t* file_path, Board* output);
std::list<Move> __declspec(dllexport) board_util_get_all_moves(const Board& board);