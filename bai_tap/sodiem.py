STUDENTS = {
    "23T1020001": {"name": "Nguyễn Văn An", "lop": "K47A", "scores": {"PMMNM": 8.5, "CSDL": 7.0, "MMT":9.0}},
    "23T1020002": {"name": "Trần Thị Bình", "lop": "K47A", "scores": {"PMMNM": 6.0, "CSDL": 5.5, "MMT":7.0}},
    "23T1020003": {"name": "Lê Hoàng Cường", "lop": "K47B", "scores": {"PMMNM": 9.5, "CSDL": 9.0}},
    "23T1020004": {"name": "Phạm Minh Dũng", "lop": "K47B", "scores": {"PMMNM": 4.0, "CSDL": 3.5, "MMT":5.0}},
    "23T1020005": {"name": "Hoàng Thu Hà", "lop": "K47A", "scores": {}},
    "23T1020006": {"name": "Võ Quốc Khánh", "lop": "K47C", "scores": {"PMMNM": 7.5, "MMT":8.0}},
}

from flask import Flask, request,url_for, make_response

app = Flask(__name__)

@app.route("/")
def hienthi():
    link = url_for("students")

    tongsv = len(STUDENTS)
    cac_lop = set()
    for student in STUDENTS.values():
        cac_lop.add(student["lop"])
    tong_lop = len(cac_lop)
    return f"""
        <p>Tổng số sinh viên: {tongsv}</p>
        <p>Tổng số lớp: {tong_lop}</p>
        <a href="{link}">Bấm vào đây để đến trang Students</a>
         
    """

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

        <a href="/">
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
    # Tạo nội dung file
    content = ""
    for mon, diem in scores.items():
        content += f'"{mon}": {diem},\n'
    # Tạo response
    response = make_response(content)
    # Kiểu file CSV
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    # Tên file tải xuống
    response.headers["Content-Disposition"] = (
        f"attachment; filename={mssv}_bang_diem.csv"
    )
    return response

@app.route("/search")
def search():
    # Lấy từ khóa từ URL
    keyword = request.args.get("q", "")

    # Chuyển về chữ thường để tìm không phân biệt hoa thường
    keyword_lower = keyword.lower()

    # Danh sách sinh viên tìm được
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

if __name__ == "__main__":
    app.run(debug=True)