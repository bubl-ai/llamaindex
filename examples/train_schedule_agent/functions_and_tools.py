from llama_index.core.tools import FunctionTool
from typing import List, Tuple, Dict, Any, Union, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import random
import string
import json

new_schedules = {}
file_path = "schedules_by_day.json"


class TrainSchedule(BaseModel):
    day: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    passengers: Optional[str] = None


def format_datetimes(schedules: List) -> List:
    """Converts string datetimes in a schedule list to datetime objects.

    Args:
        schedules (List): A list of schedule dictionaries.

    Returns:
        List: The list with formatted datetime objects.
    """
    for schedule in schedules:
        try:
            schedule["start_time"] = datetime.strptime(
                schedule["start_time"], "%Y-%m-%dT%H:%M:%S"
            )
            schedule["end_time"] = datetime.strptime(
                schedule["end_time"], "%Y-%m-%dT%H:%M:%S"
            )
        except ValueError as e:
            raise ValueError(f"Error parsing datetime: {e}")

    return schedules


def get_passenger_flows(schedules: List) -> List:
    """Calculates the passenger flow based on schedules.

    Args:
        schedules (List): List of schedule dictionaries.

    Returns:
        List: Sorted list of passenger changes over time.
    """
    flows = []
    for schedule in schedules:
        flows.append((schedule["start_time"], schedule["passengers"]))
        flows.append((schedule["end_time"], -schedule["passengers"]))
    flows.sort()

    return flows


def max_passengers_on_track(schedules: List) -> int:
    """Calculates the maximum number of passengers present on the track at any time.

    Args:
        schedules (List): List of schedule dictionaries.

    Returns:
        int: The maximum number of passengers on the track.
    """
    flows = get_passenger_flows(schedules)
    current_passengers = 0
    max_passengers = 0
    for _, change in flows:
        current_passengers += change
        max_passengers = max(max_passengers, current_passengers)

    return max_passengers


def plot_passenger_count_on_time(schedules: List) -> bool:
    """Plots passenger count over time based on provided schedules.

    Args:
        schedules (List): List of schedule dictionaries.

    Returns:
        bool: True if plotting is successful, False otherwise.
    """
    schedules = format_datetimes(schedules)
    start = schedules[0]["start_time"].replace(hour=0, minute=0)
    end = schedules[0]["start_time"].replace(hour=23, minute=59)
    time_increment = timedelta(minutes=20)

    time_arr = []
    passenger_arr = []
    while start <= end:
        passenger_count = get_passengers_at_t(schedules, start)
        time_arr.append(start)
        passenger_arr.append(passenger_count)
        start += time_increment

    plt.plot(
        time_arr,
        passenger_arr,
        label="Number of passengers throughout the day",
    )
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=4))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    plt.show()

    return True


def get_passengers_at_t(schedules: List, t: datetime) -> int:
    """Retrieves the number of passengers at a given datetime.

    Args:
        schedules (List): List of schedule dictionaries.
        t (datetime): Specific datetime to check the passenger count.

    Returns:
        int: Total number of passengers at the given time.
    """
    return sum(
        int(schedule["passengers"])
        for schedule in schedules
        if schedule["start_time"] <= t < schedule["end_time"]
    )


def read_day_schedules(day: str) -> List:
    """Reads the schedules for a specific day from file.

    Args:
        day (str): Day to read the schedules for.

    Returns:
        List: List of schedules for the specified day.
    """
    try:
        with open(file_path, "r") as file:
            all_schedules = json.load(file)
        schedules = all_schedules.get(day, [])

        for i, schedule in enumerate(schedules):
            schedules[i]["start_time"] = f'{day}T{schedule["start_time"]}:00'
            schedules[i]["end_time"] = f'{day}T{schedule["end_time"]}:00'

        return format_datetimes(schedules)
    except FileNotFoundError:
        raise FileNotFoundError("The schedule file could not be found.")
    except json.JSONDecodeError:
        raise ValueError("Error decoding JSON from the schedule file.")


def confirm_schedule(id: str) -> bool:
    """Confirms a schedule, ensuring all required fields are provided.

    Args:
        id (str): The ID of the schedule to confirm.

    Returns:
        bool: True if the schedule is successfully confirmed, raises ValueError otherwise.
    """
    new_schedule = new_schedules.get(id)
    if new_schedule is None:
        raise ValueError("No schedule found with the provided ID.")

    if new_schedule.day is None:
        raise ValueError("Please provide a day.")

    if new_schedule.start_time is None:
        raise ValueError("Please provide a start time.")

    if new_schedule.end_time is None:
        raise ValueError("Please provide an end_time.")

    if new_schedule.passengers is None:
        raise ValueError("Please provide number of passengers.")

    with open(file_path, "r") as file:
        data = json.load(file)

    day = new_schedule.day
    schedule_info = {
        "id": id,
        "start_time": new_schedule.start_time,
        "end_time": new_schedule.end_time,
        "passengers": int(new_schedule.passengers),
    }

    if day in data:
        data[day].append(schedule_info)
    else:
        data[day] = [schedule_info]

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

    return True


def create_schedule() -> str:
    """Generates a new schedule with a random ID and initializes default values.

    Returns:
        str: Description of the new schedule creation.
    """
    id = "".join(random.choices(string.ascii_lowercase, k=4))
    new_schedules[id] = TrainSchedule()
    return f"New schedule created with id {id}. Please confirm the schedule by providing day, start_time, end_time, and passengers."


def update_schedule(id: str, property: str, value: str) -> str:
    """Updates a property of a schedule with a given value.

    Useful when more information is needed to confirm a schedule.
    Properties that can be updated ["day", "start_time", "end_time", "passengers"]
    Args:
        id (str): The ID of the schedule to update.
        property (str): The property to update.
        value (str): The new value for the property.

    Returns:
        str: Confirmation message of the update.
    """
    new_schedule = new_schedules.get(id)
    if not new_schedule:
        raise ValueError(f"No schedule found with ID {id}")

    if property not in ["day", "start_time", "end_time", "passengers"]:
        raise ValueError("Invalid property name")

    setattr(new_schedule, property, value)
    return f"Schedule ID {id} updated with {property} = {value}"


update_new_schedule_tool = FunctionTool.from_defaults(fn=update_schedule)

create_schedule_tool = FunctionTool.from_defaults(fn=create_schedule)

get_passengers_at_t_tool = FunctionTool.from_defaults(
    fn=get_passengers_at_t, return_direct=False
)

read_day_schedule_tool = FunctionTool.from_defaults(
    fn=read_day_schedules, return_direct=False
)

plot_passenger_count_on_time_tool = FunctionTool.from_defaults(
    fn=plot_passenger_count_on_time, return_direct=False
)

max_passengers_on_track_tool = FunctionTool.from_defaults(
    fn=max_passengers_on_track, return_direct=False
)

confirm_schedule_tool = FunctionTool.from_defaults(
    fn=confirm_schedule, return_direct=True
)
