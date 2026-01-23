"""tui.py

Text User Interface helpers.

This module prints prompts and returns user input.
No dataset logic should live here.
"""

from __future__ import annotations


def show_title(title: str) -> None:
    line = "-" * len(title)
    # Brief asks for a title followed by a line of dashes of equal length.
    print(f"\n{title}")
    print(f"{line}\n")


def show_dataset_loaded(row_count: int) -> None:
    print("Dataset has finished reading.")
    print(f"There are {row_count} rows in the dataset.\n")


def show_message(message: str) -> None:
    print(f"{message}\n")


def show_error(message: str) -> None:
    print(f"ERROR: {message}\n")


def show_invalid_choice() -> None:
    print("Invalid menu choice. Please try again.\n")


def show_exit() -> None:
    print("Exiting the application. Goodbye!")


def _prompt_choice(prompt: str) -> str:
    return input(prompt).strip().upper()


def echo_choice(choice: str, context: str) -> None:
    """Echo the user's choice back using a context label."""
    labels = {
        "main": {"A": "View Data", "B": "Visualise Data", "C": "Export Data", "X": "Exit"},
        "view": {
            "A": "View Reviews by Park",
            "B": "Number of Reviews by Park and Reviewer Location",
            "C": "Average Score per year by Park",
            "D": "Average Score per Park by Reviewer Location",
        },
        "visual": {
            "A": "Most Reviewed Parks",
            "B": "Park Ranking by Nationality",
            "C": "Most Popular Month by Park",
        },
        "export": {"T": "Export to Text (.txt)", "C": "Export to CSV (.csv)", "J": "Export to JSON (.json)"},
    }

    label = labels.get(context, {}).get(choice)
    if label:
        print(f"You have chosen option {choice} - {label}\n")


def menu_main() -> str:
    print("Please enter the letter which corresponds with your desired menu choice:")
    print("[A] View Data")
    print("[B] Visualise Data")
    print("[C] Export Data")
    print("[X] Exit")
    return _prompt_choice("> ")


def menu_view_data() -> str:
    print("Please enter one of the following options:")
    print("[A] View Reviews by Park")
    print("[B] Number of Reviews by Park and Reviewer Location")
    print("[C] Average Score per year by Park")
    print("[D] Average Score per Park by Reviewer Location")
    return _prompt_choice("> ")


def menu_visualise() -> str:
    print("Please enter one of the following options:")
    print("[A] Most Reviewed Parks")
    print("[B] Park Ranking by Nationality")
    print("[C] Most Popular Month by Park")
    return _prompt_choice("> ")


def menu_export() -> str:
    print("Please choose an export format:")
    print("[T] Text File (.txt)")
    print("[C] CSV File (.csv)")
    print("[J] JSON File (.json)")
    return _prompt_choice("> ")


def _ask_nonempty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be blank. Please try again.")


def ask_park_name() -> str:
    return _ask_nonempty("Enter the Disneyland park name (e.g., 'Disneyland_Paris'): ")


def ask_location() -> str:
    return _ask_nonempty("Enter the reviewer's location (e.g., 'United States'): ")


def ask_year() -> str:
    while True:
        year = input("Enter the year (e.g., '2019'): ").strip()
        if year.isdigit() and len(year) == 4:
            return year
        print("Invalid year format. Please enter a 4-digit year.")


def ask_filename() -> str:
    return _ask_nonempty("Enter desired filename (e.g., 'report'): ")


def show_reviews(reviews: list[dict], park_name: str) -> None:
    if not reviews:
        print(f"No reviews found for '{park_name}'. Please check the park name.\n")
        return

    print(f"\n--- Reviews for {park_name} ({len(reviews)} reviews) ---")
    for idx, review in enumerate(reviews, start=1):
        print(f"Review {idx}:")
        print(f"  Rating: {review.get('Rating', 'N/A')}/5")
        print(f"  Date: {review.get('Year_Month', 'N/A')}")
        print(f"  Location: {review.get('Reviewer_Location', 'N/A')}")
        print("-" * 22)
    print("------------------------------------------\n")


def show_review_count(park: str, location: str, count: int) -> None:
    print(f"\n'{park}' received {count} reviews from '{location}'.\n")
    if count == 0:
        print("Tip: check spelling/capitalisation for park and location.\n")


def show_average_rating_for_year(park: str, year: str, avg: float | None) -> None:
    if avg is None:
        print(f"No reviews found for '{park}' in {year}.\n")
        return
    print(f"\nThe average rating for '{park}' in {year} is: {avg:.2f}/5\n")


def show_average_by_location_report(report: dict[str, list[tuple[str, float]]]) -> None:
    if not report:
        print("No average score data available.\n")
        return

    print("\n--- Average Scores per Park by Reviewer Location ---")
    for park in sorted(report.keys()):
        print(f"\nPark: {park}")
        rows = report[park]
        if not rows:
            print("  No data available.")
            continue
        for location, avg in rows:
            print(f"  - {location}: {avg:.2f}/5")
    print("--------------------------------------------------\n")
