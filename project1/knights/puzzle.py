from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave), # Must be knight or knave
    Not(And(AKnight, AKnave)), # Cannot be both

    Implication(AKnight, And(AKnight, AKnave)), # If A is a knight then what A says must be true
    Implication(AKnave, Not(And(AKnight, AKnave))) # if A is a knave then what A says must be false
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave), # Must be knight or knave
    Not(And(AKnight, AKnave)), # Cannot be both

    Or(BKnight, BKnave), # Must be knight or knave
    Not(And(BKnight, BKnave)), # Cannot be both

    Or(And(AKnight, BKnave), And(AKnave, BKnight)), # A and B cannot be the same kind

    Implication(AKnight, And(AKnave, BKnave)), # If A is a knight then what A says must be true
    Implication(AKnave, Not(And(AKnave, BKnave))) # if A is a knave then what A says must be false
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave), # Must be knight or knave
    Not(And(AKnight, AKnave)), # Cannot be both

    Or(BKnight, BKnave), # Must be knight or knave
    Not(And(BKnight, BKnave)), # Cannot be both

    Or(And(AKnight, BKnave), And(AKnave, BKnight)), # A and B cannot be the same kind

    Implication(AKnight, And(AKnight, BKnight)),
    Implication(AKnave, Not(And(AKnave, BKnave))),

    Implication(BKnight, And(BKnight, AKnave)),
    Implication(BKnave, Not(And(BKnight, AKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave), # Must be knight or knave
    Not(And(AKnight, AKnave)), # Cannot be both

    Or(BKnight, BKnave), # Must be knight or knave
    Not(And(BKnight, BKnave)), # Cannot be both

    Or(CKnight, CKnave), # Must be knight or knave
    Not(And(CKnight, CKnave)), # Cannot be bothy

    # A says either "I am a knight." or "I am a knave.", but you don't know which.
    Implication(AKnight, Or(AKnight, AKnave)), # If A is a knight then A is either a knight or knave
    Implication(AKnave, Not(Or(AKnight, AKnave))), # If A is a knave then A it not either a knight or knave

    # B says "A said 'I am a knave'."
    # If B is a knight then what A said is true so A is a knight
    Implication(BKnight, Implication(AKnight, AKnave)),

    # If B is a knaave then what A said is not true
    Implication(BKnave, Not(Implication(AKnight, AKnave))),

    # B says "C is a knave."
    Implication(BKnight, CKnave), # B is a knight when C is a knave
    Implication(BKnave, Not(CKnave)), # B is a knave when C is not a knave

    # C says "A is a knight."
    Implication(CKnight, AKnight), # C is a knight when A is a knight
    Implication(CKnave, Not(AKnight)) # C is a knave when A is not a knight
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
