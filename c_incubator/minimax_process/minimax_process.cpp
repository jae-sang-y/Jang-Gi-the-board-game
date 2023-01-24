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
std::ofstream g_report_stream;

void log_board(const Board& board, const char* title)
{
    g_report_stream << "----------------------------" << std::endl;
    for (int y = 0; y < 10; ++y)
    {
        for (int x = 0; x < 9; ++x)
        {
            int act = board.actor_code[x][y];
            g_report_stream << "|";
            if (act == 0)
            {
                g_report_stream << "　";
            }
            else if (act == 1) g_report_stream << "왕";
            else if (act == 2) g_report_stream << "차";
            else if (act == 3) g_report_stream << "마";
            else if (act == 4) g_report_stream << "상";
            else if (act == 5) g_report_stream << "포";
            else if (act == 6) g_report_stream << "사";
            else if (act == 7) g_report_stream << "병";
            else if (act == 8) g_report_stream << "王";
            else if (act == 9) g_report_stream << "車";
            else if (act == 10) g_report_stream << "馬";
            else if (act == 11) g_report_stream << "象";
            else if (act == 12) g_report_stream << "包";
            else if (act == 13) g_report_stream << "士";
            else if (act == 14) g_report_stream << "兵";
            else
            {
                g_report_stream << " " << act;
            }
        }
        g_report_stream << "|" << std::endl;
    }
    g_report_stream << "----------------------------" << std::endl;
    g_report_stream << "| " << title << std::endl
                    << "| evaluated as " << evaluator_basic(board) << " points" << std::endl;
    g_report_stream << "----------------------------" << std::endl;
}


//#define DEBUG

int negative_max(const Board& board, const int turn_cnt, const bool is_red)
{
    if (turn_cnt == g_minimax_level)
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
    char buffer[256];
    Board best_situation;

    for (const auto& move : all_moves)
    {
        if (
            actor_is_red(board.actor_code[move.src.x][move.src.y]) != is_red
        )
        {
            if (turn_cnt == 2)
            {
                g_report_stream << " $ " << move.src.x << ", " << move.src.y
                                << " -> " <<  move.dst.x << ", " << move.dst.y;
            }
            continue;
        }
        seq += 1;
#ifdef DEBUG
        if (turn_cnt == 2)
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
        int new_board_score = negative_max(new_board, turn_cnt + 1, !is_red);
        if (turn_cnt == 2)
        {
            g_report_stream << " / " << move.src.x << ", " << move.src.y
                            << " -> " <<  move.dst.x << ", " << move.dst.y
                            << " (" << new_board_score << ")";
            if (seq % 5 == 0)
                g_report_stream << std::endl;
        }
        if (
            result_found == false || (
                is_red && new_board_score > result ||
                (!is_red) && new_board_score < result
            )
        )
        {
            result = new_board_score;
            sprintf(buffer, " %d, %d -> %d, %d (%d)", move.src.x, move.src.y, move.dst.x, move.dst.y, new_board_score);
            result_found = true;
            best_situation = new_board;
        }
#ifdef DEBUG
        if (turn_cnt == 2)
        {
            std::cout << " >> " << new_board_score << std::endl;
        }
#endif
    }
    if (turn_cnt == 2)
    {
        g_report_stream << std::endl;

        for (const auto& awp : board_foreach_actors(board)) {
             g_report_stream << " @ " << awp.x << ", " << awp.y;
        }
        g_report_stream << std::endl;

        g_report_stream << "#" << turn_cnt;
        for (int c = 0; c < turn_cnt - 2; ++c) {
            g_report_stream << "  ";
        }
        g_report_stream << " >> " << buffer << std::endl;
        sprintf(buffer, "#%d move(%s turn)", turn_cnt, is_red ? "red" : "green");
        log_board(best_situation, buffer);
    }
    return result;
}

void parallel_execute(const int minimax_level, const int k)
{
    wchar_t v_board_file_path[256];
    wchar_t v_move_file_path[256];
    wchar_t v_out_file_path[256];
    wchar_t v_report_file_path[256];
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
    swprintf(
        v_report_file_path,
        L"C:\\Users\\apple\\OneDrive\\문서\\GitHub\\Jang-Gi-the-board-game\\working_temp\\minimax\\%d.report.dat",
        k
    );
    g_report_stream.open(v_report_file_path);

    board_util_loads_board(v_board_file_path, &g_board);

    g_report_stream << "g_minimax_level: " << g_minimax_level << std::endl;
    log_board(g_board, "before move");

    {
        int v_a, v_b, v_c, v_d;
        std::ifstream fs{};
        fs.open(v_move_file_path);
        fs >> v_a >> v_b >> v_c >> v_d;

        g_board.actor_code[v_c][v_d] = g_board.actor_code[v_a][v_b];
        g_board.actor_code[v_a][v_b] = NULL;
        g_report_stream << "1st move: " << v_a << ", " << v_b << " -> " << v_c << ", " << v_d << std::endl;
    }

    log_board(g_board, "1st moved(green)");

    int move_value = negative_max(g_board, 2, true);
    std::cout << "move_value : " << move_value << std::endl;
    g_report_stream << "move_value : " << move_value << std::endl;
    {
        std::ofstream fs{};
        fs.open(v_out_file_path);
        fs << move_value;
        fs.close();
    }
}

int main(int argc, char**argv)
{
    g_minimax_level = std::atoi(argv[1]) + 2;
    g_input_file_seq = std::atoi(argv[2]);
    std::cout << "g_minimax_level: " << g_minimax_level << std::endl;
    std::cout << "g_input_file_seq: " << g_input_file_seq << std::endl;
    printf("argc: %d\n", argc);

    parallel_execute(g_minimax_level, g_input_file_seq);

    return 0;
}