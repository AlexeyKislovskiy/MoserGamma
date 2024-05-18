class OutputHandler:
    """
    A class to handle output operations, either to the console or to a file.
    Supports appending to or overwriting a file.

    Attributes:
        mode (str): The mode of output ('console', 'file_append', 'file_overwrite').
        file_path (str): The path to the file for output operations. Used only if mode is
            'file_append' or 'file_overwrite'.
        first_write (bool): A flag to track the first write operation when in 'file_overwrite' mode.
    """

    CONSOLE = 'console'
    FILE_APPEND = 'file_append'
    FILE_OVERWRITE = 'file_overwrite'

    def __init__(self, mode: str = CONSOLE, file_path: str = None):
        """
        Initializes the OutputHandler.

        :param mode: The mode of output. Can be 'console', 'file_append', or 'file_overwrite'. Default is 'console'.
        :param file_path: The path to the file for file output modes.
        """
        self.mode = mode
        self.file_path = file_path
        self.first_write = True

    def write(self, message: str):
        """
        Writes the given message according to the output mode.

        :param message: The message to be written.
        :raises ValueError: If the mode is invalid or if the file_path is not provided for file modes.
        """
        if self.mode == self.CONSOLE:
            print(message)
        elif self.mode in [self.FILE_APPEND, self.FILE_OVERWRITE] and self.file_path:
            if self.mode == self.FILE_OVERWRITE and self.first_write:
                with open(self.file_path, 'w') as f:
                    f.write(f'{message}\n')
                self.first_write = False
            else:
                with open(self.file_path, 'a') as f:
                    f.write(f'{message}\n')
        else:
            raise ValueError(f"Invalid mode or file_path not provided for mode {self.mode}")
