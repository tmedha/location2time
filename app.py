import service as s

if __name__ == "__main__":
    location = input("Enter location: ")
    latitude, longitude = s.get_coordinates(location)
    time_at_location = s.get_time(latitude, longitude)
    final_time = s.format_time(time_at_location)
    print(f"The time at {location} is {final_time}.")