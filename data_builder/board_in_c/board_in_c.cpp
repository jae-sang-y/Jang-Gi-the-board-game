#include "board_in_c.hpp"

export void init()
{
    for (int x : {3, 4, 5})
    {
        for (int y : {0, 1, 2, 7, 8, 9})
        {
            auto &list = castle_route_list_map[x][y];
            if (3 <= x && x < 5)
                list.push_back(Pos{+1, 0});
            if (3 < x && x <= 5)
                list.push_back(Pos{-1, 0});
            if (0 <= y && y < 2 || 7 <= y && y < 9)
                list.push_back(Pos{0, +1});
            if (0 < y && y <= 2 || 7 < y && y <= 9)
                list.push_back(Pos{0, -1});

            if (x == 4 && (y == 1 || y == 8))
            {
                auto &delta_list_cross_only = castle_delta_cross_only_list_map[x][y];
                for (const Delta &delta : q_directions)
                {
                    auto &oth_list = castle_route_list_map[x + delta.x][y + delta.y];
                    auto &oth_delta_list_cross_only = castle_delta_cross_only_list_map[x + delta.x][y + delta.y];
                    list.emplace_back(x + delta.x, y + delta.y);
                    oth_list.emplace_back(x - delta.x, y - delta.y);

                    delta_list_cross_only.emplace_back(+delta.x, +delta.y);
                    oth_delta_list_cross_only.emplace_back(-delta.x, -delta.y);
                }
            }
        }
    }
}

export Board *get_board()
{
    return new Board;
}
