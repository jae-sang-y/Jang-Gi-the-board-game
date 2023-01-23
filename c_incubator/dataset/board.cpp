#include "board.h"
#include "actor.h"

std::list<ActorWithPosition> board_foreach_actors(const Board& board)
{
    std::list<ActorWithPosition> result{};
    for (int x = 0; x < 9; ++x)
    {
        for (int y = 0; y < 10; ++y)
        {
            int actor_code = board.actor_code[x][y];
            if (actor_get_actor_type(actor_code) != 0)
            {
                ActorWithPosition awp{};
                awp.actor_code = actor_code;
                awp.x = x;
                awp.y = y;

                result.push_back(awp);
            }
        }
    }
    return result;
}
