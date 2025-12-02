"""Astronomical calculations for the Solstice Season integration.

This module contains all calculation logic for seasons, equinoxes,
solstices, and daylight trends. It is independent of Home Assistant
to allow for easier testing and maintenance.
"""

from datetime import date, datetime, timezone
from typing import TypedDict

from astral import sun

from .const import (
    HEMISPHERE_NORTHERN,
    MODE_ASTRONOMICAL,
    SEASON_AUTUMN,
    SEASON_SPRING,
    SEASON_SUMMER,
    SEASON_WINTER,
    TREND_LONGER,
    TREND_SHORTER,
    TREND_SOLSTICE,
)


class AstronomicalEvents(TypedDict):
    """Type definition for astronomical events."""

    march_equinox: datetime
    june_solstice: datetime
    september_equinox: datetime
    december_solstice: datetime


class SeasonData(TypedDict):
    """Type definition for season calculation results."""

    current_season: str
    spring_start: str
    summer_start: str
    autumn_start: str
    winter_start: str
    spring_equinox: datetime
    summer_solstice: datetime
    autumn_equinox: datetime
    winter_solstice: datetime
    days_until_spring: int
    days_until_summer: int
    days_until_autumn: int
    days_until_winter: int
    daylight_trend: str
    next_trend_change: datetime
    days_until_trend_change: int
    next_trend_event_type: str


# Mapping of seasons to astronomical events per hemisphere
SEASON_MAPPING = {
    HEMISPHERE_NORTHERN: {
        SEASON_SPRING: "march_equinox",
        SEASON_SUMMER: "june_solstice",
        SEASON_AUTUMN: "september_equinox",
        SEASON_WINTER: "december_solstice",
    },
    "southern": {
        SEASON_SPRING: "september_equinox",
        SEASON_SUMMER: "december_solstice",
        SEASON_AUTUMN: "march_equinox",
        SEASON_WINTER: "june_solstice",
    },
}

# Meteorological season start dates (month, day) per hemisphere
METEOROLOGICAL_SEASONS = {
    HEMISPHERE_NORTHERN: {
        SEASON_SPRING: (3, 1),
        SEASON_SUMMER: (6, 1),
        SEASON_AUTUMN: (9, 1),
        SEASON_WINTER: (12, 1),
    },
    "southern": {
        SEASON_SPRING: (9, 1),
        SEASON_SUMMER: (12, 1),
        SEASON_AUTUMN: (3, 1),
        SEASON_WINTER: (6, 1),
    },
}


def get_astronomical_events(year: int) -> AstronomicalEvents:
    """Get all astronomical events for a given year.

    Args:
        year: The year to calculate events for.

    Returns:
        Dictionary containing all four astronomical events with UTC datetimes.
    """
    return AstronomicalEvents(
        march_equinox=sun.equinox(year, sun.SunDirection.RISING).replace(
            tzinfo=timezone.utc
        ),
        june_solstice=sun.solstice(year, sun.SunDirection.RISING).replace(
            tzinfo=timezone.utc
        ),
        september_equinox=sun.equinox(year, sun.SunDirection.SETTING).replace(
            tzinfo=timezone.utc
        ),
        december_solstice=sun.solstice(year, sun.SunDirection.SETTING).replace(
            tzinfo=timezone.utc
        ),
    )


def calculate_days_until(target_date: date, reference_date: date) -> int:
    """Calculate days until a target date.

    Args:
        target_date: The target date to calculate days until.
        reference_date: The reference date to calculate from.

    Returns:
        Number of days until the target date, minimum 0.
    """
    delta = target_date - reference_date
    return max(0, delta.days)


def get_next_event_date(
    event_name: str,
    current_year_events: AstronomicalEvents,
    next_year_events: AstronomicalEvents,
    now: datetime,
) -> datetime:
    """Get the next occurrence of an astronomical event.

    Args:
        event_name: Name of the event (march_equinox, june_solstice, etc.).
        current_year_events: Events for the current year.
        next_year_events: Events for the next year.
        now: Current datetime.

    Returns:
        The next occurrence of the event.
    """
    current_event = current_year_events[event_name]
    if now < current_event:
        return current_event
    return next_year_events[event_name]


def determine_current_season_astronomical(
    hemisphere: str, now: datetime, events: AstronomicalEvents
) -> str:
    """Determine the current season using astronomical calculation.

    Args:
        hemisphere: Either 'northern' or 'southern'.
        now: Current datetime.
        events: Astronomical events for the current year.

    Returns:
        Current season as string (spring, summer, autumn, winter).
    """
    mapping = SEASON_MAPPING[hemisphere]

    # Get event datetimes
    spring_start = events[mapping[SEASON_SPRING]]
    summer_start = events[mapping[SEASON_SUMMER]]
    autumn_start = events[mapping[SEASON_AUTUMN]]
    winter_start = events[mapping[SEASON_WINTER]]

    # Sort by month to handle year boundary correctly
    if hemisphere == HEMISPHERE_NORTHERN:
        # Northern: spring(Mar) -> summer(Jun) -> autumn(Sep) -> winter(Dec)
        if now >= winter_start:
            return SEASON_WINTER
        if now >= autumn_start:
            return SEASON_AUTUMN
        if now >= summer_start:
            return SEASON_SUMMER
        if now >= spring_start:
            return SEASON_SPRING
        return SEASON_WINTER  # Before March equinox = still winter
    else:
        # Southern: autumn(Mar) -> winter(Jun) -> spring(Sep) -> summer(Dec)
        if now >= summer_start:
            return SEASON_SUMMER
        if now >= spring_start:
            return SEASON_SPRING
        if now >= winter_start:
            return SEASON_WINTER
        if now >= autumn_start:
            return SEASON_AUTUMN
        return SEASON_SUMMER  # Before March equinox = still summer


def determine_current_season_meteorological(hemisphere: str, now: datetime) -> str:
    """Determine the current season using meteorological calculation.

    Args:
        hemisphere: Either 'northern' or 'southern'.
        now: Current datetime.

    Returns:
        Current season as string (spring, summer, autumn, winter).
    """
    month = now.month
    seasons = METEOROLOGICAL_SEASONS[hemisphere]

    # Create list of (start_month, season) sorted by month
    season_starts = [(seasons[s][0], s) for s in seasons]
    season_starts.sort(key=lambda x: x[0])

    # Find current season
    current_season = season_starts[-1][1]  # Default to last season (handles Dec-Feb)
    for start_month, season in season_starts:
        if month >= start_month:
            current_season = season

    return current_season


def calculate_daylight_trend(
    now: datetime,
    june_solstice: datetime,
    december_solstice: datetime,
) -> str:
    """Determine if days are getting longer or shorter.

    The daylight trend is hemisphere-independent as it only depends on
    the position relative to the solstices.

    Args:
        now: Current datetime.
        june_solstice: June solstice datetime for current year.
        december_solstice: December solstice datetime for current year.

    Returns:
        Trend state (days_getting_longer, days_getting_shorter, solstice_today).
    """
    today = now.date()

    # Check if today is a solstice day
    if today == june_solstice.date() or today == december_solstice.date():
        return TREND_SOLSTICE

    # After December solstice until June solstice: days getting longer
    # After June solstice until December solstice: days getting shorter
    if now < june_solstice:
        return TREND_LONGER
    if now < december_solstice:
        return TREND_SHORTER
    # After December solstice
    return TREND_LONGER


def get_next_solstice(
    hemisphere: str,
    now: datetime,
    current_year_events: AstronomicalEvents,
    next_year_events: AstronomicalEvents,
) -> tuple[datetime, str]:
    """Get the next solstice and its type relative to the hemisphere.

    Args:
        hemisphere: Either 'northern' or 'southern'.
        now: Current datetime.
        current_year_events: Events for the current year.
        next_year_events: Events for the next year.

    Returns:
        Tuple of (next solstice datetime, event type for hemisphere).
    """
    june = current_year_events["june_solstice"]
    december = current_year_events["december_solstice"]

    if now < june:
        next_solstice = june
        event_type = (
            "summer_solstice"
            if hemisphere == HEMISPHERE_NORTHERN
            else "winter_solstice"
        )
    elif now < december:
        next_solstice = december
        event_type = (
            "winter_solstice"
            if hemisphere == HEMISPHERE_NORTHERN
            else "summer_solstice"
        )
    else:
        # After December solstice, next is June of next year
        next_solstice = next_year_events["june_solstice"]
        event_type = (
            "summer_solstice"
            if hemisphere == HEMISPHERE_NORTHERN
            else "winter_solstice"
        )

    return next_solstice, event_type


def calculate_season_data(hemisphere: str, mode: str, now: datetime) -> SeasonData:
    """Calculate all season-related data.

    This is the main entry point for all calculations. It returns all
    data needed by the sensors.

    Args:
        hemisphere: Either 'northern' or 'southern'.
        mode: Either 'astronomical' or 'meteorological'.
        now: Current datetime in UTC.

    Returns:
        Dictionary containing all calculated season data.
    """
    year = now.year
    current_events = get_astronomical_events(year)
    next_events = get_astronomical_events(year + 1)

    # Determine current season
    if mode == MODE_ASTRONOMICAL:
        current_season = determine_current_season_astronomical(
            hemisphere, now, current_events
        )
    else:
        current_season = determine_current_season_meteorological(hemisphere, now)

    # Get season mapping for this hemisphere
    mapping = SEASON_MAPPING[hemisphere]

    # Get next occurrence of each seasonal event
    spring_event = get_next_event_date(
        mapping[SEASON_SPRING], current_events, next_events, now
    )
    summer_event = get_next_event_date(
        mapping[SEASON_SUMMER], current_events, next_events, now
    )
    autumn_event = get_next_event_date(
        mapping[SEASON_AUTUMN], current_events, next_events, now
    )
    winter_event = get_next_event_date(
        mapping[SEASON_WINTER], current_events, next_events, now
    )

    # Calculate days until each event
    today = now.date()
    days_until_spring = calculate_days_until(spring_event.date(), today)
    days_until_summer = calculate_days_until(summer_event.date(), today)
    days_until_autumn = calculate_days_until(autumn_event.date(), today)
    days_until_winter = calculate_days_until(winter_event.date(), today)

    # Get season start dates for current year (for attributes)
    spring_start_event = current_events[mapping[SEASON_SPRING]]
    summer_start_event = current_events[mapping[SEASON_SUMMER]]
    autumn_start_event = current_events[mapping[SEASON_AUTUMN]]
    winter_start_event = current_events[mapping[SEASON_WINTER]]

    # Calculate daylight trend
    daylight_trend = calculate_daylight_trend(
        now,
        current_events["june_solstice"],
        current_events["december_solstice"],
    )

    # Get next trend change (next solstice)
    next_trend_change, next_trend_event_type = get_next_solstice(
        hemisphere, now, current_events, next_events
    )
    days_until_trend_change = calculate_days_until(next_trend_change.date(), today)

    return SeasonData(
        current_season=current_season,
        spring_start=spring_start_event.date().isoformat(),
        summer_start=summer_start_event.date().isoformat(),
        autumn_start=autumn_start_event.date().isoformat(),
        winter_start=winter_start_event.date().isoformat(),
        spring_equinox=spring_event,
        summer_solstice=summer_event,
        autumn_equinox=autumn_event,
        winter_solstice=winter_event,
        days_until_spring=days_until_spring,
        days_until_summer=days_until_summer,
        days_until_autumn=days_until_autumn,
        days_until_winter=days_until_winter,
        daylight_trend=daylight_trend,
        next_trend_change=next_trend_change,
        days_until_trend_change=days_until_trend_change,
        next_trend_event_type=next_trend_event_type,
    )
