import os

from algorithm.gamma_algorithm import GammaAlgorithm
from detail.detail_functions import count_detail_types, serialize_details_to_json, deserialize_details_from_json, \
    find_neighbours_of_depth
from detail.detail_generator import HarmonicRectangleDetailGenerator
from detail.detail import Detail
from statistic.listener.default_gamma_algorithm_listeners import PrintEachN, NormalBoxMaxRatioTracker, \
    LrpOccupancyRatioTracker, LrpOccupancyRatioHarmonicRectangleTracker
from statistic.output import OutputHandler
from visualization.plotter import Plotter
from core.detail_placer import DetailPlacer
from visualization.settings import PlotSettings

# Example of using the main functionality

n0 = 100  # Index of the first detail to start the placement
gamma = 25 / 17  # Gamma parameter
max_placed = 10000  # Number of details to place
detail_generator = HarmonicRectangleDetailGenerator(n0, is_width_smaller=False)  # Create a generator of rectangles
# with harmonically decreasing sides, which will be placed on the larger side
base_width, base_height = detail_generator.get_base_size()  # Get the dimensions of the sheet needed to place
# all the details on it
base_bottom_left = (0, 0)  # Bottom-left coordinate of the sheet
base_top_right = (base_bottom_left[0] + base_width, base_bottom_left[1] + base_height)  # Top-right coordinate
# of the sheet
base_detail = Detail(base_bottom_left, base_top_right, 'LRP', 'lrp')  # Create a sheet that initially is entirely
# an LRP
print_each_n = PrintEachN(100, OutputHandler(OutputHandler.CONSOLE))  # Create a listener that outputs information
# to the console about all details with an index multiple of 100
normal_box_max_ratio_tracker = NormalBoxMaxRatioTracker(
    OutputHandler(OutputHandler.FILE_OVERWRITE, 'files/max_normal_box.txt'))  # Create a listener that writes to a file
# information about the maximums of the min_size / max_size^gamma ratio
lrp_occupancy_ratio_tracker = LrpOccupancyRatioHarmonicRectangleTracker(
    OutputHandler(OutputHandler.FILE_OVERWRITE, 'files/lrp_occupancy_ratio.txt'))  # Create a listener that writes
# to a file information about the LRP ratio at the moments before cutting a new strip
statistic_listeners = [print_each_n, normal_box_max_ratio_tracker, lrp_occupancy_ratio_tracker]  # Create a list
# of all the used listeners
algorithm = GammaAlgorithm(gamma, n0, max_placed, statistic_listeners=statistic_listeners, update_placed_details=True)
# Create a gamma algorithm with the prepared arguments and set the update_placed_details flag to True for visualization
detail_placer = DetailPlacer(algorithm, detail_generator, base_detail, max_placed)  # Create a detail placer
if not os.path.isfile('files/details.json'):  # Check if there is an existing file with details
    placed_details = detail_placer.run_algorithm()  # If not, run the algorithm
    serialize_details_to_json(placed_details, "files/details.json")  # And save the obtained details to a file
else:
    placed_details = deserialize_details_from_json("files/details.json")  # If there is, get the details from the file
print(count_detail_types(placed_details))  # Print information about how many details of each type were obtained
specific_detail = next((detail for detail in placed_details if detail.name == 'S1234'), None)  # Find in the list
# the detail with index 1234
specific_details = find_neighbours_of_depth(placed_details, specific_detail, depth=3)  # Among all placed details, find
# neighbors of the selected one up to a depth of 3
detail_colors = {"detail": "blue", "normal_box_1": "orange", "normal_box_2": "yellow", "endpoint_1": "green",
                 "endpoint_2": "lime", "lrp": "gray"}  # Create a dictionary mapping the type of detail to its color
plot_settings = PlotSettings(detail_colors=detail_colors)  # Create plotter settings and override the color of details.
# By default, a random color is generated for each type
plotter = Plotter(base_detail, specific_details, plot_settings=plot_settings)  # Create a plotter to display
# the selected details with the given settings
plotter.zoom_to_detail(specific_detail)  # Zoom in on the selected detail
plotter.plot()  # Display the placement
