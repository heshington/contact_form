from flask import Flask, render_template, request
import requests
import smtplib

posts = requests.get("https://api.npoint.io/ed99320662742443cc5b").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


# @app.route("/contact")
# def contact():
#     return render_template("contact.html")

@app.route('/contact',  methods=["GET", "POST"] )
def receive_data():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        print(f"{name} \n"
              f"{email} \n"
              f"{phone} \n"
              f"{message}")
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user="", password="")
            connection.sendmail(
                from_addr="",
                to_addrs="",
                msg=f"Subject:Message received from {name} \n\n{name}"
                    f" From: {email} \n"
                    f"Phone: {phone} \n"
                    f"Message: {message}"
            )
        return render_template("contact.html", post_message="Successfully sent message!")
    else:
        return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
