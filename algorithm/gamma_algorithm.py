from functools import cmp_to_key
from sortedcontainers import SortedSet
from algorithm.abstract_algorithm import Algorithm, AlgorithmExecutionException
from detail.detail import Detail
from statistic.event.abstract_event import Event
from statistic.event.gamma_algorithm_events import GammaAlgorithmBeforeLRPCutEvent, GammaAlgorithmAfterLRPCutEvent, \
    GammaAlgorithmAfterDetailPlacedEvent
from statistic.listener.abstract_listener import StatisticListener


class GammaAlgorithm(Algorithm):
    """
    GammaAlgorithm is a specific implementation of the Algorithm class for placing details on a sheet.
    This algorithm uses the gamma parameter to determine the placement strategy, including the cutting of new stripes
    and handling of normal boxes and endpoints.

    Attributes:
        gamma (float): The gamma parameter.
        statistic_listeners (list[StatisticListener]): List of statistic listeners to track during the execution.
        update_placed_details (bool): A flag indicating whether the list of placed details should be updated.
            If set to True, the list of placed details will be updated, allowing visualization of the layout
            and calculations based on the state of all placed details. Setting it to False can expedite the
            calculating process by bypassing the need for continuous updates of placed details.
        boxes (SortedSet): Set of available boxes for placing details, sorted based on their minimum side length.
        lrp (Detail): The Large Rectangular Piece (LRP).
        stripe (Detail): The current stripe, or None if there is no current stripe.
        stripe_first_detail_index (int): The index of the first detail in the current stripe.
        is_stripe_horizontal (bool): Whether the stripe is horizontal (the size along the x-axis is greater than
            along the y-axis).
        last_placed_index (int): The index of the last placed detail.
        endpoints_placed (int): The number of endpoints placed.
        stripe_from (str): Type of the detail from which the current stripe was formed.
    """

    DETAIL_PREFIX = 'S'
    DETAIL_NAME = 'detail'
    NORMAL_BOX_PREFIX = 'B'
    NORMAL_BOX_TYPE_1_NAME = 'normal_box_1'
    NORMAL_BOX_TYPE_2_NAME = 'normal_box_2'
    ENDPOINT_PREFIX = 'Ep'
    ENDPOINT_TYPE_1_NAME = 'endpoint_1'
    ENDPOINT_TYPE_2_NAME = 'endpoint_2'
    LRP_PREFIX = 'LRP'
    LRP_NAME = 'lrp'

    def __init__(self, gamma: float, n0: int, statistic_listeners: list[StatisticListener] = None,
                 update_placed_details: bool = True):
        """
        Initialize the GammaAlgorithm with the specified parameters.

        :param gamma: The gamma parameter.
        :param n0: The index of the first detail to be placed.
        :param statistic_listeners: List of statistic listeners (optional).
        :param update_placed_details: A flag indicating whether the list of placed details should be updated.
            If set to True, the list of placed details will be updated, allowing visualization of the layout
            and calculations based on the state of all placed details. Setting it to False can expedite the
            calculating process by bypassing the need for continuous updates of placed details.
        """
        if statistic_listeners is None:
            statistic_listeners = []
        self.statistic_listeners = statistic_listeners
        self.gamma = gamma
        self.update_placed_details = update_placed_details
        self.boxes = SortedSet(key=cmp_to_key(self._detail_comparator))
        self.lrp = None
        self.stripe = None
        self.stripe_first_detail_index = n0 - 1
        self.is_stripe_horizontal = False
        self.last_placed_index = n0 - 1
        self.endpoints_placed = 1
        self.stripe_from = None

    def place_next(self, detail: tuple[float, float], placed_details: list[Detail]) -> None:
        """
        Place the next detail on the sheet using the gamma algorithm.

        :param detail: The current detail to be placed. A tuple represents the width and height of the detail.
            The width here means the side on which the detail will be placed.
        :param placed_details: List of details that have been placed so far.
        """
        self._check_if_lrp_none(placed_details)
        self._check_stripe_size(detail)
        self._choose_strip(detail, placed_details)
        self._place_detail_in_stripe(detail, placed_details)

    def _check_if_lrp_none(self, placed_details: list[Detail]) -> None:
        """
        Check if LRP is None and initialize it if necessary.
        If LRP is None, it initializes LRP as the first element of the placed_details list, which initially contains
        only an empty sheet. During other stages of the algorithm, situations where LRP is None should not occur.

        :param placed_details: List of details that have been placed so far.
        """
        if self.lrp is None:
            self.lrp = placed_details[0]

    def _check_stripe_size(self, detail: tuple[float, float]) -> None:
        """
        Check the size of the current stripe.
        If the stripe's size is insufficient to place a new detail with the required gap, the stripe is set to None
        and the remaining part of it is added as a new endpoint.

        :param detail: The current detail to be placed. A tuple represents the width and height of the detail.
            The width here means the side on which the detail will be placed.
        """
        if self.stripe is not None:
            required_gap = pow(1 / self.stripe_first_detail_index, self.gamma)
            total_length = detail[0] + required_gap
            if (self.is_stripe_horizontal and total_length > self.stripe.width) or \
                    (not self.is_stripe_horizontal and total_length > self.stripe.height):
                self.boxes.add(self.stripe)
                self.stripe = None
                self.endpoints_placed += 1

    def _choose_strip(self, detail: tuple[float, float], placed_details: list[Detail]) -> None:
        """
        Choose a new stripe for placing details if the current stripe is None.
        If suitable boxes exist, the widest one is chosen; otherwise, a stripe is cut from LRP. If it's impossible
        to cut a stripe, an exception is raised.

        :param detail: The current detail to be placed. A tuple represents the width and height of the detail.
            The width here means the side on which the detail will be placed.
        :param placed_details: List of details that have been placed so far.
        """
        if self.stripe is None:
            self.stripe_first_detail_index = self.last_placed_index + 1
            max_box_size = min(self.boxes[0].width, self.boxes[0].height) if len(self.boxes) > 0 else -1
            required_gap = pow(1 / self.stripe_first_detail_index, self.gamma)
            total_length = detail[1] + required_gap
            if total_length <= max_box_size:
                self._choose_strip_from_box()
            else:
                event = GammaAlgorithmBeforeLRPCutEvent(self.gamma, self.lrp, self.stripe,
                                                        self.stripe_first_detail_index, self.is_stripe_horizontal,
                                                        self.last_placed_index, self.endpoints_placed,
                                                        self.stripe_from, detail, placed_details)
                self._notify_statistic_listeners(event)
                self._cut_new_strip(detail, placed_details)
                event = GammaAlgorithmAfterLRPCutEvent(self.gamma, self.lrp, self.stripe,
                                                       self.stripe_first_detail_index, self.is_stripe_horizontal,
                                                       self.last_placed_index, self.endpoints_placed,
                                                       self.stripe_from, detail, placed_details)
                self._notify_statistic_listeners(event)

    def _choose_strip_from_box(self) -> None:
        """
        Choose the widest available box as the new stripe for placing details. Called only when a suitable box exists.
        """
        self.stripe_from = self.boxes[0].detail_type
        self.stripe = self.boxes[0]
        self.boxes.remove(self.stripe)
        self.is_stripe_horizontal = self.stripe.width >= self.stripe.height

    def _cut_new_strip(self, detail: tuple[float, float], placed_details: list[Detail]) -> None:
        """
        Cut a new stripe from LRP if no suitable box exists.
        Called only when there is no suitable box for placing a new detail. Raises an exception if it's impossible
        to cut a stripe.

        :param detail: The current detail to be placed. A tuple represents the width and height of the detail.
            The width here means the side on which the detail will be placed.
        :param placed_details: List of details that have been placed so far.
        """
        self.stripe_from = self.lrp.detail_type
        required_gap = pow(1 / (self.last_placed_index + 1), self.gamma)
        if detail[1] + required_gap > max(self.lrp.width, self.lrp.height) or \
                detail[0] + required_gap > min(self.lrp.width, self.lrp.height):
            raise AlgorithmExecutionException("Unable to cut a new strip, LRP is too small")
        if self.lrp.width <= self.lrp.height:
            self.is_stripe_horizontal = True
            stripe_bottom_left = self.lrp.bottom_left
            stripe_top_right = (self.lrp.top_right[0], self.lrp.bottom_left[1] + detail[1] + required_gap)
            new_lrp_bottom_left = (self.lrp.bottom_left[0], self.lrp.bottom_left[1] + detail[1] + required_gap)
            new_lrp_top_right = self.lrp.top_right
        else:
            self.is_stripe_horizontal = False
            stripe_bottom_left = (self.lrp.top_right[0] - detail[1] - required_gap, self.lrp.bottom_left[1])
            stripe_top_right = self.lrp.top_right
            new_lrp_bottom_left = self.lrp.bottom_left
            new_lrp_top_right = (self.lrp.top_right[0] - detail[1] - required_gap, self.lrp.top_right[1])
        stripe = Detail(stripe_bottom_left, stripe_top_right, f'{self.ENDPOINT_PREFIX}{self.endpoints_placed}',
                        self.ENDPOINT_TYPE_1_NAME)
        new_lrp = Detail(new_lrp_bottom_left, new_lrp_top_right, self.LRP_PREFIX, self.LRP_NAME)
        if self.update_placed_details:
            placed_details.remove(self.lrp)
            placed_details.append(stripe)
            placed_details.append(new_lrp)
        self.stripe = stripe
        self.lrp = new_lrp

    def _place_detail_in_stripe(self, detail: tuple[float, float], placed_details: list[Detail]) -> None:
        """
        Place a detail into the stripe.
        Called only when the necessary stripe has already been chosen and there is enough space in it to place
        the detail with the required gap.

        :param detail: The current detail to be placed. A tuple represents the width and height of the detail.
            The width here means the side on which the detail will be placed.
        :param placed_details: List of details that have been placed so far.
        """
        normal_box_type = self._get_normal_box_type()
        endpoint_type = self._get_endpoint_type()

        self.last_placed_index += 1
        if self.is_stripe_horizontal:
            placed_detail_bottom_left = self.stripe.bottom_left
            placed_detail_top_right = (self.stripe.bottom_left[0] + detail[0], self.stripe.bottom_left[1] + detail[1])
            normal_box_bottom_left = (self.stripe.bottom_left[0], self.stripe.bottom_left[1] + detail[1])
            normal_box_top_right = (self.stripe.bottom_left[0] + detail[0], self.stripe.top_right[1])
            endpoint_bottom_left = (self.stripe.bottom_left[0] + detail[0], self.stripe.bottom_left[1])
            endpoint_top_right = self.stripe.top_right
        else:
            placed_detail_bottom_left = (self.stripe.top_right[0] - detail[1], self.stripe.bottom_left[1])
            placed_detail_top_right = (self.stripe.top_right[0], self.stripe.bottom_left[1] + detail[0])
            normal_box_bottom_left = self.stripe.bottom_left
            normal_box_top_right = (self.stripe.top_right[0] - detail[1], self.stripe.bottom_left[1] + detail[0])
            endpoint_bottom_left = (self.stripe.bottom_left[0], self.stripe.bottom_left[1] + detail[0])
            endpoint_top_right = self.stripe.top_right
        placed_detail = Detail(placed_detail_bottom_left, placed_detail_top_right,
                               f'{self.DETAIL_PREFIX}{self.last_placed_index}', self.DETAIL_NAME)
        normal_box = Detail(normal_box_bottom_left, normal_box_top_right,
                            f'{self.NORMAL_BOX_PREFIX}{self.last_placed_index}', normal_box_type)
        endpoint = Detail(endpoint_bottom_left, endpoint_top_right,
                          f'{self.ENDPOINT_PREFIX}{self.endpoints_placed}', endpoint_type)
        if self.update_placed_details:
            placed_details.remove(self.stripe)
            placed_details.append(placed_detail)
            placed_details.append(normal_box)
            placed_details.append(endpoint)
        self.stripe = endpoint
        self.boxes.add(normal_box)
        event = GammaAlgorithmAfterDetailPlacedEvent(self.gamma, self.lrp, self.stripe,
                                                     self.stripe_first_detail_index, self.is_stripe_horizontal,
                                                     self.last_placed_index, self.endpoints_placed,
                                                     self.stripe_from, detail, placed_details, placed_detail,
                                                     normal_box, endpoint)
        self._notify_statistic_listeners(event)

    def _get_normal_box_type(self) -> str:
        """
        Determine the type of normal box obtained when cutting from the current stripe.
        If the stripe is cut from LRP, the box will be of the first type; otherwise, it will be the second type.

        :return: The type of normal box that will result from cutting from the current stripe.
        """
        if self.stripe_from == self.LRP_NAME:
            return self.NORMAL_BOX_TYPE_1_NAME
        else:
            return self.NORMAL_BOX_TYPE_2_NAME

    def _get_endpoint_type(self) -> str:
        """
        Determine the type of endpoint obtained when cutting from the current stripe.
        If the stripe is cut from LRP or from a type 1 endpoint, the endpoint will be of the first type;
        otherwise, it will be the second type.

        :return: The type of endpoint that will result from cutting from the current stripe.
        """
        if self.stripe_from == self.LRP_NAME or self.stripe_from == self.ENDPOINT_TYPE_1_NAME:
            return self.ENDPOINT_TYPE_1_NAME
        else:
            return self.ENDPOINT_TYPE_2_NAME

    def _notify_statistic_listeners(self, event: Event):
        """
        Notify statistic listeners after event occurred.

        :param event: The event to be processed.
        """
        for statistic in self.statistic_listeners:
            if statistic.get_event_type() == event.get_event_type():
                statistic.handle(event)

    @staticmethod
    def _detail_comparator(detail1: Detail, detail2: Detail) -> float:
        """
        Compares two details based on their minimum side length.

        :param detail1: The first detail for comparison.
        :param detail2: The second detail for comparison.
        :return: Positive if detail1 is larger, negative if detail2 is larger, 0 if equal.
        """
        return min(detail2.width, detail2.height) - min(detail1.width, detail1.height)
