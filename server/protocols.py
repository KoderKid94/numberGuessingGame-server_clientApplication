class Protocols:
    # this file will serve as the protocol messages sent between our clients and server
    # these messages will serve as command signals that help coordinate the logic of both sides

    # the Response class provides messages, server --> clients
    class Response:
        NICKNAME = "protocol.request_nickName"
        ANSWER_VALID = "protocol.answer_valid"
        ANSWER_INVALID = "protocol.answer_invalid"
        OPPONENT = "protocol.opponent"
        OPPONENT_EXITED = "protocol.opponent_exited"
        START = "protocol.start"
        WINNER = "protocol.winner"

    # the Request class provides messages, clients --> server
    class Request:
        NICKNAME = "protocol.send_nickName"
        ANSWER = "protocol.answer"
        LEAVE_SERVER = "protocol.leave_server"
