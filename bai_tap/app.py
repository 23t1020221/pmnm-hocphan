from flask import Flask, request, url_for, make_response,render_template, session, redirect, flash

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import (
    DataRequired, Length, Regexp, Email, EqualTo
)
#ket noi sql
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase , Mapped , mapped_column 

class Base(DeclarativeBase):        #(1)
    pass

db = SQLAlchemy(model_class=Base)   # (2)

app = Flask(__name__)
app.config["SECRET_KEY"] = "my_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///qlsv.db"             # (3)
db.init_app(app)                    # (4)


#sql CHƯƠNG 6
class Students(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    mssv: Mapped[str] = mapped_column(String(10), unique=True)
    name: Mapped[str] = mapped_column (String(100))
    gpa: Mapped[float] = mapped_column(default=0.0)

with app.app_context():
    db.create_all()

@app.get("/them-mau")
def add_sample():
    total = db.session.scalar(db.select(func.count(Students.id)))
    if total > 0:
        return f"Đã có {total} sinh viên, không thêm nữa."
    an = Students(mssv = "23T1020001",
                  name = "Nguyễn Văn An",
                  gpa = 8.5)
    before = an.id  # chua ghi xuong csdl
    db.session.add(an) #dua vao "giỏ" chờ ghi
    db.session.add_all([
        Students(mssv="23T1020002", name="Trần Thị Bình", gpa=6.8),
        Students(mssv="23T1020003", name="Lê Hoàng Cường", gpa=9.1),
        Students(mssv="23T1020004", name="Phạm Minh Dũng",gpa=4.5),
        Students(mssv="23T1020005", name="Hoàng Thu Hà", gpa =7.4),
    ])
    db.session.commit()         #ghi thật sự
    return (f"Đã thêm 5 sinh viên, id của An: "
           f"trước commit = {before}, "
            f"sau commit = {an.id}")

#doc du lieu bang viewfunction
@app.get("/thu-truy-van")
def try_queries():
    if db.session.scalar(db.select(func.count(Students.id))) == 0:
        return "Chưa có dữ liệu, hãy mở /them-mau trước."
    lines = []
    lines.append(f"1. get(3): {db.session.get(Students, 3)}")
    lines.append(f"2. get(99): {db.session.get(Students, 99)}")
    everyone = db.session.execute(db.select(Students)).scalars().all()
    lines.append(f"3. Tất cả: {len(everyone)} sinh viên")
    stmt = (db.select(Students)
            .where(Students.gpa >= 8)
            .order_by(Students.gpa.desc()))
    good = db.session.execute(stmt).scalars().all()
    lines.append(f"4. Điểm >= 8 : {good}")
    binh = db.session.scalar(db.select(Students).filter_by(mssv="23T1020002"))
    lines.append(f"5. MSSV 23T1020002: {binh}")
    count = db.session.scalar(db.select(func.count(Students.id)))
    avg = db.session.scalar(db.select(func.avg(Students.gpa)))
    lines.append(f"6. Số SV: {count}, điểm TB: {avg:.2f}")
    return "<br>".join(lines)

@app.route("/dssv")
def hienthi_dssv():
    return render_template("/qlsv.html", students=db.session.execute(db.select(Students)).scalars().all())
###


@app.route("/")
def index():
    tong_sv = len(STUDENTS)
    tong_lop = len({sv["lop"] for sv in STUDENTS.values()})
    return render_template("index.html", tong_sv=tong_sv, tong_lop=tong_lop)


STUDENTS = {
    "23T1020001": {"name": "Nguyễn Văn An", "lop": "K47A", "scores": {"PMMNM": 8.5, "CSDL": 7.0, "MMT": 9.0}},
    "23T1020002": {"name": "Trần Thị Bình", "lop": "K47A", "scores": {"PMMNM": 6.0, "CSDL": 5.5, "MMT": 7.0}},
    "23T1020003": {"name": "Lê Hoàng Cường", "lop": "K47B", "scores": {"PMMNM": 9.5, "CSDL": 9.0}},
    "23T1020004": {"name": "Phạm Minh Dũng", "lop": "K47B", "scores": {"PMMNM": 4.0, "CSDL": 3.5, "MMT": 5.0}},
    "23T1020005": {"name": "Hoàng Thu Hà", "lop": "K47A", "scores": {}},
    "23T1020006": {"name": "Võ Quốc Khánh", "lop": "K47C", "scores": {"PMMNM": 7.5, "MMT": 8.0}},
}

@app.route("/students")
def students():
    # Lấy lớp từ URL
    lop = request.args.get("lop", "")
    # Tạo danh sách lớp từ dữ liệu
    cac_lop = set()
    for student in STUDENTS.values():
        cac_lop.add(student["lop"])
    # Sắp xếp lớp
    cac_lop = sorted(cac_lop)
    # Lọc sinh viên
    danh_sach = []
    for mssv, student in STUDENTS.items():
        # Nếu không lọc
        if lop == "":
            danh_sach.append((mssv, student))
        # Nếu có lọc
        elif student["lop"].lower() == lop.lower():
            danh_sach.append((mssv, student))
    # Tạo thanh lọc
    filter_html = '<a href="/students">Tất cả</a> | '
    for ten_lop in cac_lop:
        link_lop = url_for("students", lop=ten_lop)
        filter_html += f'''
            <a href="{link_lop}">{ten_lop}</a>
        '''
        if ten_lop != cac_lop[-1]:
            filter_html += " | "
    # Nếu không có sinh viên
    if len(danh_sach) == 0:
        return f"""
            <h1>Danh sách sinh viên</h1>
            <div>
                {filter_html}
            </div>
            <p>không có sinh viên phù hợp</p>
            <a href="{url_for('index')}">Quay lại trang chủ</a>
        """
    # Tạo bảng
    table_html = """
        <table border="1" cellpadding="8">
            <tr>
                <th>MSSV</th>
                <th>Họ tên</th>
                <th>Lớp</th>
                <th>Điểm</th>
                <th>TB</th>
                <th>Xếp loại</th>
                <th>Tải bảng điểm</th>
            </tr>
    """
    for mssv, student in danh_sach:
        name = student["name"]
        lop_sv = student["lop"]
        scores = student["scores"]
        # Nếu chưa có điểm
        if len(scores) == 0:
            diem = "...."
            tb = "...."
            xep_loai = "...."
        else:
            # Tạo chuỗi điểm
            diem = ", ".join(
                f"{mon}: {diem_mon}"
                for mon, diem_mon in scores.items()
            )
            # Tính điểm trung bình
            tb_value = sum(scores.values()) / len(scores)
            tb = f"{tb_value:.2f}"
            # Xếp loại
            if tb_value < 4:
                xep_loai = "Yếu"
            elif tb_value < 7:
                xep_loai = "Trung bình"
            elif tb_value < 8.5:
                xep_loai = "Khá"
            else:
                xep_loai = "Giỏi"
        # Tạo link đến trang chi tiết, tai bang diem
        link_chi_tiet = url_for("chitiet", mssv=mssv)
        link_tai = url_for("download_scores", mssv=mssv)
        # Thêm một dòng vào bảng
        table_html += f"""
            <tr>
                <td>
                    <a href="{link_chi_tiet}">{mssv}</a>
                </td>
                <td>{name}</td>
                <td>{lop_sv}</td>
                <td>{diem}</td>
                <td>{tb}</td>
                <td>{xep_loai}</td>
                <td>
                <a href="{link_tai}">
                    Tải bảng điểm
                 </a>
                </td>
            </tr>
        """
    # Đóng bảng
    table_html += "</table>"
    return f"""
        <h1>Danh sách sinh viên</h1>
        <form method="GET" action="/search">
    <input
        type="text"
        name="q"
        placeholder="Nhập họ tên hoặc MSSV"
    >
    <button type="submit">Tìm kiếm</button>
</form>
        <p>
            Lọc theo lớp:
            {filter_html}
        </p>

        {table_html}

        <br>

        <a href="{url_for('index')}">
            Quay lại trang chủ
        </a>
    """


@app.route("/students/<mssv>")
def chitiet(mssv):
    if mssv not in STUDENTS:
        return "Không tìm thấy sinh viên", 404
    student = STUDENTS[mssv]
    return f"""
        <h1>Chi tiết sinh viên</h1>

        <p>MSSV: {mssv}</p>
        <p>Họ tên: {student["name"]}</p>
        <p>Lớp: {student["lop"]}</p>
        <p>Điểm: {student["scores"]}</p>


        <a href="{url_for('students')}">
            Quay lại danh sách
        </a>
    """


@app.route("/students/<mssv>/download")
def download_scores(mssv):
    if mssv not in STUDENTS:
        return "Không tìm thấy sinh viên", 404
    student = STUDENTS[mssv]
    scores = student["scores"]
    content = ""
    for mon, diem in scores.items():
        content += f'"{mon}": {diem},\n'
    response = make_response(content)
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = (
        f"attachment; filename={mssv}_bang_diem.csv"
    )
    return response


@app.route("/search")
def search():
    keyword = request.args.get("q", "")

    keyword_lower = keyword.lower()

    ket_qua = []

    for mssv, student in STUDENTS.items():

        ho_ten = student["name"].lower()

        if keyword_lower in ho_ten or keyword_lower in mssv.lower():
            ket_qua.append((mssv, student))

    # Tạo danh sách liên kết
    danh_sach = ""

    for mssv, student in ket_qua:

        link = url_for("chitiet", mssv=mssv)

        danh_sach += f"""
            <li>
                <a href="{link}">
                    {mssv} - {student["name"]}
                </a>
            </li>
        """
    return f"""
        <h1>Tìm kiếm sinh viên</h1>

        <form method="GET" action="{url_for("search")}">
            <input 
                type="text" 
                name="q" 
                value="{keyword}"
                placeholder="Nhập họ tên hoặc MSSV"
            >

            <button type="submit">Tìm kiếm</button>
        </form>

        <hr>

        <h3>
            Tìm thấy {len(ket_qua)} kết quả cho "{keyword}"
        </h3>

        <ul>
            {danh_sach}
        </ul>

        <a href="{url_for("students")}">
            Quay lại danh sách sinh viên
        </a>
    """

# chuong 4
# may tinh
@app.route("/cal", methods=["GET", "POST"])
def cal():
    values, error = {"a": "", "b": "", "kq": "", "q": ""}, {}

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
        except ZeroDivisionError:
            error["q"] = "Không thể chia cho 0!"
    return render_template("cal.html", values=values, error=error)


# hoc phan xep laoi
@app.route("/hp", methods=["GET", "POST"])
def hp():
    values, error = {"cc": "", "gk": "", "ck": "", "kq": None, "xl": ""}, {}

    if request.method == "POST":
        try:
            values["cc"] = float(request.form.get("cc", "").replace(",", "."))
            values["gk"] = float(request.form.get("gk", "").replace(",", "."))
            values["ck"] = float(request.form.get("ck", "").replace(",", "."))
            values["kq"] = float(values["cc"] * 0.1 + values["gk"] * 0.3 + values["ck"] * 0.6)
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


# tinh bmi
@app.route("/bmi", methods=["GET", "POST"])
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


# chuong 5
#login, logout, register
USERS = {
    "admin": "admin123",
    "an": "an123456"
}

class RegisterForm(FlaskForm):
    username = StringField(
        "Tên đăng nhập",
        validators=[
            DataRequired(message="Vui lòng nhập tên đăng nhập."),
            Length(min=4, max=20,
                   message="Tên đăng nhập phải từ 4 đến 20 ký tự."),
            Regexp(
                r"^[a-z0-9_]+$",
                message="Chỉ được dùng chữ thường không dấu, số và dấu gạch dưới (_)."
            )
        ]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Vui lòng nhập email."),
            Email(message="Email không đúng định dạng.")
        ]
    )
    password = PasswordField(
        "Mật khẩu",
        validators=[
            DataRequired(message="Vui lòng nhập mật khẩu."),
            Length(min=8, message="Mật khẩu phải có ít nhất 8 ký tự.")
        ]
    )
    confirm_password = PasswordField(
        "Nhập lại mật khẩu",
        validators=[
            DataRequired(message="Vui lòng nhập lại mật khẩu."),
            EqualTo("password", message="Mật khẩu nhập lại không khớp.")
        ]
    )
    terms = BooleanField(
        "Tôi đồng ý với các điều khoản",
        validators=[
            DataRequired(message="Bạn phải đồng ý với các điều khoản.")
        ]
    )
    submit = SubmitField("Đăng ký")


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
