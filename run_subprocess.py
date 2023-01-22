import sys

if __name__ == '__main__':
    subproc_name = sys.argv[1]
    subproc_args = sys.argv[2:]
    # print('subproc_name:', subproc_name)
    # print('subproc_args:', subproc_args)

    if subproc_name == 'decision_maker/minimax':
        from decision_maker.minimax import Minimax

        Minimax.parallel_execute(*subproc_args)
    exit(0)