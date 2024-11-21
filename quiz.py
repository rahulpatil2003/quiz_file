import json
import random

QUIZ_FILE_PATH = "data.json"


def load_quiz_file():
    """Load quiz content from a JSON file."""
    try:
        with open(QUIZ_FILE_PATH, "r") as quiz_file:
            return json.load(quiz_file)
    except FileNotFoundError:
        print(f"{QUIZ_FILE_PATH} not found. Make sure it exists.")
        return {}


def list_available_topics(quiz_data):
    """Display available quiz topics."""
    print("\nAvailable Topics:")
    for idx, topic in enumerate(quiz_data.keys(), 1):
        print(f"{idx}. {topic}")
    return list(quiz_data.keys())


def conduct_quiz(selected_topic, username, quiz_data):
    """Run the quiz for a selected topic."""
    print(f"\n{username}, welcome to the {selected_topic} quiz!")
    if selected_topic not in quiz_data:
        print(f"No questions available for the topic: {selected_topic}.")
        return

    user_score = 0
    quiz_questions = random.sample(quiz_data[selected_topic], min(len(quiz_data[selected_topic]), 5))

    for question_num, question_data in enumerate(quiz_questions, 1):
        print(f"\nQ{question_num}: {question_data['q']}")
        for option_num, option_text in enumerate(question_data["o"], 1):
            print(f"{option_num}. {option_text}")
        try:
            user_answer = int(input("Choose your answer (1/2/3/4): "))
            if question_data["o"][user_answer - 1] == question_data["a"]:
                print("Correct!")
                user_score += 1
            else:
                print(f"Wrong! The correct answer was: {question_data['a']}")
        except (ValueError, IndexError):
            print("Invalid choice. Skipping this question.")

    print(f"\nYour total score: {user_score}/{len(quiz_questions)}. Well done, {username}!")


def main():
    """Main function to drive the application."""
    print("Welcome to the Quiz Game!")
    quiz_data = load_quiz_file()

    if not quiz_data:
        print("No quiz data found. Exiting.")
        return

    user_accounts = {}
    current_user = None

    # User Registration and Login
    while not current_user:
        print("\n1. Register\n2. Login\n3. Exit")
        user_action = input("Select an option: ")
        if user_action == "1":
            new_username = input("Choose a username: ")
            if new_username in user_accounts:
                print("Username already exists. Try logging in.")
            else:
                new_password = input("Set a password: ")
                user_accounts[new_username] = new_password
                print("Registration successful!")
        elif user_action == "2":
            login_username = input("Enter your username: ")
            login_password = input("Enter your password: ")
            if user_accounts.get(login_username) == login_password:
                print("Login successful!")
                current_user = login_username
            else:
                print("Invalid username or password.")
        elif user_action == "3":
            print("Exiting the application. Thank you!")
            return
        else:
            print("Invalid choice. Please try again.")

    # Quiz Menu
    while True:
        topic_list = list_available_topics(quiz_data)
        topic_selection = input(f"Select a topic (1-{len(topic_list)}): ")
        if topic_selection.isdigit() and 1 <= int(topic_selection) <= len(topic_list):
            chosen_topic = topic_list[int(topic_selection) - 1]
            conduct_quiz(chosen_topic, current_user, quiz_data)
        else:
            print("Invalid topic selection. Please try again.")

        replay_quiz = input("Do you want to take another quiz? (yes/no): ").strip().lower()
        if replay_quiz != "yes":
            print("Thank you for playing!")
            break


if __name__ == "__main__":
    main()
