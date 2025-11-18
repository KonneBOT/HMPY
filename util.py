from routes import db
from sqlalchemy import text

def getAllInfo():
    qstmt = "SELECT * FROM zugfahrt"
    result = db.session.execute(text(qstmt)).fetchall()

    print("Results Rides: ", result)

    rides = {}
    for row in result:
        if not row:
            print("Trains: Rides something wrong 2")
        else:
            rides[row.id] = {
                "id": row.id,
                "start_station_id": row.start_station_id,
                "end_station_id": row.end_station_id,
                "start_time": row.start_time.strftime("%d.%m.%Y, %H:%M"),
                "end_time": row.end_time.strftime("%d.%m.%Y, %H:%M"),
                "train_id": row.train_id,
                "comment": row.comment,
                "delay": row.delay,
            }
    print("Rides: ", rides)

    qstmt = "SELECT * FROM zug"
    result = db.session.execute(text(qstmt)).fetchall()

    print("Results Trains: ", result)

    trains = {}
    for row in result:
        if not row:
            print("Trains: Trains something wrong 3")
        else:
            trains[row.id] = {
                "id": row.id,
                "name": row.name,
                "typ": row.typ,
                "comment": row.comment,
            }
    print("Trains: ", trains)

    qstmt = "SELECT * FROM bahnhof"
    result = db.session.execute(text(qstmt)).fetchall()

    print("Results Stations: ", result)

    stations = {}
    for row in result:
        if not row:
            print("Trains: Stations something wrong")
        else:
            stations[row.id] = {
                "id": row.id,
                "name": row.name,
                "ort": row.ort,
            }
    print("Stations: ", stations)
    return trains, stations, rides
