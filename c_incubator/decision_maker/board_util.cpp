#include <fstream>
#include "board_util.h"
#include "../dataset/actor.h"

void board_util_loads_board(const wchar_t* file_path, Board* output)
{
    std::ifstream fs;
    fs.open(file_path);
    fs.read((char*)output, 90);
    fs.close();
}

std::list<Move> board_util_get_all_moves(const Board& board)
{
    std::list<Move> result;
    for (const auto& awp : board_foreach_actors(board)) {
        Pos pos {awp.x, awp.y};
        for (const auto& move_case : actor_move_cases(awp.actor_code, board, pos)) {
            result.push_back(
                Move{
                   pos, move_case
                }
            );
        }
    }

    return result;
}
