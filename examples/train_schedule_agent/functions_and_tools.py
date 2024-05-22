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
    for i, schedule in enumerate(schedules):
        if type(schedules[i]["start_time"]) == datetime:
            continue
        schedules[i]["start_time"] = datetime.strptime(
            schedule["start_time"], "%Y-%m-%dT%H:%M:%S"
        )
        schedules[i]["end_time"] = datetime.strptime(
            schedule["end_time"], "%Y-%m-%dT%H:%M:%S"
        )

    return schedules


def get_passenger_flows(schedules: List) -> List:
    flows = []
    for schedule in schedules:
        flows.append((schedule["start_time"], schedule["passengers"]))
        flows.append((schedule["end_time"], -schedule["passengers"]))

    ## Sort based on time
    flows.sort()

    return flows


def max_passengers_on_track(schedules: List) -> int:
    """
    Uses a list of schedules to get the maximum number of
    passengers within the given schedule.

    Args:
        schedule (List): Schedules, where each element is a dictionary
            with start_time, end_time, and passengers as keys.

    Returns:
        int: Maximum number of passengers
    """
    # schedules = format_datetimes(schedules)
    flows = get_passenger_flows(schedules)

    current_passengers = 0
    max_passengers = 0
    for _, change in flows:
        current_passengers += change
        max_passengers = max(max_passengers, current_passengers)

    return max_passengers


def plot_passenger_count_on_time(schedules: List) -> bool:
    """
    Uses a list of schedules to plot the time-series of the number of
    passengers throughout the day.

    Args:
        schedules (List): Schedules, where each element is a dictionary
            with start_time, end_time, and passengers as keys.

    Returns:
        bool: If True the plotting was successfull
    """
    schedules = format_datetimes(schedules)

    # Define the start and end of plot
    current_time = schedules[0]["start_time"].replace(hour=0, minute=0)
    end_day = schedules[0]["start_time"].replace(hour=23, minute=59)

    # Increment time by 10 minutes in each iteration
    time_increment = timedelta(minutes=20)

    time_arr = []
    passenger_arr = []
    while current_time <= end_day:
        current_passengers = get_passengers_at_t(schedules, current_time)
        time_arr.append(current_time)
        passenger_arr.append(current_passengers)
        current_time += time_increment

    plt.plot(
        time_arr, passenger_arr, label="Num of passenger throughout the day."
    )
    # Set the major locator to every 4 hours
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=4))

    # Set the major formatter to show time as %H:%M
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    plt.show()
    return True


def get_passengers_at_t(schedules: List, t: datetime) -> int:
    """
    Uses a list of schedules to get the number of passengers
    at any given time.

    Args:
        schedules (List): Schedules, where each element is a dictionary
            with start_time, end_time, and passengers as keys.
        t (datetime): Time to evaluate the number of passengers.

    Returns:
        int: Number of passengers
    """
    schedules_t = []
    for s in schedules:
        if t >= s["start_time"] and t < s["end_time"]:
            schedules_t.append((s["start_time"], s["passengers"]))

    return sum(j for _, j in schedules_t)


def read_day_schedules(day: str) -> List:
    """Read the schedules for a given day.

    Args:
        day (str): The day to read the schedule for.

    Returns:
        List: Schedules, where each element is a dictionary
            with start_time, end_time, and passengers as keys.
    """
    with open(file_path, "r") as file:
        schedules = json.load(file)

    schedules = schedules.get(day, [])

    for i, schedule in enumerate(schedules):
        schedules[i]["start_time"] = f'{day}T{schedule["start_time"]}:00'
        schedules[i]["end_time"] = f'{day}T{schedule["end_time"]}:00'

    schedules = format_datetimes(schedules)

    return schedules


def confirm_schedule(id: str) -> bool:
    """
    Use this if you want to confirm a schedule.

    Returns:
        bool: Returns True if sucessful.
    """

    new_schedule = new_schedules.get(id)

    if new_schedule is None:
        raise ValueError("Please create a new schedule with a valid id.")

    if new_schedule.day is None:
        raise ValueError("Please provide a day.")

    if new_schedule.start_time is None:
        raise ValueError("Please provide a start time.")

    if new_schedule.end_time is None:
        raise ValueError("Please provide an end_time.")

    if new_schedule.passengers is None:
        raise ValueError("Please provide number of passengers.")

    with open(file_path, "r") as f:
        data = json.load(f)

    day = new_schedule.day
    schedule_info = {
        "id": id,
        "start_time": new_schedule.start_time,
        "end_time": new_schedule.end_time,
        "passengers": int(new_schedule.passengers),
    }

    if data.get(day):
        data[day].append(schedule_info)
    else:
        data[day] = [schedule_info]

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

    return True


def create_schedule() -> str:
    """Create a new schedule."""
    # Generate the random ID
    id = "".join(random.choice(string.ascii_lowercase) for _ in range(4))
    new_schedules[id] = TrainSchedule()
    return f"New schedule created with id {id}, but not yet confirmed. Please provide day, start_time, end_time, and passengers."


def update_schedule(id: str, property: str, value: str) -> str:
    """
    Update a property of a new_schedule.
    Only enter details that are explicitly provided.
    """
    new_schedule = new_schedules[id]
    setattr(new_schedule, property, value)
    return f"new_schedule ID {id} updated with {property} = {value}"


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
