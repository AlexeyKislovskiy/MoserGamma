from detail.detail import Detail
from statistic.event.abstract_event import Event


class GammaAlgorithmEvent(Event):
    EVENT_TYPE = 'Gamma algorithm event'

    """
    Base class for events that occur during the execution of the gamma algorithm.

    Attributes:
        gamma (float): The gamma parameter.
        lrp (Detail): The Large Rectangular Piece (LRP).
        stripe (Detail): The current stripe, or None if there is no current stripe.
        stripe_first_detail_index (int): The index of the first detail in the current stripe.
        is_stripe_horizontal (bool): Whether the stripe is horizontal (the size along the x-axis is greater than
            along the y-axis).
        last_placed_index (int): The index of the last placed detail.
        endpoints_placed (int): The number of endpoints placed.
        stripe_from (str): Type of the detail from which the current stripe was formed.
        detail (tuple[float, float]): The current detail to be placed. A tuple represents the width and height
            of the detail. The width here means the side on which the detail will be placed.
        placed_details (list[Detail]): A list of placed details.
    """

    def __init__(self, gamma: float, lrp: Detail, stripe: Detail,
                 stripe_first_detail_index: int, is_stripe_horizontal: bool, last_placed_index: int,
                 endpoints_placed: int, stripe_from: str, detail: tuple[float, float],
                 placed_details: list[Detail]):
        """
        Initialize a GammaAlgorithmEvent object.

        :param gamma: The gamma parameter.
        :param lrp: The Large Rectangular Piece (LRP).
        :param stripe: The current stripe, or None if there is no current stripe.
        :param stripe_first_detail_index: The index of the first detail in the current stripe.
        :param is_stripe_horizontal: Whether the stripe is horizontal (the size along the x-axis is greater than
            along the y-axis).
        :param last_placed_index: The index of the last placed detail.
        :param endpoints_placed: The number of endpoints placed.
        :param stripe_from: The detail from which the current stripe was formed.
        :param detail: The current detail to be placed. A tuple represents the width and height of the detail.
            The width here means the side on which the detail will be placed.
        :param placed_details: A list of placed details.
        """
        self.gamma = gamma
        self.lrp = lrp
        self.stripe = stripe
        self.stripe_first_detail_index = stripe_first_detail_index
        self.is_stripe_horizontal = is_stripe_horizontal
        self.last_placed_index = last_placed_index
        self.endpoints_placed = endpoints_placed
        self.stripe_from = stripe_from
        self.detail = detail
        self.placed_details = placed_details

    def get_event_type(self) -> str:
        """
        Returns the type of the event as a string.

        :return: The type of the event.
        """
        return self.EVENT_TYPE


class GammaAlgorithmAfterDetailPlacedEvent(GammaAlgorithmEvent):
    EVENT_TYPE = 'Gamma algorithm after detail placed event'

    """
    Event that occurs after placing a new detail during the execution of the gamma algorithm.

    Attributes:
        gamma (float): The gamma parameter.
        lrp (Detail): The Large Rectangular Piece (LRP).
        stripe (Detail): The current stripe, or None if there is no current stripe.
        stripe_first_detail_index (int): The index of the first detail in the current stripe.
        is_stripe_horizontal (bool): Whether the stripe is horizontal (the size along the x-axis is greater than
            along the y-axis).
        last_placed_index (int): The index of the last placed detail.
        endpoints_placed (int): The number of endpoints placed.
        stripe_from (str): Type of the detail from which the current stripe was formed.
        detail (tuple[float, float]): The current detail to be placed. A tuple represents the width and height
            of the detail. The width here means the side on which the detail will be placed.
        placed_details (list[Detail]): A list of placed details.
        placed_detail (Detail): The new placed detail.
        normal_box (Detail): The normal box created after placing the detail.
        endpoint (Detail): The endpoint created after placing the detail.
    """

    def __init__(self, gamma: float, lrp: Detail, stripe: Detail, stripe_first_detail_index: int,
                 is_stripe_horizontal: bool, last_placed_index: int, endpoints_placed: int, stripe_from: str,
                 detail: tuple[float, float], placed_details: list[Detail], placed_detail: Detail, normal_box: Detail,
                 endpoint: Detail):
        """
        Initialize a GammaAlgorithmDetailPlacedEvent object.

        :param gamma: The gamma parameter.
        :param lrp: The Large Rectangular Piece (LRP).
        :param stripe: The current stripe, or None if there is no current stripe.
        :param stripe_first_detail_index: The index of the first detail in the current stripe.
        :param is_stripe_horizontal: Whether the stripe is horizontal (the size along the x-axis is greater than
            along the y-axis).
        :param last_placed_index: The index of the last placed detail.
        :param endpoints_placed: The number of endpoints placed.
        :param stripe_from: The detail from which the current stripe was formed.
        :param detail: The current detail to be placed. A tuple represents the width and height of the detail.
            The width here means the side on which the detail will be placed.
        :param placed_details: A list of placed details.
        :param placed_detail: The new placed detail.
        :param normal_box: The normal box created after placing the detail.
        :param endpoint: The endpoint created after placing the detail.
        """
        super().__init__(gamma, lrp, stripe, stripe_first_detail_index, is_stripe_horizontal, last_placed_index,
                         endpoints_placed, stripe_from, detail, placed_details)
        self.placed_detail = placed_detail
        self.normal_box = normal_box
        self.endpoint = endpoint

    def get_event_type(self) -> str:
        """
        Returns the type of the event as a string.

        :return: The type of the event.
        """
        return self.EVENT_TYPE


class GammaAlgorithmBeforeLRPCutEvent(GammaAlgorithmEvent):
    EVENT_TYPE = 'Gamma algorithm before LRP cut event'

    """
    Event that occurs before cutting a stripe from the LRP during the execution of the gamma algorithm.

    Attributes:
        gamma (float): The gamma parameter.
        lrp (Detail): The Large Rectangular Piece (LRP).
        stripe (Detail): The current stripe, or None if there is no current stripe.
        stripe_first_detail_index (int): The index of the first detail in the current stripe.
        is_stripe_horizontal (bool): Whether the stripe is horizontal (the size along the x-axis is greater than
            along the y-axis).
        last_placed_index (int): The index of the last placed detail.
        endpoints_placed (int): The number of endpoints placed.
        stripe_from (str): Type of the detail from which the current stripe was formed.
        detail (tuple[float, float]): The current detail to be placed. A tuple represents the width and height
            of the detail. The width here means the side on which the detail will be placed.
        placed_details (list[Detail]): A list of placed details.
    """

    def get_event_type(self) -> str:
        """
        Returns the type of the event as a string.

        :return: The type of the event.
        """
        return self.EVENT_TYPE


class GammaAlgorithmAfterLRPCutEvent(GammaAlgorithmEvent):
    EVENT_TYPE = 'Gamma algorithm after LRP cut event'

    """
    Event that occurs after cutting a stripe from the LRP during the execution of the gamma algorithm.

    Attributes:
        gamma (float): The gamma parameter.
        lrp (Detail): The Large Rectangular Piece (LRP).
        stripe (Detail): The current stripe, or None if there is no current stripe.
        stripe_first_detail_index (int): The index of the first detail in the current stripe.
        is_stripe_horizontal (bool): Whether the stripe is horizontal (the size along the x-axis is greater than
            along the y-axis).
        last_placed_index (int): The index of the last placed detail.
        endpoints_placed (int): The number of endpoints placed.
        stripe_from (str): Type of the detail from which the current stripe was formed.
        detail (tuple[float, float]): The current detail to be placed. A tuple represents the width and height
            of the detail. The width here means the side on which the detail will be placed.
        placed_details (list[Detail]): A list of placed details.
    """

    def get_event_type(self) -> str:
        """
        Returns the type of the event as a string.

        :return: The type of the event.
        """
        return self.EVENT_TYPE
