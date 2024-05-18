class Detail:
    """
    A class representing a detail.
    Each detail is defined by its bottom-left and top-right coordinates, a name, and a type.

    Attributes:
        bottom_left (tuple[float, float]): The bottom-left coordinates of the detail.
        top_right (tuple[float, float]): The top-right coordinates of the detail.
        name (str): The name of the detail.
        detail_type (str): The type of the detail.

    Properties:
        width (float): The width of the detail.
        height (float): The height of the detail.
    """

    def __init__(self, bottom_left: tuple[float, float], top_right: tuple[float, float], name: str, detail_type: str):
        """
        Initialize a Detail object.

        :param bottom_left: The bottom-left coordinates of the detail.
        :param top_right: The top-right coordinates of the detail.
        :param name: The name of the detail.
        :param detail_type: The type of the detail.
        """
        self.bottom_left = bottom_left
        self.top_right = top_right
        self.name = name
        self.detail_type = detail_type

    @property
    def width(self) -> float:
        """
        Calculate the width of the detail.

        :return: The width of the detail.
        """
        return self.top_right[0] - self.bottom_left[0]

    @property
    def height(self) -> float:
        """
        Calculate the height of the detail.

        :return: The height of the detail.
        """
        return self.top_right[1] - self.bottom_left[1]
