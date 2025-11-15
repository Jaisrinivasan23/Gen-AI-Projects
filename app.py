import reflex as rx

class State(rx.State):
    username: str = ""
    password: str = ""
    msg: str = ""

    def login(self):
        if self.username == "admin" and self.password == "1234":
            self.msg = "Login Successful! 🎉"
        else:
            self.msg = "Invalid username or password ❌"

def index():
    return rx.center(
        rx.vstack(
            rx.text("Simple Login", font_size="2em", font_weight="bold"),

            rx.input(
                placeholder="Username",
                width="250px",
                on_change=State.set_username
            ),

            rx.input(
                placeholder="Password",
                type="password",
                width="250px",
                on_change=State.set_password
            ),

            rx.button(
                "Login",
                width="250px",
                bg="blue",
                color="white",
                on_click=State.login
            ),

            rx.text(State.msg, margin_top="10px", font_size="1.2em"),

            spacing="4",  # FIXED (must be 0–9, not px)
        ),
        height="100vh"
    )


app = rx.App()
app.add_page(index)
app._compile()
