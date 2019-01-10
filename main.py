from gdpr_zendesk import delete_all
import os

def main():
    username = os.environ.get('USERNAME') or input("What's the username to use? ")
    password = os.environ.get('PASSWORD') pr input("What's the password to use? ")
    proceed_to_soft_delete = input("Proceed to soft delete tickets older than three years? Type (Y)es or (N)o ")
    if proceed_to_soft_delete.lower() == 'y':
        delete_all(username, password, soft_delete=True)
    else:
        exit()
    print("Please check the output")
    proceed_to_hard_delete = input("Proceed to hard delete? This will permanently remove tickets on the deleted list.Type (Y)es or (N)o ")
    if proceed_to_hard_delete.lower() == 'y':
        delete_all(username, password, soft_delete=False)
    else:
        exit()


if __name__ == '__main__':
    main()
