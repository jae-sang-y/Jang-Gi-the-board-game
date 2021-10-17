#include <Python.h>
#include <vector>

#define export extern "C" __declspec(dllexport)

constexpr int tc_north = 0x00010000;
constexpr int tc_south = 0x00020000;
#define IS_NORTH_TEAM(x) (x & tc_north)
#define IS_SOUTH_TEAM(x) (x & tc_south)

constexpr int ac_king = 0b00000001;
constexpr int ac_cart = 0b00000010;
constexpr int ac_horse = 0b00000100;
constexpr int ac_elephant = 0b00001000;
constexpr int ac_artillery = 0b00010000;
constexpr int ac_bishop = 0b00100000;
constexpr int ac_footman = 0b01000000;

constexpr int map_w = 9;
constexpr int map_h = 10;

struct Pos
{
    int x;
    int y;
};
std::vector<Pos> castle_route_list_map[map_w][map_h] = {};
std::vector<Pos> castle_route_cross_only_list_map[map_w][map_h] = {};

struct Decision
{
    Pos _old;
    Pos _new;
    int act_code;
};

struct Board
{
    int actors[map_w][map_h] = {};
    int turn_own_team = 0;

    Board()
    {
        actors[0][0] = tc_north || ac_cart;
        actors[1][0] = tc_north || ac_horse;
        actors[2][0] = tc_north || ac_elephant;
        actors[3][0] = tc_north || ac_bishop;
        actors[4][1] = tc_north || ac_king;

        actors[1][2] = tc_north || ac_artillery;
        actors[0][3] = tc_north || ac_footman;
        actors[2][3] = tc_north || ac_footman;
        actors[4][3] = tc_north || ac_footman;

        for (int x = 0; x <= 4; ++x)
        {
            for (int y = 0; y <= 3; ++y)
            {
                if (actors[x][y])
                {
                    actors[map_w - 1 - x][y] = actors[x][y];
                    actors[map_w - 1 - x][map_h - 1 - y] = actors[x][y] & (~tc_north) | tc_south;
                    actors[map_w][map_h - 1 - y] = actors[map_w - 1 - x][map_h - 1 - y];
                }
            }
        }
        turn_own_team = tc_north;
    }

    bool on_castle(const Pos &pos)[[noexcept]]
    {
        return 3 <= pos.x && pos.x <= 5 &&
               ((0 <= pos.y && pos.y <= 2) ||
                (7 <= pos.y && pos.y <= 9));
    }

    bool is_possible_pos(const Pos &pos)[[noexcept]]
    {
        return 0 <= pos.x && pos.x < map_w &&
               0 <= pos.y && pos.y < map_h;
    }

    bool is_empty_pos(const Pos &pos)[[noexcept]]
    {
        return actors[pos.x][pos.y] == NULL;
    }

    bool is_enemy_pos(const Pos &pos, const int &team_code)[[noexcept]]
    {
        return !(actors[pos.x][pos.y] & team_code);
    }

    bool is_movable_or_edible(const Pos &pos, const int &team_code)
    {
        return is_empty_pos(pos) || is_enemy_pos(pos, team_code);
    }
};

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
                auto &list_cross_only = castle_route_cross_only_list_map[x][y];
                for (const Pos &pos : {
                         Pos{-1 + 1},
                         Pos{-1 - 1},
                         Pos{+1 + 1},
                         Pos{+1 - 1}})
                {
                    auto &oth_list = castle_route_list_map[x + pos.x][y + pos.y];
                    auto &oth_list_cross_only = castle_route_cross_only_list_map[x + pos.x][y + pos.y];
                    list.push_back(Pos{+pos.x, +pos.y});
                    oth_list.push_back(Pos{-pos.x, -pos.y});

                    list_cross_only.push_back(Pos{+pos.x, +pos.y});
                    oth_list_cross_only.push_back(Pos{-pos.x, -pos.y});
                }
            }
        }
    }
}

export PyObject *get_str()
{
    char str[] = "Hello world";
    return PyUnicode_FromString(str);
}