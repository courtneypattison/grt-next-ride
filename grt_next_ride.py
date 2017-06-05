#!/usr/bin/env python


"""
This program displays the next few ride times for a Grand River Transit (GRT)
stop specified on the command line.
"""


import sys
import time
import urllib2

import gtfs_realtime_pb2


TRIP_UPDATES_URL = "http://192.237.29.212:8080/gtfsrealtime/TripUpdates"


def get_trip_updates_feed():
    """
    Read trip updates feed from GRT site using GTFS Realtime feed
    specification https://developers.google.com/transit/gtfs-realtime/
    """
    feed = gtfs_realtime_pb2.FeedMessage()

    response = urllib2.urlopen(TRIP_UPDATES_URL)
    feed.ParseFromString(response.read())
    response.close()

    return feed


def get_next_ride_times(stop_id):
    """
    Get a list of the next few ride times (in seconds) available for the
    stop id specified
    """
    next_ride_times = []
    feed = get_trip_updates_feed()

    if not feed.entity:
        sys.exit("Next ride times are not available from the GRT site.")

    for entity in feed.entity:
        if entity.HasField("trip_update"):
            for stop_time_update in entity.trip_update.stop_time_update:
                try:
                    if stop_time_update.stop_id == stop_id:
                        next_ride_times.append(stop_time_update.departure.time)
                except:
                    pass

    return next_ride_times


def format_time(secs):
    """
    Format time in seconds to 12 hour clock and minutes
    """
    return time.strftime("%I:%M", time.localtime(secs))


def display_next_ride_times(next_ride_times):
    """
    Print to console a sorted newline separated list of next ride times, with
    the approximate number of minutes until the next ride
    """

    if next_ride_times:
        next_ride_times.sort()

        mins_to_next_ride = int(next_ride_times[0] - time.time()) / 60
        next_ride_time = format_time(next_ride_times[0])
        print next_ride_time, "in", mins_to_next_ride, "minutes"

        for next_ride_time in next_ride_times[1:]:
            print format_time(next_ride_time)
    else:
        print "There are no next ride times."


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage:", sys.argv[0], "STOP_ID")

    display_next_ride_times(get_next_ride_times(sys.argv[1]))
