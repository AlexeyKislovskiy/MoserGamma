from abc import abstractmethod
from statistic.event.gamma_algorithm_events import GammaAlgorithmAfterDetailPlacedEvent, \
    GammaAlgorithmBeforeLRPCutEvent, GammaAlgorithmAfterLRPCutEvent, GammaAlgorithmEndEvent
from statistic.listener.abstract_listener import StatisticListener


class AfterDetailPlacedListener(StatisticListener):
    """
    An abstract listener class for handling events after a detail has been placed during the gamma algorithm.
    This class should be subclassed by classes that need to perform specific actions when a new detail is placed
    in the gamma algorithm.
    """

    @abstractmethod
    def handle(self, event: GammaAlgorithmAfterDetailPlacedEvent) -> None:
        """
        Handle the event that occurs after a detail is placed.

        :param event: The event that occurs after a detail is placed.
        """
        pass

    def get_event_type(self) -> str:
        """
        Get the type of event associated with this listener.

        :return: The type of event associated with this listener.
        """
        return GammaAlgorithmAfterDetailPlacedEvent.EVENT_TYPE


class BeforeLRPCutListener(StatisticListener):
    """
    An abstract listener class for handling events before cutting a stripe from the LRP during the gamma algorithm.
    This class should be subclassed by classes that need to perform specific actions before cutting a stripe
    from the LRP in the gamma algorithm.
    """

    @abstractmethod
    def handle(self, event: GammaAlgorithmBeforeLRPCutEvent) -> None:
        """
        Handle the event that occurs before cutting a stripe from the LRP.

        :param event: The event that occurs before cutting a stripe from the LRP.
        """
        pass

    def get_event_type(self) -> str:
        """
        Get the type of event associated with this listener.

        :return: The type of event associated with this listener.
        """
        return GammaAlgorithmBeforeLRPCutEvent.EVENT_TYPE


class AfterLRPCutListener(StatisticListener):
    """
    An abstract listener class for handling events after cutting a stripe from the LRP during the gamma algorithm.
    This class should be subclassed by classes that need to perform specific actions after cutting a stripe
    from the LRP in the gamma algorithm.
    """

    @abstractmethod
    def handle(self, event: GammaAlgorithmAfterLRPCutEvent) -> None:
        """
        Handle the event that occurs after cutting a stripe from the LRP.

        :param event: The event that occurs after cutting a stripe from the LRP.
        """
        pass

    def get_event_type(self) -> str:
        """
        Get the type of event associated with this listener.

        :return: The type of event associated with this listener.
        """
        return GammaAlgorithmAfterLRPCutEvent.EVENT_TYPE


class AlgorithmEndListener(StatisticListener):
    """
    An abstract listener class for handling events that occurs at the end of the gamma algorithm.
    This class should be subclassed by classes that need to perform specific actions at the end of the gamma algorithm.
    """

    @abstractmethod
    def handle(self, event: GammaAlgorithmEndEvent) -> None:
        """
        Handle the event that occurs at the end of the gamma algorithm.

        :param event: The event that occurs at the end of the gamma algorithm.
        """
        pass

    def get_event_type(self) -> str:
        """
        Get the type of event associated with this listener.

        :return: The type of event associated with this listener.
        """
        return GammaAlgorithmEndEvent.EVENT_TYPE
