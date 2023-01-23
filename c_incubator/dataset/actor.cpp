#include "actor.h"
#include "actor_type.h"

static std::vector<Pos> four_directions = {
    Pos{0, +1}, Pos{0, -1},
    Pos{+1, 0}, Pos{-1, 0},
};

static std::vector<Pos> crossing_directions = {
    Pos{+1, +1}, Pos{-1, -1},
    Pos{+1, -1}, Pos{-1, +1},
};

std::vector<Pos> actor_move_cases_as_king_or_duke(const int& actor_code, const Board& board, const Pos& pos)
{
    std::vector<Pos> result{};

    std::vector<Pos> move_directions { four_directions };
    if (board_is_on_ears_of_palaces(pos) || board_is_on_center_of_palaces(pos))
        move_directions.insert(move_directions.end(), crossing_directions.begin(), crossing_directions.end());

    for (const auto& d1 : move_directions)
    {
        Pos new_pos {
            pos.x + d1.x,
            pos.y + d1.y,
        };

        if (board_is_on_palace(new_pos))
        {
            const auto other = board_get_actor(board, new_pos);
            if (actor_get_actor_type(other) == 0 ||
                actor_is_red(actor_code) != actor_is_red(other)
            ) {
                result.push_back(new_pos);
            }
        }
    }

    return result;
}

std::vector<Pos> actor_move_cases_as_kart(const int& actor_code, const Board& board, const Pos& pos)
{
    std::vector<Pos> result{};

    std::vector<Pos> move_directions { four_directions };
    move_directions.insert(move_directions.end(), crossing_directions.begin(), crossing_directions.end());

    for (const auto& d1 : move_directions)
    {
        bool is_crossing = (d1.x != 0 && d1.y != 0);
        if (
            is_crossing && !(
                board_is_on_ears_of_palaces(pos) ||
                board_is_on_center_of_palaces(pos)
            )
        )
            continue;

        for (int c = 1; c <= 10; ++c)
        {
            Pos new_pos {
                pos.x + d1.x * c,
                pos.y + d1.y * c,
            };

            if (!board_is_pos_in_board(new_pos)) break;
            if (is_crossing && (!board_is_on_palace(new_pos))) break;

            const auto& other = board_get_actor(board, new_pos);
            if (actor_get_actor_type(other) == 0 ||
                actor_is_red(actor_code) != actor_is_red(other)
            ) {
                result.push_back(new_pos);
            }
        }
    }

    return result;
}

std::vector<Pos> actor_move_cases_as_horse(const int& actor_code, const Board& board, const Pos& pos)
{
    std::vector<Pos> result{};

    std::vector<Pos> move_directions { four_directions };

    for (const auto& d1 : move_directions)
    {
        Pos road_1 {
            pos.x + d1.x,
            pos.y + d1.y
        };

        if (!board_is_pos_in_board(road_1)) continue;
        const auto& other_1 = board_get_actor(board, road_1);
        if (actor_get_actor_type(other_1) != 0) continue;

        std::vector<Pos> tilted_directions {};
        if (d1.x == 0)
        {
            tilted_directions.push_back(Pos{-1, 0});
            tilted_directions.push_back(Pos{+1, 0});
        }
        else
        {
            tilted_directions.push_back(Pos{0, -1});
            tilted_directions.push_back(Pos{0, +1});
        }

        for (const auto& d2 : tilted_directions) {
            Pos final {
                road_1.x + d1.x + d2.x,
                road_1.y + d1.y + d2.y,
            };

            if (!board_is_pos_in_board(final)) continue;

            const auto& other_f = board_get_actor(board, final);
            if (actor_get_actor_type(other_f) == 0 ||
                actor_is_red(actor_code) != actor_is_red(other_f)
            ) {
                result.push_back(final);
            }

        }
    }

    return result;
}

std::vector<Pos> actor_move_cases_as_elephant(const int& actor_code, const Board& board, const Pos& pos)
{
    std::vector<Pos> result{};

    std::vector<Pos> move_directions { four_directions };

    for (const auto& d1 : move_directions)
    {
        Pos road_1 {
            pos.x + d1.x,
            pos.y + d1.y
        };

        if (!board_is_pos_in_board(road_1)) continue;
        const auto& other_1 = board_get_actor(board, road_1);
        if (actor_get_actor_type(other_1) != 0) continue;

        std::vector<Pos> tilted_directions {};
        if (d1.x == 0)
        {
            tilted_directions.push_back(Pos{-1, 0});
            tilted_directions.push_back(Pos{+1, 0});
        }
        else
        {
            tilted_directions.push_back(Pos{0, -1});
            tilted_directions.push_back(Pos{0, +1});
        }

        for (const auto& d2 : tilted_directions) {
            Pos road_2 {
                road_1.x + d1.x + d2.x,
                road_1.y + d1.y + d2.y,
            };

            if (!board_is_pos_in_board(road_2)) continue;
            const auto& other_2 = board_get_actor(board, road_2);
            if (actor_get_actor_type(other_2) != 0) continue;


            Pos final {
                road_2.x + d1.x + d2.x,
                road_2.y + d1.y + d2.y,
            };

            if (!board_is_pos_in_board(final)) continue;

            const auto& other_f = board_get_actor(board, final);
            if (actor_get_actor_type(other_f) == 0 ||
                actor_is_red(actor_code) != actor_is_red(other_f)
            ) {
                result.push_back(final);
            }

        }
    }

    return result;
}


std::vector<Pos> actor_move_cases_as_cannon(const int& actor_code, const Board& board, const Pos& pos)
{
    std::vector<Pos> result{};

    std::vector<Pos> move_directions { four_directions };
    move_directions.insert(move_directions.end(), crossing_directions.begin(), crossing_directions.end());

    for (const auto& d1 : move_directions)
    {
        bool is_crossing = (d1.x != 0 && d1.y != 0);
        bool meet_non_cannon = false;

        if (
            is_crossing && !(
                board_is_on_ears_of_palaces(pos) ||
                board_is_on_center_of_palaces(pos)
            )
        )
            continue;

        for (int c = 1; c <= 10; ++c)
        {
            Pos new_pos {
                pos.x + d1.x * c,
                pos.y + d1.y * c,
            };

            if (!board_is_pos_in_board(new_pos)) break;
            if (is_crossing && (!board_is_on_palace(new_pos))) break;

            const auto& other = board_get_actor(board, new_pos);

            if (meet_non_cannon)
            {
                if (actor_get_actor_type(other) == 0)
                {
                    result.push_back(new_pos);
                }
                else
                {
                    if ( actor_is_red(actor_code) != actor_is_red(other) &&
                         actor_get_actor_type(other) != ACTOR_TYPE_CANNON
                    ) {
                        result.push_back(new_pos);
                    }
                    break;
                }
            }
            else
            {
                if (actor_get_actor_type(other) == ACTOR_TYPE_CANNON)
                {
                    break;
                }
                else if (actor_get_actor_type(other) != 0)
                {
                    meet_non_cannon = true;
                }
            }
        }
    }

    return result;
}

std::vector<Pos> actor_move_cases_as_army(const int& actor_code, const Board& board, const Pos& pos)
{
    std::vector<Pos> result{};

    bool is_red = actor_is_red(actor_code);

    for (const auto& d1 : four_directions)
    {
        if (is_red)
        {
            if (d1.y > 0) continue;
        }
        else
        {
            if (d1.y < 0) continue;
        }
        Pos new_pos {pos.x + d1.x, pos.y + d1.y};

        if (board_is_pos_in_board(new_pos))
        {
            const auto& other = board_get_actor(board, new_pos);

            if (actor_get_actor_type(other) == 0 ||
                actor_is_red(actor_code) != actor_is_red(other)
            ) {
                result.push_back(new_pos);
            }
        }
    }

    return result;
}

std::vector<Pos> actor_move_cases(const int& actor_code, const Board& board, const Pos& pos)
{
    int actor_type = actor_get_actor_type(actor_code);
    int is_red = actor_is_red(actor_code);

    if (actor_type == ACTOR_TYPE_KING)
        return actor_move_cases_as_king_or_duke(actor_code, board, pos);
    else if (actor_type == ACTOR_TYPE_KART)
        return actor_move_cases_as_kart(actor_code, board, pos);
    else if (actor_type == ACTOR_TYPE_HORSE)
        return actor_move_cases_as_horse(actor_code, board, pos);
    else if (actor_type == ACTOR_TYPE_ELEPHANT)
        return actor_move_cases_as_elephant(actor_code, board, pos);
    else if (actor_type == ACTOR_TYPE_CANNON)
        return actor_move_cases_as_cannon(actor_code, board, pos);
    else if (actor_type == ACTOR_TYPE_DUKE)
        return actor_move_cases_as_king_or_duke(actor_code, board, pos);
    else if (actor_type == ACTOR_TYPE_ARMY)
        return actor_move_cases_as_army(actor_code, board, pos);

    return std::vector<Pos>{};
}

