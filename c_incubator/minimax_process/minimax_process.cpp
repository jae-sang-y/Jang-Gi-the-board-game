#include <iostream>
#include <fstream>
#include <list>
#include <stdio.h>
#include <wchar.h>
#include <string>
#include "../dataset/board.h"
#include "../dataset/actor.h"
#include "../dataset/actor_type.h"
#include "../decision_maker/board_util.h"
#include "../evaluator/evaluator.h"

int g_minimax_level = 0;
int g_input_file_seq = 0;
Board g_board = {};

//#define DEBUG

int negative_max(const Board& board, const int depth, const bool is_red)
{
    if (depth == 0)
    {
        int v = evaluator_basic(board);
#ifdef DEBUG
//        int king_count = 0;
//        for (int x = 0; x < 9; ++x)
//           for (int y = 0; y < 10; ++y)
//           {
//                int actor_code = board_get_actor(board, Pos{x,y});
//                if (actor_get_actor_type(actor_code) == ACTOR_TYPE_KING)
//                {
//                    king_count += 1;
//                }
//           }
//        std::cout << "v : " << v << " , king : " << king_count << std::endl;
#endif
        return v;
    }
    bool result_found = false;
    int result = -99999;
    int seq = 0;

    const auto& all_moves = board_util_get_all_moves(board);

    for (const auto& move : all_moves)
    {
        if (
            actor_is_red(board.actor_code[move.src.x][move.src.y]) != is_red
        )
            continue;
        seq += 1;
#ifdef DEBUG
        if (depth == g_minimax_level)
        {
//            std::cout << seq << " / " << all_moves.size() << std::endl;
            std::cout << move.src.x << ", " << move.src.y << " -> " << move.dst.x << ", " << move.dst.y
                      << " ============================================================================" << std::endl;
        }
#endif
        Board new_board { board };

        new_board.actor_code[move.dst.x][move.dst.y] = new_board.actor_code[move.src.x][move.src.y];
        new_board.actor_code[move.src.x][move.src.y] = NULL;
#ifdef DEBUG
//        int v = evaluator_basic(board);
//        std::cout << "vv : " << v << std::endl;
#endif

        int new_board_score = negative_max(new_board, depth - 1, !is_red);
        if (
            result_found == false || (
                is_red && new_board_score > result ||
                (!is_red) && new_board_score < result
            )
        )
        {
            result = new_board_score;
            result_found = true;
        }
#ifdef DEBUG
        if (depth == g_minimax_level)
        {
            std::cout << " >> " << new_board_score << std::endl;
        }
#endif
    }

    return result;
}

void parallel_execute(const int minimax_level, const int k)
{
    wchar_t v_board_file_path[256];
    wchar_t v_move_file_path[256];
    wchar_t v_out_file_path[256];
    char    v_buffer[256] = {};
    swprintf(
        v_board_file_path,
        L"C:\\Users\\apple\\OneDrive\\문서\\GitHub\\Jang-Gi-the-board-game\\working_temp\\minimax\\board.dat"
    );
    swprintf(
        v_move_file_path,
        L"C:\\Users\\apple\\OneDrive\\문서\\GitHub\\Jang-Gi-the-board-game\\working_temp\\minimax\\%d.input.dat",
        k
    );
    swprintf(
        v_out_file_path,
        L"C:\\Users\\apple\\OneDrive\\문서\\GitHub\\Jang-Gi-the-board-game\\working_temp\\minimax\\%d.output.dat",
        k
    );

    board_util_loads_board(v_board_file_path, &g_board);

#ifdef DEBUG
    for (int y = 0; y < 10; ++y)
    {
        for (int x = 0; x < 9; ++x)
        {
            int act = g_board.actor_code[x][y];
            if (act < 10)
                printf("  %d", act);
            else
                printf(" %d", act);
        }
        printf("\n");
    }
#endif

    {
        int v_a, v_b, v_c, v_d;
        std::ifstream fs{};
        fs.open(v_move_file_path);
        fs >> v_a >> v_b >> v_c >> v_d;

        g_board.actor_code[v_c][v_d] = g_board.actor_code[v_a][v_b];
        g_board.actor_code[v_a][v_b] = NULL;

    }
    int move_value = negative_max(g_board, minimax_level, true);
    std::cout << "move_value : " << move_value << std::endl;
    {
        std::ofstream fs{};
        fs.open(v_out_file_path);
        fs << move_value;
        fs.close();
    }
}

int main(int argc, char**argv)
{
    g_minimax_level = std::atoi(argv[1]);
    g_input_file_seq = std::atoi(argv[2]);
    std::cout << "g_minimax_level: " << g_minimax_level << std::endl;
    std::cout << "g_input_file_seq: " << g_input_file_seq << std::endl;
    printf("argc: %d\n", argc);

    parallel_execute(g_minimax_level, g_input_file_seq);

    return 0;
}