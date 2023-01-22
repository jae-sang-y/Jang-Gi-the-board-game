#include <Python.h>
#include <vector>
#include <array>
#include <utility>
#include <structmember.h>

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

#define GET_TEAMCODE(x) (x & 0x0003000)
#define GET_ACTCODE(x) (x & 0x00000FF)

struct Delta
{
    int x;
    int y;
    Delta &&operator*(const int &n) const
    {
        Delta result;
        result.x = this->x * n;
        result.y = this->y * n;
        return std::move(result);
    }
};

struct Pos
{
    int x;
    int y;
    Pos operator+(const Delta &delta) const
    {
        Pos result;
        result.x = this->x + delta.x;
        result.y = this->y + delta.y;
        return result;
    }
};

std::vector<Pos> castle_route_list_map[map_w][map_h] = {};
std::vector<Delta> castle_delta_cross_only_list_map[map_w][map_h] = {};
constexpr std::array<const Delta, 4> q_directions = {
    Delta{-1 + 1},
    Delta{-1 - 1},
    Delta{+1 + 1},
    Delta{+1 - 1}};

constexpr int horse_directions_count = 8;
constexpr int horse_directions_depth = 2;
constexpr std::array<std::array<Delta, horse_directions_depth>, horse_directions_count> horse_directions = {
    std::array<Delta, horse_directions_depth>{Delta{+1, +0}, Delta{+2, +1}},
    std::array<Delta, horse_directions_depth>{Delta{+1, +0}, Delta{+2, -1}},
    std::array<Delta, horse_directions_depth>{Delta{-1, +0}, Delta{-2, +1}},
    std::array<Delta, horse_directions_depth>{Delta{-1, +0}, Delta{-2, -1}},
    std::array<Delta, horse_directions_depth>{Delta{+0, -1}, Delta{-1, -2}},
    std::array<Delta, horse_directions_depth>{Delta{+0, -1}, Delta{+1, -2}},
    std::array<Delta, horse_directions_depth>{Delta{+0, +1}, Delta{-1, +2}},
    std::array<Delta, horse_directions_depth>{Delta{+0, +1}, Delta{+1, +2}},
};

constexpr int elephant_directions_count = 8;
constexpr int elephant_directions_depth = 3;
constexpr std::array<std::array<Delta, elephant_directions_depth>, elephant_directions_count> elephant_directions = {
    std::array<Delta, elephant_directions_depth>{Delta{+1, +0}, Delta{+2, +1}, Delta{+3, +2}},
    std::array<Delta, elephant_directions_depth>{Delta{+1, +0}, Delta{+2, -1}, Delta{+3, -2}},
    std::array<Delta, elephant_directions_depth>{Delta{-1, +0}, Delta{-2, +1}, Delta{-3, +2}},
    std::array<Delta, elephant_directions_depth>{Delta{-1, +0}, Delta{-2, -1}, Delta{-3, -2}},
    std::array<Delta, elephant_directions_depth>{Delta{+0, -1}, Delta{-1, -2}, Delta{-2, -3}},
    std::array<Delta, elephant_directions_depth>{Delta{+0, -1}, Delta{+1, -2}, Delta{+2, -3}},
    std::array<Delta, elephant_directions_depth>{Delta{+0, +1}, Delta{-1, +2}, Delta{-2, +3}},
    std::array<Delta, elephant_directions_depth>{Delta{+0, +1}, Delta{+1, +2}, Delta{+2, +3}},
};

struct Decision
{
    Pos _old;
    Pos _new;

    Decision() = default;
    Decision(const Pos &_old, const Pos &_new) : _old(_old), _new(_new){};
};
struct Board
{
    PyObject_HEAD;

    int actors[map_w][map_h] = {};
    int turn_own_team = tc_north;

    inline Board()
    {
        Board::init();
    }

    void init();
    bool on_castle(const Pos &pos);
    bool is_possible_pos(const Pos &pos);
    bool is_empty_pos(const Pos &pos);
    bool is_enemy_pos(const Pos &pos, const int &team_code);
    bool is_empty_or_edible(const Pos &pos, const int &team_code);
    void get_possible_decisions(std::vector<Decision> &result, const Pos &old_pos);
    bool is_ended_game();

    Board sub_board(const Decision &decision);
};

struct BoardIterator
{
    int *ptr = nullptr;
    int cnt = 0;
};

static void pre_init();
