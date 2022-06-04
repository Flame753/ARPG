class CLI:
    def display_title(self, title: str) -> None:
        style = "*"*3
        print(style ,title, style, end="\n\n")
    
    def display_choose(self, option: str, text: str) -> None:
        print(f"{option.capitalize()}: {text.capitalize()}")

    def get_user_input(self, input_text: str="Action") -> str:
        return input(f"{input_text}: ")
    
    def display_invalid_input(self, user_input: str) -> None:
        print(f"Invalid Action! <{user_input}> Try again!\n")
    
    def display_text(self, text: str) -> None:
        print(text)

