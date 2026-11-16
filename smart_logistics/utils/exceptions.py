
class ShipmentNotFoundError(Exception):
    pass


class CustomerNotFoundError(Exception):
    pass


class InvalidStatusTransitionError(Exception):
    pass


class AgentUnavailableError(Exception):
    pass


class DeliveryAttemptLimitError(Exception):
    pass


class InvalidParcelError(Exception):
    pass
