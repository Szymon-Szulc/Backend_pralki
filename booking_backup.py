# Booking
class Booking(Resource):
    # Add Booking
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("jwt")
        parser.add_argument("date")
        parser.add_argument("time")
        parser.add_argument("name")
        args = parser.parse_args(strict=True)
        try:
            booking_id = db.bookings.find_one(filter={}, sort=list({"bid": -1}.items()))["bid"] + 1
        except TypeError:
            booking_id = 1
        user_id = decode_user_jwt(args["jwt"])
        if not user_id:
            return {"code": 401}
        user = db.users.find_one({"uid": user_id})
        dorm_id = user["did"]
        user_id = user["uid"]
        try:
            machine_id = db.machines.find_one({"did": dorm_id, "name": args["name"]})
        except TypeError:
            return {"code": 406}
        date_args = args["date"].split("-")
        time_args = args["time"].split(":")
        date_time = datetime.datetime(int(date_args[0]), int(date_args[1]), int(date_args[2]), int(time_args[0]),
                                      int(time_args[1]))
        booking = {
            "did": dorm_id,
            "bid": booking_id,
            "mid": machine_id["mid"],
            "uid": user_id,
            "date": date_time
        }
        if db.bookings.find_one({"did": dorm_id, "date": date_time, "mid": machine_id["mid"]}) is not None:
            return {"code": 418}
        db.bookings.insert_one(booking)
        return {"code": 201}

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("jwt")
        args = parser.parse_args(strict=True)
        user_id = decode_user_jwt(args["jwt"])
        if not user_id:
            return {"code": 401}
        user = db.users.find_one({"uid": user_id})
        dorm_id = user["did"]
        bookings = db.bookings.find({"did": dorm_id})
        response = []
        for booking in bookings:
            name = db.machines.find_one({"mid": booking["mid"]})["name"]
            response.append({"bid": booking["bid"], "date": str(booking['date'])})
        return {"bookings": response, "code": 201}