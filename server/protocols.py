class Protocols:
    # this file will serve as the protocol messages sent between our clients and server
    # these messages will serve as command signals that help coordinate the logic of both sides

    # the Response class provides messages, server --> clients
    class Response:
        NICKNAME = "Protocols.request_nickName"
        ANSWER_VALID = "Protocols.answer_valid"
        ANSWER_INVALID = "Protocols.answer_invalid"
        OPPONENT = "Protocols.opponent"
        OPPONENT_LEFT = "Protocols.opponent_left"
        START = "Protocols.start"
        WINNER = "Protocols.winner"

    # the Request class provides messages, clients --> server
    class Request:
        NICKNAME = "Protocols.send_nickName"
        ANSWER = "Protocols.answer"
        LEAVE_SERVER = "Protocols.leave_server"
