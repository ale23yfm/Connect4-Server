# Columns errors
class ColumnFullError(Exception):
    pass

class InvalidColumn(Exception):
    pass

# Rows errors
class RowFullError(Exception):
    pass

# Pieces errors
class InvalidPiece(Exception):
    pass

# Game errors
class GameServiceError(Exception):
    pass