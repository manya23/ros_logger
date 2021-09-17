from enum import Enum


class WidgetIndexes(Enum):
    """
    all custom switched widgets types for main window
    """
    CHOOSE_ACTIVITY_WIDGET = 0
    LOG_WRITING_WIDGET = 1
    REPORT_COLLECT_WIDGET = 2

    NONE_WIDGET = 888


class LoggerWidgetIndexes(Enum):
    """
    all custom switched widgets types for logging manage window
    """
    CHOOSE_TOPIC_LAYOUT = 0
    SETUP_LOGGING_LAYOUT = 1
    START_LOGGING_LAYOUT = 2
    LOGGING_PROCESS_DISPLAY_LAYOUT = 3
    LOGGING_FINISH_LAYOUT = 4

    NONE_WIDGET = 888


class DataDisplayWidgetIndexes(Enum):
    """
    all custom switched widgets types for data display manage window
    """
    GET_DISPLAY_LAYOUT = 0
    PLOT_SETUP_LAYOUT = 1

    NONE_WIDGET = 888