class Protocols:
    # this file will serve as the protocol messages sent between our clients and server
    # these messages will serve as command signals that help coordinate the logic of both sides

    # the Response class provides messages, server --> client
    class Response:
        NICKNAME = "protocol.request_nickName"
        GUESS_VALID = "protocol.guess_valid"
        GUESS_TOO_LOW = "protocol.guess_too_low"
        GUESS_TOO_HIGH = "protocol.guess_too_high"
        OPPONENT = "protocol.opponent"
        OPPONENT_EXITED = "protocol.opponent_exited"
        START = "protocol.start"
        WINNER = "protocol.winner"
        CORRECT_NUMBER = "protocol.correct_number"
        GAME_BOUNDS = "protocol.bounds"

    # the Request class provides messages, client --> server
    class Request:
        NICKNAME = "protocol.send_nickName"
        GUESS = "protocol.answer"
        LEAVE_SERVER = "protocol.leave_server"
