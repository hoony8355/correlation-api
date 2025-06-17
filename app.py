# app.py
from flask import Flask, request, jsonify
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io, base64

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json.get("weeks", [])
    if len(data) < 4:
        return jsonify({"error": "최소 4주 이상 필요"}), 400

    df = pd.DataFrame(data)
    corr = df.corr()

    # 히트맵 이미지 생성
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    return jsonify({
        "heatmap": f"data:image/png;base64,{img_base64}",
        "corr": corr.round(2).to_dict()
    })
