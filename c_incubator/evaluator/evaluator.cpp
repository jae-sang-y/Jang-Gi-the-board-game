#include "evaluator.h"
#include "../dataset/board.h"
#include "../dataset/actor.h"
#include "../dataset/actor_type.h"
#include "../decision_maker/board_util.h"

int evaluator_basic(const Board& board)
{
    int total_value = 0;
    for (int y = 0; y < 10; ++y)
    {
        for (int x = 0; x < 9; ++x)
        {
            int value = 0;
            int actor_code = board.actor_code[x][y];
            int actor_type = actor_get_actor_type(actor_code);
            if (actor_type == ACTOR_TYPE_KING)
                value = 10000;
            else if (actor_type == ACTOR_TYPE_KART)
                value = 13;
            else if (actor_type == ACTOR_TYPE_CANNON)
                value = 7;
            else if (actor_type == ACTOR_TYPE_HORSE)
                value = 5;
            else if (actor_type == ACTOR_TYPE_ELEPHANT)
                value = 3;
            else if (actor_type == ACTOR_TYPE_DUKE)
                value = 3;
            else if (actor_type == ACTOR_TYPE_ARMY)
                value = 2;
            if (actor_is_red(actor_code))
            {
                total_value += value;
            }
            else
            {
                total_value -= value;
            }
        }
    }
    return total_value;
}
