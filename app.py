from flask import Flask, request, jsonify 
from flask_cors import CORS
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager
import io
import base64
import os

app = Flask(__name__)
CORS(app)

# ✅ 1. NotoSansKR.ttf 파일 경로 수동 지정 (static 폴더에 넣는다고 가정)
FONT_PATH = "NotoSansKR-Regular.otf"

# ✅ 2. 폰트 등록
if os.path.exists(FONT_PATH):
    font_manager.fontManager.addfont(FONT_PATH)
    plt.rcParams['font.family'] = font_manager.FontProperties(fname=FONT_PATH).get_name()
else:
    print("⚠️ 한글 폰트 파일을 찾을 수 없습니다. 기본 폰트로 진행합니다.")

@app.route('/')
def home():
    return '🔍 Flask API 작동 중!'

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json.get("weeks", [])
        if len(data) < 4:
            return jsonify({"error": "최소 4주 이상의 데이터가 필요합니다."}), 400

        df = pd.DataFrame(data)
        corr = df.corr()

        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True)
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode("utf-8")
        plt.close()

        return jsonify({
            "heatmap": f"data:image/png;base64,{img_base64}",
            "corr": corr.round(2).to_dict()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
