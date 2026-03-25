# ============================================================
# app.py - Python Flask 웹 애플리케이션 (Hello World)
#
# [비교] Tomcat + JSP 경험자를 위한 설명:
#   - Tomcat  -> Flask (내장 서버 포함)
#   - web.xml -> 이 파일 안의 라우팅 설정 (@app.route)
#   - .jsp    -> return 문으로 직접 HTML 반환 (또는 템플릿)
# ============================================================

# Flask 라이브러리에서 Flask 클래스와 render_template 함수를 가져옵니다.
# Java의 'import' 구문과 동일한 역할입니다.
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

# Flask 앱 객체를 생성합니다.
# __name__ 은 현재 파일의 이름을 의미하는 Python 내장 변수입니다.
# Flask는 이 값을 이용해 프로젝트의 루트 경로를 찾습니다.
app = Flask(__name__)
app.secret_key = 'antigravity_secret_key'  # 세션을 위한 시크릿 키

# MariaDB 연결 설정
db_config = {
    'host': '192.168.57.81',
    'port': 3301,
    'user': 'test1',
    'password': '1234',
    'database': 'test'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)


# @app.route("/") 는 '데코레이터(decorator)' 라고 부릅니다.
# 브라우저가 "/" 경로(루트, 즉 http://localhost:5000/) 로 요청을 보내면
# 바로 아래 함수(hello_world)를 실행하라는 뜻입니다.
# [비교] web.xml의 <url-pattern>/</url-pattern> 설정과 동일합니다.
@app.route("/")
def hello_world():
    """
    루트 경로(/) 로 접속했을 때 실행되는 함수입니다.
    render_template() 은 templates/ 폴더의 HTML 파일을 찾아서
    그 내용을 브라우저에 전달합니다.
    [비교] JSP 파일을 forward 하는 것과 같습니다.
    """
    # templates/index.html 파일을 렌더링해서 반환합니다.
    return render_template("index.html")


# 추가 페이지 예시: /about 경로에 접속하면 다른 내용을 보여줍니다.
@app.route("/about")
def about():
    """
    /about 경로로 접속했을 때 실행되는 함수입니다.
    """
    return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        user_pw = request.form.get("user_pw")

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # PASSWORD() 함수를 사용하여 비밀번호 검증
            # tb_users 테이블에서 id와 password(PASSWORD() 함수 적용)가 일치하는 사용자 검색
            sql = "SELECT user_id, user_nm FROM tb_users WHERE user_id = %s AND user_pw = PASSWORD(%s)"
            cursor.execute(sql, (user_id, user_pw))
            user = cursor.fetchone()

            if user:
                session["user_id"] = user["user_id"]
                session["user_nm"] = user["user_nm"]
                flash(f"{user['user_nm']}님, 환영합니다!", "success")
                return redirect(url_for("hello_world"))
            else:
                flash("아이디 또는 비밀번호가 올바르지 않습니다.", "error")
        except mysql.connector.Error as err:
            flash(f"데이터베이스 오류: {err}", "error")
        finally:
            if conn:
                conn.close()

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("로그아웃 되었습니다.", "info")
    return redirect(url_for("hello_world"))


@app.route("/test")
def test_page():
    """
    /test 경로로 접속했을 때 실행되는 함수입니다.
    """
    return render_template("test.html")


# 이 파일을 직접 실행했을 때만 서버를 시작합니다.
# (다른 파일에서 import 로 불렀을 때는 서버가 자동 시작되지 않습니다)
# [비교] Tomcat 을 startup.sh 로 시작하는 것과 같습니다.
if __name__ == "__main__":
    # debug=True : 코드를 수정하면 서버가 자동으로 재시작됩니다.
    #              개발 중에만 사용하고, 실제 서비스에는 False 로 설정하세요.
    # port=5000  : 접속할 포트 번호 (Tomcat 의 8080 과 같은 역할)
    app.run(debug=True, port=5000)
