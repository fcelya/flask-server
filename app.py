from flask import Flask, request
import mariadb
import sys

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/db')
def show__db():
    try:
        conn = mariadb.connect(
            user="fcelaya",
            password="passtest",
            host='localhost',
            port=3306,
            database='prl'
        )
    except mariadb.Error as e:
        print(f"Got following error connecting to MariaDB: {e}")
        sys.exit(1)

    cur = conn.cursor()
    try:
        cur.execute("SHOW TABLES;")
    except mariadb.Error as e:
        print(f"Error: {e}")
    res = ""
    for table in cur:
        res += str(table)
        res += " "
        print(res)
    cur.close()
    conn.close()
    return res


def fill_mat(res):
    mat = []
    m = 0
    for key in res:
        mat.append(res[key])
        l = len(res[key])
        if l > m:
            m = l
    for i in range(len(mat)):
        for _ in range(m-len(mat[i])):
            mat[i].append("NULL")
    return mat


@app.route("/post", methods=['POST'])
def post():
    request_data = request.json

    try:
        conn = mariadb.connect(
            user="fcelaya",
            password="passtest",
            host='localhost',
            port=3306,
            database='prl'
        )
    except mariadb.Error as e:
        print(f"Got following error connecting to MariaDB: {e}")
        sys.exit(1)

    cur = conn.cursor()

    try:
        mat = fill_mat(request_data["data"])
        if mat[0] != []:
            if request_data["type"]["type"] == ["health"]:
                for i in range(len(mat[0])):
                    q = f"""
                    INSERT INTO health (
                        device_id,
                        heart_rate,
                        active_energy_burned,
                        basal_energy_burned,
                        apple_stand_time,
                        apple_walking_steadiness,
                        environmental_audio_exposure,
                        heart_rate_variability,
                        o2_saturation,
                        body_temperature,
                        blood_pressure_systolic,
                        blood_pressure_diastolic,
                        respiratory_rate,
                        distance_walked
                    ) VALUES (
                        "{request_data['type']['device id'][0]}",
                        {mat[0][i]},
                        {mat[1][i]},
                        {mat[2][i]},
                        {mat[3][i]},
                        {mat[4][i]},
                        {mat[5][i]},
                        {mat[6][i]},
                        {mat[7][i]},
                        {mat[8][i]},
                        {mat[9][i]},
                        {mat[10][i]},
                        {mat[11][i]},
                        {mat[12][i]}
                    );
                    """
                    print(q)
                    cur.execute(q)

            elif request_data["type"]["type"] == ["motion"]:
                for i in range(len(mat[0])):
                    q = F"""
                    INSERT INTO motion (
                        device_id,
                        accx,
                        accy,
                        accz,
                        gyrx,
                        gyry,
                        gyrz,
                        grvx,
                        grvy,
                        grvz,
                        device_time
                    ) VALUES (
                        "{request_data['type']['device id'][0]}",
                        {mat[0][i]},
                        {mat[1][i]},
                        {mat[2][i]},
                        {mat[3][i]},
                        {mat[4][i]},
                        {mat[5][i]},
                        {mat[6][i]},
                        {mat[7][i]},
                        {mat[8][i]},
                        {mat[9][i]}
                    );
                    """
                    cur.execute(q)
            conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

    return f"Added to database {request_data['type']['type'][0]} the following: \n{request_data['data']}"


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
