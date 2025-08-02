import numpy as np
from constants import U, D, L, R, F, B

def create_solved_cube():
    """Creates a 6x3x3 numpy array representing a solved cube."""
    cube = np.zeros((6, 3, 3), dtype=int)
    for i in range(6):
        cube[i] = np.full((3, 3), i, dtype=int)
    return cube

def get_inverse_move(move):
    """Returns the inverse of a given move (e.g., R -> R', F' -> F)."""
    if "'" in move:
        return move[0]
    else:
        return move + "'"

def apply_move(cube, move):
    """Applies a single move to the cube state."""
    c = cube.copy()
    if "'" in move:
        move, rotations = move[0], 3
    else:
        rotations = 1

    for _ in range(rotations):
        if move == 'U':
            c[U] = np.rot90(c[U], k=-1); temp = c[F,0,:].copy(); c[F,0,:]=c[R,0,:]; c[R,0,:]=c[B,0,:]; c[B,0,:]=c[L,0,:]; c[L,0,:]=temp
        elif move == 'D':
            c[D] = np.rot90(c[D], k=-1); temp = c[F,2,:].copy(); c[F,2,:]=c[L,2,:]; c[L,2,:]=c[B,2,:]; c[B,2,:]=c[R,2,:]; c[R,2,:]=temp
        elif move == 'R':
            c[R] = np.rot90(c[R], k=-1); temp = c[U,:,2].copy(); c[U,:,2]=c[F,:,2]; c[F,:,2]=c[D,:,2]; c[D,:,2]=np.flip(c[B,:,0]); c[B,:,0]=np.flip(temp)
        elif move == 'L':
            c[L] = np.rot90(c[L], k=-1); temp = c[U,:,0].copy(); c[U,:,0]=np.flip(c[B,:,2]); c[B,:,2]=np.flip(c[D,:,0]); c[D,:,0]=c[F,:,0]; c[F,:,0]=temp
        elif move == 'F':
            c[F] = np.rot90(c[F], k=-1); temp = c[U,2,:].copy(); c[U,2,:]=np.flip(c[L,:,2]); c[L,:,2]=c[D,0,:]; c[D,0,:]=np.flip(c[R,:,0]); c[R,:,0]=temp
        elif move == 'B':
            c[B] = np.rot90(c[B], k=-1); temp = c[U,0,:].copy(); c[U,0,:]=c[R,:,2]; c[R,:,2]=np.flip(c[D,2,:]); c[D,2,:]=c[L,:,0]; c[L,:,0]=np.flip(temp)
    return c
