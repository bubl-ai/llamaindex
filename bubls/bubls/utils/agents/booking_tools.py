from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.core.bridge.pydantic import BaseModel
import random
import string
from typing import Optional

# we will store booking under random IDs
bookings = {}


class Booking(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None


def get_booking_state(user_id: str) -> str:
    """Get the current state of a booking for a given booking ID."""
    try:
        return str(bookings[user_id].dict())
    except:
        return f"Booking ID {user_id} not found"


get_booking_state_tool = FunctionTool.from_defaults(
    fn=get_booking_state, return_direct=True
)


def update_booking(user_id: str, property: str, value: str) -> str:
    """Update a property of a booking for a given booking ID. Only enter details that are explicitly provided."""
    booking = bookings[user_id]
    setattr(booking, property, value)
    return f"Booking ID {user_id} updated with {property} = {value}"


update_booking_tool = FunctionTool.from_defaults(fn=update_booking)


def create_booking() -> str:
    """Create a new booking and return the booking ID."""
    # Generate the random ID
    user_id = "".join(random.choice(string.ascii_uppercase) for _ in range(6))
    bookings[user_id] = Booking()
    return f"Booking created with id {user_id}, but not yet confirmed. Please provide your name, email, phone, date, and time."


create_booking_tool = FunctionTool.from_defaults(
    fn=create_booking, return_direct=True
)


def confirm_booking(user_id: str) -> str:
    """Confirm a booking for a given booking ID."""
    booking = bookings[user_id]

    if booking.name is None:
        raise ValueError("Please provide your name.")

    if booking.email is None:
        raise ValueError("Please provide your email.")

    if booking.phone is None:
        raise ValueError("Please provide your phone number.")

    if booking.date is None:
        raise ValueError("Please provide the date of your booking.")

    if booking.time is None:
        raise ValueError("Please provide the time of your booking.")

    return f"Booking for Name: {booking.name} and ID: {user_id} is confirmed!"


confirm_booking_tool = FunctionTool.from_defaults(
    fn=confirm_booking, return_direct=True
)
