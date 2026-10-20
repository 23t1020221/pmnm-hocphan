from flask import Flask , request,render_template

app = Flask(__name__)

@app.route("/cal", methods=["GET", "POST"])
def cal():
    values,error = {"a" : "", "b": "", "kq":"" , "q" : ""}, {}

    if request.method == "POST":
        try:
            values["a"] = float(request.form.get("a", "").strip())
            values["b"] = float(request.form.get("b", "").strip())
            values["q"] = request.form.get("q", "").strip()
            if values["q"] == "+":
                values["kq"] = values["a"] + values["b"]
            elif values["q"] == "-":
                values["kq"] = values["a"] - values["b"]
            elif values["q"] == "*":
                values["kq"] = values["a"] * values["b"]
            elif values["q"] == "/":
                values["kq"] = values["a"] / values["b"]         
        except ValueError:
            error["q"] = "Vui lòng nhập hai số hợp lệ!"
    return  render_template("cal.html", values=values, error=error)
if __name__ == "__main__":
    app.run(debug=True)
    