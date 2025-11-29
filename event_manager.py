import random
import time
import copy

from event import Event


class EventManager:
    def __init__(self):
        # You are not allowed to add any other attributes to this class.
        self.events = []

    def create(self, name, start_time, duration, category, position = None):
        """Task 1: This function creates an event (name, start time, duration, and category), and stores it in the event list"""
        event = Event(name=name, start_time=start_time, duration=duration, category=category) # create a new event object with provided parameters
        if position is not None and 0 <= position <= len(self.events):
            self.events.insert(position, event) # if a specific position is provided and it's valid, then insert at that position
        else: # otherwise, append that event to the end of the list
            self.events.append(event)

    def shuffle(self):
        """Task 2: This function shuffles the events"""
        n = len(self.events) # get total number of events in the list
        for i in range(n-1,0,-1):
            j = random.randint(0, i) # pick a random index from 0 to i
            self.events[i], self.events[j] = self.events[j], self.events[i] # swap events at positions i and j

    def loadFromFile(self, filename):
        """Task 3: This function reads events from a .txt file and stores them in the event list"""
        try:
            with open(filename, 'r') as f: # open files in read mode
                for line in f: # read every line in the file
                    line = line.strip() # remove extra whitespaces
                    if line: # skip empty lines
                        parts = line.split(',') # split line by commas to get the event attributes
                        if len(parts) == 4: # make sure the event has exactly 4 attributes
                            name = parts[0].strip() # remove extra whitespaces
                            start_time = int(parts[1].strip()) # convert into an integer
                            duration = int(parts[2].strip()) # convert into an integer
                            category = parts[3].strip()
                            event = Event(name=name, start_time=start_time, duration=duration, category=category) # create an event object and add to the events list
                            self.events.append(event)
        except FileNotFoundError: # when the file doesn't exist
            print(f"File {filename} not found")
        except Exception as e: # when there is an exception
            print(f"Exception: {e}")

    def findEventByName(self, name):
        """Task 4: This function finds an event by name by performing a linear search"""
        for event in self.events: # iterate through all event inside the list
            if event.name == name: # check if the current event's name is the same as the search name
                return event # return the matching event
        return None # return None otherwise

    def insertionSort(self):
        """Task 5: This function performs an in-place insertion sort of the events based on their start time"""
        n = len(self.events)
        for i in range(1,n): # start from the second element
            key = self.events[i] # position current element
            j = i-1 # index of the previous element
            while j >= 0 and self.events[j].start_time > key.start_time:
                self.events[j+1] = self.events[j] # shift the element to eht right
                j -= 1 # move to the previous element
            self.events[j+1] = key

    def bubbleSort(self):
        """This function performs an in-place bubble sort of the events based on their start time"""
        n = len(self.events)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.events[j].start_time > self.events[j+1].start_time:
                    self.events[j], self.events[j+1] = self.events[j+1], self.events[j]

    def quickSort(self):
        """This function performs an in-place quick sort of the events based on their start time"""
        self._quickSort(0, len(self.events) - 1)

    def _quickSort(self, low, high):
        if high - low < 10:  # Use insertion sort for small subarrays
            self._insertionSort(low, high)
            return
        if low < high:
            pi = self._partition(low, high)
            self._quickSort(low, pi)
            self._quickSort(pi + 1, high)

    def _insertionSort(self, low, high):
        for i in range(low + 1, high + 1):
            key = self.events[i]
            j = i - 1
            while j >= low and self.events[j].start_time > key.start_time:
                self.events[j + 1] = self.events[j]
                j -= 1
            self.events[j + 1] = key

    def _partition(self, low, high):
        # Hoare partition with median of three pivot
        mid = (low + high) // 2
        if self.events[low].start_time > self.events[mid].start_time:
            self.events[low], self.events[mid] = self.events[mid], self.events[low]
        if self.events[low].start_time > self.events[high].start_time:
            self.events[low], self.events[high] = self.events[high], self.events[low]
        if self.events[mid].start_time > self.events[high].start_time:
            self.events[mid], self.events[high] = self.events[high], self.events[mid]
        pivot = self.events[mid].start_time
        i = low - 1
        j = high + 1
        while True:
            i += 1
            while self.events[i].start_time < pivot:
                i += 1
            j -= 1
            while self.events[j].start_time > pivot:
                j -= 1
            if i >= j:
                return j
            self.events[i], self.events[j] = self.events[j], self.events[i]

    def binarySearch(self, start_time):
        """Task 6: This function performs a binary search of the events based on a specified start time"""
        l, r = 0, len(self.events) - 1 # initialize left and right pointers
        while l <= r: # as search space is still valid, keep searching
            mid = (l+r)//2 # finding middle index
            mid_time = self.events[mid].start_time # get the start time of the middle event
            if mid_time == start_time: # find the exact match
                while mid > 0 and self.events[mid-1].start_time == start_time: # move to the left to find the first occurrence
                    mid -= 1
                return mid # return the index of the first occurrence
            elif mid_time < start_time:
                l = mid + 1 # search in the right half
            else:
                r = mid - 1 # search in the left half
        return l # return insertion position if not found

    def eventHappening(self, time):
        """Task 7: This function determines if any event is occurring at a given time"""
        if not self.events: # check if events list is empty
            return None

        hpn = self.binarySearch(time) # use binary search to find the position where the event would be inserted

        if hpn < len(self.events): # check event at the found position
            event = self.events[hpn]
            if event.start_time <= time <= event.start_time + event.duration: # check if time falls within this event's duration
                return event # event is happening at the specified time

        if hpn > 0: # check for previous event to see if any overlap happens
            prev_event = self.events[hpn-1]
            if prev_event.start_time <= time <= prev_event.start_time + prev_event.duration: # check if time falls within previous event's duration
                return prev_event # another event is happening at the specified time
        return None # no event happening at that time


    def checkForConflicts(self, time, duration):
        """Task 8: This function takes in an event with a start time and duration, and checks for overlap"""
        if not self.events: # if there is no events, no conflicts
            return False

        end_time2 = time + duration # calculate end time of the proposed event

        hpn = self.binarySearch(time) # find position where the event would be inserted

        if hpn < len(self.events): # check event at found position for overlap
            event = self.events[hpn]
            if time < event.start_time + event.duration and end_time2 > event.start_time: # check if proposed event overlaps with an existing event
                return True # when conflict is found

        if hpn > 0: # check previous event for overlap
            prev_event = self.events[hpn-1]
            if time < prev_event.start_time + prev_event.duration and end_time2 > prev_event.start_time: # check if proposed event overlaps with the previous event
                return True # conflict found

        return False # no conflicts found otherwise

    def findFreeSlot(self, slot_start_time, slot_end_time, requested_duration):
        """Task 9: This function finds a free time slot for a new event"""
        if not self.events: # if there is no events, then the entire list is free
            return slot_start_time

        if slot_end_time - slot_start_time < requested_duration: # check if the requested duration fits in the available time slot
            return -1 # not enough time available

        current = slot_start_time # start checking from the beginning

        for i in range(len(self.events)): # iterate through all events to find an open slot
            event = self.events[i]

            if event.start_time + event.duration <= current: # skip events that end before the current time
                continue

            if event.start_time - current >= requested_duration: # check if there's enough time between the current time and the next event
                return current # found an open slot

            current = event.start_time + event.duration # move the current time to after this event ends

            if current + requested_duration > slot_end_time: # check if we still have enough time before the slot ends
                return -1 # not enough

        if current + requested_duration <= slot_end_time: # check if there's enough time after all events
            return current # open slot at the end

        return -1 # no open slot otherwise


if __name__ == "__main__":
    # Test with small sample events
    print("=== Testing with small sample events ===")
    manager = EventManager()
    manager.create("Event A", 10, 5, "Work")
    manager.create("Event B", 5, 3, "Personal")
    manager.create("Event C", 15, 2, "Work")

    print("Events before sorting:")
    for event in manager.events:
        print(f"Name: {event.name}, Start Time: {event.start_time}")

    # Test insertion sort
    manager_insertion = EventManager()
    manager_insertion.events = copy.deepcopy(manager.events)
    start_time = time.time()
    manager_insertion.insertionSort()
    insertion_time = time.time() - start_time
    print(f"\nInsertion sort time: {insertion_time:.6f} seconds")

    # Test bubble sort
    manager_bubble = EventManager()
    manager_bubble.events = copy.deepcopy(manager.events)
    start_time = time.time()
    manager_bubble.bubbleSort()
    bubble_time = time.time() - start_time
    print(f"Bubble sort time: {bubble_time:.6f} seconds")

    # Test quick sort
    manager_quick = EventManager()
    manager_quick.events = copy.deepcopy(manager.events)
    start_time = time.time()
    manager_quick.quickSort()
    quick_time = time.time() - start_time
    print(f"Quick sort time: {quick_time:.6f} seconds")

    print(f"Comparison: Insertion sort: {insertion_time:.6f}s, Bubble sort: {bubble_time:.6f}s, Quick sort: {quick_time:.6f}s")
    if insertion_time < bubble_time and insertion_time < quick_time:
        print("Insertion sort is fastest.")
    elif bubble_time < insertion_time and bubble_time < quick_time:
        print("Bubble sort is fastest.")
    elif quick_time < insertion_time and quick_time < bubble_time:
        print("Quick sort is fastest.")
    else:
        print("All sorts have similar performance.")

    # Test with events_small.txt
    print("\n=== Testing with events_small.txt (10 events) ===")
    manager_small = EventManager()
    manager_small.loadFromFile("events_small.txt")
    print(f"Loaded {len(manager_small.events)} events.")

    # Test insertion sort on small file
    manager_insertion_small = EventManager()
    manager_insertion_small.events = copy.deepcopy(manager_small.events)
    start_time = time.time()
    manager_insertion_small.insertionSort()
    insertion_time_small = time.time() - start_time
    print(f"Insertion sort time: {insertion_time_small:.6f} seconds")

    # Test bubble sort on small file
    manager_bubble_small = EventManager()
    manager_bubble_small.events = copy.deepcopy(manager_small.events)
    start_time = time.time()
    manager_bubble_small.bubbleSort()
    bubble_time_small = time.time() - start_time
    print(f"Bubble sort time: {bubble_time_small:.6f} seconds")

    # Test quick sort on small file
    manager_quick_small = EventManager()
    manager_quick_small.events = copy.deepcopy(manager_small.events)
    start_time = time.time()
    manager_quick_small.quickSort()
    quick_time_small = time.time() - start_time
    print(f"Quick sort time: {quick_time_small:.6f} seconds")

    print(f"Comparison: Insertion sort: {insertion_time_small:.6f}s, Bubble sort: {bubble_time_small:.6f}s, Quick sort: {quick_time_small:.6f}s")
    if insertion_time_small < bubble_time_small and insertion_time_small < quick_time_small:
        print("Insertion sort is fastest.")
    elif bubble_time_small < insertion_time_small and bubble_time_small < quick_time_small:
        print("Bubble sort is fastest.")
    elif quick_time_small < insertion_time_small and quick_time_small < bubble_time_small:
        print("Quick sort is fastest.")
    else:
        print("All sorts have similar performance.")

    # Test with events_large.txt
    print("\n=== Testing with events_large.txt (10000 events) ===")
    manager_large = EventManager()
    manager_large.loadFromFile("events_large.txt")
    print(f"Loaded {len(manager_large.events)} events.")

    # Test insertion sort on large file
    manager_insertion_large = EventManager()
    manager_insertion_large.events = copy.deepcopy(manager_large.events)
    start_time = time.time()
    manager_insertion_large.insertionSort()
    insertion_time_large = time.time() - start_time
    print(f"Insertion sort time: {insertion_time_large:.6f} seconds")

    # Test bubble sort on large file
    manager_bubble_large = EventManager()
    manager_bubble_large.events = copy.deepcopy(manager_large.events)
    start_time = time.time()
    manager_bubble_large.bubbleSort()
    bubble_time_large = time.time() - start_time
    print(f"Bubble sort time: {bubble_time_large:.6f} seconds")

    # Test quick sort on large file
    manager_quick_large = EventManager()
    manager_quick_large.events = copy.deepcopy(manager_large.events)
    start_time = time.time()
    manager_quick_large.quickSort()
    quick_time_large = time.time() - start_time
    print(f"Quick sort time: {quick_time_large:.6f} seconds")

    print(f"Comparison: Insertion sort: {insertion_time_large:.6f}s, Bubble sort: {bubble_time_large:.6f}s, Quick sort: {quick_time_large:.6f}s")
    if insertion_time_large < bubble_time_large and insertion_time_large < quick_time_large:
        print("Insertion sort is fastest.")
    elif bubble_time_large < insertion_time_large and bubble_time_large < quick_time_large:
        print("Bubble sort is fastest.")
    elif quick_time_large < insertion_time_large and quick_time_large < bubble_time_large:
        print("Quick sort is fastest.")
    else:
        print("All sorts have similar performance.")

