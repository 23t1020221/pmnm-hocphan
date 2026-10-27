from flask import Flask, request, render_template, session, redirect, url_for, flash
from register import RegisterForm

app = Flask(__name__)
app.config["SECRET_KEY"]="my_secret_key"

USERS = {
    "admin": "admin123",
    "an": "an123456"
}

@app.route("/")
def index():
    return render_template("index.html", )

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USERS and USERS[username] == password:
            session["user"] = username
            session.permanent = bool(request.form.get("remember"))
            flash("Đăng nhập thành công!")
            return redirect(url_for("index"))

        error = "Sai tên đăng nhập hoặc mật khẩu!"

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Bạn đã đăng xuất thành công!")
    return redirect(url_for("login"))




@app.route("/profile")
def profile():
    if "user" not in session:
        flash("Vui lòng đăng nhập!")
        return redirect(url_for("login"))

    username = session["user"]

    return render_template(
        "profile.html",
        username=username
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        # Kiểm tra tên đăng nhập đã tồn tại
        if username in USERS:
            form.username.errors.append(
                "Tên đăng nhập này đã tồn tại."
            )
            return render_template("register.html", form=form)
        # Lưu tài khoản mới vào USERS
        USERS[username] = form.password.data
        flash("Đăng ký tài khoản thành công! Vui lòng đăng nhập.")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
