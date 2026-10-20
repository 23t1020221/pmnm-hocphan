from flask import Flask, request, render_template

hocphan = Flask(__name__)

@hocphan.route("/hp", methods=["GET", "POST"])
def hp():
    values,error = {"cc": "", "gk": "", "ck": "","kq":"","xl": ""}, {}

    if request.method =="POST":
        try:
            values["cc"] = float(request.form.get("cc", "").replace(",", "."))
            values["gk"] = float(request.form.get("gk", "").replace(",", "."))
            values["ck"] = float(request.form.get("ck", "").replace(",", "."))
            values["kq"] = float(values["cc"]*0.1 + values["gk"]*0.3 + values["ck"]*0.6)
            if values["kq"] >= 8.5:
                values["xl"] = "A"
            elif values["kq"] >= 7.0:
                values["xl"] = "B"
            elif values["kq"] >= 5.5:
                values["xl"] = "C"
            elif values["kq"] >= 4.0:
                values["xl"] = "D"
            else:
                values["xl"] = "F"
        except ValueError:
            error["xl"] = "loi!"
    return render_template("hp.html", values=values, error=error)
if __name__ == "__main__":
    hocphan.run(debug=True)