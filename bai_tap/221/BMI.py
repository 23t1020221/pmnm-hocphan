from flask import Flask, request, render_template

BMI = Flask(__name__)

@BMI.route("/bmi", methods=["GET", "POST"])
def chiso():
    values = {
        "cao": "",
        "nang": "",
        "kq": "",
        "pl": "",
        "mau": ""
    }
    error = {}
    if request.method == "POST":
        try:
            values["cao"] = float(request.form.get("cao", "").replace(",", "."))
            values["nang"] = float(request.form.get("nang", "").replace(",", "."))
            if values["cao"] <= 0 or values["nang"] <= 0:
                raise ValueError
            values["kq"] = values["nang"] / values["cao"] ** 2
            if values["kq"] < 18.5:
                values["pl"] = "Thiếu cân"
                values["mau"] = "vang"
            elif values["kq"] < 23:
                values["pl"] = "Bình thường"
                values["mau"] = "xanh"
            elif values["kq"] < 25:
                values["pl"] = "Thừa cân"
                values["mau"] = "vang"
            else:
                values["pl"] = "Béo phì"
                values["mau"] = "do"
        except ValueError:
            error["kq"] = "Vui lòng nhập chiều cao và cân nặng hợp lệ!"
    return render_template(
        "bmi.html",
        values=values,
        error=error
    )
if __name__ == "__main__":
    BMI.run(debug=True)