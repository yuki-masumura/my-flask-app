from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

# 道路に近いバス停(工学院大学西)・Bの時刻表
bus_schedule = {
    "平日": {
        "道路に近いバス停(工学院大学西)": {
            5: [39, 58], 6: [12, 27, 45], 7: [1, 17, 33, 46], 8: [3, 15, 35, 55],
            9: [15, 35, 55], 10: [10, 30, 50], 11: [10, 25, 50], 12: [10, 25, 50],
            13: [10, 25, 50], 14: [10, 25, 50], 15: [10, 25, 50], 16: [10, 25, 50],
            17: [12, 35, 52], 18: [12, 28, 55], 19: [11, 27, 54], 20: [11, 31, 54], 21: [14,39],22:[4,19]
        },
        "学校内のバス停(工学院大学)": {
            8: [1, 30], 11: [50], 12: [20, 50], 13: [15, 35, 55], 14: [20, 50],
            15: [45], 16: [0, 15, 45], 17: [0, 15, 25, 35, 45, 55], 18: [10, 40], 19: [0, 20, 40], 20: [0, 20, 40],21:[5]
        }
    },
    "土日": {
        "道路に近いバス停(工学院大学西)": {
            5: [39], 6: [15, 27, 47], 7: [16, 35, 49], 8: [9, 29, 49],
            9: [13, 32, 50], 10: [12, 30, 52], 11: [12, 25, 50], 12: [12, 25, 50],
            13: [12, 25, 50], 14: [12, 25, 50], 15: [12, 25, 50], 16: [12, 25, 50],
            17: [12, 25, 50], 18: [13, 28, 45], 19: [10, 25, 49], 20: [9, 29, 45], 21: [9, 29, 52],22:[19]
        },
        "学校内のバス停(工学院大学)": {
            11: [50], 12: [45], 13: [33], 14: [20], 15: [50], 16: [15, 45],
            17: [15, 40], 18: [15], 19: [30]
        }
    }
}

# 次のバスを探す関数
def find_next_bus(schedule):
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute

    next_buses = {}
    for bus, times in schedule.items():
        for hour, minutes in times.items():
            if hour >= current_hour:
                for minute in minutes:
                    if hour > current_hour or minute > current_minute:
                        next_buses[bus] = f"{hour}時{minute}分"
                        break
    if next_buses:
        next_bus = min(next_buses, key=lambda k: next_buses[k])  # 最も早いバス
        return next_bus, next_buses[next_bus]
    return None, None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/result")
def result():
    today = datetime.now().weekday()
    schedule_type = "平日" if today < 5 else "土日"

    bus, time = find_next_bus(bus_schedule[schedule_type])
    return render_template("result.html", schedule_type=schedule_type, bus=bus, time=time)

if __name__ == "__main__":
    app.run(debug=True)
