void Board::init()
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

bool Board::on_castle(const Pos &pos)
{
    return 3 <= pos.x && pos.x <= 5 &&
           ((0 <= pos.y && pos.y <= 2) ||
            (7 <= pos.y && pos.y <= 9));
}

bool Board::is_possible_pos(const Pos &pos)
{
    return 0 <= pos.x && pos.x < map_w &&
           0 <= pos.y && pos.y < map_h;
}

bool Board::is_empty_pos(const Pos &pos)
{
    return actors[pos.x][pos.y] == NULL;
}

bool Board::is_enemy_pos(const Pos &pos, const int &team_code)
{
    return !(actors[pos.x][pos.y] & team_code);
}

bool Board::is_empty_or_edible(const Pos &pos, const int &team_code)
{
    return is_possible_pos(pos) && (is_empty_pos(pos) || is_enemy_pos(pos, team_code));
}

void Board::get_possible_decisions(std::vector<Decision> &result, const Pos &old_pos)
{
    const int &actor_code = actors[old_pos.x][old_pos.y];
    const int ac = GET_ACTCODE(actor_code);
    const int tc = GET_TEAMCODE(actor_code);
    Pos new_pos;
    int x, y;

    switch (ac)
    {
    case ac_footman:
        new_pos.x = old_pos.x + 1;
        new_pos.y = old_pos.y;
        if (is_empty_or_edible(new_pos, tc))
            result.emplace_back(old_pos, new_pos);

        new_pos.x = old_pos.x - 1;
        if (is_empty_or_edible(new_pos, tc))
            result.emplace_back(old_pos, new_pos);

        new_pos.x = old_pos.x;
        if (tc == tc_north)
            new_pos.y = old_pos.y + 1;
        else
            new_pos.y = old_pos.y - 1;
        if (is_empty_or_edible(new_pos, tc))
            result.emplace_back(old_pos, new_pos);

        if (on_castle(old_pos))
        {
            for (const Delta &delta : castle_delta_cross_only_list_map[old_pos.x][old_pos.y])
            {
                if (delta.y > 0 && tc == tc_north ||
                    delta.y < 0 && tc == tc_south)
                {
                    new_pos = old_pos + delta;
                    result.emplace_back(old_pos, new_pos);
                }
            }
        }
        break;
    case ac_horse:
        for (const auto &horse_direction : horse_directions)
        {
            for (x = 0; x < horse_directions_depth; ++x)
            {
                new_pos = old_pos + horse_direction[x];
                if (!is_empty_or_edible(new_pos, tc))
                {
                    x = 0xFF;
                    break;
                }
            }
            if (x == 0xFF)
                continue;
            result.emplace_back(old_pos, new_pos);
        }
        break;
    case ac_elephant:
        for (const auto &elephant_direction : elephant_directions)
        {
            for (x = 0; x < elephant_directions_depth; ++x)
            {
                new_pos = old_pos + elephant_direction[x];
                if (!is_empty_or_edible(new_pos, tc))
                {
                    x = 0xFF;
                    break;
                }
            }
            if (x == 0xFF)
                continue;
            result.emplace_back(old_pos, new_pos);
        }
        break;
    case ac_cart:
        for (const Delta &delta : q_directions)
        {
            for (x = 1;; ++x)
            {
                new_pos = old_pos + delta * x;
                if (!is_empty_or_edible(new_pos, tc))
                    break;
                result.emplace_back(old_pos, new_pos);
                if (!is_empty_pos(new_pos))
                    break;
            }
        }
        if (on_castle(old_pos))
        {
            for (const Delta &delta : castle_delta_cross_only_list_map[old_pos.x][old_pos.y])
            {
                for (x = 1;; ++x)
                {
                    new_pos = old_pos + delta * x;
                    if (!is_empty_or_edible(new_pos, tc) || !on_castle(new_pos))
                        break;
                    result.emplace_back(old_pos, new_pos);
                    if (!is_empty_pos(new_pos))
                        break;
                }
            }
        }
        break;
    case ac_artillery:
        for (const Delta &delta : q_directions)
        {
            y = 0;
            for (x = 1;; ++x)
            {
                new_pos = old_pos + delta * x;
                if (!is_possible_pos(new_pos))
                    break;

                if (is_empty_pos(new_pos))
                {
                    if (y == 1)
                        result.emplace_back(old_pos, new_pos);
                    continue;
                }

                if (GET_ACTCODE(this->actors[new_pos.x][new_pos.y]) == ac_artillery)
                    break;

                y += 1;

                if (y == 2)
                    break;

                result.emplace_back(old_pos, new_pos);
            }
        }
        if (on_castle(old_pos))
        {
            for (const Delta &delta : castle_delta_cross_only_list_map[old_pos.x][old_pos.y])
            {
                y = 0;
                for (x = 1;; ++x)
                {
                    new_pos = old_pos + delta * x;
                    if (!is_empty_or_edible(new_pos, tc) || !on_castle(new_pos))
                        break;

                    if (is_empty_pos(new_pos))
                    {
                        if (y == 1)
                            result.emplace_back(old_pos, new_pos);
                        continue;
                    }

                    if (GET_ACTCODE(this->actors[new_pos.x][new_pos.y]) == ac_artillery)
                        break;

                    y += 1;

                    if (y == 2)
                        break;

                    result.emplace_back(old_pos, new_pos);
                }
            }
        }
        break;
    case ac_king:
    case ac_bishop:
        for (const Pos &in_castle_pos : castle_route_list_map[old_pos.x][old_pos.y])
        {
            if (is_empty_or_edible(in_castle_pos, tc))
            {
                result.emplace_back(old_pos, in_castle_pos);
            }
        }
        break;
    default:
        break;
    }
}

bool Board::is_ended_game()
{
    int king_count[2] = {0, 0};
    for (int x = 0; x < map_w; ++x)
    {
        for (int y = 0; y < map_h; ++y)
        {
            const int &actor = actors[x][y];
            if (actor & ac_king)
            {
                if (actor & tc_south)
                    king_count[1] += 1;
                else if (actor & tc_north)
                    king_count[0] += 1;
            }
        }
    }

    if (king_count[0] == 0 || king_count[1] == 0)
        return true;
    else
        return false;
}

Board Board::sub_board(const Decision &decision)
{
    Board result = (*this);
    result.actors[decision._new.x][decision._new.y] =
        this->actors[decision._old.x][decision._old.y];
    result.actors[decision._old.x][decision._old.y] = NULL;
    if (this->turn_own_team & tc_north)
        result.turn_own_team = tc_south;
    else
        result.turn_own_team = tc_north;

    return result;
}

void pre_init()
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