from typing import NamedTuple


class Event(NamedTuple):
    name: str
    start_time: int
    duration: int
    category: str


if __name__ == '__main__':
    # Example usage of Event class above
    # to create an event, instantiate the class
    # with explicit named argument
    # For example, to create an event with the following attribute
    # name: Midterm Exam
    # start time: 100
    # duration: 90 minutes
    # category: school event
    # you should do
    event = Event(name="Midterm Exam", start_time=100,
                  duration=90, category="School Event")
    print(event)
    # to read any attribute for an existing event, access with dot
    # for example
    print("Exam duration is:", event.duration, "minutes")
