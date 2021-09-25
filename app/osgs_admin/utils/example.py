from flask import flash


def flash_example_message():
    flash("This is an example information message", "info")
    flash("This is an example success message", "success")
    flash("This is an example warning message", "warning")
    flash("This is an example error message", "error")


def return_example_message():
    return "Example Message!"
